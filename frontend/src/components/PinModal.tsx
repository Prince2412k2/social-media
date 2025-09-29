import { Link } from "react-router-dom";
import { X, Heart, Share, Download, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";
import { useState } from "react";

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

interface PinModalProps {
  pin: Pin | null;
  isOpen: boolean;
  onClose: () => void;
}

const PinModal = ({ pin, isOpen, onClose }: PinModalProps) => {
  const [isLiked, setIsLiked] = useState(false);
  const [isFollowed, setIsFollowed] = useState(false);
  if (!pin) return null;

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
          </div>

          {/* Content Section */}
          <div className="p-8">
            <DialogTitle className="sr-only">Pin Details</DialogTitle>

            {/* Header Actions */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsLiked(!isLiked)}
                  className="transition-smooth"
                >
                  <Heart
                    className={`h-4 w-4 mr-2 ${isLiked ? 'fill-red-500 text-red-500' : ''}`}
                  />
                  {isLiked ? 'Liked' : 'Like'}
                </Button>

              </div>


            </div>

            {/* Pin Details */}
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-foreground mb-3">
                  {pin.caption}
                </h2>
                <p className="text-muted-foreground leading-relaxed">
                  {pin.caption}
                </p>
              </div>

              {/* Author Info */}
              <Link to="/profile">
                <div className="flex items-center space-x-3 p-4 bg-muted/30 rounded-lg">
                  <div className="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center">
                    <span className="text-sm font-medium text-white">
                      {pin.user.charAt(0)}
                    </span>
                  </div>
                  <div className="flex flex-row gap-10">
                    <div>
                      <p className="font-medium text-foreground">
                        {pin.user}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {/* {pin.category} */}
                      </p>
                    </div>
                    <Button
                      onClick={() => setIsFollowed(!isFollowed)}
                      className="bg-gradient-primary text-white hover:shadow-hover transition-smooth"
                    >
                      {isFollowed ? "unfollow" : "follow"}
                    </Button>
                  </div>
                </div>
              </Link>

              {/* Stats */}
              <div className="flex items-center justify-between p-4 bg-muted/30 rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-1">
                    <Heart className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm text-muted-foreground">
                      {pin.likes_count} likes
                    </span>
                  </div>
                </div>
              </div>

              {/* Comments Section */}
              <div className="space-y-4">
                <h3 className="font-semibold text-foreground">
                  Comments
                </h3>
                {pin.comments.length > 0 ? (
                  <div className="space-y-2">
                    {pin.comments.map((comment) => (
                      <div key={comment.id} className="text-sm text-muted-foreground">
                        <strong>User {comment.user}:</strong> {comment.text}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-sm text-muted-foreground">
                    Be the first to comment on this pin!
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PinModal;
