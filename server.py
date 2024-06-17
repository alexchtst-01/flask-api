from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_database'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(server)
        
class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    nim = db.Column(db.String(50), nullable=False)
    ukt = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nim': self.nim,
            'ukt': self.ukt
        }

with server.app_context():
    db.create_all()
    

if __name__ == "__main__":
    server.run(debug=True)