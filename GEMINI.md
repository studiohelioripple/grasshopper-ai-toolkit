# Grasshopper AI Toolkit — Engineering Invariants & Coding Rules

## 1. Scripting Language Priority Invariant
- **C# Script Priority**: All custom Grasshopper scripts, synthesized definitions, and live canvas components MUST be written in **C# (`.cs`)** by default.
- **Python Exception**: Do NOT generate Python / GhPython scripts unless the user **explicitly asserts** that Python should be used.
- **Rationale**:
  - Rhino 8's .NET 8 runtime executes C# natively with 100% reliability, compiled speed, and zero external environment degradation.
  - Avoids Python environment corruption (`py39-rh8` site-env issues) and IronPython 2.7 syntax constraints.
  - Native access to all RhinoCommon (`Rhino.Geometry`, `Rhino.Display`, `Rhino.DocObjects`) and loaded GHA assemblies (`Heteroptera`, `LegoPod`, `Magpie`).

## 2. Component GUID Invariants
- **C# Script Component**: Active GUID `a9a8ebd2-fff5-4c44-a8f5-739736d129ba` (`ScriptComponents.Component_CSNET_Script`).
- **Input Parameters**: Use `Param_ScriptVariable` with type hints (`GH_BooleanHint_CS`, `GH_DoubleHint_CS`, `GH_StringHint_CS`, `GH_Point3dHint`).
- **Rhino Types**: Fully qualify `Rhino.Display.RhinoView`, `Rhino.Display.RhinoViewport`, and `Rhino.Display.DisplayModeDescription`.

## 3. Live Canvas Editing Protocol
- Always verify `DOTNET_ROLL_FORWARD=LatestMajor`.
- Keep canvas layout tidy: Sliders & Toggles on X: 100–160, Scripts on X: 400–450, Output Panels on X: 700–750.
