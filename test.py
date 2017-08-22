

class share(object):
    def __init__(self,code,price):
        self.pppp=code
        self.price=price
    def sum(self):
        print 11
        print self.pppp
        print 11

print share('003',13.2).sum()