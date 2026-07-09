import React, { useState, useEffect } from 'react';
import { replayAPI } from '../services/replayApi';
import ReplayPlayer from '../components/replay/ReplayPlayer';
import ReplayTelemetry from '../components/replay/ReplayTelemetry';
import { Video } from 'lucide-react';

export default function ReplayCenter() {
  const [list, setList] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [info, setInfo] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [frame, setFrame] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1.0);
  const [progress, setProgress] = useState(0.0);
  const [loading, setLoading] = useState(true);

  const fetchReplayData = async (violationId) => {
    try {
      const [resDetail, resTimeline, resFrame] = await Promise.all([
        replayAPI.getReplayDetails(violationId),
        replayAPI.getTimeline(violationId),
        replayAPI.getFrame(violationId, 45) // default middle frame check
      ]);
      setInfo(resDetail.data);
      setTimeline(resTimeline.data.events || []);
      setFrame(resFrame.data);
    } catch (err) {
      console.error("Failed to load replay metrics details:", err);
    }
  };

  const loadInitialData = async () => {
    try {
      const res = await replayAPI.listReplays();
      const replays = res.data.replays || [];
      setList(replays);
      if (replays.length > 0) {
        const firstId = replays[0].violation_id;
        setActiveId(firstId);
        await fetchReplayData(firstId);
      }
    } catch (err) {
      console.error("Failed to list replays:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const handleSelectReplay = async (violationId) => {
    setActiveId(violationId);
    setProgress(0.0);
    setIsPlaying(false);
    await fetchReplayData(violationId);
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center space-y-3 p-12 text-slate-550 text-xs">
        <span className="w-6 h-6 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
        <span>Loading Replay Center...</span>
      </div>
    );
  }

  const handleTogglePlay = () => setIsPlaying(!isPlaying);
  const handleStop = () => {
    setIsPlaying(false);
    setProgress(0.0);
  };

  const handleEventClick = (timeOffset) => {
    const pct = (timeOffset / 15.0) * 100;
    setProgress(pct);
    setIsPlaying(true);
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100 font-sans">Violation Replay Center</h2>
        <p className="text-xs text-slate-500">Replay surveillance footage segments linked to infraction events.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <ReplayPlayer
            videoUrl={info?.processed_video_url}
            speed={speed}
            isPlaying={isPlaying}
            progress={progress}
            timeline={timeline}
            onProgressUpdate={setProgress}
            onTogglePlay={handleTogglePlay}
            onStop={handleStop}
            onFrameBack={() => setProgress(prev => Math.max(0, prev - 1))}
            onFrameForward={() => setProgress(prev => Math.min(100, prev + 1))}
            onSpeedChange={setSpeed}
          />

          {/* List of replays */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
            <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
              <Video className="w-4.5 h-4.5 text-purple-400" />
              <span>Available Replay Footage</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              {list.map((r) => (
                <div
                  key={r.violation_id}
                  onClick={() => handleSelectReplay(r.violation_id)}
                  className={`p-3 rounded-lg border cursor-pointer transition-all ${
                    activeId === r.violation_id
                      ? 'bg-purple-500/5 border-purple-500/20 text-slate-200'
                      : 'bg-slate-950/40 border-slate-850 hover:border-slate-700/80 text-slate-450 hover:text-slate-200'
                  }`}
                >
                  <div className="font-bold text-xs truncate">{r.filename}</div>
                  <div className="text-[10px] text-slate-500 font-mono mt-1">{r.timestamp}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          <ReplayTelemetry
            info={info}
            timeline={timeline}
            frame={frame}
            currentTimeOffset={(progress / 100) * 15.0}
            onEventClick={handleEventClick}
          />
        </div>
      </div>
    </div>
  );
}
