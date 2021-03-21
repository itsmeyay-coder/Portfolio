from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from projects import projects, websites


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comments.db"
db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)


db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        comment = request.form.get("comment")
        new_comment = Comment(
            name=name,
            comment=comment,
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('home'))
    comments = db.session.query(Comment).all()
    return render_template("index.html", projects=projects, comments=comments, websites=websites)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
