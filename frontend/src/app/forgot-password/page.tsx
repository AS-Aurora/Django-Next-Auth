"use client";

import axios from "axios";
import { useRouter } from "next/navigation";
import React, { useState } from "react";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const router = useRouter();

  const handleForgotPassword = async () => {
    try {
      setLoading(true);
      await axios.post("http://localhost:8000/api/auth/password/reset", { email });
      setMessage("📧 Password reset link sent to your email.");
      setTimeout(() => router.push("/login"), 2500)
    } catch (error: any) {
      setMessage(error.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 px-4">
      <div className="w-full max-w-md bg-white shadow-lg rounded-xl p-8">
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">
          {loading ? "Processing..." : "Forgot Password"}
        </h1>

        <div className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-600">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-black"
              placeholder="Enter your email address"
            />
          </div>
        </div>

        <button
          onClick={handleForgotPassword}
          disabled={loading || email.length === 0}
          className={`mt-6 w-full py-2 px-4 rounded-md font-semibold text-white transition ${
            loading || email.length === 0
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "Sending Link..." : "Send Reset Link"}
        </button>

        {message && (
          <div
            className={`mt-4 p-3 rounded-md text-sm ${
              message.startsWith("📧")
                ? "bg-green-100 text-green-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {message}
          </div>
        )}
      </div>
    </div>
  );
};

export default ForgotPassword;
