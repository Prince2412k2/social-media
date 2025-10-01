import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import axios from 'axios';
import axiosInstance from '@/lib/axios';

interface User {
  id: number;
  username: string;
  email: string;
  bio: string;
  avatar: string;
  created_at: string;
  follower_count: number;
  following_count: number;
  post_count: number;
  is_following: boolean;
}

interface UserContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  setUser: (user: User | null) => void;
  logout: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await axiosInstance.get(`/api/user/me/`);
        setUser(response.data);
      } catch (err) {
        if (axios.isAxiosError(err) && err.response?.status === 401) {
          // Not logged in, which is expected for some users
          setUser(null);
        } else {
          setError("Failed to fetch user data.");
          console.error("Error fetching user data:", err);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const logout = async () => {
    try {
      await axiosInstance.post(`/api/auth/logout/`);
      setUser(null);
    } catch (err) {
      setError("Failed to logout.");
      console.error("Error logging out:", err);
    }
  };

  return (
    <UserContext.Provider value={{ user, loading, error, setUser, logout }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
