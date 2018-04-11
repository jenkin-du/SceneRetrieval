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

namespace SceneRetrieval
{
    public partial class mainForm : Form
    {
        //设置python的运行环境
        private ScriptRuntime pyRuntime ;
        //声明使用的python文件
        private dynamic shapeVectorPy;
        //文件的相对路径
        private String appPath;
        private String pythonPath;

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

            //初始化，并添加参数
            var options = new Dictionary<string, object>();
            options["Frames"] = true;
            options["FullFrames"] = true;
            pyRuntime = Python.CreateRuntime(options);

            shapeVectorPy = pyRuntime.UseFile(pythonPath + "/shapeVector.py");


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
            shapeVectorPy.getShapeVector("polygon.shp");
        }
    }
}