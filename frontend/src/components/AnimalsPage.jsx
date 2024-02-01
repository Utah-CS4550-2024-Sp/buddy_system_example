import { useQuery } from "react-query";

function AnimalsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["animals"],
    queryFn: () => (
      fetch("http://127.0.0.1:8000/animals")
        .then((response) => {
          if (!response.ok) {
            throw Error("api response not OK");
          }
          return response.json()
        })
    ),
  });

  if (error) {
    return <h3>oh no, something happened :(((</h3>
  }

  return (
    <>
      <h1>animals</h1>
      {isLoading ?
        "loading..." :
        <>
          <h3>number of animals: {data.meta.count}</h3>
          <ul>
            {data.animals.map((animal) => (
              <li key={animal.id}>{animal.name}</li>
            ))}
          </ul>
        </>
      }
    </>
  );
}

export default AnimalsPage;