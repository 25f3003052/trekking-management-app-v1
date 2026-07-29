from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    data_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):  #
        return f"{self.sno} - {self.title}"

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8000 )

