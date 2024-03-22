import { useState } from "react";
import { useMutation, useQueryClient } from "react-query";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/auth";
import Button from "./Button";

function Input(props) {
  return (
    <div className="flex flex-col py-2">
      <label className="text-s text-gray-400" htmlFor={props.name}>
        {props.name}
      </label>
      <input
        {...props}
        className="border rounded bg-transparent px-2 py-1"
      />
    </div>
  );
}

function Checkbox(props) {
  return (
    <div className="flex flex-row py-2">
      <input
        {...props}
        className="border rounded bg-transparent px-2 py-1"
        type="checkbox"
      />
      <label className="text-s text-gray-400 ml-4" htmlFor={props.name}>
        {props.name}
      </label>
    </div>
  );
}

function NewAnimalForm() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { token } = useAuth();

  const [name, setName] = useState("");
  const [kind, setKind] = useState("");
  const [age, setAge] = useState(0);
  const [fixed, setFixed] = useState(true);
  const [vaccinated, setVaccinated] = useState(false);

  const mutation = useMutation({
    mutationFn: () => (
      fetch(
        "http://127.0.0.1:8000/animals",
        {
          method: "POST",
          headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
            kind,
            age,
            fixed,
            vaccinated,
          }),
        },
      ).then((response) => response.json())
    ),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["animals"],
      });
      navigate(`/animals/${data.animal.id}`);
      // alternatively, we could "reset" the form
    },
  });

  const onSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <form onSubmit={onSubmit}>
      <Input
        name="name"
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <Input
        name="kind"
        type="text"
        value={kind}
        onChange={(e) => setKind(e.target.value)}
      />
      <Input
        name="age"
        type="number"
        value={age}
        onChange={(e) => setAge(e.target.value)}
      />
      <Checkbox
        name="fixed"
        checked={fixed}
        onChange={(e) => setFixed(!fixed)}
      />
      <Checkbox
        name="vaccinated"
        checked={vaccinated}
        onChange={(e) => setVaccinated(!vaccinated)}
      />
      <Button type="submit">submit</Button>
    </form>
  );
}

function NewAnimal() {
  return (
    <div className="w-96">
      <h2 className="text-center text-2xl font-bold">add new animal</h2>
      <NewAnimalForm />
    </div>
  );
}

export default NewAnimal;
