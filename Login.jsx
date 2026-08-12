// Login.jsx

import { useState } from "react";
import axios from "axios";
import { ShieldCheck, Lock, User } from "lucide-react";

export default function Login() {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post(
        "http://localhost:8000/admin/login",
        formData
      );

      localStorage.setItem("token", response.data.token);

      setMessage("Login Successful");

      // Redirect later if using React Router
      // navigate("/dashboard");

    } catch (error) {
      setMessage(
        error.response?.data?.detail || "Login Failed"
      );
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      
      {/* Background Glow */}
      <div className="absolute w-[500px] h-[500px] bg-cyan-500 opacity-20 blur-3xl rounded-full"></div>

      <div className="relative bg-white/10 backdrop-blur-lg border border-cyan-400/30 shadow-2xl rounded-3xl p-10 w-full max-w-md">

        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="bg-cyan-500/20 p-4 rounded-full mb-4">
            <ShieldCheck className="text-cyan-400 w-10 h-10" />
          </div>

          <h1 className="text-3xl font-bold text-white tracking-wide">
            A.R.E.S
          </h1>

          <p className="text-gray-300 mt-2 text-sm">
            Crime Intelligence Admin Portal
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-6">

          {/* Username */}
          <div>
            <label className="text-gray-300 text-sm mb-2 block">
              Username
            </label>

            <div className="flex items-center bg-black/40 border border-cyan-400/20 rounded-xl px-4 py-3">
              <User className="text-cyan-400 mr-3 w-5 h-5" />

              <input
                type="text"
                name="username"
                placeholder="Enter username"
                value={formData.username}
                onChange={handleChange}
                className="bg-transparent outline-none text-white w-full"
                required
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <label className="text-gray-300 text-sm mb-2 block">
              Password
            </label>

            <div className="flex items-center bg-black/40 border border-cyan-400/20 rounded-xl px-4 py-3">
              <Lock className="text-cyan-400 mr-3 w-5 h-5" />

              <input
                type="password"
                name="password"
                placeholder="Enter password"
                value={formData.password}
                onChange={handleChange}
                className="bg-transparent outline-none text-white w-full"
                required
              />
            </div>
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-cyan-500 hover:bg-cyan-400 transition-all duration-300 text-black font-semibold py-3 rounded-xl shadow-lg hover:shadow-cyan-500/50"
          >
            {loading ? "Authenticating..." : "Secure Login"}
          </button>

          {/* Message */}
          {message && (
            <div className="text-center text-sm text-cyan-300 mt-4">
              {message}
            </div>
          )}
        </form>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-xs">
          A.R.E.S Neural Crime Intelligence System
        </div>
      </div>
    </div>
  );
}