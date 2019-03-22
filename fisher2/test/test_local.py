from werkzeug.local import Local,LocalStack
import threading,time

# my_obj=Local()#采用字典，以线程id为key,进行线程隔离
# my_obj.b=1
# def worker():
#     my_obj.b=2
#     print("in new thread "+str(my_obj.b))
#
# a=threading.Thread(target=worker)
#
# a.start()
# print("in main thread "+str(my_obj.b))
#


my_stack=LocalStack()
my_stack.push(1)

print("main threading",my_stack.top)

def worker():
    print("new threading",my_stack.top)
    my_stack.push(2)
    print("new threading", my_stack.top)


t=threading.Thread(target=worker)

t.start()
time.sleep(1)
print("main threading",my_stack.top)




