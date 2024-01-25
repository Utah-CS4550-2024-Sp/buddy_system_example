function addColorToList(color) {
    const list = document.getElementById("color-list");
    const listItem = document.createElement("li");
    const text = document.createTextNode(color);
    listItem.append(text);
    // listItem.style = "background-color: " + color + ";"
    listItem.style = `background-color: ${color};`;
    list.appendChild(listItem);
}

function handleSubmitNewColor(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    addColorToList(formData.get("color"));
    form.reset();
}

document.addEventListener("DOMContentLoaded", function() {
    ["magenta", "orange", "lightgreen", "lightgray"].forEach(addColorToList);
});

document
    .getElementById("color-form")
    .addEventListener("submit", handleSubmitNewColor);
