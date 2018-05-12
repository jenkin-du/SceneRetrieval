using ESRI.ArcGIS.Controls;
using System;
using System.Windows.Forms;
using SceneRetrieval.model;
using System.IO;
using System.Text;
using SceneRetrieval.tool;
using Newtonsoft.Json;
using System.Collections.Generic;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Geometry;
using SceneRetrieval.form;

namespace SceneRetrieval
{
    public partial class MainForm : Form
    {
        //设置python进程
        private PyProcess mSceneRetrivalPy;

        //搜索的相似场景
        List<SimilarScene> mSceneList;

        //显示消息
        MessageForm mMessageForm;

        public MainForm()
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
            mSceneRetrivalPy = new PyProcess("SceneRetrieval.py");
            //添加事件响应
            mSceneRetrivalPy.setOutputHandler(new OutputHandler(handleOutput));

            mMessageForm = new MessageForm();
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void axMap_OnMouseMove(object sender, ESRI.ArcGIS.Controls.IMapControlEvents2_OnMouseMoveEvent e)
        {
            statusLabel.Text = string.Format("{0} m, {1} m", e.mapX.ToString("#######.###"), e.mapY.ToString("#######.###"));

        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void axMap_OnMouseDown(object sender, IMapControlEvents2_OnMouseDownEvent e)
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
        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void axMap_OnMouseUp(object sender, IMapControlEvents2_OnMouseUpEvent e)
        {

            axMap.MousePointer = esriControlsMousePointer.esriPointerDefault;

        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void retrievalBtn_Click(object sender, EventArgs e)
        {
            mSceneRetrivalPy.startProcess();

            retrievalBtn.Enabled = false;
            mMessageForm.ShowDialog();

        }

        /// <summary>
        /// 处理搜索的结果
        /// </summary>
        /// <param name="output"></param>
        /// <param name="exitCode"></param>
        private void handleOutput(string output, int exitCode)
        {
            retrievalBtn.Enabled = true;

            if (exitCode == 0)
            {
                String jsonString = "";
                String line;
                StreamReader sr = new StreamReader(Program.tempPath + "data", Encoding.Default);
                while ((line = sr.ReadLine()) != null)
                {
                    jsonString += line + "\n";
                }
                sr.Close();
                mSceneList = JsonConvert.DeserializeObject<List<SimilarScene>>(jsonString);

                //排序
                Util.sort(mSceneList);

                //删除datagridview中的数据
                removeData();
                //将结果显示在dataGridView中
                DataGridViewRow row;
                for (int i = 0; i < mSceneList.Count; i++)
                {
                    SimilarScene scene = mSceneList[i];
                    List<String> polygons = scene.polygonList;

                    row = new DataGridViewRow();
                    int index = dataView.Rows.Add(row);
                    dataView.Rows[index].Cells[0].Value = polygons[0].Split('_')[0];
                    dataView.Rows[index].Cells[1].Value = scene.md;

                }

                showScene(mSceneList[0]);

                mMessageForm.Close();
            }
            else
            {
                mMessageForm.Close();
                MessageBox.Show("检索失败！！");
            }

            Console.WriteLine(output);

        }

        /// <summary>
        /// 删除datagridview中的所有数据
        /// </summary>
        private void removeData()
        {
            int index = 0;
            while (index >= 0)
            {
                index = dataView.RowCount - 1;
                if (index > 0)
                {
                    dataView.Rows.Remove(dataView.Rows[index]);
                    index--;
                }
                else
                {
                    index--;
                }

            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void dataView_RowHeaderMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            int index = dataView.CurrentRow.Index;
            if (index < mSceneList.Count)
            {
                showScene(mSceneList[index]);
            }
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void dataView_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            int index = dataView.CurrentRow.Index;
            if (index < mSceneList.Count)
            {
                showScene(mSceneList[index]);
            }
        }

        /// <summary>
        /// 将选择的相似场景高亮
        /// </summary>
        /// <param name="scene"></param>
        private void showScene(SimilarScene scene)
        {
            String LayerName = scene.polygonList[0].Split('_')[0];
            IFeatureLayer layer = Util.getLayerByName(axMap.Map, LayerName) as IFeatureLayer;

            axMap.Map.ClearSelection();
            //查询
            IFeatureSelection featureSelection = layer as IFeatureSelection;
            for (int i = 0; i < scene.polygonList.Count; i++)
            {
                int id = Convert.ToInt32(scene.polygonList[i].Split('_')[1]);

                //新建IQueryFilter接口，添加where语句
                IQueryFilter queryFilter = new QueryFilterClass();

                //设置where语句内容
                queryFilter.WhereClause = "\"FID\" = " + id;

                //选择，并将其添加到选择集中
                featureSelection.SelectFeatures(queryFilter, esriSelectionResultEnum.esriSelectionResultAdd, false);
            }
            //高亮
            IActiveView activeView = axMap.Map as IActiveView;
            //刷新
            activeView.Refresh();

        }

        /// <summary>
        /// 绘制场景
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void drawBtn_Click(object sender, EventArgs e)
        {
            DrawSceneForm drawForm = new DrawSceneForm();
            drawForm.FormClosed += new FormClosedEventHandler(drawFormClosed);
            drawForm.ShowDialog();
        }

        /// <summary>
        /// 场景画板关闭时调用
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void drawFormClosed(object sender, FormClosedEventArgs e)
        {
            sceneMap.Extent = sceneMap.FullExtent;
            sceneMap.ActiveView.Refresh();
        }
    }
}