import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { useUser } from "@/context/UserContext";

interface ProfileHeaderProps {
  isCurrentUser?: boolean;
}

const ProfileHeader = ({ isCurrentUser }: ProfileHeaderProps) => {
  const { user } = useUser();

  return (
    <div className="flex flex-col items-center justify-center space-y-4 p-8">
      <Avatar className="h-24 w-24">
        <AvatarImage src={user?.profile_picture || "https://github.com/shadcn.png"} alt={user?.username || user?.email} />
        <AvatarFallback>{user?.username?.charAt(0) || user?.email?.charAt(0)}</AvatarFallback>
      </Avatar>
      <div className="text-center">
        <h1 className="text-2xl font-bold">{user?.username || user?.email}</h1>
        <p className="text-muted-foreground">@{user?.username || user?.email}</p>
      </div>
      <p className="text-center max-w-md">{user?.bio || "I'm a developer and designer. I build things for the web. I like to create beautiful and functional user interfaces."}</p>
      <div className="flex space-x-8 text-center">
        <div>
          <p className="font-bold">1.2k</p>
          <p className="text-muted-foreground">Posts</p>
        </div>
        <div>
          <p className="font-bold">5.4k</p>
          <p className="text-muted-foreground">Followers</p>
        </div>
        <div>
          <p className="font-bold">1.2k</p>
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
            <Button>Follow</Button>
            <Button variant="outline">Message</Button>
          </>
        )}
      </div>
    </div>
  );
};

export default ProfileHeader;
