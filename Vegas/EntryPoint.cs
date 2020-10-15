using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Windows.Forms;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using ScriptPortal.Vegas;

namespace velocity_export
{
    public class EntryPoint
    {
        public List<VideoCut> video_cuts = new List<VideoCut>();
        public void FromVegas(Vegas myVegas)
        {
            // Loop over tracks
            foreach (Track track in myVegas.Project.Tracks)
            {
                // Check if track is video
                if (track.IsVideo())
                {
                    // Loop over events in the trakc
                    foreach (TrackEvent evnt in track.Events)
                    {
                        // Load if selected
                        if (evnt.Selected)
                        {
                            VideoCut cut = new VideoCut();
                            // Video event
                            VideoEvent vevnt = (VideoEvent)evnt;
                            // Media name

                            var videoMedia = vevnt.ActiveTake.Media;
                            string videoName = vevnt.ActiveTake.Name;
                            // Video envelope
                            Envelope VelEnv = FindVEEnvelope(vevnt, EnvelopeType.Velocity);
                            // Check if video has envelope
                            cut.startFrame = (int)vevnt.ActiveTake.Offset.FrameCount;
                            // Total frames in vegas (NOT CUT!)
                            long totalFrames = vevnt.End.FrameCount - vevnt.Start.FrameCount;
                            cut.endFrame = cut.startFrame + (int)totalFrames;
                            if (VelEnv != null)
                            {
                                // i = currentFrame
                                for (int i = 0; i < totalFrames; i++)
                                {
                                    double frameNumber = 0.0;
                                    for (long f = 0; f < i; f++)
                                    {
                                        Timecode valueAt = Timecode.FromFrames(f);
                                        frameNumber += VelEnv.ValueAt(valueAt);
                                    }

                                    Timecode currentFrame = Timecode.FromFrames(i);
                                    var timescale = VelEnv.ValueAt(currentFrame);
                                    cut.endFrame = (int)Math.Round(frameNumber, MidpointRounding.AwayFromZero);
                                    if (!cut.velocity.ContainsKey(cut.endFrame))
                                        cut.velocity.Add(cut.endFrame, timescale);
                                }
                                cut.endFrame += cut.startFrame;
                            }
                            video_cuts.Add(cut);
                            
                        }
                    }
                }
            }

            string velocityJson = JToken.FromObject(video_cuts).ToString(Formatting.Indented);
            string outputPath = Path.Combine("D:/velostuff", "blabla.json");
            Directory.CreateDirectory(Path.GetDirectoryName(outputPath));
            File.WriteAllText(outputPath, velocityJson);
        }

        private Envelope FindVEEnvelope(VideoEvent vevnt, EnvelopeType etype)
        {
            foreach (Envelope env in vevnt.Envelopes)
            {
                if (env.Type == etype)
                {
                    return env;
                }
            }
            return null;
        }
    }
}
