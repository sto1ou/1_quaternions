import math


class Quaternion:
    # Инициализация кватерниона
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    # Представление кватерниона в читаемом формате
    def __repr__(self):
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    # Операция сложения двух кватернионов
    def __add__(self, other):
        return Quaternion(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    # Операция вычитания двух кватернионов
    def __sub__(self, other):
        return Quaternion(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    # Операция умножения двух кватернионов
    def __mul__(self, other):
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z
        z = self.w * other.z + self.x * other.y + self.z * other.w - self.y * other.x
        return Quaternion(w, x, y, z)

    # Вычисление модуля кватерниона
    def __abs__(self):
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    # Вычисление сопряжения кватерниона
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    # Вычисление обратного кватерниона
    def inverse(self):
        mod_squared = abs(self) ** 2
        conjugate = self.conjugate()
        return Quaternion(
            conjugate.w / mod_squared,
            conjugate.x / mod_squared,
            conjugate.y / mod_squared,
            conjugate.z / mod_squared
        )

    # Переопределение оператора деления для кватернионов
    def __truediv__(self, other):
        return self * other.inverse()

    # Поворот вектора в пространстве с помощью кватерниона
    def rotate_vector(self, vector):
        # Преобразуем вектор в кватернион с нулевой скалярной частью
        vec_quaternion = Quaternion(0, *vector)
        # Выполним поворот: q * v * q^(-1)
        rotated = self * vec_quaternion * self.inverse()
        # Возвращаем только векторную часть (x, y, z)
        return (rotated.x, rotated.y, rotated.z)

    @classmethod
    # Создаёт кватернион поворота на заданный угол вокруг заданной оси
    def from_angle_axis(cls, angle, axis):
        # Нормализуем ось
        x, y, z = axis
        norm = math.sqrt(x*x + y*y + z*z)
        if norm == 0:
            raise ValueError("Ось не может быть нулевым вектором")
        x /= norm
        y /= norm
        z /= norm

        half_angle = angle / 2.0
        s = math.sin(half_angle)
        c = math.cos(half_angle)

        return cls(c, x * s, y * s, z * s)

    # Преобразует кватернион поворота в угол и ось
    def to_angle_axis(self):
        # Для единичного кватерниона (поворот)
        q = self
        # Нормализуем на всякий случай
        norm = abs(q)
        if norm == 0:
            raise ValueError("Нулевой кватернион не может представлять поворот")
        w = q.w / norm
        x = q.x / norm
        y = q.y / norm
        z = q.z / norm

        angle = 2 * math.acos(w)
        # Чтобы избежать проблем с численной точностью
        sin_half_angle = math.sqrt(1 - w*w)
        if sin_half_angle < 1e-12:
            # Угол близок к 0 или pi, ось не определена однозначно
            return angle, (1.0, 0.0, 0.0)
        else:
            ax = x / sin_half_angle
            ay = y / sin_half_angle
            az = z / sin_half_angle
            return angle, (ax, ay, az)

    # Проверка равенства двух кватернионов
    def __eq__(self, other):
        if not isinstance(other, Quaternion):
            return NotImplemented
        return math.isclose(self.w, other.w, rel_tol=1e-9) and \
            math.isclose(self.x, other.x, rel_tol=1e-9) and \
            math.isclose(self.y, other.y, rel_tol=1e-9) and \
            math.isclose(self.z, other.z, rel_tol=1e-9)