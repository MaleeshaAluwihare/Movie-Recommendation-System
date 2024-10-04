import pickle
import random
import streamlit as st

# Function to display random movies
def displayRandomMovies(n_outputs):
    with open('PKL_Files/popular_movies_df', 'rb') as file:
        popular_movies_df = pickle.load(file)

    random_movies = popular_movies_df.sample(n=min(n_outputs, len(popular_movies_df)), random_state=42)

    # Create a scrollable container for the movies
    with st.container():
        # Create a layout for the movies
        cols = st.columns(3)
        
        for i, movie in random_movies.iterrows():
            title_div = f"<div style='text-align: center; font-weight: bold; margin-bottom: 10px;'>{movie['title']}</div>"
            movie_card = f"""
                <div style='border: 1px solid #e0e0e0; border-radius: 8px; padding: 10px; margin: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                    <img src="{movie['Poster URL']}" width="150" style='border-radius: 4px;'>
                    <div>{title_div}</div>
                    <button style='background-color: #007BFF; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;'>Buy Now</button>
                </div>
            """
            
            # Place cards in columns
            cols[i % 3].markdown(movie_card, unsafe_allow_html=True)
