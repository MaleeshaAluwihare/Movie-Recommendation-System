import pickle
from scripts.collaborative_personalized import recommend_collaborative_personalized
from scripts.content_based import recommend_content_based


# considering the union
def get_hybrid_recommendations(user_id, movie, outputs):
    # Get content-based and collaborative-based recommendations
    content_based = recommend_content_based(movie) 
    collaborative_based = recommend_collaborative_personalized(user_id) 
    
    unique_movies = {}
    
    # Add content-based recommendations to the dictionary
    for item in content_based:
        unique_movies[item['title']] = item 
    
    # Add collaborative-based recommendations to the dictionary
    for item in collaborative_based:
        unique_movies[item['title']] = item 
    
    # Convert the dictionary values to a list
    hybrid_recommendations = list(unique_movies.values())
    
    # Return only the top 'outputs' number of recommendations
    return hybrid_recommendations[:outputs]