from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# dialect + driver://username:password@host:post/database

@app.route('/')
def id_view():
    return render_template('index.html')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(75), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)

if __name__ == '__main__':
    app.run()