using ESRI.ArcGIS.esriSystem;
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;

namespace SceneRetrieval
{
    static class Program
    {

        public static String pyExePath = @"C:\Software\Python27\ArcGIS10.2\python.exe";
        public static  String programPath;
        public static String pyFilePath;
        public static String dataPath;
        public static String tempPath;
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
            pyFilePath = programPath + @"\python\";
            pyFilePath = pyFilePath.Replace(@"\", "/");

            dataPath = Directory.GetParent(Directory.GetParent(programPath).ToString()) +@"\data\";
            tempPath= Directory.GetParent(Directory.GetParent(programPath).ToString()) + @"\temp\";

            Application.Run(new mainForm());
        }
    }
}