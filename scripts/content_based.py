import pickle

# Content-based recommendation function
def recommend_content_based(movie, n_outputs):
    # Load files
    with open('PKL_Files/stemmed_df_content_based', 'rb') as file:
        new_df = pickle.load(file)

    with open('PKL_Files/similarity_content_based', 'rb') as file:
        similarity = pickle.load(file)

    movie = movie.strip().lower()

    # Check if movie exists in the dataset
    if movie not in new_df['title'].values:
        st.error(f"Movie '{movie}' not found in the content-based dataset.")
        return []

    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:n_outputs+1]

    mov_list = []
    for i in movie_list:
        d = dict()
        d['title'] = new_df.iloc[i[0]].title
        d['url'] = new_df.iloc[i[0]]['Poster URL']  # Handle missing URLs
        mov_list.append(d)
    return mov_list
