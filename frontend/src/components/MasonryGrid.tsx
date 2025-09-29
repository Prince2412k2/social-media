import { useEffect, useRef, useState } from "react";
import PinCard from "./PinCard";
import { Pin } from "@/data/pins";

interface MasonryGridProps {
  pins: Pin[];
  onPinClick?: (pin: Pin) => void;
}

const MasonryGrid = ({ pins, onPinClick }: MasonryGridProps) => {
  const gridRef = useRef<HTMLDivElement>(null);
  const [columns, setColumns] = useState(4);

  // Responsive column calculation
  useEffect(() => {
    const updateColumns = () => {
      const width = window.innerWidth;
      if (width < 640) setColumns(2);
      else if (width < 1024) setColumns(3);
      else if (width < 1536) setColumns(4);
      else setColumns(5);
    };

    updateColumns();
    window.addEventListener('resize', updateColumns);
    return () => window.removeEventListener('resize', updateColumns);
  }, []);

  // Create column arrays
  const columnArrays: Pin[][] = Array.from({ length: columns }, () => []);
  
  // Distribute pins across columns
  pins.forEach((pin, index) => {
    columnArrays[index % columns].push(pin);
  });

  return (
    <div className="container mx-auto px-4 py-8">
      <div 
        ref={gridRef}
        className="grid gap-4"
        style={{
          gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`
        }}
      >
        {columnArrays.map((columnPins, columnIndex) => (
          <div key={columnIndex} className="flex flex-col gap-4">
            {columnPins.map((pin) => (
              <div 
                key={pin.id}
                className="animate-in fade-in-0 slide-in-from-bottom-4 duration-500"
                style={{
                  animationDelay: `${Math.random() * 300}ms`
                }}
              >
                <PinCard 
                  pin={pin} 
                  onClick={() => onPinClick?.(pin)}
                />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MasonryGrid;