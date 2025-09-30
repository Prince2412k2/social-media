import { useEffect, useState, useRef } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import Header from "@/components/Header";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";
import { useUser } from "@/context/UserContext";
import axios from "@/lib/axios";

interface Message {
  id: number;
  sender: number;
  content: string;
  timestamp: string;
}

const ChatRoom = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user: loggedInUser } = useUser();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState("");
  const [otherUser, setOtherUser] = useState<{ id: number; username: string; avatar: string } | null>(null);
  const ws = useRef<WebSocket | null>(null);

  const userId = searchParams.get("user_id");

  useEffect(() => {
    if (!userId) {
      navigate("/inbox");
      return;
    }

    // Fetch user data for the other user in the chat
    const fetchOtherUser = async () => {
      try {
        const response = await axios.post(`/api/user/`, { user_id: userId });
        setOtherUser(response.data);
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      }
    };

    // Fetch chat history
    const fetchMessages = async () => {
      try {
        const response = await axios.post(`/chat/messages`, { user_id: userId });
        setMessages(response.data);
      } catch (error) {
        console.error("Failed to fetch messages:", error);
      }
    };

    fetchOtherUser();
    fetchMessages();

    // WebSocket connection
    ws.current = new WebSocket(`ws://localhost:8001/ws/chat/${userId}/`);

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const newMessage: Message = {
        id: Date.now(), // Temporary ID
        sender: data.sender_id,
        content: data.message,
        timestamp: new Date().toISOString(),
      };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
    };

    return () => {
      ws.current?.close();
    };
  }, [userId, navigate]);

  const handleSendMessage = () => {
    if (newMessage.trim() && ws.current) {
      ws.current.send(JSON.stringify({ message: newMessage }));
      setNewMessage("");
    }
  };

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="min-h-screen flex w-full bg-gradient-subtle">
        <AppSidebar />
        <SidebarInset className="flex-1 ml-[4rem] flex flex-col">
          <header className="sticky top-0 z-10 flex h-16 shrink-0 items-center gap-2 border-b border-white/10 px-4 bg-background">
            <div className="flex-1">
              <Header />
            </div>
          </header>
          <main className="flex-1 flex flex-col">
            {otherUser && (
              <div className="flex items-center p-4 border-b">
                <Avatar>
                  <AvatarImage src={otherUser.avatar} alt={otherUser.username} />
                  <AvatarFallback>{otherUser.username.charAt(0)}</AvatarFallback>
                </Avatar>
                <h1 className="text-xl font-bold ml-4">{otherUser.username}</h1>
              </div>
            )}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === loggedInUser?.id ? "justify-end" : "justify-start"}`}>
                  <div className={`p-2 rounded-lg max-w-xs ${ message.sender === loggedInUser?.id ? "bg-primary text-primary-foreground" : "bg-muted" }`}>
                    {message.content}
                  </div>
                </div>
              ))}
            </div>
            <div className="p-4 border-t">
              <div className="flex items-center space-x-2">
                <Input
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type a message..."
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                />
                <Button onClick={handleSendMessage}>
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
};

export default ChatRoom;
