using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.Geodatabase;
using System.Windows.Forms;
using ESRI.ArcGIS.Controls;

namespace GISEditor.EditTool
{
    public class MapManager
    {
        // 初始化

        public MapManager()
        {

        }



        //变量定义

        public static Form ToolPlatForm = null;
        private static IEngineEditor _engineEditor;
        public static IEngineEditor EngineEditor
        {
            get { return MapManager._engineEditor; }
            set { MapManager._engineEditor = value; }
        }
        // 获取颜色
        public static IRgbColor GetRgbColor(int intR, int intG, int intB)
        {
            IRgbColor pRgbColor = null;
            pRgbColor = new RgbColorClass();
            if (intR < 0) pRgbColor.Red = 0;
            else pRgbColor.Red = intR;
            if (intG < 0) pRgbColor.Green = 0;
            else pRgbColor.Green = intG;
            if (intB < 0) pRgbColor.Blue = 0;
            else pRgbColor.Blue = intB;
            return pRgbColor;
        }

        //计算两点之间X轴方向和Y轴方向上的距离
        public static bool CalDistance(IPoint lastpoint, IPoint firstpoint, out double deltaX, out double deltaY)
        {
            deltaX = 0; deltaY = 0;
            if (lastpoint == null || firstpoint == null)
                return false;
            deltaX = lastpoint.X - firstpoint.X;
            deltaY = lastpoint.Y - firstpoint.Y;
            return true;
        }

        // 单位转换

        public static double ConvertPixelsToMapUnits(IActiveView activeView, double pixelUnits)
        {
            int pixelExtent = activeView.ScreenDisplay.DisplayTransformation.get_DeviceFrame().right
                - activeView.ScreenDisplay.DisplayTransformation.get_DeviceFrame().left;

            double realWorldDisplayExtent = activeView.ScreenDisplay.DisplayTransformation.VisibleBounds.Width;
            double sizeOfOnePixel = realWorldDisplayExtent / pixelExtent;

            return pixelUnits * sizeOfOnePixel;
        }

        //获取选择要
        public static IFeatureCursor GetSelectedFeatures(IFeatureLayer pFeatLyr)
        {
            ICursor pCursor = null;
            IFeatureCursor pFeatCur = null;
            if (pFeatLyr == null) return null;
            IFeatureSelection pFeatSel = pFeatLyr as IFeatureSelection;
            ISelectionSet pSelSet = pFeatSel.SelectionSet;
            if (pSelSet.Count == 0) return null;
            pSelSet.Search(null, false, out pCursor);
            pFeatCur = pCursor as IFeatureCursor;
            return pFeatCur;
        }

        // 获取当前地图文档所有图层集合
        public static List<ILayer> GetLayers(IMap pMap)
        {
            ILayer plyr = null;
            List<ILayer> pLstLayers = null;
            try
            {
                pLstLayers = new List<ILayer>();
                for (int i = 0; i < pMap.LayerCount; i++)
                {
                    plyr = pMap.get_Layer(i);
                    if (!pLstLayers.Contains(plyr))
                    {
                        pLstLayers.Add(plyr);
                    }
                }
            }
            catch (Exception ex)
            { }
            return pLstLayers;
        }

        // 根据图层名获取图层
        //<param name="pMap">地图文档</param>
        // <param name="sLyrName">图层名</param>
        public static ILayer GetLayerByName(IMap pMap, string sLyrName)
        {
            ILayer pLyr = null;
            ILayer pLayer = null;
            try
            {
                for (int i = 0; i < pMap.LayerCount; i++)
                {
                    pLyr = pMap.get_Layer(i);
                    if (pLyr.Name.ToUpper() == sLyrName.ToUpper())
                    {
                        pLayer = pLyr;
                        break;
                    }
                }
            }
            catch (Exception ex)
            {
            }
            return pLayer;
        }


        /// <summary>
        /// 将经纬度转换成屏幕坐标XY
        /// </summary>
        /// <param name="axMap"></param>
        /// <param name="longtitude"></param>
        /// <param name="latitude"></param>
        /// <returns></returns>
        public static System.Drawing.Point getScreenCoord(AxMapControl axMap, double longtitude, double latitude)
        {

            int screenWidth = axMap.Width;
            int screenHeight = axMap.Height;

            IEnvelope worldCoord = axMap.ActiveView.ScreenDisplay.DisplayTransformation.FittedBounds;
            double maxLon = worldCoord.XMax;
            double minLon = worldCoord.XMin;
            double maxLat = worldCoord.YMax;
            double minLat = worldCoord.YMin;

            //比例因子
            double scaleX = ((maxLon - minLon) * 3600) / screenWidth;
            double scaleY = ((maxLat - minLat) * 3600) / screenHeight;

            System.Drawing.Point screenPoint = new System.Drawing.Point();
            screenPoint.X = (int)((longtitude - minLon) * 3600 / scaleX);
            screenPoint.Y = (int)((maxLat - latitude) * 3600 / scaleY);

            return screenPoint;
        }



        /// <summary>
        /// 根据名字获取图层
        /// </summary>
        /// <param name="map"></param>
        /// <param name="name"></param>
        /// <returns></returns>
        public static ILayer getLayerByName(IMap map, String name)
        {
            ILayer layer = null;

            //对Map中的每个图层进行判断并加载名称
            for (int i = 0; i < map.LayerCount; i++)
            {
                //如果该图层为图层组类型，则分别对所包含的每个图层进行操作
                if (map.get_Layer(i) is GroupLayer)
                {
                    //使用ICompositeLayer接口进行遍历操作
                    ICompositeLayer compositeLayer = map.get_Layer(i) as ICompositeLayer;
                    for (int j = 0; j < compositeLayer.Count; j++)
                    {

                        string layerName = compositeLayer.Layer[j].Name;
                        if (layerName == name)
                        {
                            layer = compositeLayer.Layer[j];
                            break;
                        }
                    }
                }
                else
                {
                    String layerName = map.Layer[i].Name;
                    if (layerName == name)
                    {
                        layer = map.Layer[i];
                        break;
                    }
                }
            }
            return layer;
        }




        /// <summary>
        /// 删除自定图层的所有要素
        /// </summary>
        /// <param name="layer"></param>
        /// <param name="axMap"></param>
        public static void deleteAllFeature(IFeatureLayer featureLayer, AxMapControl axMap)
        {
            //try
            //{

            // 定义一个要素集合，并获取图层的要素集合
            IFeatureClass featureClass = featureLayer.FeatureClass;
            ITable table = (ITable)featureClass;
            table.DeleteSearchedRows(null);
            axMap.ActiveView.Refresh();
            //}
            //catch
            //{

            //}


        }

        /// <summary>
        /// 删除自定图层的所有要素
        /// </summary>
        /// <param name="layer"></param>
        /// <param name="axMap"></param>
        public static void deleteAllFeature(AxMapControl axMap)
        {
            try
            {

                IFeatureLayer featureLayer = axMap.get_Layer(0) as IFeatureLayer;
                // 定义一个要素集合，并获取图层的要素集合
                IFeatureClass featureClass = featureLayer.FeatureClass;
                ITable table = (ITable)featureClass;
                table.DeleteSearchedRows(null);
                axMap.ActiveView.Refresh();
            }
            catch
            {

            }


        }

        /// <summary>
        /// 从Feature类中获取值
        /// </summary>
        /// <param name="feature"></param>
        /// <param name="name"></param>
        /// <returns></returns>
        public static object getFieldByName(IFeature feature, String name)
        {
            IFeatureClass featureClass = feature.Class as IFeatureClass;
            int index = featureClass.FindField(name);

            object value = feature.Value[index];

            return value;
        }

    }
}

