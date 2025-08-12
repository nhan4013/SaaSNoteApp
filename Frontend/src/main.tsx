import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { StyledEngineProvider } from '@mui/material/styles';
import App from './App.tsx'
import SignIn from './components/auth/Login.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <StyledEngineProvider injectFirst>
      <SignIn />
    </StyledEngineProvider>
    
  </StrictMode>,
)
