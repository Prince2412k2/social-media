import { Heart, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Pin } from "@/data/pins";
import { useState } from "react";
import axios from "@/lib/axios";
import { DEFAULT_URL } from "@/lib/defaults";
import { User } from "@/context/UserContext";

interface PinCardProps {
  pin: Pin;
  onClick?: () => void;
  onLikeChange: (pinId: number, newLikedStatus: boolean, newLikesCount: number) => void;
  onDelete: (pinId: number) => void;
  loggedInUser: User | null;
}

const PinCard = ({ pin, onClick, onLikeChange, onDelete, loggedInUser }: PinCardProps) => {
  const [isHovered, setIsHovered] = useState(false);

  const handleLikeClick = async (e: React.MouseEvent) => {
    e.stopPropagation();

    const newLikedStatus = !pin.liked_by_user;
    const newLikesCount = pin.liked_by_user ? pin.likes_count - 1 : pin.likes_count + 1;

    onLikeChange(pin.id, newLikedStatus, newLikesCount);

    try {
      const url = `${DEFAULT_URL}/api/post/${newLikedStatus ? 'like' : 'dislike'}`;
      await axios.post(url, { post_id: pin.id }, { withCredentials: true });
    } catch (error) {
      // Revert on error
      onLikeChange(pin.id, pin.liked_by_user, pin.likes_count);
      console.error("Failed to update like status:", error);
    }
  };

  const handleDeleteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDelete(pin.id);
  };

  const isOwner = loggedInUser?.id === pin.user_id;

  return (
    <Card
      className="group relative overflow-hidden bg-gradient-card shadow-elegant hover:shadow-hover transition-smooth cursor-pointer border-0"
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Image Container */}
      <div className="relative overflow-hidden rounded-lg">
        <img
          src={pin.image}
          alt={pin.caption}
          className="w-full h-auto object-cover transition-smooth group-hover:scale-105"
          loading="lazy"
        />

        {/* Overlay Actions */}
        {isHovered && (
          <div className="absolute inset-0 bg-black/20 transition-smooth">
            {/* Top Actions */}
            <div className="absolute top-3 right-3 flex space-x-2">
              {isOwner && (
                <Button
                  size="sm"
                  variant="secondary"
                  className="bg-card/90 hover:bg-card transition-smooth"
                  onClick={handleDeleteClick}
                >
                  <Trash2 className="h-4 w-4 text-red-500" />
                </Button>
              )}
              <Button
                size="sm"
                variant="secondary"
                className="bg-card/90 hover:bg-card transition-smooth"
                onClick={handleLikeClick}
              >
                <Heart
                  className={`h-4 w-4 ${pin.liked_by_user ? 'fill-red-500 text-red-500' : 'text-foreground'}`}
                />
              </Button>
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};

export default PinCard;
