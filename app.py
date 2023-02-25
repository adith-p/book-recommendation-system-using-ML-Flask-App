from flask import Flask, render_template, request, redirect, url_for

import pandas as pd
import numpy as np

popular_df = pd.read_pickle('popularBooks')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_Score = pd.read_pickle('similarity_Score.pkl')

# popular_df = pd.pickle.load(open('popularBooks', 'rb'))

app = Flask(__name__, template_folder='templates')


@app.route('/')
def landing():
    return render_template('home.html')


@app.route('/top50')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['No_of_Rating'].values),
                           rating=list(popular_df['AvgRating'].values.round(2)),
                           ISBN=list(popular_df['ISBN'].values)

                           )



@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    result = np.where(pt.index == user_input)
    if len(result[0]) == 0:
        # Handle error here
        return render_template('Book_not_found.html', user_input=user_input)
    index = result[0][0]

    similar_items = sorted(list(enumerate(similarity_Score[index])), key=lambda x: x[1], reverse=True)[1:9]
    data = []
    for i in similar_items:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(items)
    print(data)

    return render_template('recommend.html', data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data

        username = request.form['username']
        password = request.form['password']
        print(f"{username}and{password}")

        # Save user to database

        # Redirect to login page
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/book-details')
def book_details():
    return render_template('one-site.html')


@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')
    search_results = books[books['Book-Title'].str.contains(search_query, case=False)]
    if search_results.empty:
        return render_template('Book_not_found.html', user_input=search_query)
    else:
        return render_template('search.html', search_results=search_results)


@app.errorhandler(404)
def error_handle(e):
    return render_template('404.html'), 404


# @app.route('/book-info/<book_id>')
# def book_info(book_id):
#   book = get_book_by_id(book_id)  # retrieve book information
#  return render_template('one-site.html', book=book)


if __name__ == '__main__':
    app.run(debug=True)
