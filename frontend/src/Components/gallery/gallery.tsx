import { Link } from 'react-router-dom';
import Masonry from 'react-masonry-css';

// Function to generate dummy data with random heights and titles
const generateItems = (count = 20) => {
  return Array.from({ length: count }, (_, i) => {
    const height = Math.floor(Math.random() * 400) + 500; // Random height between 500 and 900
    return {
      id: i + 1,
      url: `https://picsum.photos/400/${height}`,
      title: `Awesome Image ${i + 1}`
    };
  });
};

const items = generateItems();

const breakpointColumnsObj = {
  default: 4,
  1100: 3,
  700: 2,
  500: 1
};

export default function Gallery() {
  return (
    <div className="p-4 bg-gray-50 min-h-screen">
      <Masonry
        breakpointCols={breakpointColumnsObj}
        className="masonry-grid"
        columnClassName="masonry-grid_column"
      >
        {items.map(item => (
          <Link to={`/pin/${item.id}`} key={item.id} className="group relative block overflow-hidden cursor-pointer bg-white shadow-md" style={{ borderRadius: '1rem', marginBottom: '1rem' }}>
            <img src={item.url} alt={item.title} className="w-full block" />
            <div className="absolute inset-0 bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            <div className="absolute top-0 right-0 p-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <button className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-3 rounded-full text-sm">
                Save
              </button>
            </div>
            <div className="absolute bottom-0 left-0 p-3 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <h3 className="font-semibold" style={{ textShadow: '1px 1px 4px rgba(0,0,0,0.5)' }}>
                {item.title}
              </h3>
            </div>
          </Link>
        ))}
      </Masonry>
    </div>
  );
}
