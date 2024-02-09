import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import "./Animals.css";

function AnimalListItem({ animal }) {
  return (
    <Link key={animal.id} to={`/animals/${animal.id}`} className="animal-list-item">
      <div className="animal-list-item-name">
        {animal.name}
      </div>
      <div className="animal-list-item-detail">
        {animal.kind}
      </div>
      <div className="animal-list-item-detail">
        {animal.age}
      </div>
    </Link>
  )
}

function AnimalList({ animals }) {
  return (
    <div className="animal-list">
      {animals.map((animal) => (
        <AnimalListItem key={animal.id} animal={animal} />
      ))}
    </div>
  )
}

function AnimalCard({ animal }) {
  const attributes = [
    "kind",
    "age",
    "intake_date",
    "fixed",
    "vaccinated",
  ];

  return (
    <div className="animal-card">
      {attributes.map((attr) => (
        <div key={attr} className="animal-card-attr">
          {attr}: {animal[attr].toString()}
        </div>
      ))}
    </div>
  )
}

function AnimalCardContainer({ animal }) {
  return (
    <div className="animal-card-container">
      <h2>{animal.name}</h2>
      <AnimalCard animal={animal} />
    </div>
  );
}

function AnimalListContainer() {
  const { data } = useQuery({
    queryKey: ["animals"],
    queryFn: () => (
      fetch("http://127.0.0.1:8000/animals")
        .then((response) => response.json())
    ),
  });

  if (data?.animals) {
    return (
      <div className="animal-list-container">
        <h2>animals</h2>
        <AnimalList animals={data.animals} />
      </div>
    )
  }

  return (
    <h2>animal list</h2>
  );
}

function AnimalCardQueryContainer({ animalId }) {
  const { data } = useQuery({
    queryKey: ["animals", animalId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/animals/${animalId}`)
        .then((response) => response.json())
    ),
  });

  if (data && data.animal) {
    return <AnimalCardContainer animal={data.animal} />
  }

  return <h2>loading...</h2>
}

function Animals() {
  const { animalId } = useParams();
  return (
    <div className="animals-page">
      <AnimalListContainer />
      {animalId ? <AnimalCardQueryContainer animalId={animalId} /> : <h2>pick an animal</h2>}
    </div>
  );
}

export default Animals;
