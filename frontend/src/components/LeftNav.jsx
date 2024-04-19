import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useQuery } from "react-query";
import { useApi } from "../hooks";

const emptyAnimal = (id) => ({
  id,
  name: "loading...",
  empty: true,
});

function Link({ animal }) {
  const url = animal.empty ? "#" : `/animals/${animal.id}`;
  const className = ({ isActive }) => [
    "p-2",
    "hover:bg-slate-800 hover:text-grn",
    "flex flex-row justify-between",
    isActive ?
      "bg-slate-800 text-grn font-bold" :
      ""
  ].join(" ");

  const animalName = ({ isActive }) => (
    (isActive ? "\u00bb " : "") + animal.name
  );

  return (
    <NavLink to={url} className={className}>
      {animalName}
    </NavLink>
  );
}

function LeftNav() {
  const [search, setSearch] = useState("");
  const api = useApi();

  const { data } = useQuery({
    queryKey: ["animals"],
    queryFn: () => (
      api.get("/animals")
        .then((response) => response.json())
    ),
  });

  const regex = new RegExp(".*" + search + ".*");

  const animals = ( data?.animals || [1, 2, 3].map(emptyAnimal)
  ).filter((animal) => (
    search === "" || regex.test(animal.name)
  ));

  return (
    <nav className="flex flex-col border-r-2 border-purple-400 h-main">
      <div className="flex flex-col overflow-y-scroll border-b-2 border-purple-400">
        {animals.map((animal) => (
          <Link key={animal.id} animal={animal} />
        ))}
      </div>
      <div className="p-2">
        <input
          className="w-36 px-4 py-2 bg-gray-700 border border-gray-500"
          type="text"
          placeholder="search"
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
    </nav>
  );
}

export default LeftNav;
