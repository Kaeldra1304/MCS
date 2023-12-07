import pandas as pd
import numpy as np

import streamlit as st
    

### DATA LOADING ###

# URLs to data files
link1 = 'https://raw.githubusercontent.com/Kaeldra1304/MCS/main/recommended_movies.csv'
link2 = 'https://raw.githubusercontent.com/Kaeldra1304/MCS/main/S_matrix.csv'
link3 = 'https://raw.githubusercontent.com/Kaeldra1304/MCS/main/movie_titles.csv'

# System 1 data
df_recommendationsByGenre = pd.read_csv(link1, sep=',', header=0, index_col='rank', dtype=str)
genres = df_recommendationsByGenre.columns.tolist()

# System 2 data
df_sMat = pd.read_csv(link2, sep=',', header=0, index_col=0, dtype=str)
tot_rows = 20
movies_per_row = 5
moviesToRate = df_sMat.columns.tolist()[:(tot_rows*movies_per_row)] # only store movieIDs to rate that will be displayed
moviesToRate[0] = "m1613"
moviesToRate[1] = "m1755"

# download movie titles (shared by System 1 & System 2
df_movie_titles = pd.read_csv(link3, sep=',', header=0, dtype=str)


### STYLING ###
st.set_page_config(layout="wide")

hide_img_fs = '''
<style>

button[title="View fullscreen"]{
    visibility: hidden;}
    
[data-testid="stForm"] {
    min-width: 830px;
 }
    
[data-testid="stExpander"] {
    min-width: 800px;
    overflow: scroll;
    overflow-x: hidden;
    max-height: 600px;
 }
    
[data-testid="stHorizontalBlock"] {
    overflow: scroll;
    overflow-x: hidden;
    min-height: 100px;
 }
 
 [data-testid="block-container"] {
    padding: 1rem;
 }
    
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)


### APP ONLY FUNCTIONS ###

def CreateImagePath(movieID) :
    movie_num = movieID[1:]
    return 'https://liangfgithub.github.io/MovieImages/' + movie_num + '.jpg'

def CreateMovieTitle(movieID) :
    movie_num = movieID[1:]
    return (df_movie_titles[df_movie_titles['id'] == movie_num]['title']).to_numpy()[0]
    
def RecommendMovies() :
    # translate ratings dictionary to (3706,) newuser array
    newuser = np.empty(len(df_sMat.columns)) * np.nan
    for movieID in ratings_dictionary.keys() :
        if (ratings_dictionary[movieID] != None) :
            index = df_sMat.columns.get_loc(movieID)
            newuser[index] = ratings_dictionary[movieID]
            #st.write(movieID + "," + str(ratings_dictionary[movieID]) + "," + str(newuser[index]))
    
    # grab ten 10 with myIBCF() functions
    top10 = myIBCF(newuser)
    
    # write top 10 to recommendations
    for i in range(10) :
        recommendations[i + 1] = top10[i]
    
    # write recommendations to UI
    with st.container() :
           
        for row in range(int(len(recommendations)/movies_per_row)) :
            # 2 rows of 5 movies in the example
            rec_col_list = st.columns(movies_per_row)     
            for col in range(movies_per_row) :
                index = row*movies_per_row + col # index within the UI, equals rank minus 1
                movieID = recommendations[index + 1] # movie ID with "m"
                with rec_col_list[col] :
                    # write rank
                    st.subheader("Rank" + str(index + 1))
                    # write movie image
                    st.image(CreateImagePath(movieID))
                    # write movie title
                    st.write(CreateMovieTitle(movieID))


### BACK-END FUNCTIONS ###

def RecommendNonSeenMovies(newuser, numToRec, previouslyRec) :
    # cycle through top 10 movies per genre collecting the top 'numToRec' that user hasn't seen
    # if user has seen all top 100, recommend first 'numToRec' movies that the user has not seen
    # make sure to exclude the movies in 'previouslyRec'
    #df_sMat = pd.read_csv('S_matrix.csv', sep=',', header=0, index_col=0, dtype=str) # global in APP
    #df_recommendationsByGenre = pd.read_csv('recommended_movies.csv', sep=',', header=0, index_col='rank', dtype=str)
    #df_movie_titles = pd.read_csv('movie_titles.csv', sep=',', header=0, dtype=str)

    newRecs = list() # list of new_recommendations
    # search through top 100 first for unseen movies to recommend
    for i in range(10) :
        rank = i + 1
        moviesOfRank = df_recommendationsByGenre.iloc[[i]].to_numpy()[0]
        #print("moviesOfRank", rank)
        #print(moviesOfRank)
        for movie_title in moviesOfRank :
            #print("movie_title", movie_title)
            movieID = "m"+ str(int(df_movie_titles[df_movie_titles['title'] == movie_title]['id']))
            #print("movieID", movieID)
            if (movieID in df_sMat.columns) :
                movie_index = df_sMat.columns.get_loc(movieID)
                #print("movie_index", movie_index)
                if (np.isnan(newuser[movie_index]) & ~(movieID in previouslyRec)) :
                    newRecs.append(movieID)
                    #print("RECOMMENDED")
                    if (len(newRecs) >= numToRec) :
                        return newRecs
            else :
                #print("movie not in newuser or smat")
                if (~(movieID in previouslyRec)) :
                    newRecs.append(movieID)
                    #print("RECOMMENDED")
                    if (len(newRecs) >= numToRec) :
                        return newRecs
    # fill in remaining spots with first unseen movies
    for movie_index in range(len(newuser)) :
        movieID = df_sMat.columns[movie_index]
        if (np.isnan(newuser[movie_index]) & ~(movieID in previouslyRec)) :
            newRecs.append(movieID)
            if (len(newRecs) >= numToRec) :
                return newRecs


    
def myIBCF(newuser) :
    #print(newuser.shape)
    # download S-matrix
    #df_sMat = pd.read_csv(link2, sep=',', header=0, index_col=0, dtype=str) # global in APP
    sMat_numpy = df_sMat.to_numpy().astype('float')

    # cycle through each user rating, rating those previously unrated & storing in newuser_predict
    newuser_predict = np.empty(newuser.shape) * np.nan #np.copy(newuser) # use this to include previously rated movies 
    for i in range(len(newuser)) :
        if (np.isnan(newuser[i])) :
            reviewed_indexes = (~np.isnan(newuser))
            tmp1 = sMat_numpy[i,reviewed_indexes]
            tmp2 = newuser[reviewed_indexes]
            tmp3 = np.nansum(tmp1)
            if (tmp3 > 0) :
                new_review = np.nansum(tmp1*tmp2) / tmp3
                #print("i:",i,"review:",new_review)
                newuser_predict[i] = new_review

    #print("first10 ratings:", newuser_predict[:10]) # print first 10 for debugging
    nonNAN_count = np.where(np.isnan(newuser_predict), 0, 1).sum()
    #print("non-NAN count:", nonNAN_count)
    
    # sort newuser_predicts by rating, selecting top 10    
    newuser_predict_noNAN = np.where(np.isnan(newuser_predict), -1, newuser_predict) #set NAN to -1 for proper sort
    predict_sorted_indexes = newuser_predict_noNAN.argsort()[::-1] # use kind='stable' for ordered
    top10_indexes = predict_sorted_indexes[:10]
    top10_ratings = newuser_predict_noNAN[top10_indexes]
    #print("top10 ratings:", top10_ratings)
    top10_movies = df_sMat.columns[top10_indexes].to_numpy()
    #print("top10 movies:", top10_movies)
    
    if (nonNAN_count < 10) :
        # need to find more movie recommendations
        previouslyRec = top10_movies[top10_ratings > -1]
        #print("previouslyRec:", previouslyRec)
        newRecs = RecommendNonSeenMovies(newuser, 10 - len(previouslyRec), previouslyRec)
        #print("newRecs:", newRecs)
        top10_movies[len(previouslyRec):] = newRecs
        #print("updated top10_movies:", top10_movies)
    
    return top10_movies



### APP STARTS HERE ###

recommendations = dict()
ratings_dictionary = dict()

st.title("Movie Recommender")

tab1, tab2 = st.tabs(["Recommend By Genre", "Recommend by Ratings"])

with tab1:
    st.header("Movie Recommendations by Genre")
   
    #st.dataframe(df_recommendationsByGenre) #debugging
   
    st.subheader("Step 1: Select your Favorite Genre")

    # Create genre selection box
    option = st.selectbox('Selected Genre:', genres, index=None)
    st.write('You selected:', option)        
   
    st.divider()
   
    st.subheader("Step 2: Movies You Might Like")   
        
    if (option != None) :
        with st.spinner() :
            #st.dataframe(df_recommendationsByGenre[option]) #debugging
        
            # 2 rows of 5 movies in the example
            genre_recommendations = df_recommendationsByGenre[option].to_numpy()
            #st.write(genre_recommendations) #debugging
            for row in range(int(len(genre_recommendations)/movies_per_row)) :
                genre_col_list = st.columns(movies_per_row)    
                for col in range(movies_per_row) :
                    index = row*movies_per_row + col # index within the UI, equals rank minus 1
                    movie_title = genre_recommendations[index] # grab movie title from movie recommendations by genre
                    # using movie title, create movie ID with "m"
                    movieID = "m" + str((df_movie_titles[df_movie_titles['title'] == movie_title]['id']).to_numpy()[0])
                    with genre_col_list[col] :
                        # write rank
                        st.subheader("Rank" + str(index + 1))
                        # write movie image
                        st.image(CreateImagePath(movieID))
                        # write movie title
                        st.write(CreateMovieTitle(movieID))

with tab2:

    # create form so user input is batched with Recommend Movies button
    with st.form(key='system2Form'):
    
        st.subheader("Step 1: Rate as Many Movies as Possible")  
        with st.expander("", expanded = True):
            with st.container() :
        
                # 20 rows of 6 movies in the example, 5 looks better in Streamlit        
                for row in range(tot_rows) :
                    col_list = st.columns(movies_per_row)
                    for col in range(movies_per_row) :
                        movie_index = row*movies_per_row + col # index within the UI & moviesToRate array
                        movieID = moviesToRate[movie_index]
                        with col_list[col] :
                            # write movie image
                            st.image(CreateImagePath(movieID))
                            # write movie title
                            st.write(CreateMovieTitle(movieID))
                            # ratings selection box
                            ratings_dictionary[movieID] = st.selectbox("", (1,2,3,4,5), index=None, key=movieID, placeholder="Rate It!", label_visibility="collapsed")
    
        #st.dataframe(ratings_dictionary) #debugging
    
        st.divider()
    
        st.subheader("Step 2: Movies You Might Like")
        if st.form_submit_button("Recommend Movies") :
            with st.spinner() :
                RecommendMovies()
    
    #st.dataframe(recommendations) #debugging