import pickle
import numpy as np
import streamlit as st


# Collaborative-based recommendation function
def recommend_collaborative(movie, n_outputs):
    # Load files
    with open('PKL_Files/movie_rating_collaborative', 'rb') as file:
        mov_ratings = pickle.load(file)

    with open('PKL_Files/similarity_scores_collaborative', 'rb') as file:
        similarity_scores = pickle.load(file)

    with open('PKL_Files/pivot_table_collaborative', 'rb') as file:
        pt = pickle.load(file)

    movie = movie.strip().lower()

    # Handle case where movie is not found
    if movie not in pt.index:
        st.info(f"We don't have enough information to recommend movies related to '{movie.title()}' at the moment, but you can explore other popular titles in our database.")
        return []

    index = np.where(pt.index == movie)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:n_outputs+1]

    data = []
    for i in similar_items:
        d = dict()
        temp_df = mov_ratings[mov_ratings['title'] == pt.index[i[0]]]
        item = temp_df.drop_duplicates('title')['title'].values[0]
        d['title'] = item
        d['url'] = temp_df['Poster URL'].values[0] if 'Poster URL' in temp_df.columns else 'https://via.placeholder.com/200'
        data.append(d)
    
    return data
