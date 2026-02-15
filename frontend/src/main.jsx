import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter, Routes, Route } from "react-router";
import Environment from './pages/Environment.jsx';
import Agent from './pages/Agent.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />

        <Route path="/environment" element={<Environment />} />
        <Route path='/agent' element={<Agent />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
