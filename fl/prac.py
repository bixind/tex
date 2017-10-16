# -*- coding: utf-8 -*-

# Если регулярное выражение некорректно, будет выдана эта ошибка
class ParseError(Exception):
    pass

# В этом классе хранится информация о том, какие части слова принимаются регулярным выражением:
# accept[i][j] == 0 <=> соответсвующая часть регулярного выражения принимает подслово word[i:j]
# pref[i] == k <=> максимальная длина общего префикса слова word[i:] и какого-то
# слова из языка, принимаемого соответсвующим регулярным выражением, равна k
class State:
    def __init__(self, n):
        self.accept = dict()
        self.pref = dict()
        for i in range(n + 1):
            self.pref[i] = 0
        for i in range(n + 1):
            self.accept[i] = dict()
            for j in range(n + 1):
                self.accept[i][j] = False


rg, word = input().split()
n = len(word)



stack = list()
try:
    for a in rg:
        if a.isalpha():
            # если a - буква из алфавита, то инициализация тривиальна
            s = State(n)
            for i in range(n):
                if word[i] == a:
                    s.accept[i][i + 1] = True
                    s.pref[i] = 1
            stack.append(s)
        elif a == '1':
            # тоже тривиально
            s = State(n)
            for i in range(n + 1):
                s.accept[i][i] = True
            stack.append(s)
        elif a == '+':
            s2 = stack.pop()
            s1 = stack.pop()
            # в сумме максимальный префикс - максимум из префиксов
            for i in range(n):
                s1.pref[i] = max(s1.pref[i], s2.pref[i])
            # подслово word[i:j] принимается суммой регулярных
            # выражений <=> оно принимается хотя бы одним из них
            for i in range(n):
                for j in range(n + 1):
                    s1.accept[i][j] |= s2.accept[i][j]
            stack.append(s1)
        elif a == '.':
            s2 = stack.pop()
            s1 = stack.pop()
            s = State(n)
            # префикс произведения - это либо префикс левого операнда,
            # либо он раскладывается на две части, левая из которых
            # принимается левым операндом, а правая - префикс правого
            for i in range(n):
                s.pref[i] = s1.pref[i]
            # j - точка разделения на две части
            for i in range(n):
                for j in range(i, n + 1):
                    if s1.accept[i][j]:
                        s.pref[i] = max(s.pref[i], j - i + s2.pref[j])
            # аналогично, слово принимается произведением,
            # если оно рскладывается на 2 части, левая из которых
            # принимается левым, а правая - правым операндами.
            for i in range(n):
                for j in range(i, n + 1):
                    for k in range(i, j + 1):
                        s.accept[i][j] |= s1.accept[i][k] & s2.accept[k][j]
            stack.append(s)
        elif a == '*':
            s = stack.pop()
            # * может раскрываться и в пустое слово
            for i in range(n + 1):
                s.accept[i][i] = True
            # заметим, что если два каких-то слова
            # принимаются s*, то их конкатенация также принимается s*,
            # и наоборот, если непустое слово принимается s*, то оно либо принимается s,
            # либо раскладывается на 2, которые принимаются s*. Таким образом,
            # если мы вообразим граф на n вершинах, в котором ориентированное рёбро
            # (i, j) присутвует только если word[i:j] принимается s,
            # то его транзитивное замыкание будет соответствовать подсловам, принимаемым s*.
            for h in range(n):
                for i in range(n):
                    for j in range(i, n + 1):
                        for k in range(i, j + 1):
                            s.accept[i][j] |= s.accept[i][k] & s.accept[k][j]
            # очевидно, префикс s* разбивается на префикс s 
            # и часть, принимаемую s*.
            for i in range(n):
                for j in range(i, n + 1):
                    if s.accept[i][j]:
                        s.pref[i] = max(s.pref[i], j - i + s.pref[j])
            stack.append(s)
        else:
            # если символ какой-то непонятный, то выражение некорректно
            raise ParseError
except IndexError:
    # IndexError выбрасывается если в стеке недостаточно элементов
    raise ParseError

if len(stack) != 1:
    raise ParseError

s = stack.pop()
print(s.pref[0])
