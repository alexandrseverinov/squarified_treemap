class Rectangle:
    def __init__(self, x, y, height, width):
        self.left_bottom_x = x
        self.left_bottom_y = y

        self.left_top_x = x
        self.left_top_y = y + height

        self.right_bottom_x = x + width
        self.right_bottom_y = y

        self.right_top_x = x + width
        self.right_top_y = y + height

        self.height = height
        self.width = width

    def get_area(self):
        return self.height * self.width
