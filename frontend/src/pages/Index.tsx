import { useEffect, useState } from "react";
import Header from "@/components/Header";
import MasonryGrid from "@/components/MasonryGrid";
import PinModal from "@/components/PinModal";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { DEFAULT_URL } from "@/lib/defaults";
import axios from "axios";
import axiosInstance from "@/lib/axios";
import { useNavigate } from "react-router-dom";
import { Loader2 } from "lucide-react";

interface Pin {
  id: number;
  user: string;
  user_id: number;
  is_following: boolean;
  image: string;
  caption: string;
  likes_count: number;
  liked_by_user: boolean;
  comments: {
    id: number;
    user_id: number;
    post: number;
    text: string;
    user_profile: string;
  }[];
}

const Index = () => {
  const [pins, setPins] = useState<Pin[]>([]);
  const [selectedPin, setSelectedPin] = useState<Pin | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [nextPageUrl, setNextPageUrl] = useState<string | null>(`${DEFAULT_URL}/api/posts`);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchPosts = async (url: string) => {
    if (loading) return;
    setLoading(true);
    try {
      const response = await axiosInstance.get(url, {
        withCredentials: true,
      });
      setPins((prevPins) => {
        const newPins = response.data.results;
        const allPins = [...prevPins, ...newPins];
        const uniquePins = allPins.filter((pin, index, self) =>
          index === self.findIndex((p) => (
            p.id === pin.id
          ))
        );
        return uniquePins;
      });
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
    fetchPosts(`${DEFAULT_URL}/api/posts`);
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

  const handleLikeChange = (pinId: number, newLikedStatus: boolean, newLikesCount: number) => {
    const updatedPins = pins.map(p => {
      if (p.id === pinId) {
        const updatedPin = { ...p, liked_by_user: newLikedStatus, likes_count: newLikesCount };
        if (selectedPin && selectedPin.id === pinId) {
          setSelectedPin(updatedPin);
        }
        return updatedPin;
      }
      return p;
    });
    setPins(updatedPins);
  };

  const handleFollowChange = (pinId: number, newFollowedStatus: boolean) => {
    const updatedPins = pins.map(p => {
      if (p.id === pinId) {
        const updatedPin = { ...p, is_following: newFollowedStatus };
        if (selectedPin && selectedPin.id === pinId) {
          setSelectedPin(updatedPin);
        }
        return updatedPin;
      }
      return p;
    });
    setPins(updatedPins);
  };

  const handleCommentAdd = (pinId: number, newComment: Pin['comments'][0]) => {
    const updatedPins = pins.map(p => {
      if (p.id === pinId) {
        const updatedPin = { ...p, comments: [...p.comments, newComment] };
        if (selectedPin && selectedPin.id === pinId) {
          setSelectedPin(updatedPin);
        }
        return updatedPin;
      }
      return p;
    });
    setPins(updatedPins);
  };

  const handleCommentDelete = (pinId: number, commentId: number) => {
    const updatedPins = pins.map(p => {
      if (p.id === pinId) {
        const updatedComments = p.comments.filter(c => c.id !== commentId);
        const updatedPin = { ...p, comments: updatedComments };
        if (selectedPin && selectedPin.id === pinId) {
          setSelectedPin(updatedPin);
        }
        return updatedPin;
      }
      return p;
    });
    setPins(updatedPins);
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
              onLikeChange={handleLikeChange}
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
          onLikeChange={handleLikeChange}
          onFollowChange={handleFollowChange}
          onCommentAdd={handleCommentAdd}
          onCommentDelete={handleCommentDelete}
        />
      </div>
    </SidebarProvider>
  );};

export default Index;
