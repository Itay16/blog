from flask import Flask, render_template

blog_posts = 'blog_posts.json'

app = Flask(__name__)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
