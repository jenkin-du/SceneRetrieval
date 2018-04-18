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
        public List<String> polygonList;
        //匹配度
        public float md = 0;

        //重心坐标
        public Point gravity;

        //外接矩形
        public Envelope envelope;
        


   
    }
}
