import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Link, useNavigate } from "react-router-dom";
import { User } from "@/context/UserContext";

interface ProfileHeaderProps {
  user: User;
  isCurrentUser?: boolean;
  onFollow: (userId: number, isFollowing: boolean) => void;
}

const ProfileHeader = ({ user, isCurrentUser, onFollow }: ProfileHeaderProps) => {
  const navigate = useNavigate();

  const handleMessageClick = () => {
    navigate(`/chat?user_id=${user.id}`);
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-4 p-8">
      <Avatar className="h-24 w-24">
        <AvatarImage src={user.avatar || "https://github.com/shadcn.png"} alt={user.username || user.email} />
        <AvatarFallback>{user.username?.charAt(0) || user.email?.charAt(0)}</AvatarFallback>
      </Avatar>
      <div className="text-center">
        <h1 className="text-2xl font-bold">{user.username || user.email}</h1>
        <p className="text-muted-foreground">@{user.username || user.email}</p>
      </div>
      <p className="text-center max-w-md">{user.bio || "I'm a developer and designer. I build things for the web. I like to create beautiful and functional user interfaces."}</p>
      <div className="flex space-x-8 text-center">
        <div>
          <p className="font-bold">{user.post_count}</p>
          <p className="text-muted-foreground">Posts</p>
        </div>
        <div>
          <p className="font-bold">{user.follower_count}</p>
          <p className="text-muted-foreground">Followers</p>
        </div>
        <div>
          <p className="font-bold">{user.following_count}</p>
          <p className="text-muted-foreground">Following</p>
        </div>
      </div>
      <div className="flex space-x-2">
        {isCurrentUser ? (
          <Link to="/edit-profile">
            <Button variant="outline">Edit Profile</Button>
          </Link>
        ) : (
          <>
            <Button onClick={() => onFollow(user.id, user.is_following)}>
              {user.is_following ? "Unfollow" : "Follow"}
            </Button>
            <Button variant="outline" onClick={handleMessageClick}>Message</Button>
          </>
        )}
      </div>
    </div>
  );
};

export default ProfileHeader;
