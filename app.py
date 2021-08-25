import streamlit as st
import pandas as pd
import joblib
import requests

st.set_page_config(
     page_title="Movie-Recommendation",
     page_icon="🎥",
     layout="wide",
     initial_sidebar_state="expanded",
 )

file_movie = 'movie_model.sav'
movies = joblib.load(file_movie)

file_similar = 'similar_model.sav'
similarity = joblib.load(file_similar)

df = pd.DataFrame(movies)

def selected_movie_information(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=802cb615fa092f44ccd09356bc78401f')
    data = response.json()
    poster = "https://image.tmdb.org/t/p/w500" + data['poster_path']
    overview = data['overview']
    tagline = data['tagline']
    return poster , overview , tagline

def get_posterpath(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=802cb615fa092f44ccd09356bc78401f')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie_name):
    index = df[df['original_title'] == movie_name].index[0]
    distances = similarity[index]
    all_movies = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:11]
    movies_name = []
    posters= []
    for i in all_movies:
        movie_id = df['id'].iloc[i[0]]
        poster = get_posterpath(movie_id)
        posters.append(poster)
        movies_name.append(df['original_title'].iloc[i[0]])

    return movies_name , posters

def selected_movie(name):
    index = df[df['original_title'] == name].index[0]
    movie_id = df['id'].iloc[index]
    poster,overview,tagline = selected_movie_information(movie_id)
    return poster,overview,tagline

st.title('Movie Recommendation')

option = st.selectbox('Which movie do you like best ?',df['original_title'])
poster , overview, tagline = selected_movie(option)
col_i, col_ii, = st.columns([1, 4])
with col_i:
    st.image(poster,width = 200, caption=option)
with col_ii:
    st.header("**" +option+ "**")
    st.subheader("_"+tagline+"_")
    st.write(overview)

if st.button('Click here to recommend movies'):
    st.write(f"Based on {option} movie you can also watch ...")
    with st.spinner('Wait for it...'):
        movies_list, posters_list = recommend(option)
    st.success('Done!')

    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.image(posters_list[0],width=200,caption=movies_list[0])
    with col2:
        st.image(posters_list[1],width=200,caption=movies_list[1])
    with col3:
        st.image(posters_list[2],width=200,caption=movies_list[2])
    with col4:
        st.image(posters_list[3],width=200,caption=movies_list[3])
    with col5:
        st.image(posters_list[4],width=200,caption=movies_list[4])

    col6, col7, col8, col9,col10 = st.columns(5)
    with col6:
        st.image(posters_list[5], width=200, caption=movies_list[5])
    with col7:
        st.image(posters_list[6], width=200, caption=movies_list[6])
    with col8:
        st.image(posters_list[7], width=200, caption=movies_list[7])
    with col9:
        st.image(posters_list[8], width=200, caption=movies_list[8])
    with col10:
        st.image(posters_list[9],width=200,caption=movies_list[9])

# footer
from htbuilder import HtmlElement, div, hr, a, p, img, styles
from htbuilder.units import percent, px

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 100px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="white",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(1)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in ",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(15), height=px(15)),
        " with ❤️ by © ",
        link("https://github.com/Pratik180198", "Pratik Bambulkar"),
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer()