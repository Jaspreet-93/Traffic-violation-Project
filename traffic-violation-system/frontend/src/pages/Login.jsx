import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/authApi';
import { Shield, Lock, User, Mail, Phone, CheckCircle, XCircle } from 'lucide-react';

export default function Login() {
  const [mode, setMode] = useState('login'); // 'login' | 'register' | 'forgot'
  
  // Login fields
  const [emailAddress, setEmailAddress] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  // Register fields
  const [fullName, setFullName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [message, setMessage] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      setMessage(null);
      const res = await authAPI.login({
        email_address: emailAddress,
        password: password,
        remember_me: rememberMe
      });
      localStorage.setItem('user_profile', JSON.stringify(res.data));
      navigate('/dashboard');
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      setMessage(null);
      await authAPI.register({
        full_name: fullName,
        email_address: emailAddress,
        phone_number: phoneNumber,
        password: password,
        confirm_password: confirmPassword
      });
      setMessage({ type: 'success', text: 'Account registered successfully! Please log in.' });
      setMode('login');
      // Reset registration specific values
      setFullName('');
      setPhoneNumber('');
      setConfirmPassword('');
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  const handleForgotPassword = async (e) => {
    e.preventDefault();
    try {
      setMessage(null);
      const res = await authAPI.forgotPassword({ email_address: emailAddress });
      setMessage({ type: 'success', text: res.data.message });
      setMode('login');
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  return (
    <div className="min-h-screen bg-slate-955 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md p-8 shadow-2xl relative overflow-hidden">
        {/* Glow accent */}
        <div className="absolute -top-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -right-40 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl"></div>

        <div className="relative flex flex-col items-center mb-6">
          <div className="bg-purple-500/15 p-4 rounded-2xl border border-purple-500/30 mb-4">
            <Shield className="w-8 h-8 text-purple-400 animate-pulse" />
          </div>
          <h2 className="text-xl font-bold text-slate-100 uppercase tracking-wide">Aura Monitor Panel</h2>
          <span className="text-[10px] text-slate-500 mt-1 uppercase font-bold tracking-wider">
            {mode === 'login' ? 'Authorized User Sign In' : mode === 'register' ? 'Authorized Account Registration' : 'Recover Account Password'}
          </span>
        </div>

        {message && (
          <div className={`p-3 rounded-lg flex items-center space-x-2 text-xs font-semibold mb-4 border ${
            message.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450'
              : 'bg-rose-500/10 border-rose-500/20 text-rose-450'
          }`}>
            {message.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
            <span>{message.text}</span>
          </div>
        )}

        {/* LOGIN MODE */}
        {mode === 'login' && (
          <form onSubmit={handleLogin} className="space-y-4 relative font-semibold">
            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="email"
                  value={emailAddress}
                  onChange={(e) => setEmailAddress(e.target.value)}
                  placeholder="name@agency.gov"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div className="flex justify-between items-center text-xs">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="rememberMe"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded bg-slate-955 border-slate-850 text-purple-650 focus:ring-purple-500/40 w-4 h-4 mr-2 cursor-pointer"
                />
                <label htmlFor="rememberMe" className="text-slate-450 cursor-pointer select-none">
                  Remember Me
                </label>
              </div>

              <button
                type="button"
                onClick={() => setMode('forgot')}
                className="text-purple-400 hover:text-purple-300 font-bold transition-colors cursor-pointer"
              >
                Forgot Password?
              </button>
            </div>

            <button
              type="submit"
              className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs uppercase tracking-wider cursor-pointer"
            >
              Access Control Deck
            </button>

            <div className="pt-2 text-center text-xs text-slate-500">
              New authorized personnel?{' '}
              <button
                type="button"
                onClick={() => { setMode('register'); setMessage(null); }}
                className="text-purple-400 font-bold hover:underline cursor-pointer"
              >
                Create an Account
              </button>
            </div>
          </form>
        )}

        {/* REGISTER MODE */}
        {mode === 'register' && (
          <form onSubmit={handleRegister} className="space-y-4 relative font-semibold">
            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Officer John Doe"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="email"
                  value={emailAddress}
                  onChange={(e) => setEmailAddress(e.target.value)}
                  placeholder="name@agency.gov"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Phone Number</label>
              <div className="relative">
                <Phone className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="+1 (555) 123-4567"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Confirm Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs uppercase tracking-wider cursor-pointer"
            >
              Sign Up Account
            </button>

            <div className="pt-2 text-center text-xs text-slate-500">
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => { setMode('login'); setMessage(null); }}
                className="text-purple-400 font-bold hover:underline cursor-pointer"
              >
                Log In
              </button>
            </div>
          </form>
        )}

        {/* FORGOT MODE */}
        {mode === 'forgot' && (
          <form onSubmit={handleForgotPassword} className="space-y-4 relative font-semibold">
            <p className="text-xs text-slate-400 leading-relaxed text-center">
              Please enter your registered email address to recover your account.
            </p>

            <div>
              <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-600 absolute left-3 top-3" />
                <input
                  type="email"
                  value={emailAddress}
                  onChange={(e) => setEmailAddress(e.target.value)}
                  placeholder="name@agency.gov"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs uppercase tracking-wider cursor-pointer"
            >
              Recover Password
            </button>

            <div className="pt-2 text-center text-xs">
              <button
                type="button"
                onClick={() => { setMode('login'); setMessage(null); }}
                className="text-purple-400 font-bold hover:underline cursor-pointer"
              >
                Back to Sign In
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
