// Grasshopper C# Script Component: Export Component to User Object (.ghuser)
// Automatically saves a target Grasshopper component as a permanent toolbar User Object.
// Target GUID: a9a8ebd2-fff5-4c44-a8f5-739736d129ba (Component_CSNET_Script)

using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Rhino;
using Rhino.Geometry;
using Grasshopper;
using Grasshopper.Kernel;

public class Script_Instance : GH_ScriptInstance
{
    public void RunScript(
        bool export,
        string category,
        string subcategory,
        ref object status,
        ref object path)
    {
        if (!export)
        {
            status = "Ready to export. Set 'export' to True to save .ghuser into Grasshopper toolbar.";
            path = null;
            return;
        }

        var doc = OnPingDocument();
        if (doc == null)
        {
            status = "Error: Active Grasshopper document not found.";
            return;
        }

        // Find the Viewport Controller component in the current document
        IGH_Component targetComp = null;
        foreach (var obj in doc.Objects)
        {
            if (obj is IGH_Component comp)
            {
                if (comp.NickName == "ViewportController" || comp.NickName == "ViewportControlCS" || comp.Name == "C# Script")
                {
                    targetComp = comp;
                    break;
                }
            }
        }

        if (targetComp == null)
        {
            status = "Error: Viewport Controller component not found on canvas.";
            return;
        }

        try
        {
            var uo = new GH_UserObject();
            uo.Description.Name = "Viewport Controller";
            uo.Description.NickName = "ViewCtrl";
            uo.Description.Description = "Parametrically controls active Rhino viewport camera, target, lens focal length, orbit, and display modes.";
            uo.Description.Category = string.IsNullOrWhiteSpace(category) ? "Display" : category;
            uo.Description.SubCategory = string.IsNullOrWhiteSpace(subcategory) ? "Viewport" : subcategory;
            uo.BaseGuid = targetComp.ComponentGuid;

            // Serialize component state into UserObject
            uo.SetDataFromObject(targetComp);

            // Save to Grasshopper's official UserObjects directory
            string userObjFolder = Folders.UserObjectFolder;
            if (!Directory.Exists(userObjFolder))
            {
                Directory.CreateDirectory(userObjFolder);
            }

            string filePath = Path.Combine(userObjFolder, "ViewportController.ghuser");
            uo.Path = filePath;
            bool saved = uo.SaveToFile();

            if (saved)
            {
                // Register in the active Grasshopper component library ribbon
                Instances.ComponentServer.AddUserObject(uo);
                status = "Successfully saved and registered User Object into Grasshopper toolbar!";
                path = filePath;
            }
            else
            {
                status = "Error: Failed to save .ghuser file.";
            }
        }
        catch (Exception ex)
        {
            status = "Exception during export: " + ex.Message;
        }
    }
}
