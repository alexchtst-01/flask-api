from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flask_database'
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
    
message = {
    100: {'msg': 'Continue'},
    101: {'msg': 'Switching Protocols'},
    200: {'msg': 'OK'},
    201: {'msg': 'Data has been created'},
    202: {'msg': 'Data has been updated'},
    204: {'msg': 'No Content'},
    301: {'msg': 'Moved Permanently'},
    302: {'msg': 'Found'},
    304: {'msg': 'Not Modified'},
    400: {'msg': 'Bad Request'},
    401: {'msg': 'Unauthorized'},
    403: {'msg': 'Forbidden'},
    404: {'msg': 'Data not found'},
    405: {'msg': 'Method Not Allowed'},
    409: {'msg': 'Conflict'},
    500: {'msg': 'Internal Server Error'},
    501: {'msg': 'Not Implemented'},
    502: {'msg': 'Bad Gateway'},
    503: {'msg': 'Service Unavailable'},
    504: {'msg': 'Gateway Timeout'}
}
    
@server.route("/api/v1/mahasiswa", methods=["GET"])
def get_mahasiswa():
    data = Mahasiswa.query.all()
    return jsonify([i.to_dict() for i in data])

@server.route("/api/v1/mahasiswa/<int:id>", methods=["GET"])
def get_mahasiswabyId(id):
    data = Mahasiswa.query.get(id)
    if data:
        return jsonify(data.to_dict())
    else:
        return jsonify(message[404]), 404

@server.route("/api/v1/mahasiswa/add", methods=["POST"])
def add_mahasiswa():
    req = request.json
    new_mahasiswa = Mahasiswa(name=req['name'], nim=req['nim'], ukt=req['ukt'])
    db.session.add(new_mahasiswa)
    db.session.commit()
    return jsonify(message[201]), 201

@server.route("/api/v1/mahasiswa/update/<int:id>", methods=["PUT", "PATCH"])
def update_mahasiswa(id):
    exists_data = Mahasiswa.query.get(id)
    req = request.json
    req_name = req['name']
    req_nim = req['nim']
    req_ukt = req['ukt']
    if not exists_data:
        return jsonify(message[404]), 404
    exists_data.name = req_name
    exists_data.nim = req_nim
    exists_data.ukt = req_ukt
    db.session.commit()
    
    return jsonify(message[202]), 202

@server.route("/api/v1/mahasiswa/delete/<int:id>", methods=["DELETE"])
def delete_data(id):
    exists_data = Mahasiswa.query.get(id)
    if not exists_data:
        return jsonify(message[404]), 404
    db.session.delete(exists_data)
    db.session.commit()
    return jsonify(message[200]), 200
    
if __name__ == "__main__":
    server.run(debug=True)