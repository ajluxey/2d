import pygame as pg
from math import sin, cos

METER = 150


class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.l = self.calc_len()

    def mul_num(self, k):
        return Vec2(self.x * k, self.y * k)

    def dev_num(self, k):
        return Vec2(self.x / k, self.y / k) if k != 0 else 0

    def calc_len(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def calc_unit(self):
        return Vec2(self.x / self.l, self.y / self.l) if self.l != 0 else Vec2()

    def __len__(self):
        return self.l

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f'V({self.x}, {self.y})'

    def __repr__(self):
        return str(self)


class Force:
    def __init__(self, vec=None):
        self.vec = Vec2() if vec is None else vec

    @classmethod
    def from_cords(cls, x=0, y=0):
        return cls(Vec2(x, y))

    @classmethod
    def from_obj(cls, obj):
        return cls(obj.resultant_force().dev_num(obj.mass))

    def __add__(self, other):
        return Force(self.vec + other.vec)

    def __sub__(self, other):
        return Force(self.vec - other.vec)

    def mul_num(self, k):
        return self.vec.mul_num(k)

    def dev_num(self, k):
        return self.vec.dev_num(k)

    def __str__(self):
        return f'F({self.vec.x}, {self.vec.y})'

    def __repr__(self):
        return str(self)


class Engine:
    def __init__(self, width=600, height=600, fps=60):
        self.width, self.height = width, height
        self.fps = fps
        pg.init()
        self.surface = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.objects = []

    def add_obj(self, obj):
        self.objects.append(obj)

    def calculation(self):
        for obj in self.objects:
            fps = self.clock.get_fps()
            t = 1 / fps if fps != 0 else 0
            obj.move_during(t, METER)

    def render(self):
        self.surface.fill('black')
        for obj in self.objects:
            obj.draw(self.surface)

    def run(self):
        RUN_FLAG = True
        while RUN_FLAG:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    RUN_FLAG = False
                    break
            self.calculation()
            self.render()
            pg.display.set_caption(f'max fps: {self.fps}, fps now: ' + str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.fps)


class Object2d:
    def __init__(self, x, y, angle=0, static=True, speed=None, mass=1):
        self.x = x
        self.y = y
        self.angle = angle
        self.static = static  # True/False
        self.speed = Vec2() if speed is None or static else speed

        self.mass = mass
        self.forces = [Force(Vec2(0, -9.8))]

    def a(self):
        if not self.static and self.mass != 0:
            return self.resultant_force().dev_num(self.mass)
        else:
            return Vec2()

    def resultant_force(self):
        return sum(self.forces, Force()) if not self.static else 0

    def move_during(self, t, coef):
        a = self.a()
        Va = a.mul_num(t)
        self.speed += Va
        S = self.speed.mul_num(t)
        self.x += S.x * coef
        self.y += S.y * coef

    def drawing_coords(self, surface):
        _, h = surface.get_size()
        return self.x, h-self.y


class Circle(Object2d):
    def __init__(self, x=None, y=None, angle=0, static=True, speed=None, mass=1, c1='green', c2='yellow'):
        super().__init__(x, y, angle, static, speed, mass)
        self.radius = int(15/150*METER)
        self.width = int(5/150*METER)
        self.c1 = c1
        self.c2 = c2

    def draw(self, surface):
        x, y = self.drawing_coords(surface)
        pg.draw.circle(surface, self.c1, (x, y), self.radius)
        pg.draw.circle(surface, self.c2, (x, y), self.radius - self.width)
        end_x, end_y = x + self.radius * sin(self.angle), y + self.radius * cos(self.angle)
        pg.draw.line(surface, self.c1, (x, y), (end_x-self.width, end_y-self.width), self.width)


if __name__ == '__main__':
    width, height = 1000, 600
    e = Engine(width, height)
    # c = Circle(0, 450, static=False, speed=Vec2(8, 4))
    # e.add_obj(c)
    colors = ['red', 'white', 'green', 'black', 'blue', 'orange', 'yellow']
    from random import choice, randint, random as r
    for _ in range(1000):
        c1, c2 = choice(colors), choice(colors)
        s_x, s_y = width // 2 , height // 2
        # s_x, s_y = randint(0, width), randint(0, height)
        speed = Vec2(randint(-8, 8)*r(), randint(0, 10)*r())
        e.add_obj(Circle(s_x, s_y, static=False, speed=speed, c1=c1, c2=c2))
    e.run()
