// Selecting the elements
const form = document.querySelector("form");
const select = document.querySelector("select")
const input1 = document.querySelector("input[name='input1']");
const input2 = document.querySelector("input[name='input2']");
const list = document.querySelector("ul")


// Function to calculate
function calcuation(input1, input2, operator){
    // Converting string to number as input is string
    num1 = parseFloat(input1);
    num2 = parseFloat(input2); 

    if (operator == "+"){
        return num1 + num2;
    }
    else if (operator == "-"){
        return num1 - num2;
    }
    else if (operator == "*"){
        return num1 * num2;
    }
    else if (operator == "/"){
        return num1 / num2;
    }
    else{
        return "Select a valid  operator";
    }
}


// Event listner for form submission
form.addEventListener('submit', function(e){
    e.preventDefault();

    const num1 = input1.value;
    const num2 = input2.value;
    const operator = select.value;
    const result = calcuation(num1, num2, operator);

    // Displaying result in result box;
    const listItem = document.createElement("li");
    listItem.textContent = result;
    list.appendChild(listItem);

    // Clearing the input after each calculation
    input1.value = "";
    input2.value = "";
})