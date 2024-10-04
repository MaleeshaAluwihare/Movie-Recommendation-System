import streamlit as st
import pandas as pd
import numpy as np
from scripts.content_based import recommend_content_based   # Content-based recommendation function
from scripts.collaborative import recommend_collaborative   # Collaborative-based recommendation function
from scripts.collaborative_personalized import recommend_collaborative_personalized  # Collaborative-based Personalized recommendation function
from scripts.popular_movies import getTopRatedMovies  # Popular movies function
from scripts.popular_movies_year import popular_movie_year # Popular movies by year function
from scripts.home import displayRandomMovies 

# Function to display movies in a card format
def recommend(movie_name, n_outputs, mode, ):
    if mode == 'Content based':
        result = recommend_content_based(movie_name, n_outputs)
    elif mode == 'Collaborative':
        result = recommend_collaborative(movie_name, n_outputs)
    elif mode == 'Collaborative Personalized':
        if user_id is not None:
            result = recommend_collaborative_personalized(user_id, n_outputs)
        else:
            st.error("Please enter a valid User ID for personalized recommendations.")
            result = []
    else:
        result = []  

    col1, col2, col3 = st.columns(3)
    title_height = "70px" 

    for i, val in enumerate(result):
        title_div = f"<div style='height: {title_height}; display: flex; align-items: center;'>{val['title']}</div>"
        if i % 3 == 0:
            with col1:
                st.write(title_div, unsafe_allow_html=True)
                st.image(val['url'], width=200)
                st.button('Buy Now', key=f"buy1_{i}")

        elif i % 3 == 1:
            with col2:
                st.write(title_div, unsafe_allow_html=True)
                st.image(val['url'], width=200)
                st.button('Buy Now', key=f"buy2_{i}")

        else:
            with col3:
                st.write(title_div, unsafe_allow_html=True)
                st.image(val['url'], width=200)
                st.button('Buy Now', key=f"buy3_{i}")



# Get movie list for the dropdown
def get_movie_list():
    movies = pd.read_csv(r'Implementation/movie_data_with_urls.csv')
    return list(movies['title'])


# Streamlit UI
st.title("CineBazaar")

st.markdown("""Dive into the world of cinema with our curated collection of movies available for purchase. Whether you’re a fan of timeless classics or the latest blockbusters, we have something for everyone.\n
Not sure what to watch next? Our personalized movie recommendation feature suggests titles tailored to your taste, making it easier than ever to find your next favorite film.
Explore, discover, and enjoy the magic of movies with us!""")

st.markdown("---")
displayRandomMovies(10)  # Display random movies
st.markdown("---")

st.subheader("Movie Recommendations")
st.markdown("Choose an option formovie recommendations:")
selected_page = st.selectbox("", ["Recommendation", "Popular", "Recommendation by Year"], key="my_selectbox")

# Depending on the selected page, show the appropriate content
if selected_page == "Recommendation":
    st.sidebar.title("User Preferences")
    mode = st.sidebar.selectbox("Recommendation Mode", ["Content based", "Collaborative", "Collaborative Personalized"])

    if mode == 'Collaborative Personalized':
        movie = st.sidebar.selectbox("Movie", get_movie_list(), disabled=True)
        user_id = st.sidebar.text_input("User_ID", "1")
    else:
        movie = st.sidebar.selectbox("Movie", get_movie_list())

    num_recommendations = st.sidebar.number_input("Number of Recommendations", min_value=1, max_value=10, value=5)

    if st.button("Recommend Movies"):
        if movie:
            recommend(movie, num_recommendations, mode)
        else:
            st.error("Please select a movie.")

elif selected_page == "Popular":
    # Disable inputs in the sidebar when "Popular" is selected
    st.sidebar.markdown("### Popular Page")
    st.sidebar.selectbox("Movie", options=get_movie_list(), key="popular_movie", disabled=True)
    st.sidebar.selectbox("Recommendation Mode", options=["Content based", "Collaborative", "Collaborative Personalized"], key="popular_mode", disabled=True)
    n_movies = st.sidebar.slider("Number of Movies", min_value=1, max_value=50, value=5, key="popular_recommendations", disabled=False)

    getTopRatedMovies(n_movies)


elif selected_page == "Recommendation by Year":
    # Disable inputs in the sidebar when "Recommendation by Year" is selected
    st.sidebar.markdown("### Recommendation by Year")
    st.sidebar.selectbox("Movie", options=get_movie_list(), key="popular_movie", disabled=True)
    st.sidebar.selectbox("Recommendation Mode", options=["Content based", "Collaborative", "Collaborative Personalized"], key="popular_mode", disabled=True)
    year = st.sidebar.text_input("Enter a year (e.g., 1983):", "2000")
    n_movies = st.sidebar.slider("Number of Movies", min_value=1, max_value=50, value=5, key="popular_recommendations", disabled=False)

    popular_movie_year(year,n_movies)