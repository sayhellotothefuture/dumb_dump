import pandas as pd
import numpy as np
import copy


def xo(symb):
    if symb == 'x':
        compsymb = 'o'
    elif symb == 'o':
        compsymb = 'x'
    pole = [['-' for x in range(3)] for y in range(3)]
    pole = np.array(pole)
    print('Начнем')
    weight = [[0 for x in range(3)] for y in range(3)]
    n = 0
    while (np.sum(pole[0] == compsymb) < 3 and np.sum(pole[1] == compsymb) < 3 and np.sum(pole[2] == compsymb) < 3 and
           np.sum(np.transpose(pole)[0] == compsymb) < 3 and np.sum(np.transpose(pole)[1] == compsymb) < 3 and
           np.sum(np.transpose(pole)[2] == compsymb) < 3 and
           np.sum(np.diagonal(pole) == compsymb) < 3 and
           np.sum(np.diagonal(np.fliplr(pole)) == compsymb) < 3) and \
            ''.join(pole.flatten()).count('-') > 0: # end of the game check
        if symb == 'x' and n == 0: # if player's symbol is x. his first move
            print(pd.DataFrame(pole, columns=['1', '2', '3'], index=['1', '2', '3']))
            print('Введите координаты')
            coord = input()
            x = int(coord[0]) - 1
            y = int(coord[2]) - 1
            pole[x][y] = symb
            n = 1
        weight = [[0 for x in range(3)] for y in range(3)]
        diag = ''.join(np.diagonal(pole))
        pdiag = ''.join(np.diagonal(np.fliplr(pole)))
        for str in range(len(pole)):
            hor = ''.join(pole[str])
            for elem in range(len(pole[str])):
                vert = ''.join(np.transpose(pole)[elem])
                if pole[str][elem] == '-':
                    # make a doublet
                    if compsymb in hor and symb not in hor:
                        weight[str][elem] += 1.1
                    if compsymb in vert and symb not in vert:
                        weight[str][elem] += 1.1
                    if compsymb in diag and symb not in diag and str == elem:
                        weight[str][elem] += 1.1
                    if compsymb in pdiag and symb not in pdiag and (
                            (str == 0 and elem == 2) or (str == 2 and elem == 0) or (str == 1 and elem == 1)):
                        weight[str][elem] += 1.1
                    # get a new line with 1 element
                    if compsymb not in hor and symb not in hor:
                        weight[str][elem] += 1
                    if compsymb not in vert and symb not in vert:
                        weight[str][elem] += 1
                    if compsymb not in diag and symb not in diag and str == elem:
                        weight[str][elem] += 1
                    if compsymb not in pdiag and symb not in pdiag and (
                            (str == 0 and elem == 2) or (str == 2 and elem == 0) or (str == 1 and elem == 1)):
                        weight[str][elem] += 1
                    # intercept player's line of one symbol
                    if hor.count(symb) == 1 and compsymb not in hor:
                        weight[str][elem] += 1.01
                    if vert.count(symb) == 1 and compsymb not in vert:
                        weight[str][elem] += 1.01
                    if diag.count(symb) == 1 and compsymb not in diag and str == elem:
                        weight[str][elem] += 1.01
                    if pdiag.count(symb) == 1 and compsymb not in pdiag and \
                            ((str == 0 and elem == 2) or (str == 2 and elem == 0) or (str == 1 and elem == 1)):
                        weight[str][elem] += 1.01
                    # intercept player's line of two symbols
                    if hor.count(symb) == 2 and compsymb not in hor:
                        weight[str][elem] += 50
                    if vert.count(symb) == 2 and compsymb not in vert:
                        weight[str][elem] += 50
                    if diag.count(symb) == 2 and compsymb not in diag and str == elem:
                        weight[str][elem] += 50
                    if pdiag.count(symb) == 2 and compsymb not in pdiag and \
                            ((str == 0 and elem == 2) or (str == 2 and elem == 0) or (str == 1 and elem == 1)):
                        weight[str][elem] += 50
                    # to win 
                    if hor.count(compsymb) == 2 and symb not in hor:
                        weight[str][elem] += 111
                    if vert.count(compsymb) == 2 and symb not in vert:
                        weight[str][elem] += 111
                    if diag.count(compsymb) == 2 and symb not in diag and str == elem:
                        weight[str][elem] += 111
                    if pdiag.count(compsymb) == 2 and symb not in pdiag and \
                            ((str == 0 and elem == 2) or (str == 2 and elem == 0) or (str == 1 and elem == 1)):
                        weight[str][elem] += 111
                    # last move in draw
                    if ''.join(pole.flatten()).count('-') == 1:
                        if pole[str][elem] == '-':
                            weight[str][elem] += 100500
        # if player got two potential forks
        temp = [[0], [0], [0]]
        check = copy.deepcopy(weight)
        check[0][:] = [x - round(x, 1) for x in check[0]]
        check[1][:] = [x - round(x, 1) for x in check[1]]
        check[2][:] = [x - round(x, 1) for x in check[2]]
        temp[0] = round(max(check[0]), 2)
        temp[1] = round(max(check[1]), 2)
        temp[2] = round(max(check[2]), 2)
        if temp.count(0.02) > 1:
            for st in range(len(check)):
                for el in range(len(check[st])):
                    if round(check[st][el], 2) >= 0.02:
                        weight[st][el] = 0
        # making move
        temp = [[0], [0], [0]]
        temp[0] = max(weight[0])
        temp[1] = max(weight[1])
        temp[2] = max(weight[2])
        a = temp.index(max(temp))
        b = weight[a].index(max(weight[a]))
        pole[a][b] = compsymb
        # players move and end of the game
        if (np.sum(pole[0] == compsymb) < 3 and np.sum(pole[1] == compsymb) < 3 and np.sum(pole[2] == compsymb) < 3 and
            np.sum(np.transpose(pole)[0] == compsymb) < 3 and np.sum(np.transpose(pole)[1] == compsymb) < 3 and
            np.sum(np.transpose(pole)[2] == compsymb) < 3 and
            np.sum(np.diagonal(pole) == compsymb) < 3 and
            np.sum(np.diagonal(np.fliplr(pole)) == compsymb) < 3) and \
                ''.join(pole.flatten()).count('-') > 0:
            #print(pd.DataFrame(np.array(weight), columns=['1', '2', '3'], index=['1', '2', '3']))
            print(pd.DataFrame(pole, columns=['1', '2', '3'], index=['1', '2', '3']))
            print('Введите координаты')
            coord = input()
            x = int(coord[0]) - 1
            y = int(coord[2]) - 1
            pole[int(x)][int(y)] = symb
            if ''.join(pole.flatten()).count('-') == 0:
                print('Draw')
        elif ''.join(pole.flatten()).count('-') == 0:
            print(pd.DataFrame(pole, columns=['1', '2', '3'], index=['1', '2', '3']))
            print('Draw')
        else:
            print(pd.DataFrame(pole, columns=['1', '2', '3'], index=['1', '2', '3']))
            print('Wasted')

xo('x')
