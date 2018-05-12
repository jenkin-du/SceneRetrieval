using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.model
{
    class SimilarScene
    {
        //找到的相似场景中的polygon的id
        private List<String> polygonList;
        //匹配度
        public float md = 0;


        public List<string> PolygonList
        {
            get
            {
                return polygonList;
            }

            set
            {
                polygonList = value;
            }
        }
    }
}
