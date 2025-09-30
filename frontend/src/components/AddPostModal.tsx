import { useState, type FormEvent, type ReactElement } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import axios from "@/lib/axios";

interface AddPostModalProps {
  isOpen: boolean;
  onClose: () => void;
  onPostAdd: (newPost: any) => void; // Define a proper type for the new post
}

export default function AddPostModal({ isOpen, onClose, onPostAdd }: AddPostModalProps): ReactElement {
  const [caption, setCaption] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImage(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!image) {
      return;
    }

    const formData = new FormData();
    if (caption) {
      formData.append("caption", caption);
    }
    formData.append("image", image);

    try {
      const response = await axios.post("/api/post", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      onPostAdd(response.data);
      onClose();
    } catch (error) {
      console.error("Failed to create post:", error);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create a new post</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="caption">Caption</Label>
            <Textarea
              id="caption"
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              rows={3}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="image">Image</Label>
            <Input
              id="image"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
            />
          </div>
          {imagePreview && (
            <div className="flex justify-center">
              <img src={imagePreview} alt="Image preview" className="max-h-64 rounded-lg" />
            </div>
          )}
          <Button type="submit" className="w-full">
            Create Post
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}
