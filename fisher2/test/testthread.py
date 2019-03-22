from threading import Thread


def printhello():
    print("hello")


t=Thread(target=printhello)
t.start()