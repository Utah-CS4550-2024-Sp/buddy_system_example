import { useState } from "react";

function DeleteColorButton({ onClick }) {
  const style={
    padding: "0px 5px",
    backgroundColor: "transparent",
    color: "black",
    borderRadius: "0px",
  };
  return (
    <button style={style} onClick={onClick}>X</button>
  )
}


function ColorListItem({ color, removeColor }) {
  const style = {
    backgroundColor: color,
    display: "flex",
    justifyContent: "space-between",
    paddingLeft: "10px",
  };
  return (
    <li style={style}>
      {color}
      <DeleteColorButton color={color} onClick={() => removeColor(color)} />
    </li>
  )
}

function ColorList({ colors, removeColor }) {
  const style = {
    paddingLeft: "0px",
    listStyle: "none",
    color: "black",
    fontWeight: "bolder",
  };
  return (
    <ul style={style}>
      {colors.map((color) => (
        <ColorListItem key={color} color={color} removeColor={removeColor} />
      ))}
    </ul>
  )
}

function ColorForm({ addColor }) {
  const onSubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    const color = new FormData(form).get("color");
    addColor(color);
    form.reset();
  };

  return (
    <form onSubmit={onSubmit}>
      <input name="color" type="text" placeholder="color" />
    </form>
  )
}

function ColorsPage() {
  const [colors, setColors] = useState(
    ["magenta", "orange", "lightgreen"],
  );

  const addColor = (color) => {
    if (!colors.includes(color)) {
      setColors([...colors, color]);
    }
  };

  const removeColor = (color) => {
    setColors(colors.filter((c) => c !== color));
  }

  return (
    <>
      <h1>list of colors</h1>
      <ColorList colors={colors} removeColor={removeColor} />
      <h2>add new color</h2>
      <ColorForm addColor={addColor} />
    </>
  );
}

export default ColorsPage;
