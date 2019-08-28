from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jnwpdydqyhpcmu:cf1f4895fd2cadaffcf590d550f7bb4f64ef3bc5e88aa2e1b3faa938d0731688@ec2-50-19-222-129.compute-1.amazonaws.com:5432/d4es4orn3m2gh6'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class KidneyData(db.Model):
    __tablename__ = 'KidneyData'

    Id = db.Column(db.Integer, primary_key=True)
    specific_gravity = db.Column(db.Float)
    Albumin = db.Column(db.Integer)
    Blood_Gluc_rand = db.Column(db.Integer)
    Blood_Urea = db.Column(db.Integer)
    Serum_Cr = db.Column(db.Float)
    sodium = db.Column(db.Integer)
    Hemoglobin = db.Column(db.Float)
    packed_cell_volume = db.Column(db.Integer)
    rbc_cnt = db.Column(db.Float)
    htn = db.Column(db.Integer)
    diabetes = db.Column(db.Integer)
    actual_class = db.Column(db.Integer)
    predicted_class=db.Column(db.Integer)
    CreateDate = db.Column(db.DateTime)

    def __init__(self
                 , specific_gravity
                 , Albumin 
                 , Blood_Gluc_rand 
                 , Blood_Urea 
                 , Serum_Cr 
                 , sodium 
                 , Hemoglobin 
                 , packed_cell_volume 
                 , rbc_cnt 
                 , htn 
                 , diabetes 
                 , actual_class
                 , predicted_class
                , CreateDate 
                 ):
        self.specific_gravity = specific_gravity
        self.Albumin = Albumin
        self.Blood_Gluc_rand = Blood_Gluc_rand
        self.Blood_Urea = Blood_Urea
        self.Serum_Cr = Serum_Cr
        self.sodium = sodium
        self.Hemoglobin = Hemoglobin
        self.packed_cell_volume = packed_cell_volume
        self.rbc_cnt = rbc_cnt
        self.htn = htn
        self.diabetes = diabetes
        self.actual_class = actual_class
        self.predicted_class = predicted_class
        self.CreateDate = CreateDate
        



if __name__ == '__main__':
    manager.run()
