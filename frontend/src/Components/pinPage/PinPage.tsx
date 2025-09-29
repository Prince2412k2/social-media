import { useParams } from 'react-router-dom';

export default function PinPage() {
  const { id } = useParams();

  // In a real app, you would fetch the pin data based on the id
  const pin = {
    title: "Awesome Image Title",
    description: "This is a detailed description of the awesome image. It can be a few sentences long, giving more context to the user.",
    imageUrl: `https://picsum.photos/seed/${id}/600/800`
  }

  return (
    <div className="pin-detail-layout">
      <div className="pin-page-container">
        <div className="pin-page-left">
          <img src={pin.imageUrl} alt={pin.title} />
        </div>
        <div className="pin-page-right">
          <h1 style={{fontSize: '2.25rem', fontWeight: 'bold'}}>{pin.title}</h1>
          <p style={{marginTop: '1rem', color: '#4a5568'}}>{pin.description}</p>
          {/* Other pin details like Save button, etc. would go here */}
        </div>
      </div>

      <div className="comments-section">
        <h2 style={{fontSize: '1.5rem', fontWeight: 'bold'}}>Comments</h2>
        
        <div style={{marginTop: '1rem'}}>
          {/* Comments would be mapped here */}
          <div className="comment">
            <p style={{fontWeight: 'bold'}}>User1</p>
            <p>This is a great pin!</p>
          </div>
          <div className="comment">
            <p style={{fontWeight: 'bold'}}>User2</p>
            <p>I love this!</p>
          </div>
        </div>

        <form className="comment-form">
          <input type="text" placeholder="Add a comment" className="comment-input" />
          <button type="submit" className="comment-button">
            Post
          </button>
        </form>
      </div>
    </div>
  );
}
