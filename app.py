from flask import Flask,flash,redirect,render_template,request
import pickle
import requests
import pandas as pd

app = Flask(__name__)

movies=pickle.load(open('model/movies_list.pkl','rb'))
similarity=pickle.load(open('model/similarity.pkl','rb'))

def fetchPoster(movie_id):
     
    try:
      url="https://api.themoviedb.org/3/movie/{}?api_key=bc70c2dda99c3887b43749d091aede16&language=en-US".format(movie_id)
      headers = {
      "accept": "application/json",
      "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYzcwYzJkZGE5OWMzODg3YjQzNzQ5ZDA5MWFlZGUxNiIsIm5iZiI6MTc0NTUxNTY5NS45NDQsInN1YiI6IjY4MGE3NGFmMjcxZWNiM2FlMDhhMjhlNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._cBt6ijeY91hxTJdtOesq5wGBkjSmhOzZ9OkvStdMKg"
      }
      response = requests.get(url, headers=headers,timeout=10)
      data=response.json()
      poster_path=data['poster_path']
      movie_name=data['original_title']
      m_id=data['id']
      imbd_id=data['imdb_id']
      full_p_path="https://image.tmdb.org/t/p/w500/"+poster_path
      return [full_p_path,movie_name,m_id,imbd_id]
    except Exception as e:
     pass
     

def get_recommend(movie):
    recommend_movies_poster=[]
    recommend_movies_name=[]
    recommend_movies_tmdb_id=[]
    recommend_movies_imdb_id=[]

    index=movies[movies['title']==movie].index[0]
    print(index)
    distance=sorted(list(enumerate(similarity[index])),reverse=True , key=lambda x:x[1])

    for i in distance[0:15]:
         movie_id=movies.iloc[i[0]].id
         movie_detail=fetchPoster(movie_id)
         if movie_detail:
          recommend_movies_poster.append(movie_detail[0])
          recommend_movies_name.append(movie_detail[1])
          recommend_movies_tmdb_id.append(movie_detail[2])
          recommend_movies_imdb_id.append(movie_detail[3])
        #   recommend_movies_name.append(movie_name)
        # #  recommend_movies_name.append(movies.iloc[i[0]].title)

    return recommend_movies_name,recommend_movies_poster,recommend_movies_tmdb_id,recommend_movies_imdb_id



@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/recommend',methods=["GET","POST"])
def recommend():
    status=False
    movie_list=movies['title'].values.tolist()
    if request.method=='POST':
        try:
             if request.form:
                 status=True
                 movie_data=zip()
                 movie_name=request.form['movie_name']
            
                 recommend_movies_name,recommend_movies_poster,recommend_movies_tmdb_id,recommend_movies_imdb_id=get_recommend(movie_name)
                
                 
                 recommend_movies=zip(recommend_movies_name,recommend_movies_poster,recommend_movies_tmdb_id,recommend_movies_imdb_id)
                 return render_template('predict.html',movie_data=recommend_movies, movie_list=movie_list,status=status )

        except Exception as e:
            
            pass
            


    recommend_movies_poster=[]
    recommend_movies_name=[]
    recommend_movies_tmdb_id=[]
    recommend_movies_imdb_id=[]      
    for i in range(0,15):
        movie_id=movies.iloc[i].id

        movie_detail=fetchPoster(movie_id)
        if movie_detail:
          recommend_movies_poster.append(movie_detail[0])
          recommend_movies_name.append(movie_detail[1])
          recommend_movies_tmdb_id.append(movie_detail[2])
          recommend_movies_imdb_id.append(movie_detail[3])
    popular_movies=zip(recommend_movies_name,recommend_movies_poster,recommend_movies_tmdb_id,recommend_movies_imdb_id)

    return render_template('predict.html',movie_list=movie_list,status=status,popular_movies=popular_movies)






if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')