

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


// Extract the counter from id of last present input field and increment it to create counter for id of new input field
let counter = 0;
const lastChild = document.querySelector("#present div:last-child"); // Select div element which has last-child property
if (lastChild) {
  counter = Number((lastChild.id).split("-")[1]) + 1;
}

// Add new input field in div with 'new' id while updating the counter
function addGame() {
  const newDiv = document.querySelector("#new");

  // <div class="mb-3" id="counter">
  const mainDiv = document.createElement("div");
  mainDiv.className = "mb-3";
  mainDiv.id = `input-${counter}`;

  // Create input field for game name
  const gameInputField = document.createElement("input");
  gameInputField.type = "text";
  gameInputField.name = `games-${counter}`;
  gameInputField.className = "game_name form-control";
  gameInputField.setAttribute("list", "gameNameList"); // list is non-standard attribute so .list do not work
  gameInputField.placeholder = "Game Name";
  gameInputField.required = true;

  // Create input field for rating value
  const ratingInputField = document.createElement("input");
  ratingInputField.type = "number";
  ratingInputField.name = `ratings-${counter}`;
  ratingInputField.className = "form-control mt-1";
  ratingInputField.min = "0";
  ratingInputField.max = "10";
  ratingInputField.placeholder = "Rating (0-10)";
  ratingInputField.required = true;

  // Create input field for delete button
  const deleteButton = document.createElement("input");
  deleteButton.type = "button";
  deleteButton.className = "btn btn-danger btn-sm mt-1";
  deleteButton.value = "Delete";
  deleteButton.setAttribute("onclick",`deleteGame('input-${counter}')`);


  newDiv.appendChild(mainDiv);
  mainDiv.appendChild(gameInputField);
  mainDiv.appendChild(ratingInputField);
  mainDiv.appendChild(deleteButton);

  // Increment counter for next game field
  counter ++;
}


function deleteGame(id) {
  const divToDelete = document.getElementById(id);
  divToDelete.remove();
}