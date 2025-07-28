import streamlit as st
import pickle, gzip
import requests

OMDB_API_KEY = "d8ca6191"

def get_omdb_poster(title):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={requests.utils.quote(title)}"
        res = requests.get(url)
        data = res.json()
        if data.get("Response") == "True":
            return data.get("Poster")
    except Exception as e:
        print(f"Error fetching '{title}': {e}")
    return None

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:11]

    names = []
    poster = []
    for i in movie_list:
        movie_title = movies_list.iloc[i[0]].title
        names.append(movie_title)
        poster.append(get_omdb_poster(movie_title))

    return names, poster

movies_list = pickle.load(open("Movies.pkl","rb"))
movies_titles = movies_list['title'].values
movie_options = ["Select a Movie"] + list(movies_titles)


url = "https://drive.google.com/file/d/1t4q1DBNbyQvK-rOxGRw-4m4XmT3fRB35/view?usp=sharing"

r = requests.get(url)
with open("similarity.pkl.gz", "wb") as f:
    f.write(r.content)

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

st.title("Movie Recommender System")
selected_movie_name = st.selectbox(
    "Please select a movie", movie_options
)

if st.button("Recommend") and selected_movie_name != "Select a Movie":
    names, posters = recommend(selected_movie_name)  # should return 10 names & posters
    
    # First row (first 5 movies)
    cols1 = st.columns(5)
    for i in range(5):
        with cols1[i]:
            if posters[i] is not None:
                st.image(posters[i], width=150)
            else:
                st.markdown('<span style="color:red">Poster not available</span>', unsafe_allow_html=True)
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)

    # Second row (next 5 movies)
    cols2 = st.columns(5)
    for i in range(5, 10):
        with cols2[i - 5]:  # index 0 to 4
            if posters[i] is not None:
                st.image(posters[i], width=150)
            else:
                st.markdown('<span style="color:red">Poster not available</span>', unsafe_allow_html=True)
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)
