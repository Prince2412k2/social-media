import { DEFAULT_URL, GITHUB_CLIENT_ID, GOOGLE_CLIENT_ID } from "@/lib/defaults"
import axios from "axios"
import { useEffect, useState, type FormEvent, type ReactElement } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Chrome, Github } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useUser } from "@/context/UserContext";

export default function Login(): ReactElement {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [failed, setFailed] = useState<boolean>(false)
  const navigate = useNavigate();
  const { setUser } = useUser();

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const code = urlParams.get('error');
        if (code) {
          setFailed(true)
        }
      } catch {
        console.log("password login")
      }
    }
    checkLoginStatus();
  }, [])

  async function handlePasswordLogin(e: FormEvent) {
    e.preventDefault()
    try {
      const response = await axios.post(`${DEFAULT_URL}/api/auth/login`, { email, password }, {
        withCredentials: true
      })
      setUser(response.data.user); // Assuming the API returns user data on successful login
      navigate("/");
    } catch (error) {
      setFailed(true)
      console.log(error)
    }
  }

  const handleGoogleLogin = () => {
    const googleAuthUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    const options = {
      redirect_uri: 'http://localhost:8080/auth/callback',
      client_id: GOOGLE_CLIENT_ID,
      access_type: 'offline',
      response_type: 'code',
      prompt: 'consent',
      scope: [
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
      ].join(' '),
      state: 'google',
    };
    const queryString = new URLSearchParams(options).toString();
    window.location.href = `${googleAuthUrl}?${queryString}`;
  };

  const handleGitHubLogin = () => {
    const githubAuthUrl = 'https://github.com/login/oauth/authorize';
    const options = {
      client_id: GITHUB_CLIENT_ID,
      redirect_uri: 'http://localhost:8080/auth/callback',
      scope: 'read:user user:email',
      state: 'github',
    };
    const queryString = new URLSearchParams(options).toString();
    window.location.href = `${githubAuthUrl}?${queryString}`;
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-subtle">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl">Sign in to your account</CardTitle>
          <CardDescription>Enter your email below to sign in</CardDescription>
        </CardHeader>
        <CardContent>
          {failed && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>Login failed. Please check your credentials.</AlertDescription>
            </Alert>
          )}
          <form onSubmit={handlePasswordLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email address</Label>
              <Input
                id="email"
                type="email"
                required
                autoComplete="email"
                onChange={e => setEmail(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Password</Label>
              </div>
              <Input
                id="password"
                type="password"
                required
                autoComplete="current-password"
                onChange={e => setPassword(e.target.value)}
              />
            </div>
            <Button type="submit" className="w-full">
              Sign in
            </Button>
          </form>
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-2 text-muted-foreground">Or continue with</span>
            </div>
          </div>
          <div className="flex flex-col space-y-4">
            <Button variant="outline" onClick={handleGoogleLogin}>
              <Chrome className="mr-2 h-4 w-4" />
              Google
            </Button>
            <Button variant="outline" onClick={handleGitHubLogin}>
              <Github className="mr-2 h-4 w-4" />
              <span>GitHub</span>
            </Button>
          </div>
          <p className="mt-4 text-center text-sm text-muted-foreground">
            Not a member?{" "}
            <Link to="/register" className="font-semibold text-primary hover:text-primary/80">
              Register Now
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
