import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import AuthContext from './context/authContext.jsx';
import LocationContext from './context/locationContext.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthContext>
      <LocationContext>
        <App />
      </LocationContext>
    </AuthContext>
  </StrictMode>,
)
