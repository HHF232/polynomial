from copy import deepcopy


class Polynomial(object):
    def __init__(self, *coeff):
        if len(coeff) == 1 and isinstance(coeff[0], list):
            listt = deepcopy(list(coeff[0]))
            while listt[-1] == 0 and len(listt) >= 2:
                listt = listt[:len(listt) - 1]
            self.coeff = listt
        elif len(coeff) == 1 and isinstance(coeff[0], dict):
            listt = []
            dictt = deepcopy(dict(coeff[0]))
            for i in range(max(dictt.keys()) + 1):
                if i in dictt.keys():
                    listt.append(dictt[i])
                else:
                    listt.append(0)
            while listt[-1] == 0 and len(listt) >= 2:
                listt = listt[:len(listt) - 1]
            self.coeff = listt
        elif isinstance(coeff[0], int):
            listt = deepcopy(list(coeff))
            while listt[-1] == 0 and len(listt) >= 2:
                listt = listt[:len(listt) - 1]
            self.coeff = listt
        else:
            raise BaseException(self)

    def __repr__(self):
        coeff = self.coeff
        while coeff[-1] == 0:
            coeff = coeff[:len(coeff) - 1]
        ret = "Polynomial ["
        for i in range(len(coeff)):
            ret += str(coeff[i]) + ", "
        ret = ret[:len(ret) - 2] + "]"
        return ret

    def __str__(self):
        poly = ""
        for i in range(len(self.coeff)):
            if self.coeff[i] != 0:
                if i == 0:
                    poly += str(self.coeff[i])
                elif i == 1:
                    if self.coeff[i] != 1 and self.coeff[i] != -1:
                        poly = str(self.coeff[i]) + "x" + " + " + poly
                    elif self.coeff[i] == 1:
                        poly = "x" + " + " + poly
                    else:
                        poly = "-x" + " + " + poly
                elif self.coeff[i] != 1 and self.coeff[i] != -1:
                    poly = str(self.coeff[i]) + "x^" + str(i) + " + " + poly
                elif self.coeff[i] == -1:
                    poly = "-x^" + str(i) + " + " + poly
                else:
                    poly = "x^" + str(i) + " + " + poly
        if self.coeff[0] == 0:
            poly = poly[:len(poly) - 3]
        for i in range(len(poly)):
            if poly[i: i + 3] == "+ -":
                poly = poly[:i] + "- " + poly[i + 3:]
        if poly == "":
            return "0"
        else:
            return poly

    def degree(self):
        return len(self.coeff) - 1

    def __add__(self, other):
        if isinstance(other, Polynomial) and isinstance(self, Polynomial):
            answ = []
            if len(self.coeff) >= len(other.coeff):
                list2 = other.coeff
                for i in range(len(self.coeff) - len(other.coeff)):
                    list2.append(0)
                for i in range(len(self.coeff)):
                    answ.append(self.coeff[i] + list2[i])
            else:
                list2 = self.coeff
                for i in range(len(other.coeff) - len(self.coeff)):
                    list2.append(0)
                for i in range(len(list2)):
                    answ.append(list2[i] + other.coeff[i])
            return Polynomial(answ)
        elif isinstance(other, int) and isinstance(self, Polynomial):
            answ = self.coeff
            answ[0] = answ[0] + other
            return Polynomial(answ)
        else:
            raise BaseException(self)

    def __radd__(self, other):
        poly1 = deepcopy(self)
        poly2 = deepcopy(other)
        if isinstance(other, Polynomial) and isinstance(self, Polynomial):
            return poly1 + poly2
        elif isinstance(other, int) and isinstance(self, Polynomial):
            return poly1 + poly2
        else:
            raise BaseException(self)

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            answ = []
            if len(self.coeff) >= len(other.coeff):
                for i in range(len(other.coeff)):
                    answ.append(self.coeff[i] - other.coeff[i])
                answ += self.coeff[len(other.coeff):]
            else:
                for i in range(len(self.coeff)):
                    answ.append(self.coeff[i] - other.coeff[i])
                answ += list(map(lambda x: -x, other.coeff[len(other.coeff):]))
            return Polynomial(answ)
        elif isinstance(other, int):
            answ = deepcopy(self.coeff)
            answ[0] = answ[0] - other
            return Polynomial(answ)
        else:
            raise BaseException(self)

    def __rsub__(self, other):
        poly1 = deepcopy(self)
        poly2 = deepcopy(other)
        if isinstance(other, Polynomial):
            return poly2 - poly1
        elif isinstance(other, int):
            ans = deepcopy(self.coeff)
            for i in range(len(ans)):
                ans[i] = (-1) * ans[i]
            return Polynomial(ans) + other
        else:
            raise BaseException(self)

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            if len(self.coeff) != len(other.coeff):
                return False
            else:
                for i in range(len(self.coeff)):
                    if self.coeff[i] != other.coeff[i]:
                        return False
            return True
        else:
            raise BaseException(self, other)

    def __call__(self, x):
        if isinstance(x, float) or isinstance(x, int):
            summ = self.coeff[0]
            for i in range(1, len(self.coeff)):
                summ += self.coeff[i] * (x ** i)
            return summ
        else:
            raise BaseException(self)

    def __mul__(self, other):
        if isinstance(other, int):
            res = []
            for i in range(len(self.coeff)):
                res.append(self.coeff[i] * other)
            return Polynomial(res)
        elif isinstance(other, Polynomial):
            res = [self.coeff[0] * other.coeff[0]]
            for i in range(1, self.degree() + other.degree() + 1):
                coeff_res = 0
                for j in range(max(0, i - other.degree()), min(i, self.degree()) + 1):
                    coeff_res += self.coeff[j] * other.coeff[i - j]
                res.append(coeff_res)
            return Polynomial(res)
        else:
            raise BaseException(self, other)

    def __rmul__(self, other):
        return Polynomial(other) * Polynomial(self)

    def __mod__(self, other):
        if isinstance(other, int):
            ans = []
            for i in range(len(self.coeff)):
                ans.append(self.coeff[i] % other)

            return Polynomial(ans)
        elif isinstance(other, Polynomial):
            if self.degree() < other.degree():
                raise BaseException(self, other)
            else:
                l1 = list(self.coeff)
                l2 = list(other.coeff)
                l1.reverse()
                l2.reverse()
                k = l1[0] / l2[0]
                for i in range(len(l2)):
                    l1[i] -= (l2[i] * k)
                l1 = l1[1:]
                while len(l1) >= len(l2):
                    k = l1[0] / l2[0]
                    for i in range(len(l2)):
                        l1[i] -= (l2[i] * k)
                    l1 = l1[1:]
                l1.reverse()
                if len(l1) == 0 or set(l1) == {0}:
                    return Polynomial([0])
                else:
                    return Polynomial(l1)
        else:
            raise BaseException(self, other)

    def gcd(self, other):
        if isinstance(other, Polynomial):
            m1 = deepcopy(self)
            m2 = deepcopy(other)
            if m1.degree() < m2.degree():
                m3 = m1
                m1 = m2
                m2 = m3
            while str(m1 % m2) != "0":
                m3 = m2
                m2 = m1 % m2
                m1 = m3
            return m2
        else:
            raise BaseException(self, other)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.degree():
            monome = (self.n, self.coeff[self.n])
            self.n += 1
            return monome
        else:
            raise StopIteration
