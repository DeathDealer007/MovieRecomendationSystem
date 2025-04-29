import pickle
import pandas as pd
import requests
import streamlit as st

# --- Helper Functions ---

# Fetch poster from TMDB API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=415824fdedd7d788f9646c4518e669da&language=en-US'
    try:
        response = requests.get(url)
        response.raise_for_status()
        poster_path = response.json().get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
    except requests.RequestException as e:
        st.error(f"Failed to fetch poster: {e}")
        return None

# Recommend similar movies
def recommend(movie):
    if movie not in movies['title'].values:
        st.warning("Selected movie not found.")
        return [], []

    idx = movies[movies['title'] == movie].index[0]
    scores = list(enumerate(similarity[idx]))
    top_movies = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]

    recommendations = []
    posters = []
    for i in top_movies:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster = fetch_poster(movie_id)
        if poster:
            recommendations.append(title)
            posters.append(poster)
    return recommendations, posters

# --- Load Data ---

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# --- Streamlit UI ---

# Page styling
st.markdown("""
    <style>
        .stApp { background-color: #000; }
        .title-text { color: yellow; font-size: 36px; font-weight: bold; text-align: center; }
        .subtitle-text { color: yellow; font-size: 20px; text-align: center; }
        .label-text { color: yellow; font-size: 20px; margin-top: 20px; }
        .recommended-text { color: yellow; font-size: 16px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="title-text">Movie Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Made By: Ankit Shah</div>', unsafe_allow_html=True)

# Movie selection
st.markdown('<div class="label-text">Select a movie:</div>', unsafe_allow_html=True)
selected_movie = st.selectbox('', movies['title'].values)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    if not names:
        st.info("No recommendations found.")
    else:
        cols = st.columns(len(names))
        for i, col in enumerate(cols):
            with col:
                st.markdown(f'<p class="recommended-text">{names[i]}</p>', unsafe_allow_html=True)
                st.image(posters[i] if posters[i] else "https://via.placeholder.com/150", use_column_width=True)
