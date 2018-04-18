using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using System.Threading.Tasks;
using SceneRetrieval.model;
using ESRI.ArcGIS.Carto;

namespace SceneRetrieval.tool
{
    class Util
    {

        public static void sort(List<SimilarScene> sceneList)
        {

            for (int i = 0; i < sceneList.Count; i++)
            {
                sceneList[i].md *= 1000;
            }


            int k = 0;
            SimilarScene temp;
            for (int i = 0; i < sceneList.Count - 1; i++)
            {
                k = i;
                for (int j = i + 1; j < sceneList.Count; j++)
                {
                    if (sceneList[j].md > sceneList[k].md)
                    {
                        k = j;
                    }
                }

                if (k != i)
                {
                    temp = sceneList[i];
                    sceneList[i] = sceneList[k];
                    sceneList[k] = temp;
                }

            }

            for (int i = 0; i < sceneList.Count; i++)
            {
                sceneList[i].md /= 1000;
            }

        }


        // 根据图层名获取图层
        //<param name="pMap">地图文档</param>
        // <param name="sLyrName">图层名</param>
        public static ILayer getLayerByName(IMap pMap, string sLyrName)
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
    }
}
