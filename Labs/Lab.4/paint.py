import math


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, h, **kargs):
        for i in range(x, x+h):
            self.set_pixel(i, y, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(y, y+w):
            self.set_pixel(x, i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (x2-x1) / (y2-y1)
        for y in range(y1, y2):
            x = x1 + int(slope * (y-y1))
            self.set_pixel(x, y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))


class Shape:
    def __init__(self, x, y, name=""):
        self.__x = x
        self.__y = y
        self.name = name
        
    def area(self):
        raise NotImplementedError

    def perimeter(self):
        raise NotImplementedError

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_perimeter_points(self):
        raise NotImplementedError

    def contains(self, x, y):
        raise NotImplementedError

    def overlaps(self, other):
        for point in self.get_perimeter_points():
            if other.contains(point[0], point[1]):
                return True

        for point in other.get_perimeter_points():
            if self.contains(point[0], point[1]):
                return True

        return False

    def paint(self, canvas):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        super().__init__(x, y)
        self.__length = length
        self.__width = width

    def area(self):
        return self.__length * self.__width

    def perimeter(self):
        return 2 * (self.__length + self.__width)

    def get_perimeter_points(self):
        x = self.get_x()
        y = self.get_y()

        return [
            (x, y),
            (x + self.__length, y),
            (x + self.__length, y + self.__width),
            (x, y + self.__width)
        ]

    def contains(self, x, y):
        return (
            self.get_x() <= x <= self.get_x() + self.__length
            and
            self.get_y() <= y <= self.get_y() + self.__width
        )

    def paint(self, canvas):
        for x in range(self.get_x(), self.get_x() + self.__length + 1):
            canvas.set_pixel(self.get_y(), x)
            canvas.set_pixel(self.get_y() + self.__width, x)

        for y in range(self.get_y(), self.get_y() + self.__width + 1):
            canvas.set_pixel(y, self.get_x())
            canvas.set_pixel(y, self.get_x() + self.__length)

    def __repr__(self):
        return f"Rectangle({self.__length}, {self.__width}, {self.get_x()}, {self.get_y()})"


class Circle(Shape):
    def __init__(self, radius, x, y):
        super().__init__(x, y)
        self.__radius = radius

    def area(self):
        return math.pi * self.__radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.__radius

    def get_perimeter_points(self):
        points = []

        for i in range(16):
            angle = 2 * math.pi * i / 16
            x = self.get_x() + self.__radius * math.cos(angle)
            y = self.get_y() + self.__radius * math.sin(angle)
            points.append((x, y))

        return points

    def contains(self, x, y):
        distance = math.sqrt(
            (x - self.get_x()) ** 2 +
            (y - self.get_y()) ** 2
        )

        return distance <= self.__radius

    def paint(self, canvas):
        for point in self.get_perimeter_points():
            x = round(point[0])
            y = round(point[1])

            if 0 <= y < canvas.height and 0 <= x < canvas.width:
                canvas.set_pixel(y, x)

    def __repr__(self):
        return f"Circle({self.__radius}, {self.get_x()}, {self.get_y()})"


class Triangle(Shape):
    def __init__(self, side1, side2, side3, base, height, x, y):
        super().__init__(x, y)
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3
        self.__base = base
        self.__height = height

    def area(self):
        return 0.5 * self.__base * self.__height

    def perimeter(self):
        return self.__side1 + self.__side2 + self.__side3

    def get_side1(self):
        return self.__side1

    def get_side2(self):
        return self.__side2

    def get_side3(self):
        return self.__side3

    def get_base(self):
        return self.__base

    def get_height(self):
        return self.__height

    def get_perimeter_points(self):
        x = self.get_x()
        y = self.get_y()

        return [
            (x, y),
            (x + self.__base, y),
            (x + self.__base / 2, y + self.__height)
        ]

    def contains(self, x, y):
        x0 = self.get_x()
        y0 = self.get_y()

        if y < y0 or y > y0 + self.__height:
            return False

        half_width = (self.__base / 2) * (1 - (y - y0) / self.__height)

        return (
            x0 + self.__base / 2 - half_width
            <= x
            <= x0 + self.__base / 2 + half_width
        )

    def paint(self, canvas):
        points = self.get_perimeter_points()

        for x in range(round(points[0][0]), round(points[1][0]) + 1):
            canvas.set_pixel(round(points[0][1]), x)

        for i in range(16):
            t = i / 15
            x = round(
                points[0][0] +
                t * (points[2][0] - points[0][0])
            )
            y = round(
                points[0][1] +
                t * (points[2][1] - points[0][1])
            )

            if 0 <= y < canvas.height and 0 <= x < canvas.width:
                canvas.set_pixel(y, x)

        for i in range(16):
            t = i / 15
            x = round(
                points[1][0] +
                t * (points[2][0] - points[1][0])
            )
            y = round(
                points[1][1] +
                t * (points[2][1] - points[1][1])
            )

            if 0 <= y < canvas.height and 0 <= x < canvas.width:
                canvas.set_pixel(y, x)

    def __repr__(self):
        return f"Triangle({self.__side1}, {self.__side2}, {self.__side3}, {self.__base}, {self.__height}, {self.get_x()}, {self.get_y()})"


class CompoundShape(Shape):
    def __init__(self, shapes):
        super().__init__(0, 0)
        self.shapes = shapes

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)

    def __repr__(self):
        return f"CompoundShape([{', '.join(repr(s) for s in self.shapes)}])"

class RasterDrawing:
    def __init__(self):
        self.shapes = dict()
        self.shape_names = list()

    def add_shape(self, shape):
        if shape.name == "":
            shape.name = self.assign_name()

        self.shapes[shape.name] = shape
        self.shape_names.append(shape.name)

    def update(self, canvas):
        canvas.clear_canvas()
        self.paint(canvas)

    def paint(self, canvas):
        for shape_name in self.shape_names:
            self.shapes[shape_name].paint(canvas)

    def assign_name(self):
        name_base = "shape"
        name = name_base + "_0"

        i = 1
        while name in self.shapes:
            name = name_base + "_" + str(i)
            i += 1

        return name

    def __repr__(self):
        lines = []

        for shape_name in self.shape_names:
            lines.append(
                f"rd.add_shape({repr(self.shapes[shape_name])})"
            )

        return "\n".join(lines)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(repr(self))

    @staticmethod
    def load(filename):
        rd = RasterDrawing()

        with open(filename, "r") as f:
            for line in f:
                eval(
                    line,
                    {
                        "rd": rd,
                        "Rectangle": Rectangle,
                        "Circle": Circle,
                        "Triangle": Triangle,
                        "CompoundShape": CompoundShape
                    }
                )

        return rd