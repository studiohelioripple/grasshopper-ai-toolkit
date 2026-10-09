using System;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Rhino.Display;
using Rhino.UI;
using Eto.Forms;
using Eto.Drawing;

public class ViewportPiP
{
    /*
    Rhino Viewport Picture-in-Picture (PiP) Window for Grasshopper (C# Script Component)
    ===================================================================================
    Creates and manages a high-performance floating mini-viewport window directly over
    the Grasshopper / Rhino workspace with real-time live refresh.

    Inputs (add to C# Script Component):
      run          (bool)     : Active toggle (True to open/stream PiP window, False to close)
      view_name    (string)   : Target viewport name (e.g. "Perspective", or empty for ActiveView)
      width        (double)   : PiP window width in pixels (default: 420)
      height       (double)   : PiP window height in pixels (default: 320)
      fps          (double)   : Live refresh frame rate (default: 15.0 fps)
      display_mode (string)   : Display mode ("Shaded", "Rendered", "Arctic", "Ghosted", "Wireframe", or empty)

    Outputs:
      is_open      (bool)     : True if PiP window is currently visible and active
      active_view  (string)   : Name of the Rhino viewport currently being displayed
      resolution   (string)   : Render resolution of the mini-viewport (e.g. "420 x 280")
      status       (string)   : Live telemetry / diagnostics / status report
    */

    public void RunScript(
        bool run,
        string view_name,
        double width,
        double height,
        double fps,
        string display_mode,
        ref object is_open,
        ref object active_view,
        ref object resolution,
        ref object status)
    {
        // Safe parameter clamping
        int w = (int)Math.Max(200, Math.Min(3840, width <= 0 ? 420 : width));
        int h = (int)Math.Max(150, Math.Min(2160, height <= 0 ? 320 : height));
        double targetFps = Math.Max(1.0, Math.Min(60.0, fps <= 0 ? 15.0 : fps));

        RhinoDoc doc = RhinoDoc.ActiveDoc;
        if (doc == null)
        {
            is_open = false;
            active_view = "None";
            resolution = "0 x 0";
            status = "Waiting: RhinoDoc not available.";
            return;
        }

        // Handle Close request
        if (!run)
        {
            if (PiPWindowInstance.Current != null)
            {
                PiPWindowInstance.Current.SafeClose();
            }
            is_open = false;
            active_view = "Closed";
            resolution = "0 x 0";
            status = "PiP Window closed (run=false). Toggle 'run' to True to open.";
            return;
        }

        // Resolve target Rhino View
        Rhino.Display.RhinoView targetView = null;
        if (!string.IsNullOrWhiteSpace(view_name))
        {
            targetView = doc.Views.Find(view_name.Trim(), false);
        }
        if (targetView == null)
        {
            targetView = doc.Views.ActiveView;
        }

        if (targetView == null)
        {
            is_open = false;
            active_view = "Not found";
            resolution = "0 x 0";
            status = "Error: No matching Rhino viewport found.";
            return;
        }

        // Apply display mode if specified
        if (!string.IsNullOrWhiteSpace(display_mode))
        {
            var modeDesc = Rhino.Display.DisplayModeDescription.FindByName(display_mode.Trim());
            if (modeDesc != null && targetView.ActiveViewport.DisplayMode.Id != modeDesc.Id)
            {
                targetView.ActiveViewport.DisplayMode = modeDesc;
                targetView.Redraw();
            }
        }

        // Ensure PiP Window is open and running
        PiPWindowInstance.EnsureOpen(targetView.MainViewport.Name, w, h, targetFps);

        // Populate outputs
        is_open = PiPWindowInstance.Current != null && PiPWindowInstance.Current.Visible;
        active_view = targetView.MainViewport.Name;
        resolution = string.Format("{0} x {1}", w, h);
        status = string.Format(
            "PiP Active | View: '{0}' | Res: {1}x{2} | FPS: {3:F0} | Mode: '{4}'",
            targetView.MainViewport.Name,
            w,
            h,
            targetFps,
            targetView.ActiveViewport.DisplayMode.EnglishName
        );
    }

    // =========================================================================
    // Additional Code: PiP Window Lifecycle & UI Implementation
    // =========================================================================

    public class PiPWindowInstance : Eto.Forms.FloatingForm
    {
        public static PiPWindowInstance Current { get; private set; }

        private readonly Eto.Forms.ImageView _imageView;
        private readonly Eto.Forms.Label _titleLabel;
        private readonly Eto.Forms.Label _statusBadge;
        private readonly Eto.Forms.DropDown _modeDropDown;
        private readonly Eto.Forms.DropDown _viewDropDown;
        private readonly Eto.Forms.UITimer _timer;

        private string _targetViewName;
        private double _fps;
        private int _frameCount = 0;
        private DateTime _lastFpsCheck = DateTime.UtcNow;
        private double _currentFps = 0.0;
        private bool _isUpdating = false;

        public static void EnsureOpen(string viewName, int width, int height, double fps)
        {
            if (Current == null || Current.IsDisposed)
            {
                Current = new PiPWindowInstance(viewName, width, height, fps);
                Current.Show();
            }
            else
            {
                Current.UpdateSettings(viewName, width, height, fps);
            }
        }

        public PiPWindowInstance(string viewName, int width, int height, double fps)
        {
            Current = this;
            _targetViewName = viewName;
            _fps = fps;

            Title = "Rhino Viewport PiP";
            Topmost = true;
            Resizable = true;
            MinimumSize = new Eto.Drawing.Size(260, 180);
            ClientSize = new Eto.Drawing.Size(width, height);
            Padding = new Eto.Drawing.Padding(0);
            BackgroundColor = Eto.Drawing.Colors.Black;

            // Header Toolbar
            _titleLabel = new Eto.Forms.Label
            {
                Text = " ● PiP",
                TextColor = Eto.Drawing.Colors.WhiteSmoke,
                Font = Eto.Drawing.SystemFonts.Bold(11),
                VerticalAlignment = Eto.Forms.VerticalAlignment.Center
            };

            _statusBadge = new Eto.Forms.Label
            {
                Text = "LIVE",
                TextColor = Eto.Drawing.Color.FromArgb(76, 217, 100),
                Font = Eto.Drawing.SystemFonts.Bold(10),
                VerticalAlignment = Eto.Forms.VerticalAlignment.Center
            };

            // Mode selector dropdown
            _modeDropDown = new Eto.Forms.DropDown();
            _modeDropDown.Items.Add("Shaded");
            _modeDropDown.Items.Add("Rendered");
            _modeDropDown.Items.Add("Arctic");
            _modeDropDown.Items.Add("Ghosted");
            _modeDropDown.Items.Add("Wireframe");
            _modeDropDown.SelectedValue = "Shaded";
            _modeDropDown.SelectedValueChanged += OnModeChanged;

            // View selector dropdown
            _viewDropDown = new Eto.Forms.DropDown();
            PopulateViews();
            _viewDropDown.SelectedValueChanged += OnViewChanged;

            // Quick Snapshot Button
            var snapBtn = new Eto.Forms.Button { Text = "📷 Snap" };
            snapBtn.Click += (s, e) => SaveSnapshot();

            // Toolbar layout
            var headerLayout = new Eto.Forms.DynamicLayout();
            headerLayout.Padding = new Eto.Drawing.Padding(6, 4);
            headerLayout.Spacing = new Eto.Drawing.Size(6, 4);
            headerLayout.BackgroundColor = Eto.Drawing.Color.FromArgb(32, 32, 36);

            headerLayout.BeginHorizontal();
            headerLayout.Add(_titleLabel);
            headerLayout.Add(_statusBadge);
            headerLayout.Add(null, true);
            headerLayout.Add(_viewDropDown);
            headerLayout.Add(_modeDropDown);
            headerLayout.Add(snapBtn);
            headerLayout.EndHorizontal();

            // Central Image View
            _imageView = new Eto.Forms.ImageView
            {
                BackgroundColor = Eto.Drawing.Colors.Black
            };

            // Main Layout
            var contentLayout = new Eto.Forms.DynamicLayout();
            contentLayout.Padding = new Eto.Drawing.Padding(0);
            contentLayout.Spacing = new Eto.Drawing.Size(0, 0);

            contentLayout.Add(headerLayout);
            contentLayout.Add(_imageView, yscale: true);

            Content = contentLayout;

            // Timer setup for live refresh
            _timer = new Eto.Forms.UITimer();
            _timer.Interval = 1.0 / Math.Max(1.0, _fps);
            _timer.Elapsed += (s, e) => CaptureFrame();
            _timer.Start();

            // Handle window close
            Closed += (s, e) =>
            {
                _timer.Stop();
                _timer.Dispose();
                if (Current == this) Current = null;
            };

            // Capture initial frame
            CaptureFrame();
        }

        public void UpdateSettings(string viewName, int width, int height, double fps)
        {
            if (!string.IsNullOrEmpty(viewName) && _targetViewName != viewName)
            {
                _targetViewName = viewName;
                _viewDropDown.SelectedValue = viewName;
            }

            if (Math.Abs(_fps - fps) > 0.5)
            {
                _fps = fps;
                _timer.Interval = 1.0 / Math.Max(1.0, _fps);
            }
        }

        private void PopulateViews()
        {
            _viewDropDown.Items.Clear();
            var doc = RhinoDoc.ActiveDoc;
            if (doc != null)
            {
                foreach (var v in doc.Views)
                {
                    _viewDropDown.Items.Add(v.MainViewport.Name);
                }
            }
            if (!string.IsNullOrEmpty(_targetViewName))
            {
                _viewDropDown.SelectedValue = _targetViewName;
            }
        }

        private void OnModeChanged(object sender, EventArgs e)
        {
            var doc = RhinoDoc.ActiveDoc;
            if (doc == null || _modeDropDown.SelectedValue == null) return;
            string modeName = _modeDropDown.SelectedValue.ToString();
            var modeDesc = Rhino.Display.DisplayModeDescription.FindByName(modeName);
            if (modeDesc != null)
            {
                var view = GetActiveView();
                if (view != null)
                {
                    view.ActiveViewport.DisplayMode = modeDesc;
                    view.Redraw();
                    CaptureFrame();
                }
            }
        }

        private void OnViewChanged(object sender, EventArgs e)
        {
            if (_viewDropDown.SelectedValue != null)
            {
                _targetViewName = _viewDropDown.SelectedValue.ToString();
                CaptureFrame();
            }
        }

        private Rhino.Display.RhinoView GetActiveView()
        {
            var doc = RhinoDoc.ActiveDoc;
            if (doc == null) return null;
            Rhino.Display.RhinoView view = null;
            if (!string.IsNullOrEmpty(_targetViewName))
            {
                view = doc.Views.Find(_targetViewName, false);
            }
            return view ?? doc.Views.ActiveView;
        }

        private void CaptureFrame()
        {
            if (_isUpdating) return;
            _isUpdating = true;

            try
            {
                var view = GetActiveView();
                if (view == null) return;

                int w = Math.Max(100, _imageView.Width > 0 ? _imageView.Width : ClientSize.Width);
                int h = Math.Max(80, _imageView.Height > 0 ? _imageView.Height : (ClientSize.Height - 34));

                using (var sysBmp = view.CaptureToBitmap(new System.Drawing.Size(w, h), true, true, false))
                {
                    if (sysBmp != null)
                    {
                        var etoBmp = Rhino.UI.EtoExtensions.ToEto(sysBmp);
                        _imageView.Image = etoBmp;
                    }
                }

                // FPS Counter
                _frameCount++;
                var elapsed = (DateTime.UtcNow - _lastFpsCheck).TotalSeconds;
                if (elapsed >= 1.0)
                {
                    _currentFps = _frameCount / elapsed;
                    _frameCount = 0;
                    _lastFpsCheck = DateTime.UtcNow;
                    _statusBadge.Text = string.Format("● LIVE ({0:F0} FPS)", _currentFps);
                }
            }
            catch (Exception)
            {
                // Silently absorb frame capture drops
            }
            finally
            {
                _isUpdating = false;
            }
        }

        private void SaveSnapshot()
        {
            var view = GetActiveView();
            if (view == null) return;
            string desktop = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            string filename = string.Format("Rhino_PiP_{0:yyyyMMdd_HHmmss}.png", DateTime.Now);
            string fullPath = System.IO.Path.Combine(desktop, filename);
            using (var bmp = view.CaptureToBitmap(new System.Drawing.Size(1920, 1080), true, true, false))
            {
                if (bmp != null)
                {
                    bmp.Save(fullPath, System.Drawing.Imaging.ImageFormat.Png);
                    RhinoApp.WriteLine("PiP Snapshot saved to: " + fullPath);
                }
            }
        }

        public void SafeClose()
        {
            try
            {
                _timer.Stop();
                _timer.Dispose();
                Close();
            }
            catch (Exception)
            {
            }
            finally
            {
                Current = null;
            }
        }
    }
}
