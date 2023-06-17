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


def fetch_post_by_id(post_id):
    for post in posts_data:
        if post['id'] == post_id:
            return post
    return None


posts_data = load_posts_data()


@app.route('/', methods=['GET'])
def index():
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

        # Redirect to the homepage
        return redirect('/')

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the index of the post with the specified ID
    post_index = -1
    for index, post in enumerate(posts_data):
        if post['id'] == post_id:
            post_index = index
            break

    if post_index != -1:
        # Remove the post from the list
        del posts_data[post_index]

        # Save the updated data to the file
        save_posts_data(posts_data)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog post from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Get the form data
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Update the post dictionary
        post['author'] = author
        post['title'] = title
        post['content'] = content

        # Save the updated data to the file
        save_posts_data(posts_data)

        # Redirect to the homepage
        return redirect('/')

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
