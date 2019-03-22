from flask_login import login_user

from . import web

from flask import render_template, request, redirect, url_for, flash
from apps.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPassword
from apps.models.base import db
from apps.models.user import User

__author__ = '七月'


@web.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm(request.form)
    if request.method=="POST" and form.validate():
        user=User()
        user.set_attrs(form.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("web.login"))
    return render_template("auth/register.html",form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method=="POST" and form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user,remember=True)
            next=request.args.get("next")
            print("next", next)
            if  not next or not next.startswith("/"):
                next=url_for("web.index")

            return redirect(next)
        else:
            flash("该用户不存在或者密码错误")
            # return redirect(url_for("web.index"))
    return render_template("auth/login.html",form=form)


@web.route('/reset/password/', methods=['GET', 'POST'])
def forget_password_request():
    form=EmailForm(request.form)
    if request.method=="POST":
        if form.validate():
            account_email=form.email.data
            user=User.query.filter_by(email=account_email).first_or_404()
            from apps.libs.email import send_mail
            send_mail(account_email,"重置你的密码","email/reset_password",user=user,token=user.get_tokon())
            flash("你的修改密码邮件已发送成功"+account_email+"请及时查收")
    return render_template("auth/forget_password_request.html",form=form)



@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form=ResetPassword(request.form)
    if request.method=="POST" and form.validate():
        res=User.reset_password(token,form.password1.data)
        if res:
            flash("密码已经更新成功")
            return redirect(url_for("web.login"))

        else:
            flash("密码重置失败")


    return render_template("auth/forget_password.html")


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
   pass


@web.route('/logout')

def logout():
    pass


@web.route('/register/confirm/<token>')
def confirm(token):
    pass
    # if current_user.confirmed:
    #     return redirect(url_for('main.index'))
    # if current_user.confirm(token):
    #     db.session.commit()
    #     flash('You have confirmed your account. Thanks!')
    # else:
    #     flash('The confirmation link is invalid or has expired.')
    # return redirect(url_for('main.index'))


@web.route('/register/ajax', methods=['GET', 'POST'])
def register_ajax():
    pass


