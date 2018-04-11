using ESRI.ArcGIS.Controls;
using System;
using System.Windows.Forms;
using System.IO;
using System.Diagnostics;
using SceneRetrieval.util;

namespace SceneRetrieval
{
    public partial class mainForm : Form
    {


        private Process shapeVectorPy;

        public mainForm()
        {
            InitializeComponent();

            Control.CheckForIllegalCrossThreadCalls = false;

            init();

        }

        /// <summary>
        /// 初始化
        /// </summary>
        private void init()
        {

            //设置python脚本参数
            shapeVectorPy = new Process();
            String[] args = { "polygon.shp" };
            Tool.setProcessArgs(shapeVectorPy, "shapeVector.py", args, new EventHandler(shapeVectorPyExited));
            
        }

        private void shapeVectorPyExited(object sender, EventArgs e)
        {
            int exitCode = shapeVectorPy.ExitCode;
            testBtn.Text = "测试Python";
            testBtn.Enabled = true;
            if (exitCode == 0)
            {
                MessageBox.Show("测试成功！！");
            }else 
            {
                MessageBox.Show("程序出错！！");
            }


           


            
        }

        private void axMap_OnMouseMove(object sender, ESRI.ArcGIS.Controls.IMapControlEvents2_OnMouseMoveEvent e)
        {
            statusLabel.Text = string.Format("{0} m, {1} m", e.mapX.ToString("#######.###"), e.mapY.ToString("#######.######"));

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
            shapeVectorPy.Start();
            Console.WriteLine("开始执行！！！！！！！！！！！！！！！");

            testBtn.Text = "正在执行";
            testBtn.Enabled = false;
        }
    }
}