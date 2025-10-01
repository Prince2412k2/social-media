import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from "@/lib/axios";
import { Loader2 } from "lucide-react";
import { DEFAULT_URL } from "@/lib/defaults";
import { useUser } from "@/context/UserContext";

export default function AuthCallback() {
  const navigate = useNavigate();
  const { setUser } = useUser();

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
          url = `${DEFAULT_URL}/api/auth/google/`;
        } else if (provider === "github") {
          url = `${DEFAULT_URL}/api/auth/github/`;
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
        setUser(response.data.user); // Assuming the API returns user data on successful social login
        navigate('/');
        console.log("successful")
      } catch (error) {
        console.error('Authentication Error:', error);
        // Redirect on error
        navigate('/login?error=auth_failed');
      }
    };

    processAuth();
  }, [navigate, setUser]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-subtle">
      <div className="flex flex-col items-center justify-center space-y-5">
        <p className="text-4xl text-primary">
          Redirecting...
        </p>
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
      </div>
    </div>
  );
}
