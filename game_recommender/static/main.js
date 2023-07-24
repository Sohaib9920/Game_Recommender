

// Unlike python, Global variable in JavaScript can be changed within a function by not explicitly declaring it as a local variable and only reassigning it.
let gameNamesValid = new Set();

// Function to fetch the game names from the route, store them in the global variable and creating the datalist:
async function fetchGameNames() {                                         
  try {
    // fetch JSON data from route (ajax) and then store it
    const response = await fetch("/get_recommended_names");
    const data = await response.json();
    gameNamesValid = new Set(data.recommended_names);

    // Populate the datalist with the recommended names
    const gameNamesList = document.getElementById("gameNameList");
    gameNamesValid.forEach(name => {
      const option = document.createElement("option");
      option.value = name;
      gameNamesList.appendChild(option);
    })

    console.log("Game names Loaded:", gameNamesValid);
  } catch (error) {
    console.error("Falided to fetch games names:", error);
  }
}

fetchGameNames();

// NOTES:
// Use async function to fetch data without blocking the program execution
// await pause the execution until the Promise returned by the asynchronous operation is settled (resolved or rejected).
// response.json() returns a Promise that resolves to the JavaScript object corresponding to the JSON data in the response body.
// If an error occurs during the fetch or JSON parsing, it will be caught in the catch block for error handling.

// Alternative way: 
// 1) Convert python data to json using `json.dumps()`  
// 2) Pass it to html form in `data-game_names` attribute  
// 3) Using Js: select the form element, get value of `data-game_names` attribute and then parse JSON to Js object using `JSON.parse()`


function validateForm() {

  const gameNames = new Set();
  const inputElements = document.querySelectorAll(".game_name");

  // For every input element
  for (let i = 0; i < inputElements.length; i++) {
    // Get game name from the element
    const inputElement = inputElements[i];
    const gameName = inputElement.value.trim();  
    // element.value will give the current value in the element 
    // element.getAttribute("value") gives the initial value set in the HTML attribute.

    // Check if the game name is empty
    if (gameName === "") {
      alert(`Please enter a game name in field ${i}.`);
      inputElement.focus();
      return false;
    }
    
    // Check if the game name is in the set of valid game names
    if (!gameNamesValid.has(gameName)) {
      alert(`Please enter a valid game name in field ${i + 1}.`);
      inputElement.focus();
      return false;
    }
    
    // Check if the game name is already in the set
    if (gameNames.has(gameName)) {
      alert("Please enter different game names in each field.");
      inputElement.focus();
      return false;
    }

    gameNames.add(gameName);
  }
  return true; // Allow form submission if all validations pass
}
