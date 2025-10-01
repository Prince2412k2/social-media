import { useEffect, useState } from "react";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import Header from "@/components/Header";
import axios from "@/lib/axios";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Link } from "react-router-dom";
import { User } from "@/context/UserContext";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

const Inbox = () => {
  const [chats, setChats] = useState<User[]>([]);
  const [following, setFollowing] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [chatsResponse, followingResponse] = await Promise.all([
          axios.get("/chat/inbox/"),
          axios.get("/api/user/following"),
        ]);
        setChats(chatsResponse.data);
        setFollowing(followingResponse.data);
      } catch (error) {
        console.error("Failed to fetch chat data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const filteredChats = chats.filter((user) =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredFollowing = following
    .filter((followingUser) => !chats.some((chatUser) => chatUser.id === followingUser.id))
    .filter((user) =>
      user.username.toLowerCase().includes(searchTerm.toLowerCase())
    );

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="min-h-screen flex w-full bg-gradient-subtle">
        <AppSidebar />
        <SidebarInset className="flex-1 ml-[4rem]">
          <header className="sticky top-0 z-10 flex h-16 shrink-0 items-center gap-2 border-b border-white/10 px-4 bg-background">
            <div className="flex-1">
              <Header />
            </div>
          </header>
          <main className="flex-1 pb-8">
            <div className="container mx-auto px-4 py-8">
              <h1 className="text-3xl font-bold mb-8">Inbox</h1>

              <div className="mb-8">
                <Input
                  placeholder="Search..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>

              <div>
                <h2 className="text-xl font-semibold mb-4">Past Chats</h2>
                {loading ? (
                  <p>Loading...</p>
                ) : (
                  <div className="space-y-4">
                    {filteredChats.map((user) => (
                      <Link to={`/chat?user_id=${user.id}`} key={user.id} className="flex items-center space-x-4 p-2 rounded-lg hover:bg-muted/50 transition-colors">
                        <Avatar>
                          <AvatarImage src={user.avatar} alt={user.username} />
                          <AvatarFallback>{user.username.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <p className="font-semibold">{user.username}</p>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>

              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4">Following</h2>
                <div className="flex items-center space-x-4 overflow-x-auto pb-4">
                  {loading ? (
                    <p>Loading...</p>
                  ) : (
                    <>
                      {filteredFollowing.map((user) => (
                        <Link to={`/chat?user_id=${user.id}`} key={user.id} className="flex flex-col items-center space-y-2">
                          <Avatar className="h-16 w-16">
                            <AvatarImage src={user.avatar} alt={user.username} />
                            <AvatarFallback>{user.username?.charAt(0) || 'U'}</AvatarFallback>
                          </Avatar>
                          <p className="text-sm font-semibold">{user.username}</p>
                        </Link>
                      ))}
                    </>
                  )}
                </div>
              </div>
            </div>
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
};

export default Inbox;
