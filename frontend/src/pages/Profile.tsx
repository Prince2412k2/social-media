import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import Header from "@/components/Header";
import ProfileHeader from "@/components/ProfileHeader";
import MasonryGrid from "@/components/MasonryGrid";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { useUser } from "@/context/UserContext";
import axios from "@/lib/axios";
import { Pin } from "@/data/pins";
import { User } from "@/context/UserContext";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import AddPostModal from "@/components/AddPostModal";
import PinModal from "@/components/PinModal";

const Profile = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user: loggedInUser, loading: userLoading } = useUser();

  const [profileUser, setProfileUser] = useState<User | null>(null);
  const [userPins, setUserPins] = useState<Pin[]>([]);
  const [loading, setLoading] = useState(true);
  const [addPostModalOpen, setAddPostModalOpen] = useState(false);
  const [selectedPin, setSelectedPin] = useState<Pin | null>(null);
  const [isPinModalOpen, setIsPinModalOpen] = useState(false);

  useEffect(() => {
    const userId = searchParams.get("user_id");

    if (!userId) {
      navigate("/404");
      return;
    }

    if (userId === "me" && userLoading) {
      return; // Wait for user to be loaded
    }

    const fetchProfileData = async () => {
      setLoading(true);
      try {
        let userToFetchId: number | 'me';
        if (userId === "me") {
          if (loggedInUser) {
            setProfileUser(loggedInUser);
            userToFetchId = loggedInUser.id;
          } else {
            navigate("/login");
            return;
          }
        } else {
          userToFetchId = parseInt(userId, 10);
          const userResponse = await axios.post("/api/user/", { user_id: userToFetchId });
          setProfileUser(userResponse.data);
        }

        let postsResponse;
        if (userId === "me") {
          postsResponse = await axios.get("/api/user/posts/");
        } else {
          postsResponse = await axios.post("/api/user/posts/", { user_id: userToFetchId });
        }
        setUserPins(postsResponse.data.results);

      } catch (error) {
        console.error("Failed to fetch profile data:", error);
        navigate("/404");
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, [searchParams, loggedInUser, navigate, userLoading]);

  if (loading || userLoading) {
    return <div>Loading...</div>; // Or a spinner component
  }

  if (!profileUser) {
    return <div>User not found</div>;
  }

  const isCurrentUser = loggedInUser?.id === profileUser.id;

  const handleFollow = async (userId: number, isFollowing: boolean) => {
    if (!profileUser) return;

    const originalIsFollowing = profileUser.is_following;
    const originalFollowerCount = profileUser.follower_count;

    const newFollowedStatus = !isFollowing;
    const newFollowerCount = isFollowing ? profileUser.follower_count - 1 : profileUser.follower_count + 1;

    setProfileUser({ ...profileUser, is_following: newFollowedStatus, follower_count: newFollowerCount });

    try {
      const url = `/api/user/${newFollowedStatus ? 'follow' : 'unfollow'}`;
      await axios.post(url, { user_id: userId });
    } catch (error) {
      setProfileUser({ ...profileUser, is_following: originalIsFollowing, follower_count: originalFollowerCount });
      console.error("Failed to update follow status:", error);
    }
  };

  const handleLikeChange = (pinId: number, newLikedStatus: boolean, newLikesCount: number) => {
    const updatedPins = userPins.map(p => {
      if (p.id === pinId) {
        return { ...p, liked_by_user: newLikedStatus, likes_count: newLikesCount };
      }
      return p;
    });
    setUserPins(updatedPins);
    if (selectedPin && selectedPin.id === pinId) {
      setSelectedPin({ ...selectedPin, liked_by_user: newLikedStatus, likes_count: newLikesCount });
    }
  };

  const handleFollowChange = (pinId: number, newFollowedStatus: boolean) => {
    const updatedPins = userPins.map(p => {
      if (p.id === pinId) {
        return { ...p, is_following: newFollowedStatus };
      }
      return p;
    });
    setUserPins(updatedPins);
    if (selectedPin && selectedPin.id === pinId) {
      setSelectedPin({ ...selectedPin, is_following: newFollowedStatus });
    }
  };

  const handleCommentAdd = (pinId: number, newComment: Pin['comments'][0]) => {
    const updatedPins = userPins.map(p => {
      if (p.id === pinId) {
        const updatedPin = { ...p, comments: [...p.comments, newComment] };
        if (selectedPin && selectedPin.id === pinId) {
          setSelectedPin(updatedPin);
        }
        return updatedPin;
      }
      return p;
    });
    setUserPins(updatedPins);
  };

  const handleCommentDelete = (pinId: number, commentId: number) => {
    const updatedPins = userPins.map(p => {
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
    setUserPins(updatedPins);
  };

  const handlePostAdd = (newPost: Pin) => {
    setUserPins([newPost, ...userPins]);
  };

  const handlePostDelete = async (pinId: number) => {
    try {
      await axios.post("/api/post/del", { post_id: pinId });
      setUserPins(userPins.filter(p => p.id !== pinId));
    } catch (error) {
      console.error("Failed to delete post:", error);
    }
  };

  const handlePinClick = (pin: Pin) => {
    setSelectedPin(pin);
    setIsPinModalOpen(true);
  };

  const closeModal = () => {
    setIsPinModalOpen(false);
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
            <ProfileHeader user={profileUser} isCurrentUser={isCurrentUser} onFollow={handleFollow} />
            {isCurrentUser && (
              <div className="fixed bottom-8 right-8 z-10">
                <Button
                  size="lg"
                  className="rounded-full h-16 w-16"
                  onClick={() => setAddPostModalOpen(true)}
                >
                  <Plus className="h-8 w-8" />
                </Button>
              </div>
            )}
            <MasonryGrid
              pins={userPins}
              onPinClick={handlePinClick}
              onLikeChange={handleLikeChange}
              onDelete={handlePostDelete}
              loggedInUser={loggedInUser}
            />
          </main>
        </SidebarInset>
        <AddPostModal
          isOpen={addPostModalOpen}
          onClose={() => setAddPostModalOpen(false)}
          onPostAdd={handlePostAdd}
        />
        <PinModal
          pin={selectedPin}
          isOpen={isPinModalOpen}
          onClose={closeModal}
          onLikeChange={handleLikeChange}
          onFollowChange={handleFollowChange}
          onCommentAdd={handleCommentAdd}
          onCommentDelete={handleCommentDelete}
        />
      </div>
    </SidebarProvider>
  );
};

export default Profile;
