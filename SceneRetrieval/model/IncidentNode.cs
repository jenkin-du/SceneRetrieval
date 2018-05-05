using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.model
{
    /// <summary>
    /// 关联节点
    /// </summary>
    class IncidentNode
    {
        //场景中的polygon
        public String oid;

        //数据库中的polygon
        public String did;

        //匹配度
        public double md;

        public override string ToString()
        {
            return "oid:" + oid + ",did:" + did + ",md:" + md;
        }

    }
}
