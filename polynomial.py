class Polynomial:

    def __init__(self, *coeff):
        if isinstance(list(coeff)[0], dict):
            a = []
            d = list(coeff)[0]
            for element in d:
                a.append(element)
            length = max(a)
            self.coeffs = []
            for i in range(length + 1):
                if i in d:
                    self.coeffs.append(d[i])
                else:
                    self.coeffs.append(0)
        elif isinstance(coeff[0], list):
            self.coeffs = coeff[0]
        elif isinstance(coeff[0], Polynomial):
            self.coeffs = coeff[0].coeffs
        else:
            self.coeffs = list(coeff)
        j = len(self.coeffs) - 1
        while self.coeffs[j] == 0 and j > 0:
            j -= 1
        if j == 0:
            ans = self.coeffs[0]
            self.coeffs = []
            self.coeffs.append(ans)
        else:
            self.coeffs = self.coeffs[:j + 1]

    def __repr__(self):
        return "Polynomial " + str(self.coeffs)

    def __str__(self):
        ans = ""
        for i in range(1, len(self.coeffs) + 1):
            if self.coeffs[-i] == 0:
                continue
            elif self.coeffs[-i] > 0:
                ans += " + "
            else:
                ans += " - "
            if abs(self.coeffs[-i]) != 1 or len(self.coeffs) - i == 0:
                ans += str(abs(self.coeffs[-i]))
            if len(self.coeffs) - i > 0:
                ans += "x"
            if len(self.coeffs) - i > 1:
                ans += "^" + str(len(self.coeffs) - i)
        if ans[1] == "+":
            ans = ans[3:]
        elif ans[1] == "-":
            ans = "-" + ans[3:]
        return ans

    def __eq__(self, other):
        if isinstance(other, int):
            if len(self.coeffs) == 1 and self.coeffs[0] == other:
                return True
            else:
                return False
        elif isinstance(other, Polynomial):
            if self.coeffs == other.coeffs:
                return True
            else:
                return False
        else:
            return False

    def __add__(self, other):
        ans = Polynomial([element for element in self.coeffs])
        if isinstance(other, (float, int)):
            ans.coeffs[0] += other
        elif isinstance(other, Polynomial):
            l0 = len(self.coeffs)
            l1 = len(other.coeffs)
            length = min(l0, l1)
            for i in range(length):
                ans.coeffs[i] += other.coeffs[i]
            if l0 < l1:
                for i in range(l0, l1):
                    ans.coeffs.append(other.coeffs[i])
        return Polynomial(ans.coeffs)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        new = Polynomial(self.coeffs)
        for i in range(len(new.coeffs)):
            new.coeffs[i] = -new.coeffs[i]
        return new

    def __pos__(self):
        return Polynomial(self.coeffs)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __call__(self, x):
        result = 0
        length = len(self.coeffs)
        for i in range(length):
            result += self.coeffs[i] * (x ** i)
        return result

    def degree(self):
        return len(self.coeffs) - 1

    def der(self, d=1):
        if d > self.degree():
            return Polynomial(0)
        new = Polynomial(self)
        for k in range(d):
            for i in range(len(new.coeffs)):
                new.coeffs[i] *= i
            new.coeffs = new.coeffs[1:]
        if len(new.coeffs) == 0:
            return Polynomial([0])
        return new

    def __mul__(self, other):
        l0 = len(self.coeffs)
        if isinstance(other, Polynomial):
            l1 = len(other.coeffs)
            ans = [0 for i in range(l0 + l1)]
            for i in range(l0):
                for j in range(l1):
                    ans[i + j] += self.coeffs[i] * other.coeffs[j]
            return Polynomial(ans)
        elif isinstance(other, (float, int)):
            ans = []
            for i in range(l0):
                ans.append(self.coeffs[i] * other)
            return Polynomial(ans)

    def __rmul__(self, other):
        return self * other

    def __iter__(self):
        ans = []
        i = 0
        while i < len(self.coeffs):
            if self.coeffs[i] != 0:
                ans.append((i, self.coeffs[i]))
            i += 1
        return iter(ans)

    def __next__(self):
        return next(self)

class NotOddDegreeException(Exception):
    def __init__(self):
        pass

class DegreeIsTooBigException(Exception):
    def __init__(self):
        pass

class RealPolynomial(Polynomial):
    def __init__(self, *coefficients):
        if isinstance(coefficients[0], (Polynomial, list, dict)):
            super().__init__(coefficients[0])
        else:
            super().__init__(coefficients)
        if self.degree() % 2 != 1:
            raise NotOddDegreeException

    def find_root(self):
        s = -1
        e = 1
        while (self(s) > 0 and self(e) > 0) or (self(s) < 0 and self(e) < 0):
            s *= 2
            e *= 2
        if self(s) == 0:
            return s
        if self(e) == 0:
            return e
        vs = self(s)
        ve = self(e)
        while abs(ve - vs) >= 1e-6:
            m = (s + e) / 2
            vm = self(m)
            if vs == 0:
                return s
            if ve == 0:
                return e
            if vm == 0:
                return m
            if (vs < 0 and vm > 0) or (vs > 0 and vm < 0):
                e = m
            if (ve < 0 and vm > 0) or (ve > 0 and vm < 0):
                s = m
            vs = self(s)
            ve = self(e)
        return (e + s) / 2


class QuadraticPolynomial(Polynomial):
    def __init__(self, *coeff):
        if isinstance(coeff[0], (Polynomial, list, dict)):
            super().__init__(coeff[0])
        else:
            super().__init__(coeff)
        if self.degree() > 2:
            raise DegreeIsTooBigException

    def solve(self):
        if len(self.coeffs) == 3:
            a, b, c = self.coeffs[2], self.coeffs[1], self.coeffs[0]
            disc = b ** 2 - (4 * a * c)
            if disc > 0:
                x1 = (-b + disc ** (1 / 2)) / (2 * a)
                x2 = (-b - disc ** (1 / 2)) / (2 * a)
                return [x1, x2]
            elif disc == 0:
                x = -b / (2 * a)
                return [x]
            else:
                return []
        elif len(self.coeffs) == 2:
            b, c = self.coeffs[1], self.coeffs[0]
            x = -c / b
            return [x]
        else:
            return []
