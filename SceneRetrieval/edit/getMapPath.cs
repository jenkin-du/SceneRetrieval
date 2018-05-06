using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace milk.地图编辑
{
    class getMapPath
    {
        public static string getPath(string path)
        {
            int t;
            for (t = 0; t < path.Length; t++)
            {

                if (path.Substring(t, 4) == "milk")
                {
                    break;
                }
            }
            string name = path.Substring(0, t + 4);
            return name;
        }
    }
}
