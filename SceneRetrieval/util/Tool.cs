using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.util
{
    class Tool
    {
        public static void setProcessArgs(Process process,String pyFile,String[] param,EventHandler handler)
        {
            process.StartInfo.FileName = Program.pythonExePath;

            String arguments = Program.pythonFilePath + pyFile;
            
            if (param != null)
            {
                foreach (String arg in param)
                {
                    arguments += " " + arg;
                }
            }
           
            process.StartInfo.Arguments = arguments;

            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.RedirectStandardInput = true;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.CreateNoWindow = true;

            if (handler != null)
            {
                process.EnableRaisingEvents = true;
                process.Exited += handler;
            }
           
        }
    }
}
