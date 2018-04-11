using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.util
{
    class Tool
    {
        public static Process mProcess;

        /// <summary>
        /// 设置python进程的参数
        /// </summary>
        /// <param name="process"></param>
        /// <param name="pyFile"></param>
        /// <param name="param"></param>
        /// <param name="handler"></param>
        public static void setProcessArgs(Process process,String pyFile,String[] param,EventHandler handler)
        {
            mProcess = process;

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
            //输出错误信息
            process.Exited += new EventHandler(handleErr);
            //自定义事件
            if (handler != null)
            {
                process.EnableRaisingEvents = true;
                process.Exited += handler;
            }

            
        }

        /// <summary>
        /// 设置python进程的参数
        /// </summary>
        /// <param name="process"></param>
        /// <param name="pyFile"></param>
        /// <param name="param"></param>
        public static void setProcessArgs(Process process, String pyFile, String[] param)
        {
            mProcess = process;

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

            //输出错误信息
            process.Exited += new EventHandler(handleErr);
        }

        /// <summary>
        /// 设置python进程的参数
        /// </summary>
        /// <param name="process"></param>
        /// <param name="pyFile"></param>
        /// <param name="handler"></param>
        public static void setProcessArgs(Process process, String pyFile, EventHandler handler)
        {
            mProcess = process;

            process.StartInfo.FileName = Program.pythonExePath;
            String arguments = Program.pythonFilePath + pyFile;
            
            process.StartInfo.Arguments = arguments;

            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.RedirectStandardInput = true;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.CreateNoWindow = true;

            //输出错误信息
            process.Exited += new EventHandler(handleErr);

            if (handler != null)
            {
                process.EnableRaisingEvents = true;
                process.Exited += handler;
            }

           
        }

        /// <summary>
        /// 设置python进程的参数
        /// </summary>
        /// <param name="process"></param>
        /// <param name="pyFile"></param>
        public static void setProcessArgs(Process process, String pyFile)
        {
            mProcess = process;

            process.StartInfo.FileName = Program.pythonExePath;
            String arguments = Program.pythonFilePath + pyFile;
            process.StartInfo.Arguments = arguments;

            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardError = true;
            process.StartInfo.RedirectStandardInput = true;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.CreateNoWindow = true;
         
            //输出错误信息
            process.Exited += new EventHandler(handleErr);



        }

        /// <summary>
        ///处理进程执行的错误信息 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private static void handleErr(object sender, EventArgs e)
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

        public static string GBKToUTF8(string str)
        {
            Encoding utf8;
            Encoding gb2312;
            utf8 = Encoding.GetEncoding("UTF-8");
            gb2312 = Encoding.GetEncoding("GB2312");
            byte[] gb = gb2312.GetBytes(str);
            gb = Encoding.Convert(gb2312, utf8, gb);
            return utf8.GetString(gb);
        }

        public static string UTF8ToGBK(string text)
        {
            byte[] bs = Encoding.GetEncoding("UTF-8").GetBytes(text);
            bs = Encoding.Convert(Encoding.GetEncoding("UTF-8"), Encoding.GetEncoding("GB2312"), bs);
            return Encoding.GetEncoding("GB2312").GetString(bs);
        }
    }
}
