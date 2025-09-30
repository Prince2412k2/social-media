import { useEffect, useState } from "react";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import Header from "@/components/Header";
import axios from "@/lib/axios";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Link } from "react-router-dom";
import { User } from "@/context/UserContext";

const Inbox = () => {
  const [chats, setChats] = useState<User[]>([]);
  const [following, setFollowing] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

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
              <h1 className="text-2xl font-bold mb-4">Inbox</h1>
              
              <div className="space-y-8">
                <div>
                  <h2 className="text-xl font-semibold mb-4">Past Chats</h2>
                  {loading ? (
                    <p>Loading...</p>
                  ) : (
                    <div className="space-y-4">
                      {chats.map((user) => (
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

                <div>
                  <h2 className="text-xl font-semibold mb-4">Following</h2>
                  {loading ? (
                    <p>Loading...</p>
                  ) : (
                    <div className="space-y-4">
                      {following
                        .filter((followingUser) => !chats.some((chatUser) => chatUser.id === followingUser.id))
                        .map((user) => (
                        <Link to={`/chat?user_id=${user.id}`} key={user.id} className="flex items-center space-x-4 p-2 rounded-lg hover:bg-muted/50 transition-colors">
                          <Avatar>
                            <AvatarImage src={user.avatar} alt={user.username} />
                            <AvatarFallback>{user.username?.charAt(0) || 'U'}</AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="font-semibold">{user.username}</p>
                          </div>
                        </Link>
                      ))}
                    </div>
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
