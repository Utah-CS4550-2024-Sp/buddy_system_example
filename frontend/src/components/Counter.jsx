import { createContext, useContext, useState } from "react";

const buttonClassName = "border rounded px-8 py-4 m-4";

const CounterContext = createContext();

function CounterProvider({ children }) {
  const [count, setCount] = useState(0);

  const reset = () => {
    setCount(0);
  }

  const increment = () => {
    setCount(count + 1);
  }

  const decrement = () => {
    setCount(count - 1);
  }

  return (
    <CounterContext.Provider
      value={{ count, reset, increment, decrement, setCount }}
    >
      {children}
    </CounterContext.Provider>
  );
}

const useCounter = () => useContext(CounterContext);

function CountResetButton() {
  const { reset } = useCounter();

  return (
    <button
      className={buttonClassName + " mx-auto"}
      onClick={reset}
    >
      reset count
    </button>
  );
}

function CountDecrementButton() {
  const { decrement } = useCounter();

  return (
    <button
      className={buttonClassName}
      onClick={decrement}
    >
      count--
    </button>
  );
}

function CountIncrementButton() {
  const { increment } = useCounter();

  return (
    <button
      className={buttonClassName}
      onClick={increment}
    >
      count++
    </button>
  );
}

function CountChangerButtons() {
  return (
    <div className="flex flex-row mx-auto">
      <CountDecrementButton />
      <CountIncrementButton />
    </div>
  );
}

function CountSetterForm() {
  const { setCount } = useCounter();
  const [newCount, setNewCount] = useState(0)

  const onSubmit = (e) => {
    e.preventDefault()
    setCount(newCount);
  }

  return (
    <form
      className={buttonClassName + " flex flex-col mx-auto"}
      onSubmit={onSubmit}
    >
      <label htmlFor="count" className="text-center">count =</label>
      <input
        className="text-black"
        name="count"
        type="number"
        defaultValue={newCount}
        onChange={(e) => setNewCount(e.target.value)}
      />
    </form>
  );
}

function Header() {
  const { count } = useCounter();

  return (
    <h1 className="text-center text-3xl py-4">count: {count}</h1>
  );
}

function Counter() {
  return (
    <CounterProvider>
      <div className="flex flex-col font-mono pt-4">
        <Header />
        <CountResetButton />
        <CountChangerButtons />
        <CountSetterForm />
      </div>
    </CounterProvider>
  );
}

export default Counter;

