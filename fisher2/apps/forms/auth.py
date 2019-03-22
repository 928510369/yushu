
from wtforms import StringField, PasswordField, Form, ValidationError
from wtforms.validators import DataRequired, Length, Email, length, EqualTo

from apps.models.user import User


class EmailForm(Form):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
                                            Email(message='电子邮箱不符合规范')])

class RegisterForm(EmailForm):
    nickname = StringField('昵称', validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])

    password = PasswordField('密码', validators=[
        DataRequired(), Length(6, 20)])


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已经被注册")

        def validate_nickname(self, field):
            if User.query.filter_by(nickname=field.data).first():
                raise ValidationError('昵称已存在')


class LoginForm(EmailForm):
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可以为空，请输入你的密码')])

class ResetPassword(Form):
    password1=PasswordField("新密码",validators=[DataRequired(),length(6.32,message="密码长度必须多于6个字符少于32个字符"),
                            EqualTo("password2",message="两个密码必须相同")]
                            )
    password2=PasswordField("确认新密码",validators=[DataRequired(),length(6,32)])

