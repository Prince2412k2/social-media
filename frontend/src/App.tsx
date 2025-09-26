import './App.css'
import Login from './Components/Login'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Redirect from './Components/Redirect';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/auth/callback" element={<Redirect />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
