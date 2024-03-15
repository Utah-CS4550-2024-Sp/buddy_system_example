import { NavLink } from "react-router-dom";

function NavItem({ to, name, right }) {
  const className = [
    "border-purple-400",
    "py-2 px-4",
    "hover:bg-gray-500",
    right ? "border-l-2" : "border-r-2"
  ].join(" ")

  const getClassName = ({ isActive }) => (
    isActive ? className + " bg-gray-500" : className
  );

  return (
    <NavLink to={to} className={getClassName}>
      {name}
    </NavLink>
  );
}

function TopNav() {
  return (
    <nav className="flex flex-row border-b-4 border-purple-400">
      <NavItem to="/" name="home" />
      <NavItem to="/animals" name="animals" />
      <NavItem to="/counter" name="counter" />
      <div className="flex-1" />
      <NavItem to="/login" name="login" right />
    </nav>
  );
}

export default TopNav;
