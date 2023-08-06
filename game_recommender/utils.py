from game_recommender.models import Rating

def add_db_users(current_users_df):
    # Add the users from database into the current users dataframe loaded from csv
    df_last_id = current_users_df.index[-1]
    ratings = Rating.query.all()
    if ratings:
        for rating_object in ratings:
            new_user_id = df_last_id + rating_object.user_id
            game_title = rating_object.game.title
            if new_user_id not in current_users_df.index:
                current_users_df.loc[new_user_id] = 0
            current_users_df.at[new_user_id, game_title] = rating_object.rating