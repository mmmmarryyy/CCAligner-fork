import math


class Point(object):
    """
    Creates a point on a coordinate plane with values x and y.
    """
    def bazz(self):
        f = 123123
        a = 124432
        return f + a + f

    COUNT = 0
    a = 1242314132421 + 123
    def __init__(self, x, y):
        '''Defines x and y variables'''
        self.a = "https://www.codingconception.com/python-examples/ \
        write-a-program-to-delete-comment-lines-from-a-file-in-python/"
        self.X = x; self.Y = y

    def move(self, dx, dy):
        '''Determines where x and y move'''
        self.X =self.X + dx
        self.Y= self.Y + dy

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y) # kek lol ekeeke
#dkfljsdlfsldk

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def distance(self, other):
        dx = self.X - other.X
        dy = self.Y - other.Y
        return math.sqrt(dx**2 + dy**2)


