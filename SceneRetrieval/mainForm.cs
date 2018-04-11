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
        /// ��ʼ��
        /// </summary>
        private void init()
        {

            //����python�ű�����
            shapeVectorPy = new Process();
            String[] args = { "polygon.shp" };
            Tool.setProcessArgs(shapeVectorPy, "shapeVector.py", args, new EventHandler(shapeVectorPyExited));
            
        }

        private void shapeVectorPyExited(object sender, EventArgs e)
        {
            int exitCode = shapeVectorPy.ExitCode;
            testBtn.Text = "����Python";
            testBtn.Enabled = true;
            if (exitCode == 0)
            {
                MessageBox.Show("���Գɹ�����");
            }else 
            {
                MessageBox.Show("���������");
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
            Console.WriteLine("��ʼִ�У�����������������������������");

            testBtn.Text = "����ִ��";
            testBtn.Enabled = false;
        }
    }
}