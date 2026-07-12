import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { UploadProvider } from './context/UploadContext.jsx'
import { SystemProvider } from './context/SystemContext.jsx'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <SystemProvider>
        <UploadProvider>
          <App />
        </UploadProvider>
      </SystemProvider>
    </BrowserRouter>
  </StrictMode>,
)
