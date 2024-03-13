import { NavLink } from "react-router-dom";

function TopNav() {
  const linkClass = [
    "border-r-2 border-purple-400",
    "py-2 px-4",
    "hover:bg-gray-500",
  ].join(" ")

  const getLinkClass = ({ isActive }) => (
    isActive ? linkClass + " bg-gray-500" : linkClass
  );

  return (
    <nav className="flex flex-row border-b-4 border-purple-400">
      <NavLink to="/" className={getLinkClass}>
        home
      </NavLink>
      <NavLink to="/animals" className={getLinkClass}>
        animals
      </NavLink>
      <NavLink to="/counter" className={getLinkClass}>
        counter
      </NavLink>
    </nav>
  );
}

export default TopNav;
