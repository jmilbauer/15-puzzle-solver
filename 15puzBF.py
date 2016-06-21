#!/usr/bin/env python3
#
# Name: Warren Mo
# 
# 15puz.py
# 15 puzzle solver (https://en.wikipedia.org/wiki/15_puzzle)

import sys

def num_entries(row):
    if ( len(row) > 4 ):
        print("Error: row has more than four entries.\n")
        sys.exit(1)
    elif ( len(row) < 4 ):
        print("Error: row has fewer than four entries.\n")
        sys.exit(1)
        
def ran_entries(row):
    for i in range(0, 16):
        if (i not in row):
            print("Error: all integers in [0,15] must be present. You forgot to enter", i, ".\n")
            sys.exit(2)

def inv(row,x,c):
    while ( row.index(x) + 1 != x ):
        if ( row.index(x) + 1 - x >  0 ):            
            pos  = row.index(x)
            posM = row.index(x) - 1
            row[posM], row[pos] = row[pos], row[posM]
            c += 1
        else: # ( row.index(x) + 1 - x <  0 ):
            pos  = row.index(x)
            posP = row.index(x) + 1
            row[posP], row[pos] = row[pos], row[posP]
            c += 1
    return c

# https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
# https://en.wikipedia.org/wiki/15_puzzle#Solvability
def solvable(row):
    m = 0
    COUNT = 0
    if ( (row.index(0) in range(0, 4)) | (row.index(0) in range(8, 12)) ):
        m = 1
    if ( (row.index(0) in range(4, 8)) | (row.index(0) in range(12, 16)) ):
        m = 2

    row.remove(0)

    for i in range(1, 16):
        temp   = 0
        result = inv(row, i, temp)
        COUNT += result
	
    if ( ((COUNT % 2 == 0) & (m == 2)) | ((COUNT % 2 != 0) & (m == 1)) ):
        print("Good! The puzzle is solvable!\n")
    else:
        print("Sorry, the puzzle is not solvable.")
        print(m)
        print(COUNT)
        sys.exit(3)

class Solver(object):

    def __init__(self):
        self.array =[]
        for i in range(0, 4):
            row = [(j + 1) for j in range(4 * (i), 4 * (i + 1))]
            self.array.append(row)
        self.array[3][3] = 0

    def assign(self, i, j, x):
        self.array[i][j] = x

    def switch(self, i1, j1, i2, j2):
        temp = self.array[i1][j1]
        self.array[i1][j1] = self.array[i2][j2]
        self.array[i2][j2] = temp

    def __eq__(self, x):
        return self.array == x.array

    def __ne__(self, x):
        return self.array != x.array

# https://waymoot.org/home/python_string/   (method 4)
    def __str__(self):
        string = []
        for row in self.array:
            for element in row:
                string.append(str(element) + "\t")
            string.append("\n")
        string.pop()
        return "".join(string)

    def __hash__(self):
        return hash(self.__str__())

    def dup(self):
        new = Solver()
        for i in range(0, 4):
            for j in range(0, 4):
                new.assign(i, j, self.array[i][j])
        return new

# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
    def neighbors(self):
        neighbors = []
        for i in range(0, 4):
            for j in range(0, 4):
                if (self.array[i][j] == 0):
                    if (i != 0):
                        neighbor = self.dup()
                        neighbor.switch(i, j, i - 1, j)
                        neighbors.append(neighbor)
                    if (j != 0):
                        neighbor = self.dup()
                        neighbor.switch(i, j, i, j - 1)
                        neighbors.append(neighbor)
                    if (i != 3):
                        neighbor = self.dup()
                        neighbor.switch(i, j, i + 1, j)
                        neighbors.append(neighbor)
                    if (j != 3):
                        neighbor = self.dup()
                        neighbor.switch(i, j, i, j + 1)
                        neighbors.append(neighbor)
        return neighbors

    def h_cost_est(self):
        total = 0
        for i in range(0, 4):
            for j in range(0, 4):
                x = self.array[i][j] - 1
                if (x == -1):
                    x = 15
                y = divmod(x,4)
                total += abs(i - y[0]) + abs(j - y[1])
        return total

    def game(self,board):
        self.begin = Solver()
        for i in range(0,4):
            for j in range(0,4):
                self.begin.assign(i, j, board[i][j])

    def minimum(self, openset, score):
        return min(openset, key=score.get)

# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
    def solve(self):
        start = self.begin.dup()
        goal = Solver()

        ClosedSet = set()           # http://stackoverflow.com/questions/2831212/python-sets-vs-lists   
        OpenSet = set([start])      # (sets are faster for determining the presence of an element but not for iteration over the elements)
        Came_From = {}

        g_score = { start: 0 }
        f_score = { start: g_score[start] + start.h_cost_est()}

        while len(OpenSet) != 0:
            current = self.minimum(OpenSet, f_score)
            if (current == goal):
                return self.reconstruct_path(Came_From, current)

            OpenSet.remove(current)
            ClosedSet.add(current)
            neighbors = current.neighbors()
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                tentative_f_score = neighbor.h_cost_est() # change line to "tentative_f_score = tentative_g_score + neighbor.h_cost_est()" to
                                                          # convert algorithm into A* search

                if (neighbor in ClosedSet) and (neighbor in f_score) and (tentative_f_score >= f_score[neighbor]):
                    continue

                if (neighbor not in OpenSet) or (neighbor in f_score) and (tentative_f_score < f_score[neighbor]): 
                    Came_From[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_f_score
                    if neighbor not in OpenSet:
                        OpenSet.add(neighbor)
        return None

    def reconstruct_path(self, Came_From, cur):
        if cur in Came_From:
            p = self.reconstruct_path(Came_From, Came_From[cur])
            return p + [cur]
        else:
            return [cur]

def main():

    print('\nHello! Welcome to the 15-puzzle solver!\n\nWhen giving your entries, please use the convention as listed in wikipedia: https://en.wikipedia.org/wiki/15_puzzle\n\nUse the number zero for the empty space in your puzzle.\n')    

    firstR  = input( 'Enter the first row: ' )
    firstP  = list( map( int, firstR.split() ) )
    num_entries(firstP)

    secondR = input( 'Enter the second row: ' )
    secondP = list( map( int, secondR.split() ) )
    num_entries(secondP)

    thirdR  = input( 'Enter the third row: ' )
    thirdP  = list( map( int, thirdR.split() ) )
    num_entries(thirdP)

    fourthR = input( 'Enter the fourth row: ' )
    fourthP = list( map( int, fourthR.split() ) )
    num_entries(fourthP)

    puz_row = firstP + secondP + thirdP + fourthP
    collection = []
    collection.append(firstP)
    collection.append(secondP)
    collection.append(thirdP)
    collection.append(fourthP)

    ran_entries(puz_row)

    solvable(puz_row)

    puzzle = Solver()
    puzzle.game(collection)
    solution = puzzle.solve()
    for step in solution:
        print(step, "\n")

if __name__ == "__main__":
    main()
