# type: ignore
from dotenv import load_dotenv
load_dotenv()
from game_recommender import app

if __name__ == "__main__":
    app.run(debug=True)
