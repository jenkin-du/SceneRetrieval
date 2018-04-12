using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.model
{
    class PyArgument
    {
        private String mArgument = "";

        public void addArgument(String arg)
        {
            mArgument += " "+ arg;
        }

        public String getArgument()
        {
            return mArgument;
        }


    }
}
