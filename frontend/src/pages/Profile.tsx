import Header from "@/components/Header";
import ProfileHeader from "@/components/ProfileHeader";
import MasonryGrid from "@/components/MasonryGrid";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { dummyPins } from "@/data/pins";

const Profile = () => {
  // For now, we'll just display all dummy pins.
  const userPins = dummyPins;

  return (
    <SidebarProvider defaultOpen={true}>
          <div className="min-h-screen flex w-full bg-gradient-subtle">
            <AppSidebar />
            <SidebarInset className="flex-1 ml-[4rem]">          <header className="sticky top-0 z-10 flex h-16 shrink-0 items-center gap-2 border-b border-white/10 px-4 bg-background">
            <div className="flex-1">
              <Header />
            </div>
          </header>
          <main className="flex-1 pb-8">
            <ProfileHeader isCurrentUser={true} />
            <MasonryGrid pins={userPins} onPinClick={() => {}} />
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
};

export default Profile;
