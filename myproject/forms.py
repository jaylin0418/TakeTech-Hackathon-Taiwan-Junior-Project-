from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, DateField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, Email, EqualTo, email_validator
from wtforms import ValidationError
from wtforms.widgets.core import TextArea


class RegistrationForm(FlaskForm):
    username = StringField('你的Email帳號', validators=[DataRequired()])
    user_id = StringField('使用者名稱',validators=[DataRequired()])
    role = RadioField('請輸入您要註冊的身份', choices=[
                      ('G', '受捐助機構申請'), ('I', '個人捐助者申請')])
    password = PasswordField(
        '密碼', validators=[DataRequired(), EqualTo('pass_confirm', message='密碼需要吻合')])
    pass_confirm = PasswordField('確認密碼', validators=[DataRequired()])
    submit = SubmitField('註冊')


class LoginForm(FlaskForm):
    username = StringField('你的Email帳號', validators=[DataRequired()])
    password = PasswordField('密碼', validators=[DataRequired()])
    submit = SubmitField('登入系統')


class ProductForm(FlaskForm):
    product_name = StringField('裝置名稱', validators=[DataRequired()])
    product_details = TextField('裝置概述、細節', validators=[DataRequired()])
    image = StringField('裝置照片連結')
    quantities = IntegerField('裝置數量', validators=[DataRequired()])
    brand = StringField('裝置品牌', validators=[DataRequired()])
    expiration_date = DateField('保固日期', format='%Y-%m-%d', validators=[DataRequired()])
    date_posted = DateField('上傳日期', format='%Y-%m-%d')
    submit = SubmitField('公布裝置')

class ApplyForm(FlaskForm):
    sender = StringField('寄件者',validators=[DataRequired()])
    reciever = StringField('收件者', validators=[DataRequired()])
    content = TextField("申請原因、計畫",validators=[DataRequired()])
    submit = SubmitField('寄出申請信')

class VolunteerForm(FlaskForm):
    name = StringField('您的大名',validators=[DataRequired()])
    age = IntegerField('寄件者',validators=[DataRequired()])
    experience = TextField("過去志工經驗",validators=[DataRequired()])
    reason = TextField("申請原因",validators=[DataRequired()])
    professional = TextField("專長",validators=[DataRequired()])
    time = TextField('您可以服務的時間（月份、星期幾、時間）等等',validators=[DataRequired()])
    contact = StringField('聯絡方式（需要志工的機構會透過此方式聯絡您）',validators=[DataRequired()])
    submit = SubmitField('成為志工')

class SearchForm(FlaskForm):
    word = StringField('以物品名稱查詢',validators=[DataRequired()])
    submit = SubmitField('搜尋')