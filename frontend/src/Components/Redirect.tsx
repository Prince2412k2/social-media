import { FaSpinner } from "react-icons/fa";
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "axios";


export default function Redirect() {
  const navigate = useNavigate();
  useEffect(() => {
    const processAuth = async () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('code');
        const provider = urlParams.get('state'); // 'google' or 'github'

        if (!code || !provider) {
          throw new Error('Authorization code or state not found.');
        }

        let url: string
        if (provider === "google") {
          url = "http://localhost:8000/api/auth/google/";
        } else if (provider === "github") {
          url = "http://localhost:8000/api/auth/github/";
        } else {
          throw new Error("Invalid provider")
        }

        // Append code as a query param correctly
        url = `${url}?code=${encodeURIComponent(code)}`;

        // Use axios instead of fetch
        const response = await axios.get(url, {
          withCredentials: true
        });

        // Optionally, check response data or status here
        if (response.status !== 200) {
          throw new Error('Failed to authenticate with backend.');
        }

        // Authentication successful - redirect with success message
        navigate('/login');
        console.log("successful")
      } catch (error) {
        console.error('Authentication Error:', error);
        // Redirect on error
        navigate('/login?error=auth_failed');
      }
    };

    processAuth();
  }, [navigate]);



  return (
    <div className="flex justify-center bg-slate-800">
      <div className="flex items-center h-screen">
        <div className="flex flex-col justify-center space-y-5">
          <p className="text-4xl text-indigo-500">
            Redirecting
          </p>
          <FaSpinner className="text-5xl self-center text-indigo-500 animate-spin" />

        </div>
      </div>
    </div>
  )
}
