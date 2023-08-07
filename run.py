# type: ignore
from dotenv import load_dotenv
from game_recommender import app

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
