import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Link, Routes, Route } from 'react-router-dom';
import AnimalsPage from './components/AnimalsPage';
import Greeter from './components/Greeter';
import ColorsPage from './components/ColorsPage';
import './App.css'

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <nav className="nav">
          <Link to="/colors">colors</Link>
          <Link to="/greeter">greeter</Link>
          <Link to="/animals">animals</Link>
        </nav>
        <Routes>
          <Route path="/" element={<h1>home</h1>} />
          <Route path="/colors" element={<ColorsPage />} />
          <Route path="/greeter" element={<Greeter />} />
          <Route path="/animals" element={<AnimalsPage />} />
          <Route path="*" element={<h1>not found</h1>} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
