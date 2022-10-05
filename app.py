from flask import Flask, render_template, request

import pandas as pd
import numpy as np

popular_df = pd.read_pickle('popularBooks')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_Score = pd.read_pickle('similarity_Score.pkl')

# popular_df = pd.pickle.load(open('popularBooks', 'rb'))

app = Flask(__name__, template_folder='templates')


@app.route('/')
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

    index = np.where(pt.index == user_input)[0][0]

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


if __name__ == '__main__':
    app.run(debug=True)
