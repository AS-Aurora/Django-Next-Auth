"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState<any>(null);
  const [errorData, setErrorData] = useState<any>(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/auth/user/", {
      withCredentials: true, // This sends cookies to the backend
    })
    .then((res) => {
      console.log("User data:", res.data);
      setUserData(res.data);
      setLoading(false);
    })
    .catch((err) => {
      setErrorData(err?.response?.data);
      router.push("/login");
    });
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center h-screen text-xl">Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold">Welcome, {userData?.username || "User"}!</h1>
      <p className="mt-2 text-gray-600">This is your protected home page.</p>

      {errorData && (
        <div className="mt-4 p-4 bg-red-100 text-red-800 rounded-md">
          <p>Error: {errorData.detail || "An error occurred."}</p>
        </div>
      )}
    </div>
  );
}
