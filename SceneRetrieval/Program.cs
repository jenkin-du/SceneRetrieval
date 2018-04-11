using ESRI.ArcGIS.esriSystem;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;

namespace SceneRetrieval
{
    static class Program
    {

        public static string pythonExePath = @"C:\Software\Python27\ArcGIS10.2\python.exe";
        public static  String programPath;
        public static String pythonFilePath;
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            ESRI.ArcGIS.RuntimeManager.Bind(ESRI.ArcGIS.ProductCode.EngineOrDesktop);
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            //获得python文件的相对路径
            DirectoryInfo topDir = Directory.GetParent(Environment.CurrentDirectory);
            programPath = Directory.GetParent(topDir.ToString()).ToString();
            pythonFilePath = programPath + "\\python\\";
            pythonFilePath = pythonFilePath.Replace("\\", "/");

            Application.Run(new mainForm());
        }
    }
}