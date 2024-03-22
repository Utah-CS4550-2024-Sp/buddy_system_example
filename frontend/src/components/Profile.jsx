import { useEffect, useState } from "react";
import { useAuth } from "../context/auth";
import { useUser } from "../context/user";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
  const { logout } = useAuth();
  const user = useUser();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [readOnly, setReadOnly] = useState(true);

  const reset = () => {
    if (user) {
      setUsername(user.username);
      setEmail(user.email);
    }
  }

  useEffect(reset, [user]);

  const onSubmit = (e) => {
    e.preventDefault();
    console.log("username: " + username);
    console.log("email: " + email);
    setReadOnly(true);
  }

  const onClick = () => {
    setReadOnly(!readOnly);
    reset();
  };

  return (
    <div className="max-w-96 mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold py-2">
        details
      </h2>
      <form className="border rounded px-4 py-2" onSubmit={onSubmit}>
        <FormInput
          name="username"
          type="text"
          value={username}
          readOnly={readOnly}
          setter={setUsername}
        />
        <FormInput
          name="email"
          type="email"
          value={email}
          readOnly={readOnly}
          setter={setEmail}
        />
        {!readOnly &&
          <Button className="mr-8" type="submit">
            update
          </Button>
        }
        <Button type="button" onClick={onClick}>
          {readOnly ? "edit" : "cancel"}
        </Button>
      </form>
      <Button onClick={logout}>
        logout
      </Button>
    </div>
  );
}

export default Profile;

