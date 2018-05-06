using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Controls;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.SystemUI;
using GISEditor.EditTool;
using GISEditor.EditTool.Command;
using GISEditor.EditTool.Tool;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SceneRetrieval.form
{

    public partial class DrawSceneForm : Form
    {

        private IMap mMap = null;
        private IFeatureLayer mCurrentLayer = null;
        private IEngineEditor pEngineEditor = null;
        private IEngineEditTask pEngineEditTask = null;
        private IEngineEditLayers mEngineEditLayers = null;

        public DrawSceneForm()
        {
            InitializeComponent();

            mMap = drawMap.Map;

            pEngineEditor = new EngineEditorClass();
            MapManager.EngineEditor = pEngineEditor;
            pEngineEditTask = pEngineEditor as IEngineEditTask;
            mEngineEditLayers = pEngineEditor as IEngineEditLayers;


            mCurrentLayer = drawMap.get_Layer(0) as IFeatureLayer;
            //设置编辑目标层
            mEngineEditLayers.SetTargetLayer(mCurrentLayer, 0);

            //获取当前编辑图层工作空间
            IDataset pDataSet = mCurrentLayer.FeatureClass as IDataset;
            IWorkspace pWs = pDataSet.Workspace;
            //设置编辑模式，如果是ArcSDE采用版本模式
            if (pWs.Type == esriWorkspaceType.esriRemoteDatabaseWorkspace)
            {
                pEngineEditor.EditSessionMode = esriEngineEditSessionMode.esriEngineEditSessionModeVersioned;
            }
            else
            {
                pEngineEditor.EditSessionMode = esriEngineEditSessionMode.esriEngineEditSessionModeNonVersioned;
            }
            //设置编辑任务
            pEngineEditTask = pEngineEditor.GetTaskByUniqueName("ControlToolsEditing_CreateNewFeatureTask");
            pEngineEditor.CurrentTask = pEngineEditTask;// 设置编辑任务
            pEngineEditor.EnableUndoRedo(true); //是否可以进行撤销、恢复操作
            pEngineEditor.StartEditing(pWs, mMap); //开始编辑操作

        }

        /// <summary>
        /// 开始绘制
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void startMenu_Click(object sender, EventArgs e)
        {

            drawMap.MousePointer = esriControlsMousePointer.esriPointerCrosshair;

            ICommand m_CreateFeatTool = new CreateFeatureToolClass();
            m_CreateFeatTool.OnCreate(drawMap.Object);
            m_CreateFeatTool.OnClick();
            drawMap.CurrentTool = m_CreateFeatTool as ITool;




        }

        private void stopMenu_Click(object sender, EventArgs e)
        {
            try
            {
                ICommand m_saveEditCom = new SaveEditCommandClass();
                m_saveEditCom.OnCreate(drawMap.Object);
                m_saveEditCom.OnClick();
            }
            catch (Exception ex)
            {
            }

        }

        /// <summary>
        /// 清楚绘制的图案
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void clearMenu_Click(object sender, EventArgs e)
        {
            MapManager.deleteAllFeature(drawMap);
        }


        /// <summary>
        /// 关闭时
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void DrawSceneForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            drawMap.CurrentTool = null;
            ICommand m_stopEditCom = new StopEditCommandClass();
            m_stopEditCom.OnCreate(drawMap.Object);
            m_stopEditCom.OnClick();
        }

        /// <summary>
        /// 选择
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void selectMenu_Click(object sender, EventArgs e)
        {
            try
            {
                ICommand m_SelTool = new SelectFeatureToolClass();
                m_SelTool.OnCreate(drawMap.Object);
                m_SelTool.OnClick();
                drawMap.CurrentTool = m_SelTool as ITool;
                drawMap.MousePointer = esriControlsMousePointer.esriPointerArrow;
            }
            catch (Exception ex)
            {
            }
        }

        private void deleteMenu_Click(object sender, EventArgs e)
        {
            try
            {
                drawMap.MousePointer = esriControlsMousePointer.esriPointerArrow;
                ICommand m_delFeatCom = new DelFeatureCommandClass();
                m_delFeatCom.OnCreate(drawMap.Object);
                m_delFeatCom.OnClick();
            }
            catch (Exception ex)
            {
            }
        }
    }
}
