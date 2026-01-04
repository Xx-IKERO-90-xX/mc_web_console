from extensions import db

class Console(db.Model):
    __tablename__ = 'console'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True)
    ip = db.Column(db.String(100), unique=True)
    port = db.Column(db.Numeric)
    passwd = db.Column(db.String(200))
    status = db.Column(db.String(50))

    def __init__(self, name, ip, port, passwd, status):
        self.name = name
        self.ip = ip
        self.port = port
        self.passwd = passwd
        self.status = status