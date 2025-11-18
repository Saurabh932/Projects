const form = document.querySelector("#feedback-form");
const nameInput = document.querySelector("#name");
const emailInput = document.querySelector("#email");
const desInput = document.querySelector("#des");
const ul = document.querySelector(".feed-list");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const user = nameInput.value;
    const contact = emailInput.value;
    const description = desInput.value;

    let response = await fetch("/api/feedback", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: user,
            email: contact,
            des: description
        })
    });

    const feed = await response.json();

    const li = document.createElement("li");
    li.innerText = `${feed.name} - ${feed.email}: ${feed.description}`;
    ul.appendChild(li);

    nameInput.value = "";
    emailInput.value = "";
    desInput.value = "";
});
