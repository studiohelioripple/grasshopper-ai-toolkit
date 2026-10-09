"""
Rhino Viewport Controller for Grasshopper (GhPython)
=====================================================
Directly controls Rhino 3D viewports from Grasshopper in real-time.

Inputs (add to GhPython Script Component):
  run          (bool)     : Active toggle. Set True to update viewport, False to pause/unlock.
  view_name    (str)      : Target viewport name (e.g. 'Perspective', 'Top', 'Front'). Empty for ActiveView.
  target       (Point3d)  : Look-at target point. Default is (0, 0, 0).
  camera       (Point3d)  : Explicit camera position. If None, calculated from orbit (azim, elev, dist).
  azim         (float)    : Orbit Azimuth angle in degrees (0..360). Default 45.0.
  elev         (float)    : Orbit Elevation angle in degrees (-89..89). Default 30.0.
  dist         (float)    : Distance from target in model units. Default 100.0.
  lens         (float)    : 35mm camera focal length in mm. Default 50.0.
  up           (Vector3d) : Camera UP vector. Default UnitZ (0, 0, 1).
  display_mode (str)      : Display mode name ('Shaded', 'Rendered', 'Wireframe', 'Ghosted', 'Arctic', 'Raytraced').
  projection   (str)      : 'Perspective' or 'Parallel'. Default 'Perspective'.
  bbox         (geom/bbox): Optional geometry or BoundingBox to Zoom-Fit into view.
  redraw       (bool)     : If True, triggers immediate Rhino view redraw. Default True.

Outputs:
  cam_pt       (Point3d)  : Current / applied camera location.
  target_pt    (Point3d)  : Current / applied target point.
  cam_dir      (Vector3d) : Normalized camera view direction vector.
  cam_plane    (Plane)    : Camera view plane (origin at camera, Z pointing at target).
  frustum      (list)     : 3D visual wireframe lines of camera cone/frustum in GH preview.
  status       (str)      : Diagnostic status summary.

Hot-reload via gh-toolkit CLI:
  gh-toolkit live inject ViewportControl examples/viewport_controller.py
  gh-toolkit live watch  ViewportControl examples/viewport_controller.py
"""

import math

# Safe imports for standalone execution and Rhino/GhPython execution
try:
    import Rhino
    import Rhino.Geometry as rg
    import scriptcontext as sc
    RHINO_AVAILABLE = True
except ImportError:
    RHINO_AVAILABLE = False
    Rhino = None
    rg = None
    sc = None


def get_rhino_doc():
    """Retrieve active Rhino document reliably from Grasshopper."""
    if not RHINO_AVAILABLE:
        return None
    # In GhPython, sc.doc is the Grasshopper definition.
    # The active Rhino document is always Rhino.RhinoDoc.ActiveDoc.
    return Rhino.RhinoDoc.ActiveDoc


def calculate_orbit_camera(target_point, azimuth_deg, elevation_deg, distance):
    """Calculate camera position in spherical coordinates around target point."""
    azim_rad = math.radians(float(azimuth_deg))
    elev_rad = math.radians(max(-89.9, min(89.9, float(elevation_deg))))
    d = max(0.001, float(distance))

    dx = d * math.cos(elev_rad) * math.sin(azim_rad)
    dy = d * math.cos(elev_rad) * math.cos(azim_rad)
    dz = d * math.sin(elev_rad)

    if rg:
        return rg.Point3d(target_point.X + dx, target_point.Y + dy, target_point.Z + dz)
    return (target_point[0] + dx, target_point[1] + dy, target_point[2] + dz)


def build_camera_frustum(cam_p, tgt_p, focal_length_mm, distance):
    """
    Generate 3D wireframe lines representing the camera's field of view (frustum).
    Standard 35mm film / full-frame sensor: 36mm x 24mm.
    """
    if not rg:
        return []

    lines = []
    fl = max(5.0, float(focal_length_mm))
    d = max(1.0, float(distance))

    # Field of view angles
    hfov = 2.0 * math.atan(18.0 / fl)  # half sensor width = 18mm
    vfov = 2.0 * math.atan(12.0 / fl)  # half sensor height = 12mm

    half_w = d * math.tan(hfov / 2.0)
    half_h = d * math.tan(vfov / 2.0)

    # Direction and frame orientation
    forward = tgt_p - cam_p
    if not forward.Unitize():
        forward = rg.Vector3d(0, 1, 0)

    world_up = rg.Vector3d.ZAxis
    right = rg.Vector3d.CrossProduct(forward, world_up)
    if not right.Unitize():
        world_up = rg.Vector3d.YAxis
        right = rg.Vector3d.CrossProduct(forward, world_up)
        right.Unitize()

    cam_up = rg.Vector3d.CrossProduct(right, forward)
    cam_up.Unitize()

    # Center of target plane
    plane_center = cam_p + forward * d

    # 4 corner points on target plane
    p_tl = plane_center - right * half_w + cam_up * half_h
    p_tr = plane_center + right * half_w + cam_up * half_h
    p_br = plane_center + right * half_w - cam_up * half_h
    p_bl = plane_center - right * half_w - cam_up * half_h

    # Frustum boundary lines (rectangle at target distance)
    lines.append(rg.Line(p_tl, p_tr))
    lines.append(rg.Line(p_tr, p_br))
    lines.append(rg.Line(p_br, p_bl))
    lines.append(rg.Line(p_bl, p_tl))

    # Ray lines from camera eye to 4 corners
    lines.append(rg.Line(cam_p, p_tl))
    lines.append(rg.Line(cam_p, p_tr))
    lines.append(rg.Line(cam_p, p_br))
    lines.append(rg.Line(cam_p, p_bl))

    # Sightline centerline
    lines.append(rg.Line(cam_p, plane_center))

    return lines


# ==============================================================================
# Main Execution in Grasshopper
# ==============================================================================

# Parse and normalize inputs safely
_is_active     = bool(run) if 'run' in globals() and run is not None else True
_view_name     = str(view_name).strip() if 'view_name' in globals() and view_name else ""
_target        = target if 'target' in globals() and target is not None else (rg.Point3d.Origin if rg else (0, 0, 0))
_camera_input  = camera if 'camera' in globals() and camera is not None else None
_azim          = float(azim) if 'azim' in globals() and azim is not None else 45.0
_elev          = float(elev) if 'elev' in globals() and elev is not None else 30.0
_dist          = float(dist) if 'dist' in globals() and dist is not None else 100.0
_lens          = float(lens) if 'lens' in globals() and lens is not None else 50.0
_up            = up if 'up' in globals() and up is not None else (rg.Vector3d.ZAxis if rg else (0, 0, 1))
_display_mode  = str(display_mode).strip() if 'display_mode' in globals() and display_mode else ""
_projection    = str(projection).strip().lower() if 'projection' in globals() and projection else "perspective"
_bbox          = bbox if 'bbox' in globals() and bbox is not None else None
_redraw        = bool(redraw) if 'redraw' in globals() and redraw is not None else True

# Determine camera position (explicit point or orbit calculation)
if _camera_input is not None:
    _final_cam = _camera_input
    if rg and hasattr(_final_cam, "DistanceTo"):
        _final_dist = _final_cam.DistanceTo(_target)
    else:
        _final_dist = _dist
else:
    _final_cam = calculate_orbit_camera(_target, _azim, _elev, _dist)
    _final_dist = _dist

# Direction vector & camera plane
if rg:
    _direction = _target - _final_cam
    _dir_unit = rg.Vector3d(_direction)
    _dir_unit.Unitize()
    _cam_plane = rg.Plane(_final_cam, _dir_unit)
    _frustum = build_camera_frustum(_final_cam, _target, _lens, _final_dist)
else:
    _direction = None
    _dir_unit = None
    _cam_plane = None
    _frustum = []

# Expose Outputs to Grasshopper canvas
cam_pt    = _final_cam
target_pt = _target
cam_dir   = _dir_unit
cam_plane = _cam_plane
frustum   = _frustum
status    = "Ready"

# Apply Viewport Changes if active and running inside Rhino
doc = get_rhino_doc()

if not _is_active:
    status = "Paused (run=False). Viewport unlocked for interactive navigation."
elif not doc:
    status = "Waiting: Rhino document not connected."
else:
    try:
        # Find specified view or fallback to active view
        target_view = None
        if _view_name:
            target_view = doc.Views.Find(_view_name, False)
        if not target_view:
            target_view = doc.Views.ActiveView

        if not target_view:
            status = "Error: Viewport '{0}' not found and no active view exists.".format(_view_name)
        else:
            vp = target_view.ActiveViewport

            # 1. Update Camera Projection Mode (Perspective vs Parallel)
            if _projection in ("parallel", "ortho", "isometric"):
                if not vp.IsParallelProjection:
                    vp.ChangeToParallelProjection(True)
            elif _projection in ("perspective", "persp"):
                if not vp.IsPerspectiveProjection:
                    vp.ChangeToPerspectiveProjection(True)

            # 2. Update Camera Position & Target
            # Setting camera target first, then location, maintains correct direction
            vp.SetCameraTarget(_target, False)
            vp.SetCameraLocation(_final_cam, False)
            vp.CameraUp = _up

            # 3. Update Focal Length / Lens
            if vp.IsPerspectiveProjection:
                vp.Camera35mmLensLength = _lens

            # 4. Optional Display Mode (e.g. Shaded, Rendered, Arctic)
            if _display_mode:
                mode_desc = Rhino.Display.DisplayModeDescription.FindByName(_display_mode)
                if mode_desc:
                    vp.DisplayMode = mode_desc

            # 5. Optional Zoom to Bounding Box / Extents
            if _bbox is not None:
                if hasattr(_bbox, "GetBoundingBox"):
                    b = _bbox.GetBoundingBox(True)
                    vp.ZoomBoundingBox(b)
                elif isinstance(_bbox, rg.BoundingBox):
                    vp.ZoomBoundingBox(_bbox)

            # 6. Redraw Viewport
            if _redraw:
                target_view.Redraw()

            status = (
                "Active View: '{0}' | Camera: ({1:.1f}, {2:.1f}, {3:.1f}) | Target: ({4:.1f}, {5:.1f}, {6:.1f}) | Lens: {7:.0f}mm | Dist: {8:.1f}"
            ).format(
                target_view.MainViewport.Name,
                _final_cam.X, _final_cam.Y, _final_cam.Z,
                _target.X, _target.Y, _target.Z,
                _lens, _final_dist
            )

    except Exception as e:
        status = "Viewport update exception: {0}".format(str(e))
