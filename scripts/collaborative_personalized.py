import pickle

# Collaborative-based Personalized recommendation function
def recommend_collaborative_personalized(user_id, top_n=5):
    # Load files
    with open('PKL_Files/movie_rating_collaborative', 'rb') as file:
        mov_ratings = pickle.load(file)

    with open('PKL_Files/similarity_scores_collaborative', 'rb') as file:
        similarity_scores = pickle.load(file)

    with open('PKL_Files/pivot_table_collaborative', 'rb') as file:
        pt = pickle.load(file)


    # Get the user's ratings from the user-movie rating matrix
    user_ratings = pt[user_id]

    # Create an empty list to store recommended movies
    recommended_movies = []

    for movie_index, similarity in enumerate(similarity_scores):
        item = []

        # Skip movies the user has already rated
        if user_ratings[movie_index] > 0:
            continue

        temp_df = mov_ratings[mov_ratings['title'] == pt.index[movie_index]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))

        d = dict()
        d['title'] = item[0]
        d['url'] = temp_df['Poster URL'].values.tolist()[0]

        recommended_movies.append(d)

    return recommended_movies[:5]