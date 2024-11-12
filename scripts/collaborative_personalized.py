import pickle

def recommend_collaborative_personalized(user_id, top_n):
    try:
        with open('PKL_Files/movie_rating_collaborative', 'rb') as file:
            mov_ratings = pickle.load(file)

        with open('PKL_Files/similarity_scores_collaborative', 'rb') as file:
            similarity_scores = pickle.load(file)

        with open('PKL_Files/pivot_table_collaborative', 'rb') as file:
            pt = pickle.load(file)
            
        
        # Ensure user_id is an integer
        user_id = int(user_id) 
        
        # Check if the user_id exists in the pivot table
        if user_id not in pt.columns:
            
            return f"User ID {user_id} not found in the systemm."

        user_ratings = pt[user_id]
        
        if len(user_ratings) != len(pt.index):
            return "Error: Mismatch between user ratings and movie indices."


        recommended_movies = []

        for movie_index, similarity in enumerate(similarity_scores):
            if user_ratings.iloc[movie_index] > 0:
                continue

            temp_df = mov_ratings[mov_ratings['title'] == pt.index[movie_index]]

            # Ensure there's valid movie data
            if temp_df.empty:
                continue

            # Prepare the movie dictionary
            item = temp_df.drop_duplicates('title')['title'].values
            if len(item) > 0:
                movie_title = item[0]
                movie_poster_url = temp_df['Poster URL'].values[0] if 'Poster URL' in temp_df.columns else None

                recommended_movies.append({
                    'title': movie_title,
                    'url': movie_poster_url,
                })

        # Return top_n recommendations
        return recommended_movies[:top_n]

    except FileNotFoundError as e:
        return f"Error: {e}"
    except KeyError as e:
        return f"Error: {e} key not found in the dataset"
