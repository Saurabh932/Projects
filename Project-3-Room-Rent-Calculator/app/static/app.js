const form = document.querySelector("form")
const room = document.getElementById("room-rent")
const food = document.getElementById("food-req")
const wifi = document.getElementById("wifi-charge")
const elec = document.getElementById("elec")
const noPerson = document.getElementById("persons")
const container = document.querySelector(".container")


// function rentCalculation(room, food, wifi, elec, noPerson){

//     room1 = parseFloat(room);
//     food1 = parseFloat(food);
//     wifi1 = parseFloat(wifi);
//     elec1 = parseFloat(elec);
//     noPerson1 = parseFloat(noPerson);

//     let result = (room1+food1+wifi1+elec1)/noPerson1;

//     return result;
// }

form.addEventListener("submit", async function(e){
    e.preventDefault();

    const room1 = parseInt(room.value);
    const food1 = parseInt(food.value);
    const wifi1 = parseInt(wifi.value);
    const elec1 = parseInt(elec.value);
    const noPerson1 = parseInt(noPerson.value);
    
    // Check for NaN/invalid input (a good practice)
    if (isNaN(room1) || isNaN(food1) || isNaN(wifi1) || isNaN(elec1) || isNaN(noPerson1)) {
        container.innerText = "Please fill in all fields with valid numbers.";
        return;
    }

    // Fetch API call to FastAPI backend
    const response = await fetch("/api/expense" , {
        method:"POST",
        headers : {
            "Content-Type" : "application/json",
        },
        body : JSON.stringify({
            room_rent : room1,
            food : food1,
            wifi : wifi1,
            electricity : elec1,
            no_person : noPerson1
        })
    })

    const rent = await response.json()
    console.log(rent)

    // const result = rentCalculation(room1, food1, wifi1, elec1, noPerson1);

    // Removing the previous result
    container.textContent = "";
    
    // Displaying the new result
    const resultDisplay = document.createElement("h2");
    resultDisplay.innerText = rent.result;
    container.appendChild(resultDisplay);

    // Clearing the input values
    room.value = "";
    food.value = "";
    wifi.value = "";
    elec.value = "";
    noPerson.value = "";
})