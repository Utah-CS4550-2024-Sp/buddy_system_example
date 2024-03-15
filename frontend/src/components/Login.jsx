import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/auth";

function Error({ message }) {
  if (message === "") {
    return <></>;
  }
  return (
    <div className="text-red-300 text-xs">
      {message}
    </div>
  );
}

function SubmitButton({ disabled }) {
  const className = [
    "rounded px-4 py-2 my-4",
    disabled ?
      "bg-lgrn text-slate-400 italic" :
      "border border-lgrn bg-transparent hover:bg-slate-800"
  ].join(" ");
  return (
    <button className={className} type="submit" disabled={disabled}>
      submit
    </button>
  );
}

function Input({ type, name, setter }) {
  return (
    <div className="flex flex-col py-2">
      <label htmlFor={name}>{name}</label>
      <input
        name={name}
        type={type}
        className="border rounded bg-transparent px-4 py-2"
        onChange={(e) => setter(e.target.value)}
      />
    </div>
  );
}

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const { login } = useAuth();

  const disabled = username === "" || password === "";

  const onSubmit = (e) => {
    e.preventDefault();

    fetch(
      "http://127.0.0.1:8000/auth/token",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ username, password }),
      },
    ).then((response) => {
      if (response.ok) {
        response.json().then(login);
        navigate("/");
      } else if (response.status === 401) {
        response.json().then((data) => {
          setError(data.detail.error_description);
        });
      } else {
        setError("error logging in");
      }
    });
  }

  return (
    <form className="max-w-64 mx-auto py-8 px-4" onSubmit={onSubmit}>
      <Input type="text" name="username" setter={setUsername} />
      <Input type="password" name="password" setter={setPassword} />
      <SubmitButton disabled={disabled} />
      <Error message={error} />
    </form>
  );
}

export default Login;

