using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.model
{
    class Graph
    {
        public List<List<Node>> nodes;

        /// <summary>
        /// 初始化图
        /// </summary>
        /// <param name="incidentPairs"></param>
        Graph(List<IncidentPair> incidentPairs)
        {
            nodes = new List<List<Node>>();

            foreach (IncidentPair pair in incidentPairs)
            {
                IncidentNode firstNode = pair.firstNode;
                IncidentNode lastNode = pair.lastNode;

                String foid = firstNode.oid;
                String fdid = firstNode.did;

                int index = foid.Substring('_')[1];
                if (nodes[index] == null)
                {

                }

                String loid = lastNode.oid;
                String ldid = lastNode.did;
            }
        }
    }
}
