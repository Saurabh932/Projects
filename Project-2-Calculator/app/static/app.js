// Selecting the elements
const form = document.querySelector("form");
const select = document.querySelector("select")
const input1 = document.querySelector("input[name='input1']");
const input2 = document.querySelector("input[name='input2']");
const res = document.querySelector("#result-box")


// Function to calculate
// function calcuation(input1, input2, operator){
//     // Converting string to number as input is string
//     num1 = parseFloat(input1);
//     num2 = parseFloat(input2); 

//     if (operator == "+"){
//         return num1 + num2;
//     }
//     else if (operator == "-"){
//         return num1 - num2;
//     }
//     else if (operator == "*"){
//         return num1 * num2;
//     }
//     else if (operator == "/"){
//         return num1 / num2;
//     }
//     else{
//         return "Select a valid  operator";
//     }
// }


// Event listner for form submission
form.addEventListener('submit', async function(e){
    e.preventDefault();

    const num1 = parseInt(input1.value);
    const num2 = parseInt(input2.value);
    const operator = select.value;

    // Fetch API call to Fastapi backend
    const response = await fetch("/api/calculate", {
        method : "POST",
        headers : {
            "Content-Type":"application/json"
        },
        body : JSON.stringify({
            input1 : num1,
            input2 : num2,
            operator : operator,
        })
    })

    const data = await response.json();
    console.log(data)
    res.innerText = "Result: " + data.result; 

    // const result = calcuation(num1, num2, operator);

    // Displaying result in result box;
    // const listItem = document.createElement("h2");
    // listItem.textContent = result;
    // list.appendChild(listItem);

    // res.innerText = result

    // Clearing the input after each calculation
    input1.value = "";
    input2.value = "";
})