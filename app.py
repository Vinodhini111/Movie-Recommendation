from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load the saved models
print("Loading AI Model...")
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        movie_name = data['movie_input']
        
        # Check if movie exists (case insensitive)
        movie_match = movies[movies['title'].str.lower() == movie_name.lower()]
        
        if movie_match.empty:
            return jsonify({'status': 'error', 'message': 'Movie not found! Try checking the spelling.'})

        movie_index = movie_match.index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommendations = []
        for i in movies_list:
            recommendations.append(movies.iloc[i[0]].title)
            
        return jsonify({'status': 'success', 'rec_movies': recommendations})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)