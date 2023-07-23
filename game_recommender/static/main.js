$(function() {
    // Fetch the recommended game names from the server
    $.ajax({
    url: '/get_recommended_names',
    type: 'GET',
    success: function(response) {
        // Initialize the autocomplete input field with the recommended names
        $('.game_name').autocomplete({
        source: response.recommended_names
        });
    }
    });
});


function validateForm() {

  const gameNames = new Set();
  const inputElements = document.querySelectorAll(".game_name");
  const gameNamesJson = document.querySelector("#game_form").getAttribute("data-game-names");
  const gameNamesValid = new Set(JSON.parse(gameNamesJson));

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
