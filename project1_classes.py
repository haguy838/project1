import random

class color_square:
    def __init__(self, top, right, bottom, left, line_width):

        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.line = line_width


    def grow(self):
        self.top = (self.top[0], self.top[1] + 25)
        self.bottom = (self.bottom[0], self.bottom[1] - 25)
        self.left = (self.left[0]-15, self.left[1])
        self.right = (self.right[0]+15, self.right[1])


class rand_circ:

    def __init__(self, color,start, size):

        self.color = color
        self.start = start
        self.size = size

    def shrink(self):
        self.size = (self.size - 8)



