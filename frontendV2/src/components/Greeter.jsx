import { useState } from "react";
import './Greeter.css'

function IncreaseExcitementButton({ onClick }) {
  return <button
    onClick={onClick}
    className="change-excitement-button happy-face"
  >
    :)
  </button>
}

function DecreaseExcitementButton({ onClick }) {
  return <button
    onClick={onClick}
    className="change-excitement-button sad-face"
  >
    :(
  </button>
}

function NameInput({ setName }) {
  return (
    <form>
      <input
        type="text"
        onChange={(e) => setName(e.target.value)}
        placeholder="name"
      />
    </form>
  );
}

function Greeter() {
  const [name, setName] = useState("world");
  const [excitement, setExcitement] = useState(0);

  const punctuation = excitement >= 0 ? "!" : ".";

  const increaseExcitement = () => {
    setExcitement(excitement + 1);
  }

  const decreaseExcitement = () => {
    setExcitement(excitement - 1);
  }

  return (
    <>
      <h1>hello {name}{punctuation.repeat(Math.abs(excitement))}</h1>
      <NameInput setName={setName} />
      <IncreaseExcitementButton onClick={increaseExcitement} />
      <DecreaseExcitementButton onClick={decreaseExcitement} />
    </>
  )
}

export default Greeter
