using System;
using System.IO;
using System.Reflection;

class Program
{
    static int Main(string[] args)
    {
        if (args.Length < 1)
        {
            Console.Error.WriteLine("Usage: rhino_bridge <python_script_path> [pipe_id]");
            return 1;
        }

        string scriptPath = Path.GetFullPath(args[0]);
        string pipeId = args.Length > 1 ? args[1] : null;

        if (string.IsNullOrEmpty(pipeId))
        {
            try
            {
                var tempPath = Path.GetTempPath();
                var pipes = Directory.GetFiles(tempPath, "*remotepipe*");
                if (pipes.Length > 0)
                {
                    pipeId = Path.GetFileName(pipes[0]).Replace("CoreFxPipe_", "");
                }
            }
            catch {}
        }

        if (string.IsNullOrEmpty(pipeId))
        {
            pipeId = "rhinocode_remotepipe_1074";
        }

        try
        {
            var asmPath = "/Applications/Rhino 8.app/Contents/Frameworks/RhCore.framework/Versions/Current/Resources/Rhino.Runtime.Code.Remote.dll";
            var asm = Assembly.LoadFrom(asmPath);
            var clientType = asm.GetType("Rhino.Runtime.Code.Remote.Client.PipeClient");
            var client = Activator.CreateInstance(clientType, new object[] { pipeId });

            var jobReqType = asm.GetType("Rhino.Runtime.Code.Remote.Requests.JobRequest");
            var job = Activator.CreateInstance(jobReqType);
            jobReqType.GetProperty("Endpoint").SetValue(job, "command");
            jobReqType.GetProperty("Payload").SetValue(job, $"_-RunPythonScript \"{scriptPath}\"");

            var executeMethod = clientType.GetMethod("Execute", new Type[] { jobReqType });
            executeMethod.Invoke(client, new object[] { job });
            return 0;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Bridge error: {ex.InnerException?.Message ?? ex.Message}");
            return 2;
        }
    }
}
