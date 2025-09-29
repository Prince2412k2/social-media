import { Link } from 'react-router-dom';
import { FaHome, FaUser, FaBell } from 'react-icons/fa';
import { MdExplore } from 'react-icons/md';

export default function LeftBar() {
  return (
    <aside className="left-bar">
      <nav className="left-bar-nav">
        <ul>
          <li>
            <Link to="/">
              <FaHome />
              <span>Home</span>
            </Link>
          </li>
          <li>
            <Link to="/explore">
              <MdExplore />
              <span>Explore</span>
            </Link>
          </li>
          <li>
            <Link to="/notifications">
              <FaBell />
              <span>Notifications</span>
            </Link>
          </li>
          <li>
            <Link to="/profile">
              <FaUser />
              <span>Profile</span>
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
