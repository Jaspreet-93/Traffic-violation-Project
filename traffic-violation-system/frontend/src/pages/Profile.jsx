import React, { useState, useEffect } from 'react';
import { authAPI } from '../services/authApi';
import { User, Lock, CheckCircle, XCircle } from 'lucide-react';

export default function Profile() {
  const [userId, setUserId] = useState('');
  const [fullName, setFullName] = useState('');
  const [emailAddress, setEmailAddress] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');

  const [profileMsg, setProfileMsg] = useState(null);
  const [passwordMsg, setPasswordMsg] = useState(null);

  useEffect(() => {
    // Load logged-in user profile from localStorage
    const savedUser = localStorage.getItem('user_profile');
    if (savedUser) {
      const u = JSON.parse(savedUser);
      setUserId(u.id);
      setFullName(u.full_name);
      setEmailAddress(u.email_address);
      setPhoneNumber(u.phone_number);
    }
  }, []);

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    try {
      setProfileMsg(null);
      const res = await authAPI.updateProfile(userId, {
        full_name: fullName,
        phone_number: phoneNumber
      });
      localStorage.setItem('user_profile', JSON.stringify(res.data));
      setProfileMsg({ type: 'success', text: 'Profile successfully updated.' });
    } catch (err) {
      setProfileMsg({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    try {
      setPasswordMsg(null);
      const res = await authAPI.changePassword(userId, {
        old_password: oldPassword,
        new_password: newPassword,
        confirm_new_password: confirmNewPassword
      });
      setPasswordMsg({ type: 'success', text: 'Password successfully changed.' });
      setOldPassword('');
      setNewPassword('');
      setConfirmNewPassword('');
    } catch (err) {
      setPasswordMsg({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">User Account Profile</h2>
        <p className="text-xs text-slate-500">Edit account configurations and update authorization credentials.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Edit Profile */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col space-y-4">
          <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
            <User className="w-4.5 h-4.5 text-purple-400" />
            <span>Edit Profile Info</span>
          </h3>

          {profileMsg && (
            <div className={`p-3 rounded-lg flex items-center space-x-2 text-xs font-semibold border ${
              profileMsg.type === 'success'
                ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450'
                : 'bg-rose-500/10 border-rose-500/20 text-rose-450'
            }`}>
              {profileMsg.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              <span>{profileMsg.text}</span>
            </div>
          )}

          <form onSubmit={handleUpdateProfile} className="space-y-4 font-semibold">
            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2.5 px-3.5 text-xs text-slate-255 outline-none transition-colors"
              />
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Email Address</label>
              <input
                type="email"
                value={emailAddress}
                disabled
                className="w-full bg-slate-955 border border-slate-850 opacity-40 rounded-xl py-2.5 px-3.5 text-xs text-slate-450 outline-none cursor-not-allowed"
              />
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Phone Number</label>
              <input
                type="text"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2.5 px-3.5 text-xs text-slate-255 outline-none transition-colors"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs uppercase tracking-wider cursor-pointer"
            >
              Update Profile details
            </button>
          </form>
        </div>

        {/* Change Password */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col space-y-4">
          <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
            <Lock className="w-4.5 h-4.5 text-purple-400" />
            <span>Change Secure Password</span>
          </h3>

          {passwordMsg && (
            <div className={`p-3 rounded-lg flex items-center space-x-2 text-xs font-semibold border ${
              passwordMsg.type === 'success'
                ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450'
                : 'bg-rose-500/10 border-rose-500/20 text-rose-450'
            }`}>
              {passwordMsg.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
              <span>{passwordMsg.text}</span>
            </div>
          )}

          <form onSubmit={handleChangePassword} className="space-y-4 font-semibold">
            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Current Password</label>
              <input
                type="password"
                value={oldPassword}
                onChange={(e) => setOldPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2.5 px-3.5 text-xs text-slate-255 outline-none transition-colors"
              />
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">New Password</label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2.5 px-3.5 text-xs text-slate-255 outline-none transition-colors"
              />
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Confirm New Password</label>
              <input
                type="password"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2.5 px-3.5 text-xs text-slate-255 outline-none transition-colors"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs uppercase tracking-wider cursor-pointer"
            >
              Update Password
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
