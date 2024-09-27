import pickle
import streamlit as st

def popular_movie_year(year,outputs):
    with open('PKL_Files\popular_movies_year_df', 'rb') as file:
        popular_movie_year = pickle.load(file)

   # Filter movies by the given year
    movies_by_year = popular_movie_year[popular_movie_year['year'] == year]
    
    # Sort the movies by rating
    movies_by_year = movies_by_year.sort_values(by='avg_rating', ascending=False)
    
    # Limit the number of displayed movies by the 'outputs' parameter
    movies_to_display = movies_by_year.head(outputs)
    
    # Display the movies using Streamlit
    st.write(f"Top {outputs} popular movies for the year {year}:")
    
    col1, col2, col3 = st.columns(3)
    
    # Loop through the movies and display the titles and posters
    for i, (index, movie) in enumerate(movies_to_display.iterrows()):
        title = movie['title']
        poster_url = movie['Poster URL']
        
        if i % 3 == 0:
            with col1:
                st.write(title)
                st.image(poster_url, width=200)
                st.button('BUY NOW', key=f"buy1_{i}")
        elif i % 3 == 1:
            with col2:
                st.write(title)
                st.image(poster_url, width=200)
                st.button('BUY NOW', key=f"buy2_{i}")
        else:
            with col3:
                st.write(title)
                st.image(poster_url, width=200)
                st.button('BUY NOW', key=f"buy3_{i}")