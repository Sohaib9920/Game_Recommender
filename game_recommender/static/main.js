// SCROLL REVEAL

// Initialize ScrollReveal
const sr = ScrollReveal({
  reset: true,
  distance: "80px",
  duration: 2000,
  delay: 10,
});

// Apply individual reveal effects
sr.reveal(".sr-slide-left", { origin: "left" });
sr.reveal(".sr-slide-right", { origin: "right" });
sr.reveal(".sr-slide-top", { origin: "top" });
sr.reveal(".sr-slide-bottom", { origin: "bottom" });
sr.reveal(".sr-fade", { origin: "bottom", distance: "0px", delay: 500});

sr.reveal(".sr-slide-left-noreset", { origin: "left", reset: false});
sr.reveal(".sr-slide-right-noreset", { origin: "right", reset: false});
sr.reveal(".sr-fade-noreset", { origin: "bottom", distance: "0px", delay: 500, reset: false});


/// WE REQUIRE DATA OF VALID GAME NAMES FOR FORM VALIDATION AS WELL AS DATALIST IN TEMPELATE FOR VALID NAMES RECOMMENDATIONS.
/// IT CAN BE DONE IN TWO WAYS:
/// 1) Use fetch API to get game_names from a route (AJAX) and then use it to create datalist using JS
///                                              OR
/// 2) Extracting game names from <option> values in already created datalist. To create datalist:
///    Pass game_names list to tempelate then iterate through the list to create a <option> tag inside datalist for each name

/// Method 2 is very good but I will use method 1 in order to learn AJAX, async, await, promises

// Using method 1:

// Declare gameNamesValid as a global variable
let gameNamesValid = null;

async function fetchGameNames() {
  try {
    // fetch JSON data from route (ajax) and then store it
    const response = await fetch("/get_recommended_names");
    const data = await response.json();
    gameNamesValid = new Set(data.recommended_names);
    console.log("Game names Loaded:", gameNamesValid);
    // Call the function to populate the datalist after the data is fetched
    populateDatalist(gameNamesValid);
  } catch (error) {
    console.error("Failed to fetch games names:", error);
  }
}

function populateDatalist(recommendedNames) {
  const dataList = document.getElementById("gameNameList");
  recommendedNames.forEach((name) => {
    const option = document.createElement("option");
    option.value = name;
    dataList.appendChild(option);
  });
}

// Function to only execute fetchGameNames() only when needed
function fetchGamesifNeeded() {
  const currentUrlPath = window.location.pathname;
  // home route '/' has two templates to render but we only have to fetch for recommender template
  const tempelate = document.querySelector("#main").getAttribute("data-template");
  if ((currentUrlPath === "/" && tempelate === "recommender") || currentUrlPath === "/profile") {
    fetchGameNames();
  }
}

// Call the function to fetch the data if needed
fetchGamesifNeeded();

// LEARNING NOTES:
// Use async function to fetch data without blocking the program execution
// await pause the execution until the Promise returned by the asynchronous operation is settled (resolved or rejected).
// response.json() returns a Promise that resolves to the JavaScript object corresponding to the JSON data in the response body.
// If an error occurs during the fetch or JSON parsing, it will be caught in the catch block for error handling.


// Using method 2:

// // Extract game names form datalist, assuming it has been created in tempelate
// function ExtractGameNames() {
//   const optionList = document.querySelectorAll("option");
//   optionList.forEach(option => {
//     gameNamesValid.add(option.value);
//   })
// }

// const gameNamesValid = ExtractGameNames()


/// VALIDATION FUNCTION TO AVOID EMPTY, INVALID AND DUPLICATED GAME NAMES ///

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


/// ADDING AND DELETING THE GAME INPUT FIELDS

// Extract the counter from id of last present input field and increment it to create counter for id of new input field
// counter should be global in order to keep using and updating it with addGame() function calls

let counter = 0;
const lastChild = document.querySelector("#present div:last-child"); // Select div element which has last-child property
if (lastChild) {
  counter = Number(lastChild.id.split("-")[1]) + 1;
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
  gameInputField.autocomplete="off"

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
  deleteButton.setAttribute("onclick", `deleteGame('input-${counter}')`);

  newDiv.appendChild(mainDiv);
  mainDiv.appendChild(gameInputField);
  mainDiv.appendChild(ratingInputField);
  mainDiv.appendChild(deleteButton);

  // Increment counter for next game field
  counter++;
}

// delete input element using its id
function deleteGame(id) {
  const divToDelete = document.getElementById(id);
  divToDelete.remove();
}
