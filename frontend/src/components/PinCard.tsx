import { Heart, Share, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Pin } from "@/data/pins";
import { useState } from "react";

interface PinCardProps {
  pin: Pin;
  onClick?: () => void;
}

const PinCard = ({ pin, onClick }: PinCardProps) => {
  const [isLiked, setIsLiked] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

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
          alt={pin.title}
          className="w-full h-auto object-cover transition-smooth group-hover:scale-105"
          loading="lazy"
        />

        {/* Overlay Actions */}
        {isHovered && (
          <div className="absolute inset-0 bg-black/20 transition-smooth">
            {/* Top Actions */}
            <div className="absolute top-3 right-3 flex space-x-2">
              <Button
                size="sm"
                variant="secondary"
                className="bg-card/90 hover:bg-card transition-smooth"
                onClick={(e) => {
                  e.stopPropagation();
                  setIsLiked(!isLiked);
                }}
              >
                <Heart
                  className={`h-4 w-4 ${isLiked ? 'fill-red-500 text-red-500' : 'text-foreground'}`}

                />
              </Button>
            </div>

            {/* Bottom Action */}
          </div>
        )}
      </div>

      {/* Card Content */}
      {/* <div className="p-4"> */}

      {/* Author & Stats */}
      {/* <div className="flex items-center justify-between"> */}
      {/*   <div className="flex items-center space-x-2"> */}
      {/*     <div className="w-6 h-6 rounded-full bg-gradient-primary flex items-center justify-center"> */}
      {/*       <span className="text-xs font-medium text-white"> */}
      {/*         {pin.author.charAt(0)} */}
      {/*       </span> */}
      {/*     </div> */}
      {/*     <span className="text-xs text-muted-foreground"> */}
      {/*       {pin.author} */}
      {/*     </span> */}
      {/*   </div> */}

      {/*     <div className="flex items-center space-x-1 text-xs text-muted-foreground"> */}
      {/*       <Heart className="h-3 w-3" /> */}
      {/*       <span>{pin.likes}</span> */}
      {/*     </div> */}
      {/*   </div> */}
      {/* </div> */}
    </Card>
  );
};

export default PinCard;
