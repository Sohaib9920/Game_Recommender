# Game_Recommender
Game Recommender is a web application that helps users discover new games based on their preferences. 
It utilizes Matrix Factorization as a recommendation engine and uses user data from the Steam platform. 
The application asks users to provide their three favorite games along with ratings, and based on this input, it recommends five games that the user might enjoy.

![Recommender](./Recommender.JPG)

![Recommendations](./Recommendations.JPG)

## Specification

The recommendation engine in Game Recommender is built using Matrix Factorization. 
The [Steam user data](https://www.kaggle.com/datasets/tamber/steam-video-games) is processed to create a user-by-item matrix called ubyi_norm_0.csv. 
The model is trained on this dataset using 80 latent factors/features and a regularization factor of 0.01.

For a detailed explanation of how matrix factorization works, information about the ubyi_norm_0 dataset, and details about the model, please refer to the app.py file.
  
## Usage

To use the Game Recommender, follow the steps below after changing the current directory to the Game_Recommender directory.
Start with the fourth step, and if it gives any errors, proceed with all the steps as given.

1. Create a virtual environment:
  ```
  python -m venv game_rec
  ```
2. Activate the virtual environment (for using Git Bash on Windows):
  ```bash
  source game_rec/Scripts/activate
  ```
3. Install the project requirements:
  ```
  pip install -r requirements.txt
  ```
4. Run app using local server:
  ```
  python app.py
  ```

