using ESRI.ArcGIS.Controls;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System.IO;
using System.Diagnostics;

namespace SceneRetrieval
{
    public partial class mainForm : Form
    {
       
        //文件的相对路径
        private String appPath;
        private String pythonPath;

        private Process pyP_shapeVector;

        public mainForm()
        {
            InitializeComponent();

            init();

        }

        /// <summary>
        /// 初始化
        /// </summary>
        private void init()
        {
            //获得python文件的相对路径
            DirectoryInfo topDir = Directory.GetParent(Environment.CurrentDirectory);
            appPath = Directory.GetParent(topDir.ToString()).ToString();
            pythonPath = appPath + "\\python";
            pythonPath = pythonPath.Replace("\\", "/");

            //设置python脚本参数
            pyP_shapeVector.StartInfo.FileName = @"C:\Software\Python27\ArcGIS10.2\python.exe";
            


        }

        private void axMap_OnMouseMove(object sender, ESRI.ArcGIS.Controls.IMapControlEvents2_OnMouseMoveEvent e)
        {
            statusLabel.Text = string.Format("{0} m, {1} m", e.mapX.ToString("#######.######"), e.mapY.ToString("#######.######"));

        }

        private void axMap_OnMouseDown(object sender, ESRI.ArcGIS.Controls.IMapControlEvents2_OnMouseDownEvent e)
        {
            if (axMap.MousePointer == esriControlsMousePointer.esriPointerPan && e.button == 1)
            {
                axMap.Pan();
            }

            if (e.button == 4)
            {
                axMap.MousePointer = esriControlsMousePointer.esriPointerPan;
                axMap.Pan();
            }
        }

        private void axMap_OnMouseUp(object sender, IMapControlEvents2_OnMouseUpEvent e)
        {

            axMap.MousePointer = esriControlsMousePointer.esriPointerDefault;

        }

        private void testBtn_Click(object sender, EventArgs e)
        {

            pyP_shapeVector.StartInfo.Arguments = "D:\\毕设\\工程\\SceneRetrieval\\SceneRetrieval\\python\\shapeVector_p.py polygon.shp";
            pyP_shapeVector.StartInfo.UseShellExecute = false;
            pyP_shapeVector.StartInfo.RedirectStandardError = true;
            pyP_shapeVector.StartInfo.RedirectStandardInput = true;
            pyP_shapeVector.StartInfo.RedirectStandardOutput = true;

            pyP_shapeVector.StartInfo.CreateNoWindow = true;

            pyP_shapeVector.Start();
        }
    }
}