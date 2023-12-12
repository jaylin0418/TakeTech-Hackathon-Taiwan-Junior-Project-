from myproject import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 使用者資料庫


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64))
    intro = db.Column(db.Text)

    def __init__(self, username,user_id, password, role):
        # 初始化
        self.username = username
        self.user_id = user_id
        # 存入hash password
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.intro = ''

    def check_password(self, password):
        # 檢查使用者密碼
        return check_password_hash(self.password_hash, password)

# 物資資料庫


class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    uploader = db.Column(db.String(64))
    uploader_id = db.Column(db.String(64))
    product_name = db.Column(db.String(64))
    product_details = db.Column(db.Text)
    image = db.Column(db.String(128))
    quantities = db.Column(db.Integer)
    brand = db.Column(db.String(128))
    expiration_date = db.Column(db.String(64))
    date_posted = db.Column(db.String(64))
    '''
    def __init__(self,uploader,uploader_id,product_name,product_details,image,quantities,brand,expiraion_date,date_posted):
        self.uploader = uploader
        self.uploader_id = uploader_id
        self.product_name = product_name
        self.product_details = product_details
        self.image = image
        self.quantities = quantities
        self.brand = brand
        self.expiraion_date = expiraion_date
        self.date_posted = date_posted
    '''


class Volunteer(db.Model):
    __tablename__='volunteer'
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.String(64),unique=True,index=True)
    name = db.Column(db.String(64))
    experience = db.Column(db.Text)
    reason = db.Column(db.Text)
    professional = db.Column(db.Text)
    time = db.Column(db.Text)
    contact = db.Column(db.String(64))
    def __init__(self,volunteer_id,name,experience,reason,professional,time,contact):
        self.volunteer_id = volunteer_id
        self.name=name
        self.experience=experience
        self.reason=reason
        self.professional=professional
        self.time=time
        self.contact=contact

with app.app_context():
    db.create_all()

#db.create_all() 
db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
