"""
gh_toolkit.live - Direct bridge to running Rhino 8 and active Grasshopper canvas.

Enables agents, CLI, and scripts to:
1. Inspect running Rhino 8 instances and the active Grasshopper document.
2. List canvas components, coordinates, parameter pins, and wire graphs.
3. Add native, Heteroptera, LegoPod, and Magpie components live.
4. Wire outputs to inputs, or disconnect wires.
5. Set parameter values (Number Sliders, Panels, Boolean Toggles).
6. Delete components or clear the canvas.
7. Trigger real-time recomputations and canvas refreshes.
8. Save and open Grasshopper definitions quietly.
"""

import os
import sys
import json
import uuid
import subprocess
import shutil
from typing import Dict, Any, List, Optional, Union


def find_rhinocode() -> Optional[str]:
    """Locate the rhinocode CLI on macOS or in PATH."""
    standard_mac_path = "/Applications/Rhino 8.app/Contents/Resources/bin/rhinocode"
    if os.path.isfile(standard_mac_path) and os.access(standard_mac_path, os.X_OK):
        return standard_mac_path
    which_path = shutil.which("rhinocode")
    if which_path:
        return which_path
    return None


def get_rhino_env() -> Dict[str, str]:
    """Prepare environment variables with .NET roll forward enabled for Rhino 8."""
    env = os.environ.copy()
    env["DOTNET_ROLL_FORWARD"] = "LatestMajor"
    return env


def get_bridge_tmp_dir() -> str:
    """
    Get a persistent user-level directory for script exchange.
    Avoids macOS sandbox restrictions on /tmp and /var/folders.
    """
    bridge_dir = os.path.expanduser("~/.gh_toolkit/bridge")
    os.makedirs(bridge_dir, exist_ok=True)
    return bridge_dir


def is_rhino_running() -> bool:
    """Check if any Rhino 8 instance is running with an active script server."""
    instances = get_rhino_instances()
    return len(instances) > 0


def get_rhino_instances() -> List[Dict[str, Any]]:
    """List running Rhino instances via `rhinocode list`."""
    rhinocode_bin = find_rhinocode()
    if not rhinocode_bin:
        return []

    try:
        res = subprocess.run(
            [rhinocode_bin, "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=get_rhino_env(),
            timeout=5,
        )
        if res.returncode != 0:
            return []

        lines = res.stdout.strip().splitlines()
        instances = []
        for line in lines[1:]:  # Skip header
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0].isdigit():
                instances.append({
                    "pid": int(parts[0]),
                    "pipe_id": parts[1],
                    "doc": parts[2] if len(parts) > 2 else None,
                    "path": parts[3] if len(parts) > 3 else None,
                })
        return instances
    except Exception:
        return []


def run_in_rhino(python_code: str, instance_id: Optional[str] = None, timeout: int = 15) -> Dict[str, Any]:
    """
    Execute a Python snippet inside the running Rhino 8 instance via rhinocode.
    Communicates results back through a user-space JSON payload.
    """
    rhinocode_bin = find_rhinocode()
    if not rhinocode_bin:
        return {
            "success": False,
            "error": "RhinoCode CLI not found. Expected at '/Applications/Rhino 8.app/Contents/Resources/bin/rhinocode'."
        }

    instances = get_rhino_instances()
    target_pipe = instance_id
    if not target_pipe and instances:
        target_pipe = instances[0]["pipe_id"]

    bridge_dir = get_bridge_tmp_dir()
    temp_id = uuid.uuid4().hex[:8]
    script_path = os.path.join(bridge_dir, f"cmd_{temp_id}.py")
    result_path = os.path.join(bridge_dir, f"res_{temp_id}.json")

    wrapper = f"""# -*- coding: utf-8 -*-
import sys
import os
import json
import traceback

__RESULT_PATH__ = {repr(result_path)}

def __execute():
{chr(10).join('    ' + line for line in python_code.strip().splitlines())}

try:
    __res = __execute()
    with open(__RESULT_PATH__, 'w', encoding='utf-8') as __f:
        json.dump({{'success': True, 'result': __res}}, __f, indent=2)
except Exception as __e:
    with open(__RESULT_PATH__, 'w', encoding='utf-8') as __f:
        json.dump({{'success': False, 'error': str(__e), 'traceback': traceback.format_exc()}}, __f, indent=2)
"""

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(wrapper)

    cmd = [rhinocode_bin]
    if target_pipe:
        cmd.extend(["-r", target_pipe])
    cmd.extend(["script", script_path])

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=get_rhino_env(),
            timeout=timeout,
        )

        if not os.path.exists(result_path):
            hint = "Ensure 'StartScriptServer' is running in Rhino 8."
            err_msg = proc.stderr.strip() or proc.stdout.strip()
            return {
                "success": False,
                "error": f"Rhino script produced no result payload. {err_msg} ({hint})",
                "stderr": proc.stderr,
                "stdout": proc.stdout,
            }

        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Execution timed out after {timeout} seconds"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        # Cleanup
        if os.path.exists(script_path):
            try:
                os.remove(script_path)
            except Exception:
                pass
        if os.path.exists(result_path):
            try:
                os.remove(result_path)
            except Exception:
                pass


# ==============================================================================
# Live Document High-Level API
# ==============================================================================

def live_status() -> Dict[str, Any]:
    """Get status of running Rhino, Grasshopper canvas, and active document."""
    instances = get_rhino_instances()
    if not instances:
        return {
            "rhino_running": False,
            "error": "Rhino 8 is not running or script server is not active. Run 'StartScriptServer' in Rhino 8 command line."
        }

    script = """
import Rhino
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc_server = Grasshopper.Instances.DocumentServer
active_doc = canvas.Document if canvas else None

docs = []
if doc_server:
    for d in doc_server:
        docs.append({
            'name': str(d.DisplayName),
            'file_path': str(d.FilePath) if d.FilePath else None,
            'object_count': d.ObjectCount,
            'modified': d.Modified
        })

active_info = None
if active_doc:
    active_info = {
        'name': str(active_doc.DisplayName),
        'file_path': str(active_doc.FilePath) if active_doc.FilePath else None,
        'object_count': active_doc.ObjectCount,
        'modified': active_doc.Modified
    }

return {
    'rhino_version': str(Rhino.RhinoApp.Version),
    'rhino_doc': Rhino.RhinoDoc.ActiveDoc.Name if Rhino.RhinoDoc.ActiveDoc else None,
    'canvas_available': canvas is not None,
    'documents_count': len(docs),
    'documents': docs,
    'active_document': active_info
}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        res_data = res.get("result", {})
        res_data["rhino_running"] = True
        res_data["instances"] = instances
        return res_data
    return {"rhino_running": True, "instances": instances, "error": res.get("error")}


def live_list_objects() -> Dict[str, Any]:
    """List all components and parameters on the active Grasshopper canvas with their pins and wires."""
    script = """
import Rhino
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {'error': 'No active Grasshopper document found on canvas'}

objects = []
for obj in doc.Objects:
    pivot = obj.Attributes.Pivot
    info = {
        'instance_guid': str(obj.InstanceGuid),
        'component_guid': str(obj.ComponentGuid),
        'name': str(obj.Name),
        'nickname': str(obj.NickName),
        'category': str(obj.Category),
        'subcategory': str(obj.SubCategory),
        'type': type(obj).__name__,
        'pivot': [round(pivot.X, 1), round(pivot.Y, 1)],
        'locked': obj.Locked,
        'hidden': getattr(obj, 'Hidden', False)
    }

    if isinstance(obj, gh_kernel.IGH_Component):
        inputs = []
        for p in obj.Params.Input:
            sources = [str(s.InstanceGuid) for s in p.Sources]
            inputs.append({
                'name': str(p.Name),
                'nickname': str(p.NickName),
                'instance_guid': str(p.InstanceGuid),
                'sources': sources,
                'type_name': str(p.TypeName)
            })
        outputs = []
        for p in obj.Params.Output:
            recipients = [str(r.InstanceGuid) for r in p.Recipients]
            outputs.append({
                'name': str(p.Name),
                'nickname': str(p.NickName),
                'instance_guid': str(p.InstanceGuid),
                'recipients': recipients,
                'type_name': str(p.TypeName)
            })
        info['inputs'] = inputs
        info['outputs'] = outputs
    elif isinstance(obj, gh_kernel.IGH_Param):
        sources = [str(s.InstanceGuid) for s in obj.Sources]
        recipients = [str(r.InstanceGuid) for r in obj.Recipients]
        info['sources'] = sources
        info['recipients'] = recipients
        info['type_name'] = str(obj.TypeName)

    tname = type(obj).__name__
    if 'Slider' in tname or hasattr(obj, 'Slider'):
        try:
            info['value'] = float(obj.Slider.Value)
            info['min'] = float(obj.Slider.Minimum)
            info['max'] = float(obj.Slider.Maximum)
        except Exception:
            pass
    elif 'Panel' in tname or hasattr(obj, 'UserText'):
        try:
            info['value'] = str(obj.UserText)
        except Exception:
            pass
    elif 'BooleanToggle' in tname or hasattr(obj, 'Value'):
        try:
            info['value'] = bool(obj.Value)
        except Exception:
            pass

    objects.append(info)

return {
    'doc_name': str(doc.DisplayName),
    'total_objects': len(objects),
    'objects': objects
}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"error": res.get("error")}


def live_add_component(
    name_or_guid: str,
    x: float = 100.0,
    y: float = 100.0,
    nickname: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a component or parameter to the active Grasshopper document.
    name_or_guid can be a component name (e.g. 'Number Slider', 'Panel', 'Divide Curve')
    or a GUID string.
    """
    script = f"""
import System
from System.Drawing import PointF
import Rhino
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    doc = gh_kernel.GH_Document()
    Grasshopper.Instances.DocumentServer.AddDocument(doc)
    if canvas:
        canvas.Document = doc

target_str = {repr(name_or_guid)}
comp_server = Grasshopper.Instances.ComponentServer

proxy = None
try:
    guid = System.Guid(target_str)
    proxy = comp_server.EmitObjectProxy(guid)
except Exception:
    pass

if not proxy:
    proxy = comp_server.FindObjectByName(target_str, True, True)

if not proxy:
    return {{'success': False, 'error': f"Component '{{target_str}}' not found in ComponentServer."}}

instance = proxy.CreateInstance()
if not instance:
    return {{'success': False, 'error': f"Failed to instantiate component '{{target_str}}'."}}

instance.CreateAttributes()
instance.Attributes.Pivot = PointF(float({x}), float({y}))

custom_nick = {repr(nickname)}
if custom_nick:
    instance.NickName = custom_nick

doc.AddObject(instance, False)
doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'instance_guid': str(instance.InstanceGuid),
    'component_guid': str(instance.ComponentGuid),
    'name': str(instance.Name),
    'nickname': str(instance.NickName),
    'category': str(instance.Category),
    'pivot': [float({x}), float({y})]
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_remove_object(target_id_or_name: str) -> Dict[str, Any]:
    """Remove a component or parameter from the active canvas by instance GUID, name, or nickname."""
    script = f"""
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

target = {repr(str(target_id_or_name).lower())}
to_remove = []

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    cguid = str(obj.ComponentGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if target in (iguid, cguid, name, nick):
        to_remove.append(obj)

if not to_remove:
    return {{'success': False, 'error': f"No object matching '{{target}}' found on canvas"}}

removed = []
for obj in to_remove:
    doc.RemoveObject(obj, False)
    removed.append(str(obj.InstanceGuid))

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{'success': True, 'removed_count': len(removed), 'removed_guids': removed}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_wire(
    source_id_or_name: str,
    target_id_or_name: str,
    source_pin: Union[int, str] = 0,
    target_pin: Union[int, str] = 0
) -> Dict[str, Any]:
    """
    Connect an output parameter of source component to an input parameter of target component.
    Pins can be 0-based integer indexes or pin Names/NickNames.
    """
    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

src_target = {repr(str(source_id_or_name).lower())}
dst_target = {repr(str(target_id_or_name).lower())}

src_obj = None
dst_obj = None

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if not src_obj and src_target in (iguid, name, nick):
        src_obj = obj
    if not dst_obj and dst_target in (iguid, name, nick):
        dst_obj = obj

if not src_obj:
    return {{'success': False, 'error': f"Source object '{{src_target}}' not found"}}
if not dst_obj:
    return {{'success': False, 'error': f"Target object '{{dst_target}}' not found"}}

src_param = None
if isinstance(src_obj, gh_kernel.IGH_Component):
    outputs = src_obj.Params.Output
    s_pin = {repr(source_pin)}
    if isinstance(s_pin, int) and 0 <= s_pin < outputs.Count:
        src_param = outputs[s_pin]
    else:
        s_pin_str = str(s_pin).lower()
        for p in outputs:
            if p.Name.lower() == s_pin_str or p.NickName.lower() == s_pin_str:
                src_param = p
                break
elif isinstance(src_obj, gh_kernel.IGH_Param):
    src_param = src_obj

if not src_param:
    return {{'success': False, 'error': f"Could not resolve output pin '{{{repr(source_pin)}}}' on source object"}}

dst_param = None
if isinstance(dst_obj, gh_kernel.IGH_Component):
    inputs = dst_obj.Params.Input
    d_pin = {repr(target_pin)}
    if isinstance(d_pin, int) and 0 <= d_pin < inputs.Count:
        dst_param = inputs[d_pin]
    else:
        d_pin_str = str(d_pin).lower()
        for p in inputs:
            if p.Name.lower() == d_pin_str or p.NickName.lower() == d_pin_str:
                dst_param = p
                break
elif isinstance(dst_obj, gh_kernel.IGH_Param):
    dst_param = dst_obj

if not dst_param:
    return {{'success': False, 'error': f"Could not resolve input pin '{{{repr(target_pin)}}}' on target object"}}

dst_param.AddSource(src_param)
doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'source': {{'name': str(src_obj.Name), 'instance_guid': str(src_obj.InstanceGuid), 'output': str(src_param.Name)}},
    'target': {{'name': str(dst_obj.Name), 'instance_guid': str(dst_obj.InstanceGuid), 'input': str(dst_param.Name)}}
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_unwire(
    target_id_or_name: str,
    target_pin: Union[int, str] = 0,
    source_id_or_name: Optional[str] = None
) -> Dict[str, Any]:
    """Disconnect wire(s) leading into target input pin."""
    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

dst_target = {repr(str(target_id_or_name).lower())}
dst_obj = None

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if dst_target in (iguid, name, nick):
        dst_obj = obj
        break

if not dst_obj:
    return {{'success': False, 'error': f"Target object '{{dst_target}}' not found"}}

dst_param = None
if isinstance(dst_obj, gh_kernel.IGH_Component):
    inputs = dst_obj.Params.Input
    d_pin = {repr(target_pin)}
    if isinstance(d_pin, int) and 0 <= d_pin < inputs.Count:
        dst_param = inputs[d_pin]
    else:
        d_pin_str = str(d_pin).lower()
        for p in inputs:
            if p.Name.lower() == d_pin_str or p.NickName.lower() == d_pin_str:
                dst_param = p
                break
elif isinstance(dst_obj, gh_kernel.IGH_Param):
    dst_param = dst_obj

if not dst_param:
    return {{'success': False, 'error': f"Could not resolve input pin '{{{repr(target_pin)}}}' on target object"}}

src_target = {repr(str(source_id_or_name).lower() if source_id_or_name else None)}
disconnected = 0

if src_target:
    to_remove = []
    for s in dst_param.Sources:
        parent_obj = s.Attributes.GetTopLevel.DocObject
        if src_target in (str(s.InstanceGuid).lower(), str(parent_obj.Name).lower(), str(parent_obj.NickName).lower()):
            to_remove.append(s)
    for s in to_remove:
        dst_param.RemoveSource(s)
        disconnected += 1
else:
    disconnected = dst_param.Sources.Count
    dst_param.Sources.Clear()

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'disconnected_count': disconnected,
    'target': str(dst_obj.Name),
    'input': str(dst_param.Name)
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_set_value(target_id_or_name: str, value: Any) -> Dict[str, Any]:
    """Set the value of a Number Slider, Panel text, or Boolean Toggle on canvas."""
    script = f"""
import sys
import System
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

target = {repr(str(target_id_or_name).lower())}
target_obj = None

for obj in doc.Objects:
    iguid = str(obj.InstanceGuid).lower()
    name = str(obj.Name).lower()
    nick = str(obj.NickName).lower()
    if target in (iguid, name, nick):
        target_obj = obj
        break

if not target_obj:
    return {{'success': False, 'error': f"Object '{{target}}' not found on canvas"}}

val = {repr(value)}
tname = type(target_obj).__name__
updated_type = None

if 'Slider' in tname or hasattr(target_obj, 'Slider'):
    try:
        target_obj.Slider.Value = System.Decimal(float(val))
    except Exception:
        target_obj.Slider.Value = float(val)
    target_obj.ExpireSolution(False)
    updated_type = 'Slider'
elif 'Panel' in tname or hasattr(target_obj, 'UserText'):
    target_obj.UserText = str(val)
    target_obj.ExpireSolution(False)
    updated_type = 'Panel'
elif 'BooleanToggle' in tname or hasattr(target_obj, 'Value'):
    target_obj.Value = bool(val if isinstance(val, bool) else (str(val).lower() in ('true', '1', 'yes')))
    target_obj.ExpireSolution(False)
    updated_type = 'BooleanToggle'
else:
    return {{'success': False, 'error': f"Object type '{{tname}}' does not support live value mutation"}}

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {{
    'success': True,
    'object': str(target_obj.Name),
    'instance_guid': str(target_obj.InstanceGuid),
    'type': updated_type,
    'new_value': val
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_solve() -> Dict[str, Any]:
    """Force recomputation of the active Grasshopper document and refresh canvas."""
    script = """
import Grasshopper

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {'success': False, 'error': 'No active Grasshopper document'}

doc.NewSolution(False)
if canvas:
    canvas.Refresh()

return {
    'success': True,
    'doc_name': str(doc.DisplayName),
    'objects_count': doc.ObjectCount
}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_save(filepath: Optional[str] = None) -> Dict[str, Any]:
    """Save the active Grasshopper document quietly without prompting."""
    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

canvas = Grasshopper.Instances.ActiveCanvas
doc = canvas.Document if canvas else None

if not doc:
    return {{'success': False, 'error': 'No active Grasshopper document'}}

path = {repr(filepath)} or doc.FilePath
if not path:
    return {{'success': False, 'error': 'No target file path specified and document has no existing FilePath'}}

doc_io = gh_kernel.GH_DocumentIO(doc)
saved = doc_io.SaveQuiet(path)

return {{
    'success': bool(saved),
    'file_path': str(path),
    'objects_count': doc.ObjectCount
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}


def live_open(filepath: str) -> Dict[str, Any]:
    """Open a .gh or .ghx file directly into the active Grasshopper canvas."""
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        return {"success": False, "error": f"File does not exist: {abs_path}"}

    script = f"""
import Grasshopper
import Grasshopper.Kernel as gh_kernel

target = {repr(abs_path)}
canvas = Grasshopper.Instances.ActiveCanvas
doc_server = Grasshopper.Instances.DocumentServer

doc_io = gh_kernel.GH_DocumentIO()
opened = doc_io.Open(target)

if not opened or not doc_io.Document:
    return {{'success': False, 'error': f"Failed to open definition from {{target}}"}}

new_doc = doc_io.Document
if doc_server:
    doc_server.AddDocument(new_doc)
if canvas:
    canvas.Document = new_doc
    canvas.Refresh()

return {{
    'success': True,
    'file_path': str(target),
    'doc_name': str(new_doc.DisplayName),
    'objects_count': new_doc.ObjectCount
}}
"""
    res = run_in_rhino(script)
    if res.get("success"):
        return res.get("result", {})
    return {"success": False, "error": res.get("error")}
