import { useEffect, useState } from "react";
import Header from "@/components/Header";
import MasonryGrid from "@/components/MasonryGrid";
import PinModal from "@/components/PinModal";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { DEFAULT_URL } from "@/lib/defaults";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";

interface Pin {
  id: number;
  user: string;
  image: string;
  caption: string;
  likes_count: number;
  liked_by_user: boolean;
  comments: {
    id: number;
    user: number;
    post: number;
    text: string;
  }[];
}

const Index = () => {
  const [pins, setPins] = useState<Pin[]>([]);
  const [selectedPin, setSelectedPin] = useState<Pin | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(`${DEFAULT_URL}/api/user/posts`);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchPosts = async (url: string) => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await axios.get(url, {
        withCredentials: true,
      });
      setPins((prevPins) => [...prevPins, ...response.data.results]);
      setNextPageUrl(response.data.next);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 400) {
        navigate("/login");
      } else {
        console.error("Error fetching posts:", error);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts(`${DEFAULT_URL}/api/user/posts`);
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (
        window.innerHeight + document.documentElement.scrollTop >=
          document.documentElement.offsetHeight - 100 && // 100px from bottom
        nextPageUrl &&
        !loading
      ) {
        fetchPosts(nextPageUrl);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [nextPageUrl, loading]);

  const handlePinClick = (pin: Pin) => {
    setSelectedPin(pin);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedPin(null);
  };

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
            <MasonryGrid
              pins={pins}
              onPinClick={handlePinClick}
            />
            {loading && (
              <div className="flex justify-center py-4">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            )}
          </main>
        </SidebarInset>

        <PinModal
          pin={selectedPin}
          isOpen={isModalOpen}
          onClose={closeModal}
        />
      </div>
    </SidebarProvider>
  );
};

export default Index;
