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

        private void dataView_RowHeaderMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            int index = dataView.CurrentRow.Index;
            if (index < mSceneList.Count)
            {
                showScene(mSceneList[index]);
            }
        }

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
            IEnvelope extent = activeView.Extent;
            double sceenWidth = extent.Width;
            double sceenHeight = extent.Height;
            double sceenMin = sceenWidth > sceenHeight ? sceenHeight : sceenWidth;
            double sceenMax = sceenWidth < sceenHeight ? sceenHeight : sceenWidth;
            double sceenScale = sceenMax / sceenMin;


          

            float scale = 2.0f;
            model.Envelope envelope = scene.envelope;

            model.Point gravity = new model.Point((envelope.xMin+envelope.xMax)/2,(envelope.yMin+envelope.yMax) /2);

            double width = envelope.xMax - envelope.xMin;
            double height = envelope.yMax - envelope.yMin;
            double max = width > height ? width : height;

            if (sceenHeight == sceenMin)
            {
                ESRI.ArcGIS.Geometry.Point rt = new ESRI.ArcGIS.Geometry.Point();
                rt.X = gravity.x + max * sceenScale * scale / 2;
                rt.Y = gravity.y + max * scale / 2;

                ESRI.ArcGIS.Geometry.Point lb = new ESRI.ArcGIS.Geometry.Point();
                lb.X = gravity.x - max * sceenScale * scale / 2;
                lb.Y = gravity.y - max * scale / 2;

                ESRI.ArcGIS.Geometry.Point rb = new ESRI.ArcGIS.Geometry.Point();
                rb.X = gravity.x + max * sceenScale * scale / 2;
                rb.Y = gravity.y - max * scale / 2;

                ESRI.ArcGIS.Geometry.Point lt = new ESRI.ArcGIS.Geometry.Point();
                lt.X = gravity.x - max * sceenScale * scale / 2;
                lt.Y = gravity.y + max * scale / 2;

                extent.LowerLeft = lb;
                extent.UpperRight = rt;
                extent.UpperLeft = lt;
                extent.LowerRight = rb;
            }
            else
            {
                ESRI.ArcGIS.Geometry.Point rt = new ESRI.ArcGIS.Geometry.Point();
                rt.X = gravity.x + max / 2;
                rt.Y = gravity.y + max * sceenScale / 2;

                ESRI.ArcGIS.Geometry.Point lb = new ESRI.ArcGIS.Geometry.Point();
                lb.X = gravity.x - max / 2;
                lb.Y = gravity.y - max * sceenScale / 2;

                ESRI.ArcGIS.Geometry.Point rb = new ESRI.ArcGIS.Geometry.Point();
                rb.X = gravity.x + max * scale / 2;
                rb.Y = gravity.y - max * sceenScale * scale / 2;

                ESRI.ArcGIS.Geometry.Point lt = new ESRI.ArcGIS.Geometry.Point();
                lt.X = gravity.x - max * scale / 2;
                lt.Y = gravity.y + max * sceenScale * scale / 2;

                extent.LowerLeft = lb;
                extent.UpperRight = rt;
                extent.UpperLeft = lt;
                extent.LowerRight = rb;
            }

            activeView.Extent = extent;
            //刷新
            activeView.Refresh();

        }
    }
}   