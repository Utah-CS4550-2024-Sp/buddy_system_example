import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Navigate, Routes, Route } from 'react-router-dom';
import Animals from './components/Animals';
import './App.css'

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Animals />} />
          <Route path="/animals" element={<Animals />} />
          <Route path="/animals/:animalId" element={<Animals />} />
          <Route path="/error/404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/error/404" />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
