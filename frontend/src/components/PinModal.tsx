import { Link } from "react-router-dom";
import { X, Heart, Trash2, Share, Download, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { useState, useEffect } from "react";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { Input } from "./ui/input";
import axios from "@/lib/axios";
import { DEFAULT_URL } from "@/lib/defaults";
import { useUser } from "@/context/UserContext";

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

interface PinModalProps {
  pin: Pin | null;
  isOpen: boolean;
  onClose: () => void;
  onLikeChange: (pinId: number, newLikedStatus: boolean, newLikesCount: number) => void;
  onFollowChange: (pinId: number, newFollowedStatus: boolean) => void;
  onCommentAdd: (pinId: number, newComment: Pin['comments'][0]) => void;
  onCommentDelete: (pinId: number, commentId: number) => void;
}

const PinModal = ({ pin, isOpen, onClose, onLikeChange, onFollowChange, onCommentAdd, onCommentDelete }: PinModalProps) => {
  const { user: loggedInUser } = useUser();
  const [isLiked, setIsLiked] = useState(pin?.liked_by_user || false);
  const [likes, setLikes] = useState(pin?.likes_count || 0);
  const [isFollowed, setIsFollowed] = useState(pin?.is_following || false);
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    if (pin) {
      setIsLiked(pin.liked_by_user);
      setLikes(pin.likes_count);
      setIsFollowed(pin.is_following);
    }
  }, [pin]);

  if (!pin) return null;

  const handleLikeClick = async () => {
    if (!pin) return;

    const originalIsLiked = isLiked;
    const originalLikes = likes;

    const newLikedStatus = !isLiked;
    const newLikesCount = isLiked ? likes - 1 : likes + 1;

    onLikeChange(pin.id, newLikedStatus, newLikesCount);

    try {
      const url = `${DEFAULT_URL}/api/post/${newLikedStatus ? 'like' : 'dislike'}`;
      await axios.post(url, { post_id: pin.id }, { withCredentials: true });
    } catch (error) {
      // Revert on error
      onLikeChange(pin.id, originalIsLiked, originalLikes);
      console.error("Failed to update like status:", error);
    }
  };

  const handleFollowClick = async () => {
    if (!pin) return;

    const originalIsFollowed = isFollowed;
    const newFollowedStatus = !isFollowed;

    onFollowChange(pin.id, newFollowedStatus);

    try {
      const url = `${DEFAULT_URL}/api/user/${newFollowedStatus ? 'follow' : 'unfollow'}`;
      await axios.post(url, { user_id: pin.user_id }, { withCredentials: true });
    } catch (error) {
      // Revert on error
      onFollowChange(pin.id, originalIsFollowed);
      console.error("Failed to update follow status:", error);
    }
  };

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim() || !pin) return;

    const payload = {
      text: newComment,
      post_id: pin.id,
    };

    try {
      const response = await axios.post(`${DEFAULT_URL}/api/user/post/comment`, payload, {
        withCredentials: true,
      });
      const newCommentData = response.data;
      onCommentAdd(pin.id, newCommentData);
      setNewComment("");
    } catch (error) {
      console.error("Failed to add comment:", error);
    }
  };

  const handleCommentDelete = async (commentId: number) => {
    if (!pin) return;

    onCommentDelete(pin.id, commentId);

    try {
      await axios.post(`${DEFAULT_URL}/api/user/post/comment/del`, { comment_id: commentId }, {
        withCredentials: true,
      });
    } catch (error) {
      // Revert (logic to be added in parent)
      console.error("Failed to delete comment:", error);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl w-full p-0 gap-0 bg-card border-0 shadow-glass">
        <div className="grid md:grid-cols-2 gap-0">
          {/* Image Section */}
          <div className="relative overflow-hidden">
            <img
              src={pin.image}
              alt={pin.caption}
              className="w-full h-full object-cover"
            />
            <Button
              variant="ghost"
              size="icon"
              className="absolute top-4 left-4 bg-card/80 backdrop-blur-sm hover:bg-card"
              onClick={onClose}
            >
              <X className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleLikeClick}
              className="absolute bottom-4 right-4 z-10 transition-smooth bg-card/80 backdrop-blur-sm hover:bg-card"
            >
              <Heart
                className={`h-4 w-4 mr-2 ${isLiked ? 'fill-red-500 text-red-500' : ''}`}
              />
              {likes}
            </Button>
          </div>

          {/* Content Section */}
          <div className="p-8">
            <DialogTitle className="sr-only">Pin Details</DialogTitle>
            <DialogDescription className="sr-only">Details for the selected pin.</DialogDescription>

            {/* Pin Details */}
            <div className="space-y-6">

              {/* Author Info */}
              <div className="flex items-center justify-between">
                <Link to={`/profile?user_id=${pin.user_id}`} className="flex items-center space-x-3">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={undefined} alt={pin.user} />
                    <AvatarFallback>{pin.user.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-medium text-foreground">{pin.user}</p>
                    <p className="text-sm text-muted-foreground">
                      {/* {pin.category} */}
                    </p>
                  </div>
                </Link>
                <Button
                  variant={isFollowed ? "secondary" : "outline"}
                  onClick={handleFollowClick}
                  className="transition-smooth"
                >
                  {isFollowed ? "Unfollow" : "Follow"}
                </Button>
              </div>
              <div>
                <p className="text-base text-foreground pt-4">
                  {pin.caption}
                </p>
              </div>



              {/* Comments Section */}
              <div className="space-y-4">
                <h3 className="font-semibold text-foreground">
                  Comments
                </h3>
                {pin.comments.length > 0 ? (
                  <div className="space-y-4">
                    {pin.comments.map((comment) => (
                      <div key={comment.id} className="flex items-center justify-between">
                        <div className="flex items-start space-x-3">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={comment.user_profile} alt={`User ${comment.user_id}`} />
                            <AvatarFallback>{comment.user_id.toString().charAt(0)}</AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="text-sm font-semibold">User {comment.user_id}</p>
                            <p className="text-sm text-muted-foreground">{comment.text}</p>
                          </div>
                        </div>
                        {loggedInUser && loggedInUser.id === comment.user_id && (
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleCommentDelete(comment.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-sm text-muted-foreground">
                    Be the first to comment on this pin!
                  </div>
                )}
                <form onSubmit={handleCommentSubmit} className="flex items-center space-x-2 pt-4">
                  <Input
                    placeholder="Add a comment..."
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                  />
                  <Button type="submit">Post</Button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PinModal;
