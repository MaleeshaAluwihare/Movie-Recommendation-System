import streamlit as st
import pandas as pd
import numpy as np
from scripts.content_based import recommend_content_based   # Content-based recommendation function
from scripts.collaborative import recommend_collaborative   # Collaborative-based recommendation function
from scripts.collaborative_personalized import recommend_collaborative_personalized  # Collaborative-based Personalized recommendation function
from scripts.popular_movies import getTopRatedMovies  # Popular movies function
from scripts.popular_movies_year import popular_movie_year # Popular movies by year function
from scripts.hybrid_approch import get_hybrid_recommendations 
from scripts.cold_start import recommend_based_on_favorites
from scripts.home import displayRandomMovies 

# Add the CSS for styling the header and cover photo
st.markdown("""
    <style>
    .header {
        display: flex;
        justify-content: center; 
        align-items: center;
        padding: 20px;
        background-color: #0d6efd;
        color: white;
        position: sticky;
        top: 0;
        z-index: 1000;
        border-radius: 10px; /* Optional: rounded corners */
        margin-bottom: 10px;
    }
    .logo {
        font-size: 50px;
        font-weight: bold;
        margin: 0 20px; /* Add some margin to the left and right */
    }

    .cover-photo {
        width: 100%;
        height: 400px; 
        border-radius: 10px; 
        margin-bottom: 20px;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Add the header
st.markdown('<div class="header"><div class="logo">CineBazaar</div></div>', unsafe_allow_html=True)

# Add the cover photo using the web image URL
st.markdown('<img src="https://wallpapers.com/images/high/movie-poster-background-q1zm830g0hfww2lk.webp" class="cover-photo">', unsafe_allow_html=True)



# Function to display movies in a card format
def recommend(movie_name, n_outputs, mode):
    if mode == 'Content based':
        result = recommend_content_based(movie_name, n_outputs)
    elif mode == 'Collaborative':
        result = recommend_collaborative(movie_name, n_outputs)
    elif mode=='Hybrid':
        if user_id is not None:
            result = get_hybrid_recommendations(user_id, movie_name, n_outputs)
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

st.markdown("""
<div class="intro-section">
    <h2>Welcome to CineBazaar...</h2>
    <p>Dive into the world of cinema with our curated collection of movies available for purchase. Whether you’re a fan of timeless classics or the latest blockbusters, we have something for everyone.<br>
    Not sure what to watch next? Our personalized movie recommendation feature suggests titles tailored to your taste, making it easier than ever to find your next favorite film.
    Explore, discover, and enjoy the magic of movies with us!</p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Latest Movies...")
displayRandomMovies(3)  # Display random movies
st.markdown("---")

# Cold start
movie_list = get_movie_list()
st.title('Get Recommendations Based on Your Favorites!')
favorite_movies = st.multiselect('Select your favorite movies', movie_list)

# Button to generate recommendations
if st.button('Get Recommendations'):
    if favorite_movies:  # Ensure the user has selected at least one movie
        # Call the recommendation function
        recommendations = recommend_based_on_favorites(favorite_movies, n_outputs=10)

        # Display the recommended movies
        st.write("Recommended Movies:")
        col1, col2, col3 = st.columns(3)
        title_height = "70px" 
        for i, val in enumerate(recommendations):

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
    else:
        st.error("Please select at least one favorite movie.")

st.markdown('---')

global user_id

# Streamlit UI
st.title("Find Movie Here...")

selected_page = st.selectbox("", ["Recommendation", "Popular", "Recommendation by Year"], key="my_selectbox")

# Depending on the selected page, show the appropriate content
if selected_page == "Recommendation":
    st.sidebar.title("User Preferences")
    mode = st.sidebar.selectbox("Recommendation Mode", ["Content based", "Collaborative", "Collaborative Personalized","Hybrid"])
    
    if mode == 'Hybrid':
        user_id = st.sidebar.text_input("User_ID", "1")
        movie = st.sidebar.selectbox("Movie", get_movie_list())

    elif mode == 'Collaborative Personalized':
        movie = st.sidebar.selectbox("Movie", get_movie_list(), disabled=True)
        user_id = st.sidebar.text_input("User_ID", "1")

    else:
        movie = st.sidebar.selectbox("Movie", get_movie_list())

    num_recommendations = st.sidebar.number_input("Number of Recommendations", min_value=1, max_value=10, value=5)

    st.subheader("Click below to get a movie recommendation:")
    if st.button("Recommend a Movie"):
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

st.markdown('---')
        
st.markdown("""
<style>
div.stButton > button {
    background-color: #007BFF; 
    color: white;
    font-size: 16px;
    padding: 10px 20px;
    border-radius: 10px;
    border: none;
    transition: background-color 0.3s ease;
}

div.stButton > button:hover {
    background-color: #0056b3;
}

.intro-section h2 {
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 15px;
    text-align: center;
}

.intro-section p {
    font-size: 18px; 
    text-align: center; 
    line-height: 1.8; 
    font-weight: bold;
    margin: 0 0 20px 0; 
    
    
}

</style>
""", unsafe_allow_html=True)

