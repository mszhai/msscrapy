
def g():
    print('1')
    x = yield 'hello'
    print('2' + 'x='+ x)
    y = 5 + (yield x)
    print('3' + 'y=' + y)

if __name__ == '__main__':
    f = g()
    f.send(5)