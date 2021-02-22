import numpy as np
import copy
class Game:
    def __init__(self, x, y, turn):
        self.board = np.zeros(shape=(x, y), dtype=int)
        self.x = x
        self.y = y
        self.heightArray = np.zeros(shape=(x), dtype = int)
        self.turn = turn
        self.last = None


    def getNewTurn(self, turn):
        if turn == 1:
            return 2
        elif turn == 2:
            return 1
        else:
            return False

    def updateTurn(self):
        self.turn = self.getNewTurn(self.turn)

    def play(self, x):
        if 0 <= x < self.x:
            if self.heightArray[x] < self.y:
                self.board[x, self.heightArray[x]] = self.turn
                self.heightArray[x] += 1
                self.last = x
                self.updateTurn()
                return True
            else:
                #print("full column")
                return False
        else:
            print("place out of bounds")
        return False

    def getChildren(self):
        children = []
        for i in range(self.x):
            new = copy.deepcopy(self)
            if new.play(i):
                children.append(new)
        return children


    def checkWin(self):
        if self.last is None:
            return False
        #check horizontal
        count = 0
        Xindex = self.last
        Yindex = self.heightArray[self.last]-1
        turn = self.board[Xindex, Yindex]
        while self.board[Xindex, Yindex] == turn:
            count += 1
            Xindex += 1
            if Xindex >= self.x:
                break
        Xindex = self.last
        Yindex = self.heightArray[self.last]-1
        while self.board[Xindex, Yindex] == turn:
            count += 1
            Xindex -= 1
            if Xindex < 0:
                break
        if count > 4:
            #print("horizontal detected for player", turn)
            return True

        #check diagonal1
        count = 0
        Xindex = self.last
        Yindex = self.heightArray[self.last]-1
        while self.board[Xindex, Yindex] == turn:
            count += 1
            Xindex += 1
            Yindex += 1
            if Xindex >= self.x or Yindex >= self.y:
                break
        Xindex = self.last
        Yindex = self.heightArray[self.last]-1
        while self.board[Xindex, Yindex] == turn:
            count += 1
            Xindex -= 1
            Yindex -= 1
            if Xindex < 0 or Yindex < 0:
                break
        if count > 4:
            #print("diagonal detected / for player =", turn)
            return True

        #check other diagonal
        count = 0
        Xindex = self.last
        Yindex = self.heightArray[self.last]-1
        while self.board[Xindex, Yindex] == turn:
            count += 1
            Xindex += 1
            Yindex -= 1
            if Xindex >= self.x or Yindex < 0:
                break
        Xindex = self.last
        Yindex = self.heightArray[self.last]-1
        while self.board[Xindex, Yindex] == turn:
            count += 1
            Xindex -= 1
            Yindex += 1
            if Xindex < 0 or Yindex >= self.y:
                break
        if count > 4:
            #print("diagonal detected \\ for player =", turn)
            return True

        #check vetical
        count = 0
        Xindex = self.last
        Yindex = self.heightArray[self.last]-1
        while self.board[Xindex, Yindex] == turn:
            count += 1
            Yindex -= 1
            if Yindex < 0:
                break
        if count >= 4:
            #print("Vertical detected for player", turn)
            return True
        return False

    def __str__(self):
        string = ""
        for i in range(self.y - 1, -1, -1):
            for j in range(self.x):
                string += str(self.board[j, i])
                if j == self.last and i == self.heightArray[self.last]-1:
                    string += '<'
                else:
                    string += ' '
            string += "\n"
        return string

    def getH(self, agent):
        return self.getHSimplistic(agent) - self.getHSimplistic(self.getNewTurn(agent))

    def getHSimplistic(self, agent):
        if self.checkWin():
            if self.turn == agent:
                return float("-inf")
            else:
                return float("inf")
        h = 0
        #check horizontal
        for x in range(self.x - 3):
            for y in range(self.y):
                count = 0
                isObtainable = True
                for i in range(4):
                    if self.board[x + i, y] == agent:
                        count += 1
                    elif self.board[x + i ,y] == self.getNewTurn(agent):
                        isObtainable = False
                        break
                if isObtainable:
                    h += count ** 2
        #check diagonal
        for x in range(self.x - 3):
            for y in range(self.y - 3):
                count = 0
                isObtainable = True
                for i in range(4):
                    if self.board[x + i, y + i] == agent:
                        count += 1
                    elif self.board[x + i ,y + i] == self.getNewTurn(agent):
                        isObtainable == False
                        break
                if isObtainable:
                    h += count ** 2

        for x in range(self.x - 3):
            for y in range(3, self.y):
                count = 0
                isObtainable = True
                for i in range(4):
                    if self.board[x + i, y - i] == agent:
                        count += 1
                    elif self.board[x + i ,y - i] == self.getNewTurn(agent):
                        isObtainable == False
                        break
                if isObtainable:
                    h += count ** 2
        #check Vertical
        for x in range(self.x):
            for y in range(self.y - 3):
                count = 0
                isObtainable = True
                for i in range(4):
                    if self.board[x, y + i] == agent:
                        count += 1
                    elif self.board[x ,y + i] == self.getNewTurn(agent):
                        isObtainable == False
                        break
                if isObtainable:
                    h += count ** 3
        return h



def minmax(state, agent, d):
    if state.checkWin() or d == 0:
        return state.getH(agent), None

    children = state.getChildren()
    if state.turn == agent:
        maxVal = float("-inf")
        nextMove = 0
        for c in children:
            val = minmax(c, agent, d - 1)[0]
            if val > maxVal:
                maxVal = val
                nextMove = c.last
        return maxVal, nextMove
    else:
        minVal = float("inf")
        nextMove = 0
        for c in children:
            val = minmax(c, agent, d - 1)[0]
            if val < minVal:
                minVal = val
                nextMove = c.last
        return minVal, nextMove



def main():
    x = Game(7, 6, 1)
    winner = False
    print(x)
    while not winner:
        print("its", x.turn, "turn")
        if x.turn == 1:
            x.play(int(input()))
        else:
            play = minmax(x, 2, 4)
            print("the computer placed", play[1])
            x.play(play[1])
            print(play[0])
        if x.checkWin():
            winner = x.getNewTurn(x.turn)
        print(x)
    print("the winner is", winner)


main()