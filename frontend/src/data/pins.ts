import pin1 from "@/assets/pin-1.jpg";
import pin2 from "@/assets/pin-2.jpg";
import pin3 from "@/assets/pin-3.jpg";
import pin4 from "@/assets/pin-4.jpg";
import pin5 from "@/assets/pin-5.jpg";
import pin6 from "@/assets/pin-6.jpg";

export interface Pin {
  id: string;
  title: string;
  description: string;
  image: string;
  author: string;
  likes: number;
  category: string;
}

export const dummyPins: Pin[] = [
  {
    id: "1",
    title: "Modern Living Room",
    description: "Minimalist living space with warm natural lighting and comfortable furniture",
    image: pin1,
    author: "Sarah Design",
    likes: 234,
    category: "Home & Decor"
  },
  {
    id: "2", 
    title: "Coffee & Pastries",
    description: "Artisanal coffee and fresh pastries for the perfect morning",
    image: pin2,
    author: "Café Lover",
    likes: 189,
    category: "Food & Drink"
  },
  {
    id: "3",
    title: "Mountain Sunset",
    description: "Breathtaking mountain landscape at golden hour",
    image: pin3,
    author: "Nature Photographer",
    likes: 456,
    category: "Nature"
  },
  {
    id: "4",
    title: "Fashion Styling",
    description: "Stylish outfit coordination with modern accessories",
    image: pin4,
    author: "Style Guru",
    likes: 321,
    category: "Fashion"
  },
  {
    id: "5",
    title: "Contemporary Architecture",
    description: "Modern building design with clean geometric lines",
    image: pin5,
    author: "ArchitecturalEye",
    likes: 167,
    category: "Architecture"
  },
  {
    id: "6",
    title: "Botanical Beauty",
    description: "Beautiful flower arrangement with soft natural lighting",
    image: pin6,
    author: "Botanical Artist",
    likes: 298,
    category: "Art & Design"
  }
];