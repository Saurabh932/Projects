// Selecting DOM elements
const select = document.querySelector("select")
const resultBox = document.getElementById("result-box");
const form = document.querySelector("form");
const list = document.querySelector("ul")


// Game options
const choices = ["snake", "water", "gun"]


// Function to get computer choice`
function getComputerChoice(){
    const randomIndex = Math.floor(Math.random() * choices.length);
    return choices[randomIndex];
} 


// Function to decide winner
function getWinner(user, computer){
    if (user == computer) return "It's a tie.";

    if ((user === "snake" && computer === "water") ||
        (user === "water" && computer === "gun") ||
        (user === "gun" && computer === "snake")){
            return "You win!!";
    }
    else{
        return "Computer Wins!!";
    }
}


// Event listener for form submission
form.addEventListener("submit", function (e) {
    e.preventDefault();  // Stops form from reloading

    const userChoice = select.value;
    const computerCHoice = getComputerChoice();
    const result = getWinner(userChoice, computerCHoice);

    // Display result in result box;
    resultBox.textContent = `You chose ${userChoice} | Computer chose ${computerCHoice} -> ${result}`;

    // Adding result to list
    const listItem = document.createElement("li");
    listItem.textContent = `User ${userChoice} VS Computer ${computerCHoice} -> ${result}`;
    list.appendChild(listItem);
})