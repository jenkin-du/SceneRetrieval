using ESRI.ArcGIS.Controls;
using System;
using System.Windows.Forms;
using SceneRetrieval.model;
using static SceneRetrieval.model.PyProcess;
using System.IO;
using System.Text;
using SceneRetrieval.tool;
using Newtonsoft.Json;
using System.Collections.Generic;

namespace SceneRetrieval
{
    public partial class mainForm : Form
    {
        //设置python进程
        private PyProcess sceneRetrivalPy;


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
            sceneRetrivalPy = new PyProcess("SceneRetrieval.py");
            //添加事件响应
            sceneRetrivalPy.setOutputHandler(new OutputHandler(handleOutput));

            this.MaximizeBox = false;
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

    
        private void retrievalBtn_Click(object sender, EventArgs e)
        {
            sceneRetrivalPy.startProcess();

            retrievalBtn.Text = "正在检索";
            retrievalBtn.Enabled = false;

        }

        private void handleOutput(string output, int exitCode)
        {
            retrievalBtn.Text = "检索";
            retrievalBtn.Enabled = true;
            String jsonOut = ""; 
            if (exitCode == 0)
            {
                String line;
                StreamReader sr = new StreamReader(Program.tempPath + "data", Encoding.Default);
                while ((line = sr.ReadLine()) != null)
                {
                    jsonOut += line + "\n";
                }
                sr.Close();
                Console.WriteLine(jsonOut);

                List<SimilarScene> similarSceneList = JsonConvert.DeserializeObject<List<SimilarScene>>(jsonOut);
                for (int i = 0; i < similarSceneList.Count; i++)
                {
                    SimilarScene scene = similarSceneList[i];
                    List<String> polygons = scene.polygonList;
                    String result = "";
                    for (int j = 0; j < polygons.Count; j++)
                    {
                        result += polygons[j] + ",";
                    }
                    result += " md:" + scene.md;

                    resultLB.Items.Add(result);
                }
                MessageBox.Show("测试成功！！");
            }
            else
            {
                MessageBox.Show("程序出错！！");
            }


            

        }
    }
}