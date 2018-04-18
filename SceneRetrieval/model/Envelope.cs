using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SceneRetrieval.model
{
    class Envelope
    {
        public Point rtPoint;
        public Point lbPoint;

        private double width = 0;
        private double height = 0;

        public double Width
        {
            get
            {
                return (rtPoint.x - lbPoint.x) / 2;
            }

            set
            {
                width = value;
            }
        }

        public double Height
        {
            get
            {
                return (rtPoint.y - lbPoint.y) / 2;
            }

            set
            {
                height = value;
            }
        }
    }
}
