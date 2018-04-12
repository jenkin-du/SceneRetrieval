using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.util
{
    class PythonProcess
    {

        public delegate void OutputHandler(String output,int exitCode);
        public OutputHandler outputHandler;

        public  Process mProcess;

        /// <summary>
        /// 初始化
        /// </summary>
        /// <param name="pyFile"></param>
        public PythonProcess(String pyFile)
        {
            mProcess = new Process();
            mProcess.StartInfo.FileName = Program.pythonExePath;
            String arguments = Program.pythonFilePath + pyFile;

            mProcess.StartInfo.Arguments = arguments;

            mProcess.StartInfo.UseShellExecute = false;
            mProcess.StartInfo.RedirectStandardError = true;
            mProcess.StartInfo.RedirectStandardInput = true;
            mProcess.StartInfo.RedirectStandardOutput = true;
            mProcess.StartInfo.CreateNoWindow = true;
            //设置接受信息
            mProcess.EnableRaisingEvents = true;

            //输出错误信息
            mProcess.Exited += new EventHandler(handleErr);
            
        }

        /// <summary>
        /// 初始化
        /// </summary>
        /// <param name="pyFile"></param>
        /// <param name="param"></param>
        public PythonProcess(String pyFile, String[] param)
        {
            mProcess = new Process();
            mProcess.StartInfo.FileName = Program.pythonExePath;
            String arguments = Program.pythonFilePath + pyFile;

            //添加参数
            if (param != null)
            {
                foreach (String arg in param)
                {
                    arguments += " " + arg;
                }
            }

            mProcess.StartInfo.Arguments = arguments;

            mProcess.StartInfo.UseShellExecute = false;
            mProcess.StartInfo.RedirectStandardError = true;
            mProcess.StartInfo.RedirectStandardInput = true;
            mProcess.StartInfo.RedirectStandardOutput = true;
            mProcess.StartInfo.CreateNoWindow = true;

            //设置接受信息
            mProcess.EnableRaisingEvents = true;
            //输出错误信息
            mProcess.Exited += new EventHandler(handleErr);
        }

        /// <summary>
        /// 初始化
        /// </summary>
        /// <param name="pyFile"></param>
        /// <param name="handler"></param>
        public PythonProcess(String pyFile, OutputHandler handler)
        {
            mProcess = new Process();
            mProcess.StartInfo.FileName = Program.pythonExePath;
            String arguments = Program.pythonFilePath + pyFile;

            mProcess.StartInfo.Arguments = arguments;

            mProcess.StartInfo.UseShellExecute = false;
            mProcess.StartInfo.RedirectStandardError = true;
            mProcess.StartInfo.RedirectStandardInput = true;
            mProcess.StartInfo.RedirectStandardOutput = true;
            mProcess.StartInfo.CreateNoWindow = true;
            //设置接受信息
            mProcess.EnableRaisingEvents = true;
            //输出错误信息
            mProcess.Exited += new EventHandler(handleErr);

            //输出结果
            outputHandler = handler;
            mProcess.Exited += new EventHandler(handleOutput);

        }

        /// <summary>
        /// 初始化
        /// </summary>
        /// <param name="pyFile"></param>
        /// <param name="param"></param>
        /// <param name="handler"></param>
        public PythonProcess(String pyFile, String[] param,OutputHandler handler)
        {
            mProcess = new Process();
            mProcess.StartInfo.FileName = Program.pythonExePath;
            String arguments = Program.pythonFilePath + pyFile;

            //添加参数
            if (param != null)
            {
                foreach (String arg in param)
                {
                    arguments += " " + arg;
                }
            }

            mProcess.StartInfo.Arguments = arguments;

            mProcess.StartInfo.UseShellExecute = false;
            mProcess.StartInfo.RedirectStandardError = true;
            mProcess.StartInfo.RedirectStandardInput = true;
            mProcess.StartInfo.RedirectStandardOutput = true;
            mProcess.StartInfo.CreateNoWindow = true;
            //设置接受信息
            mProcess.EnableRaisingEvents = true;
            //输出错误信息
            mProcess.Exited += new EventHandler(handleErr);

            //输出结果
            outputHandler = handler;
            mProcess.Exited += new EventHandler(handleOutput);

        }


        /// <summary>
        ///处理进程执行的错误信息 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private  void handleErr(object sender, EventArgs e)
        {   

            //输出错误信息
            StreamReader errReader = mProcess.StandardError;
            String errString = "";
            while (!errReader.EndOfStream)
            {
                errString += errReader.ReadLine();
            }
            Console.WriteLine(errString);
            
        }

        /// <summary>
        ///处理执行的结果 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private  void handleOutput(object sender, EventArgs e)
        {
            int exitCode = mProcess.ExitCode;
            StreamReader reader = mProcess.StandardOutput;
            String resultString = "";
            while (!reader.EndOfStream)
            {
                resultString += reader.ReadLine();
            }
            //将消息发送给主线程
            outputHandler(resultString,exitCode);
        }

        /// <summary>
        /// 开始进程
        /// </summary>
        public void startProcess()
        {
            mProcess.Start();
        }
    }
}
