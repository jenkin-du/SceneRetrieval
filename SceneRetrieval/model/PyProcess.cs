using System;
using System.Diagnostics;
using System.IO;

namespace SceneRetrieval.model
{
    class PyProcess
    {

        public delegate void OutputHandler(String output, int exitCode);
        //处理返回数据的委托
        private OutputHandler mOutputHandler;
        //python进程
        private Process mProcess;

        /// <summary>
        /// 初始化
        /// </summary>
        /// <param name="pyFile"></param>
        public PyProcess(String pyFile)
        {
            mProcess = new Process();
            mProcess.StartInfo.FileName = Program.pythonExePath;
            mProcess.StartInfo.Arguments = Program.pythonFilePath + pyFile;


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
            mProcess.Exited += new EventHandler(handleOutput);

        }

        /// <summary>
        /// 设置运行参数
        /// </summary>
        /// <param name="arg"></param>
        public void setArgument(PyArgument arg)
        {
            mProcess.StartInfo.Arguments += arg.getArgument();
            Console.WriteLine(mProcess.StartInfo.Arguments);
        }


        /// <summary>
        /// 添加事件相应函数
        /// </summary>
        public void setOutputHandler(OutputHandler handler)
        {
            mOutputHandler = handler;
        }

        /// <summary>
        ///处理进程执行的错误信息 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void handleErr(object sender, EventArgs e)
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
        private void handleOutput(object sender, EventArgs e)
        {
            if (mOutputHandler != null)
            {
                int exitCode = mProcess.ExitCode;
                StreamReader reader = mProcess.StandardOutput;
                String result = "";
                while (!reader.EndOfStream)
                {
                    result += reader.ReadLine();
                }
                //将消息发送给主线程
                mOutputHandler(result, exitCode);
            }

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
