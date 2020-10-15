using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace velocity_export
{
    public class VideoCut
    {
        public int startFrame;
        public int endFrame;
        public Dictionary<double, double> velocity = new Dictionary<double, double>();
    }

}
