using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Rhino.Display;

public class ViewportController
{
    /*
    Rhino Viewport Controller for Grasshopper (C# Script Component)
    ===============================================================
    Directly controls Rhino 3D viewports from Grasshopper in real-time.

    Inputs (add to C# Script Component):
      run          (bool)     : Active toggle (True to sync viewport, False to pause/unlock)
      view_name    (string)   : Target viewport name (e.g. "Perspective", or empty for ActiveView)
      target       (Point3d)  : Look-at target point (default Origin 0,0,0)
      camera       (Point3d)  : Explicit camera location (or Point3d.Unset to use orbit)
      azim         (double)   : Orbit Azimuth angle in degrees (0..360)
      elev         (double)   : Orbit Elevation angle in degrees (-89..89)
      dist         (double)   : Orbit Distance from target
      lens         (double)   : 35mm camera focal length in mm (default 50.0)
      display_mode (string)   : Display mode ("Shaded", "Rendered", "Arctic", etc.)

    Outputs:
      cam_pt       (Point3d)  : Current applied camera point
      target_pt    (Point3d)  : Current applied target point
      cam_dir      (Vector3d) : Normalized camera direction vector
      frustum      (List<Line>): 3D wireframe preview of camera frustum
      status       (string)   : Diagnostic status message
    */

    public void RunScript(
        bool run,
        string view_name,
        Point3d target,
        Point3d camera,
        double azim,
        double elev,
        double dist,
        double lens,
        string display_mode,
        ref object cam_pt,
        ref object target_pt,
        ref object cam_dir,
        ref object frustum,
        ref object status)
    {
        // Safe defaults
        if (target == Point3d.Unset) target = Point3d.Origin;
        if (dist <= 0) dist = 100.0;
        if (lens <= 0) lens = 50.0;

        // Compute camera position (explicit or spherical orbit)
        Point3d finalCam;
        if (camera != Point3d.Unset && camera.IsValid && camera != Point3d.Origin)
        {
            finalCam = camera;
        }
        else
        {
            double azimRad = azim * (Math.PI / 180.0);
            double clampedElev = Math.Max(-89.9, Math.Min(89.9, elev));
            double elevRad = clampedElev * (Math.PI / 180.0);

            double dx = dist * Math.Cos(elevRad) * Math.Sin(azimRad);
            double dy = dist * Math.Cos(elevRad) * Math.Cos(azimRad);
            double dz = dist * Math.Sin(elevRad);
            finalCam = new Point3d(target.X + dx, target.Y + dy, target.Z + dz);
        }

        Vector3d forward = target - finalCam;
        Vector3d forwardUnit = new Vector3d(forward);
        forwardUnit.Unitize();

        // Build frustum wireframe visualization
        List<Line> frustumLines = BuildFrustum(finalCam, target, lens, finalCam.DistanceTo(target));

        // Assign output parameters
        cam_pt = finalCam;
        target_pt = target;
        cam_dir = forwardUnit;
        frustum = frustumLines;

        if (!run)
        {
            status = "Paused (run=false). Interactive navigation unlocked.";
            return;
        }

        RhinoDoc doc = RhinoDoc.ActiveDoc;
        if (doc == null)
        {
            status = "Waiting: RhinoDoc not available.";
            return;
        }

        try
        {
            Rhino.Display.RhinoView view = null;
            if (!string.IsNullOrWhiteSpace(view_name))
            {
                view = doc.Views.Find(view_name.Trim(), false);
            }
            if (view == null)
            {
                view = doc.Views.ActiveView;
            }

            if (view == null)
            {
                status = "Error: No active Rhino viewport found.";
                return;
            }

            Rhino.Display.RhinoViewport vp = view.ActiveViewport;

            // Update Target, Location, and Up
            vp.SetCameraTarget(target, false);
            vp.SetCameraLocation(finalCam, false);
            vp.CameraUp = Vector3d.ZAxis;

            // Update lens focal length
            if (vp.IsPerspectiveProjection)
            {
                vp.Camera35mmLensLength = lens;
            }

            // Display Mode
            if (!string.IsNullOrWhiteSpace(display_mode))
            {
                var modeDesc = Rhino.Display.DisplayModeDescription.FindByName(display_mode.Trim());
                if (modeDesc != null)
                {
                    vp.DisplayMode = modeDesc;
                }
            }

            view.Redraw();

            status = string.Format(
                "Active View: '{0}' | Camera: ({1:F1}, {2:F1}, {3:F1}) | Target: ({4:F1}, {5:F1}, {6:F1}) | Lens: {7:F0}mm",
                view.MainViewport.Name, finalCam.X, finalCam.Y, finalCam.Z, target.X, target.Y, target.Z, lens
            );
        }
        catch (Exception ex)
        {
            status = "Exception: " + ex.Message;
        }
    }

    private static List<Line> BuildFrustum(Point3d camP, Point3d tgtP, double lensMm, double distance)
    {
        var lines = new List<Line>();
        double fl = Math.Max(5.0, lensMm);
        double d = Math.Max(1.0, distance);

        double hfov = 2.0 * Math.Atan(18.0 / fl);
        double vfov = 2.0 * Math.Atan(12.0 / fl);

        double halfW = d * Math.Tan(hfov / 2.0);
        double halfH = d * Math.Tan(vfov / 2.0);

        Vector3d forward = tgtP - camP;
        if (!forward.Unitize()) forward = new Vector3d(0, 1, 0);

        Vector3d worldUp = Vector3d.ZAxis;
        Vector3d right = Vector3d.CrossProduct(forward, worldUp);
        if (!right.Unitize())
        {
            worldUp = Vector3d.YAxis;
            right = Vector3d.CrossProduct(forward, worldUp);
            right.Unitize();
        }

        Vector3d camUp = Vector3d.CrossProduct(right, forward);
        camUp.Unitize();

        Point3d center = camP + forward * d;
        Point3d tl = center - right * halfW + camUp * halfH;
        Point3d tr = center + right * halfW + camUp * halfH;
        Point3d br = center + right * halfW - camUp * halfH;
        Point3d bl = center - right * halfW - camUp * halfH;

        lines.Add(new Line(tl, tr));
        lines.Add(new Line(tr, br));
        lines.Add(new Line(br, bl));
        lines.Add(new Line(bl, tl));

        lines.Add(new Line(camP, tl));
        lines.Add(new Line(camP, tr));
        lines.Add(new Line(camP, br));
        lines.Add(new Line(camP, bl));
        lines.Add(new Line(camP, center));

        return lines;
    }
}
