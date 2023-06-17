from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

posts_file = 'data/blog_posts.json'


def load_posts_data():
    try:
        with open(posts_file, 'r') as file:
            blog_posts = json.load(file)
    except FileNotFoundError:
        blog_posts = []
    return blog_posts


def save_posts_data(posts_data):
    with open(posts_file, 'w') as file:
        json.dump(posts_data, file, indent=4)


posts_data = load_posts_data()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', posts=posts_data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Handle the form submission
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        # Rest of the code for adding a new post...

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the index of the post with the specified ID
    post_index = -1
    for i in range(len(posts_data)):
        if posts_data[i]['id'] == post_id:
            post_index = i
            break

    if post_index != -1:
        # Remove the post from the list
        del posts_data[post_index]

        # Save the updated data to the file
        save_posts_data(posts_data)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
