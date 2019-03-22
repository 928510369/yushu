from threading import Thread

from flask import render_template, current_app
from flask_mail import Message

from apps import mail


def send_async_email(app,msg):

    try:
        with app.app_context():
            mail.send(msg)
    except Exception:
        pass


def send_mail(to,subject,template,**kwargs):
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'], recipients=[to])

    msg.html = render_template(template + '.html', **kwargs)
    app=current_app._get_current_object()
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr
