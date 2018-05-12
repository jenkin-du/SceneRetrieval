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
        //����python����
        private PyProcess mSceneRetrivalPy;

        //���������Ƴ���
        List<SimilarScene> mSceneList;

        //��ʾ��Ϣ
        MessageForm mMessageForm;

        public MainForm()
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
            mSceneRetrivalPy = new PyProcess("SceneRetrieval.py");
            //����¼���Ӧ
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
        /// ���������Ľ��
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

                //����
                Util.sort(mSceneList);

                //ɾ��datagridview�е�����
                removeData();
                //�������ʾ��dataGridView��
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
                MessageBox.Show("����ʧ�ܣ���");
            }

            Console.WriteLine(output);

        }

        /// <summary>
        /// ɾ��datagridview�е���������
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
        /// ��ѡ������Ƴ�������
        /// </summary>
        /// <param name="scene"></param>
        private void showScene(SimilarScene scene)
        {
            String LayerName = scene.polygonList[0].Split('_')[0];
            IFeatureLayer layer = Util.getLayerByName(axMap.Map, LayerName) as IFeatureLayer;

            axMap.Map.ClearSelection();
            //��ѯ
            IFeatureSelection featureSelection = layer as IFeatureSelection;
            for (int i = 0; i < scene.polygonList.Count; i++)
            {
                int id = Convert.ToInt32(scene.polygonList[i].Split('_')[1]);

                //�½�IQueryFilter�ӿڣ����where���
                IQueryFilter queryFilter = new QueryFilterClass();

                //����where�������
                queryFilter.WhereClause = "\"FID\" = " + id;

                //ѡ�񣬲�������ӵ�ѡ����
                featureSelection.SelectFeatures(queryFilter, esriSelectionResultEnum.esriSelectionResultAdd, false);
            }
            //����
            IActiveView activeView = axMap.Map as IActiveView;
            //ˢ��
            activeView.Refresh();

        }

        /// <summary>
        /// ���Ƴ���
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
        /// ��������ر�ʱ����
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