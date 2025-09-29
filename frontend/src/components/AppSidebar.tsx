import { Home, MessageCircle, Compass, Settings, User, UserPlus, LogOut, LogIn } from "lucide-react";
import { NavLink, useLocation } from "react-router-dom";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useUser } from "@/context/UserContext";
import { Link } from "react-router-dom";

const navigationItems = [
  { title: "Home", url: "/", icon: Home },
  { title: "Chat", url: "/chat", icon: MessageCircle },
  { title: "Discover", url: "/discover", icon: Compass },
  { title: "Settings", url: "/settings", icon: Settings },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const location = useLocation();
  const currentPath = location.pathname;
  const { user, logout } = useUser();

  const isActive = (path: string) => currentPath === path;

  return (
    <Sidebar 
      className="border-r border-white/10 bg-glass backdrop-blur-xl w-20" 
      style={{ "--sidebar-width": "5rem" } as React.CSSProperties}
    >
      <SidebarHeader className="p-4 flex justify-center">
        {user ? (
          <Link to="/profile">
            <Avatar className="h-12 w-12">
              <AvatarImage src={user.profile_picture || "https://github.com/shadcn.png"} alt={user.username || user.email} />
              <AvatarFallback>{user.username?.charAt(0) || user.email.charAt(0)}</AvatarFallback>
            </Avatar>
          </Link>
        ) : (
          <div className="flex flex-col items-center space-y-2">
            <Link to="/login">
              <SidebarMenuButton asChild size="lg" tooltip="Login">
                <div className="flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-200 text-foreground/70 hover:bg-white/5 hover:text-foreground">
                  <LogIn className="h-6 w-6" />
                </div>
              </SidebarMenuButton>
            </Link>
            <Link to="/register">
              <SidebarMenuButton asChild size="lg" tooltip="Register">
                <div className="flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-200 text-foreground/70 hover:bg-white/5 hover:text-foreground">
                  <UserPlus className="h-6 w-6" />
                </div>
              </SidebarMenuButton>
            </Link>
          </div>
        )}
      </SidebarHeader>

      <SidebarContent className="px-2">
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu className="space-y-3">
              {navigationItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild size="lg" tooltip={item.title}>
                    <NavLink
                      to={item.url}
                      className={({ isActive }) =>
                        `flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-200 ${
                          isActive
                            ? "bg-primary/10 text-primary border border-primary/20 shadow-sm"
                            : "text-foreground/70 hover:bg-white/5 hover:text-foreground"
                        }`
                      }
                    >
                      <item.icon className="h-6 w-6" />
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
              {user && (
                <SidebarMenuItem>
                  <SidebarMenuButton asChild size="lg" tooltip="Logout">
                    <div
                      onClick={logout}
                      className="flex items-center justify-center w-12 h-12 rounded-xl transition-all duration-200 text-foreground/70 hover:bg-white/5 hover:text-foreground"
                    >
                      <LogOut className="h-6 w-6" />
                    </div>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              )}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
