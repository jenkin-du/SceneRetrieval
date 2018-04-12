using ESRI.ArcGIS.Controls;
using System;
using System.Windows.Forms;
using System.IO;
using System.Diagnostics;
using SceneRetrieval.util;
using static SceneRetrieval.util.PythonProcess;

namespace SceneRetrieval
{
    public partial class mainForm : Form
    {
        //����python����
        PythonProcess shapeVectorPy;

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
            String[] args = { "polygo.shp" };
            shapeVectorPy = new PythonProcess("shapeVector.py", args, new OutputHandler(handleOutput));

        }

        private void handleOutput(string output, int exitCode)
        {
            testBtn.Text = "����Python";
            testBtn.Enabled = true;
            if (exitCode == 0)
            {
                MessageBox.Show("���Գɹ�����");
            }
            else
            {
                MessageBox.Show("���������");
            }

            Console.WriteLine(output);

        }

        private void axMap_OnMouseMove(object sender, ESRI.ArcGIS.Controls.IMapControlEvents2_OnMouseMoveEvent e)
        {
            statusLabel.Text = string.Format("{0} m, {1} m", e.mapX.ToString("#######.###"), e.mapY.ToString("#######.###"));

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
            shapeVectorPy.startProcess();
            Console.WriteLine("��ʼִ�У�����������������������������");

            testBtn.Text = "����ִ��";
            testBtn.Enabled = false;
        }
    }
}