import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, NavLink, Navigate, Routes, Route } from 'react-router-dom';
import Animals from './components/Animals';
import Counter from "./components/Counter";
import LeftNav from "./components/LeftNav";
import TopNav from "./components/TopNav";

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="h-screen max-h-screen max-w-2xl mx-auto bg-gray-700 text-white flex flex-col">
          <header>
            <TopNav />
          </header>
          <main className="max-h-main">
            <Routes>
              <Route path="/" element={<></>} />
              <Route path="/animals" element={<Animals />} />
              <Route path="/animals/:animalId" element={<Animals />} />
              <Route path="/counter" element={<Counter />} />
              <Route path="/error/404" element={<NotFound />} />
              <Route path="*" element={<Navigate to="/error/404" />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App
