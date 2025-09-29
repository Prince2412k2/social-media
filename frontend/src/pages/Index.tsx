import { useState } from "react";
import Header from "@/components/Header";
import MasonryGrid from "@/components/MasonryGrid";
import PinModal from "@/components/PinModal";
import { AppSidebar } from "@/components/AppSidebar";
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { dummyPins, Pin } from "@/data/pins";

const Index = () => {
  const [selectedPin, setSelectedPin] = useState<Pin | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handlePinClick = (pin: Pin) => {
    setSelectedPin(pin);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedPin(null);
  };

  // Duplicate pins to create more content for demo
  const allPins = [...dummyPins, ...dummyPins, ...dummyPins];

  return (
    <SidebarProvider defaultOpen={true}>
      <div className="min-h-screen flex w-full bg-gradient-subtle">
        <AppSidebar />
        
        <SidebarInset className="flex-1">
          <header className="flex h-16 shrink-0 items-center gap-2 border-b border-white/10 px-4">
            <SidebarTrigger className="-ml-1" />
            <div className="flex-1">
              <Header />
            </div>
          </header>
          
          <main className="flex-1 pb-8">
            <MasonryGrid 
              pins={allPins} 
              onPinClick={handlePinClick}
            />
          </main>
        </SidebarInset>

        <PinModal
          pin={selectedPin}
          isOpen={isModalOpen}
          onClose={closeModal}
        />
      </div>
    </SidebarProvider>
  );
};

export default Index;