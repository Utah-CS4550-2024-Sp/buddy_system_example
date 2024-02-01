import { useQuery } from "react-query";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import "./AnimalsPage.css";

function AnimalPreview({ animal }) {
  return (
    <Link className="animal-preview" to={`/animals/${animal.id}`}>
      <div className="animal-name">{animal.name}</div>
      <div className="animal-detail">{animal.kind}</div>
      <div className="animal-detail">{animal.age}</div>
    </Link>
  );
}

function AnimalCardWrapper() {
  const { animalId } = useParams();
  if (!animalId) {
    return <AnimalCard animal={{}} />
  }

  const navigate = useNavigate();
  const { data, isLoading } = useQuery({
    queryKey: ["animals", animalId],
    queryFn: () => (
      fetch(`http://127.0.0.1:8000/animals/${animalId}`)
        .then((response) => {
          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()
        })
    ),
  });

  if (isLoading) {
    return <AnimalCard animal={{}} />;
  }

  if (data?.animal) {
    return <AnimalCard animal={data.animal} />;
  }

  return <Navigate to="/error" />;
}

function AnimalCard({ animal }) {
  return (
    <div className="animal-card">
      <h2 className="animal-card-title">{animal.name || "name"}</h2>
      <hr />
      {["kind", "age", "intake_date", "fixed", "vaccinated"].map((attr) => (
        <div key={attr} className="animal-card-row">
          <div className="animal-detail-category">{attr}</div>
          <div className="animal-detail-value">
            {(animal || {})[attr]?.toString() || attr}
          </div>
        </div>
      ))}
    </div>
  );
}

function EmptyAnimalList() {
  return <AnimalList animals={[0, 1, 2, 3, 4].map(() => ({
    name: "loading...",
    kind: "kind",
    age: "age",
  }))} />
}

function AnimalList({ animals }) {
  return (
    <div className="animal-list">
      {animals.map((animal) => (
        <AnimalPreview key={animal.id} animal={animal} />
      ))}
    </div>
  );
}

function AnimalsPage() {
  const navigate = useNavigate();
  const { data, isLoading, error } = useQuery({
    queryKey: ["animals"],
    queryFn: () => (
      fetch("http://127.0.0.1:8000/animals")
        .then((response) => {
          if (!response.ok) {
            response.status === 404 ?
              navigate("/error/404") :
              navigate("/error");
          }
          return response.json()
        })
    ),
  });

  if (error) {
    return <Navigate to="/error" />
  }

  return (
    <>
      <h1>animals</h1>
      <div className="animals-page">
        {!isLoading && data?.animals ?
          <AnimalList animals={data.animals} /> :
          <EmptyAnimalList />
        }
        <AnimalCardWrapper />
      </div>
    </>
  );
}

export default AnimalsPage;