import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, NavLink, Navigate, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from "./context/auth";
import Animals from './components/Animals';
import Counter from "./components/Counter";
import LeftNav from "./components/LeftNav";
import Login from "./components/Login";
import TopNav from "./components/TopNav";

const queryClient = new QueryClient();

function NotFound() {
  return <h1>404: not found</h1>;
}

function Home() {
  const { isLoggedIn, logout } = useAuth();

  return (
    <div className="max-w-4/5 mx-auto text-center px-4 py-8">
      <div className="py-2">
        logged in: {isLoggedIn.toString()}
      </div>
      {isLoggedIn &&
        <button
          className="my-2 p-2 border rounded hover:bg-slate-800"
          onClick={logout}
        >
          logout
        </button>
      }
    </div>
  );
}

function Header() {
  return (
    <header>
      <TopNav />
    </header>
  );
}

function Main() {
  return (
    <main className="max-h-main">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/animals" element={<Animals />} />
        <Route path="/animals/:animalId" element={<Animals />} />
        <Route path="/counter" element={<Counter />} />
        <Route path="/login" element={<Login />} />
        <Route path="/error/404" element={<NotFound />} />
        <Route path="*" element={<Navigate to="/error/404" />} />
      </Routes>
    </main>
  );
}

function App() {
  const className = [
    "h-screen max-h-screen",
    "max-w-2xl mx-auto",
    "bg-gray-700 text-white",
    "flex flex-col",
  ].join(" ");

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <div className={className}>
            <Header />
            <Main />
          </div>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App

