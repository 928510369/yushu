from flask import Flask,current_app

app=Flask(__name__)
#进行单元测试，离线应用
# ctx=app.app_context()
# ctx.push()
# a=current_app
# print(a)
# a.pop()

with app.app_context():
    a = current_app
    print(a)



