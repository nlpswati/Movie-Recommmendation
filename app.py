import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    api_key = "f017e9abff5f55600ce977069ea6c6cf"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

select_value = st.selectbox("Select a movie from the dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movies = []
    recommend_posters = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_posters

if st.button("Show Recommendations"):
    movie_names, movie_posters = recommend(select_value)
    for movie_name, movie_poster in zip(movie_names, movie_posters):
        st.text(movie_name)
        st.image(movie_poster)
