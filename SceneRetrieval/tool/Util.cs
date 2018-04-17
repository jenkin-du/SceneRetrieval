using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using System.Threading.Tasks;

namespace SceneRetrieval.tool
{
    class Util
    {
        /// <summary>
        /// 将对象解析成json字符串
        /// </summary>
        /// <param name="obj"></param>
        /// <returns></returns>
        public static String toJsonString(Object obj)
        {

            return JsonConvert.SerializeObject(obj);
        }

        /// <summary>
        /// 将json字符串解析成对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="jsonString"></param>
        /// <returns></returns>
        public static T toObject<T>(String jsonString)
        {


            return JsonConvert.DeserializeObject<T>(jsonString);
        }
    }
}
