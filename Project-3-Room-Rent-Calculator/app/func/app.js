const form = document.querySelector("form")
const room = document.getElementById("room-rent")
const food = document.getElementById("food-req")
const wifi = document.getElementById("wifi-charge")
const elec = document.getElementById("elec")
const noPerson = document.getElementById("persons")
const container = document.querySelector(".container")


function rentCalculation(room, food, wifi, elec, noPerson){

    room1 = parseFloat(room);
    food1 = parseFloat(food);
    wifi1 = parseFloat(wifi);
    elec1 = parseFloat(elec);
    noPerson1 = parseFloat(noPerson)

    let result = (room1+food1+wifi1+elec1)/noPerson1;

    return result;
}

form.addEventListener("submit", function(e){
    e.preventDefault();

    const room1 = room.value;
    const food1 = food.value;
    const wifi1 = wifi.value;
    const elec1 = elec.value;
    const noPerson1 = noPerson.value;

    const result = rentCalculation(room1, food1, wifi1, elec1, noPerson1);

    // Removing the previous result
    container.textContent = "";

    const listItem = document.createElement("h2");
    listItem.innerText = result;
    container.appendChild(listItem);

    // Clearing the input values
    room.value = "";
    food.value = "";
    wifi.value = "";
    elec.value = "";
    noPerson.value = "";
})