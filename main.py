from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    content = db.Column(db.String(10240))

    def __init__(self, name, content):
        self.name = name
        self.content = content

@app.route('/blog', methods=['POST', 'GET'])
def index():

    entries = {}
    qry_id = request.args.get('id')

    if qry_id == None:
        entries = Blog.query.all()
        return render_template("blog.html",
            title="Raven's Ranting",
            entries=entries)

    else:
        entries = Blog.query.filter_by(id=qry_id).all()
        return render_template("blog.html",
            title="Raven's Ranting",
            entries=entries)

@app.route('/blogentry', methods=['POST', 'GET'])
def blogentry():

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        title_error = ""
        content_error = ""
        errorcount = 0

        if post_title == "":
            errorcount += 1
            title_error = "The Post Title field may not be blank."

        if post_content == "":
            errorcount += 1
            content_error = "The Post Content field may not be blank."   
    
        if errorcount > 0:

            return render_template('blogentry.html',
                title_error=title_error,
                content_error=content_error, 
                post_content=post_content,
                post_title=post_title,
                )

        else:
            new_entry = Blog(post_title, post_content)

            db.session.add(new_entry)
            db.session.commit()

            new_id = str(new_entry.id)

            return redirect('/blog?id='+ new_id)

    else:
        return render_template('blogentry.html')

if __name__ == '__main__':
    app.run()
