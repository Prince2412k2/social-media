import { Routes, Route, Outlet } from 'react-router-dom';
import './App.css';
import Gallery from './Components/gallery/gallery';
import TopBar from './Components/topBar/topBar';
import PinPage from './Components/pinPage/PinPage';

import LeftBar from './Components/leftBar/leftBar';

// Simple placeholder components for Login and Signup
const Login = () => <div className="text-center p-8">Login Page</div>;
const Signup = () => <div className="text-center p-8">Signup Page</div>;

const AppLayout = () => (
  <div className="app">
    <LeftBar />
    <div className="content-with-sidebar">
      <TopBar />
      <main className="content">
        <Outlet /> 
      </main>
    </div>
  </div>
);

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppLayout />}>
        <Route index element={<Gallery />} />
        <Route path="login" element={<Login />} />
        <Route path="signup" element={<Signup />} />
        <Route path="pin/:id" element={<PinPage />} />
      </Route>
    </Routes>
  );
}

export default App;
