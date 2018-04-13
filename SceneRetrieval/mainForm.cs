using ESRI.ArcGIS.Controls;
using System;
using System.Windows.Forms;
using SceneRetrieval.model;
using static SceneRetrieval.model.PyProcess;
using System.IO;
using System.Text;

namespace SceneRetrieval
{
    public partial class mainForm : Form
    {
        //����python����
        PyProcess shapeVectorPy;

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
            shapeVectorPy = new PyProcess("shapeVector.py");
            //���ò���
            PyArgument arg = new PyArgument();
            arg.addArgument("polygon.shp");
            shapeVectorPy.setArgument(arg);
            //����¼���Ӧ
            shapeVectorPy.setOutputHandler(new OutputHandler(handleOutput));

        }

        private void handleOutput(string output, int exitCode)
        {
            testBtn.Text = "����Python";
            testBtn.Enabled = true;
            if (exitCode == 0)
            {
                StreamReader sr = new StreamReader(Program.tempPath+"data.cp", Encoding.Default);
                String line;
                while ((line = sr.ReadLine()) != null)
                {
                    Console.WriteLine(line.ToString());
                }
                sr.Close();
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