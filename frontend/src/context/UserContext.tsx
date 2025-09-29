import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import axios from 'axios';
import { DEFAULT_URL } from '@/lib/defaults';

interface User {
  id: number;
  email: string;
  username: string;
  profile_picture?: string;
  bio?: string;
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
        const response = await axios.get(`${DEFAULT_URL}/api/user/me/`, {
          withCredentials: true,
        });
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
      await axios.post(`${DEFAULT_URL}/api/auth/logout/`, {}, {
        withCredentials: true,
      });
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
