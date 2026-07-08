import React, { useState, useEffect } from 'react';
import { cameraAPI } from '../services/cameraApi';
import CameraCard from '../components/camera/CameraCard';
import CameraStatus from '../components/camera/CameraStatus';
import CameraHealth from '../components/camera/CameraHealth';
import { Plus } from 'lucide-react';

export default function CameraManagement() {
  const [cameras, setCameras] = useState([]);
  const [status, setStatus] = useState(null);
  const [health, setHealth] = useState(null);
  const [activeId, setActiveId] = useState(null);
  const [loading, setLoading] = useState(true);

  // Form states for new camera
  const [name, setName] = useState('');
  const [url, setUrl] = useState('');

  const fetchDetails = async (id) => {
    try {
      const res = await cameraAPI.getHealth(id);
      setHealth(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadData = async () => {
    try {
      const [resCams, resStatus] = await Promise.all([
        cameraAPI.getAll(),
        cameraAPI.getStatus()
      ]);
      setCameras(resCams.data);
      setStatus(resStatus.data);
      if (resCams.data.length > 0) {
        const firstId = resCams.data[0].id;
        setActiveId(firstId);
        await fetchDetails(firstId);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name || !url) return;
    try {
      await cameraAPI.create({ name, url, resolution: "1920x1080", fps: 30, recording_enabled: true });
      setName('');
      setUrl('');
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleRec = async (id, val) => {
    try {
      await cameraAPI.update(id, { recording_enabled: val });
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await cameraAPI.delete(id);
      if (activeId === id) {
        setHealth(null);
        setActiveId(null);
      }
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSelect = async (id) => {
    setActiveId(id);
    await fetchDetails(id);
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-550 text-xs">
        <span>Loading Camera Manager...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Camera Management</h2>
        <p className="text-xs text-slate-500">Monitor and configure surveillance feed capture streams.</p>
      </div>

      <CameraStatus status={status} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {cameras.map((c) => (
              <CameraCard
                key={c.id}
                item={c}
                isActive={c.id === activeId}
                onSelect={handleSelect}
                onToggle={handleToggleRec}
                onDelete={handleDelete}
              />
            ))}
          </div>
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          {/* Add camera */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
            <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Register Stream</h3>
            <form onSubmit={handleCreate} className="space-y-4">
              <div className="space-y-1 text-xs">
                <label className="text-[10px] text-slate-500 font-bold uppercase">Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
                  placeholder="e.g. North Camera"
                />
              </div>
              <div className="space-y-1 text-xs">
                <label className="text-[10px] text-slate-500 font-bold uppercase">RTSP/URL</label>
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
                  placeholder="rtsp://192.168.1.10/live"
                />
              </div>
              <button
                type="submit"
                className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2 rounded-lg text-xs flex items-center justify-center space-x-1 cursor-pointer transition-all"
              >
                <Plus className="w-4 h-4" />
                <span>Register Device</span>
              </button>
            </form>
          </div>

          {activeId && <CameraHealth health={health} />}
        </div>
      </div>
    </div>
  );
}
