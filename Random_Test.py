class Fater():
    def __init__(self, money=100):
        self.money = money

        def fun(self):
            print('very funny')


class Son(Fater):
    def __init__(self, money=200):
        super().__init__(money)


class Kid(Fater):
    pass

    def operator(self):
        pass

    operator.short_description = '操作'


Ko = Kid().operator()
print(Ko)
s = Son()
k = Kid()
k2 = Kid(2)
print(k2.money)
print(k.money)
print(s.money)
