from contextlib import contextmanager


class MyResource():
    # def __enter__(self):
    #     print("链接资源")
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     #后三个参数设计用来处理异常，该函数返回true函数外不会出现异常否侧出现异常
    #     if exc_tb:
    #         print("出现异常")
    #
    #     print('释放资源')
    #     return True

    def query(self):
        print("查询资源")



@contextmanager
def query_sth():
    print("链接资源")

    yield MyResource()

    print('释放资源')

with query_sth():#f就是__enter__返回的值
    MyResource().query()