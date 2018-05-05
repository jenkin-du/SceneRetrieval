using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.model
{
    /// <summary>
    /// 关联对
    /// </summary>
    class IncidentPair
    {
        //第一个节点
        public IncidentNode firstNode;

        //第二个节点
        public IncidentNode lastNode;

        //关联度
        public double correlation;

        public override string ToString()
        {
            return "firstNode:" + firstNode + ";lastNode:" + lastNode + ";correlation:" + correlation;
        }
    }
}
