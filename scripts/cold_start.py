import numpy as np
import pickle
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

def recommend_based_on_favorites(favorite_movies, n_outputs=10):
    # Load the preprocessed DataFrame and movie vectors
    with open('PKL_Files/stemmed_df_content_based', 'rb') as file:
        new_df = pickle.load(file)

    with open('PKL_Files/movie_vectors_content_based', 'rb') as file:
        titles, vectors = pickle.load(file)

    # Convert vectors to a NumPy array (if not already)
    vectors = np.array(vectors)

    # Initialize cumulative similarity scores
    cumulative_similarity = np.zeros(len(new_df))

    # Loop through each favorite movie and calculate similarity
    for movie in favorite_movies:
        movie_index = new_df[new_df['title'].str.lower() == movie.lower()].index

        if len(movie_index) > 0:
            movie_index = movie_index[0]  # Get the first index
            similarity = cosine_similarity(vectors[movie_index].reshape(1, -1), vectors)[0]  # Ensure 2D shape
            cumulative_similarity += similarity
        else:
            st.info(f"We don't have enough information to recommend movies related to '{movie.title()}' at the moment, but you can explore other popular titles in our database.")
    
    # Sort movies based on the cumulative similarity scores
    similar_movies = sorted(list(enumerate(cumulative_similarity)), key=lambda x: x[1], reverse=True)

    # Prepare the recommended movies as a list of dictionaries
    mov_list = []
    for i in similar_movies:
        movie_title = new_df.iloc[i[0]]['title']
        if movie_title.lower() not in [movie.lower() for movie in favorite_movies]:
            d = {
                'title': movie_title,
                'url': new_df.iloc[i[0]]['Poster URL']  # Handle missing URLs
            }
            mov_list.append(d)

        # Limit the number of recommended movies to n_outputs
        if len(mov_list) >= n_outputs:
            break
    
    return mov_list
