from flask import Flask, request, render_template, redirect
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the form submission
        return redirect('/add')

    # Handle GET request to render the home page
    return render_template('index.html', posts=posts_data)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get the form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Find the maximum ID in the existing posts
        max_id = max([post['id'] for post in posts_data]) if posts_data else 0

        # Create a new post dictionary
        new_post = {
            "id": max_id + 1,
            "author": author,
            "title": title,
            "content": content
        }

        # Append the new post to the existing data
        posts_data.append(new_post)

        # Save the updated data to the file
        save_posts_data(posts_data)

        return redirect('/')

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
