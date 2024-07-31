class Backgammon:
    def __init__(self):
        """
        电脑用O, 人类用X
        """
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def evaluate(self, board):
        """
        检查是否胜利的情况
        :param board: 棋盘
        :return: 10->电脑赢 -10->人赢 0—>平局
        """
        # 检查行
        for row in board:
            if row[0] == row[1] == row[2]:
                if row[0] == 'O':
                    return 10
                elif row[0] == 'X':
                    return -10

        # 检查列
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col]:
                if board[0][col] == 'O':
                    return 10
                elif board[0][col] == 'X':
                    return -10

        # 检查对角线
        if board[0][0] == board[1][1] == board[2][2]:
            if board[0][0] == 'O':
                return 10
            elif board[0][0] == 'X':
                return -10

        if board[0][2] == board[1][1] == board[2][0]:
            if board[0][2] == 'O':
                return 10
            elif board[0][2] == 'X':
                return -10

        # 没有赢家
        return 0

    def is_board_full(self, board):
        """
        判断是否棋盘是满的
        :return: True->满; False->没满
        """
        for row in board:
            if " " in row:
                return False
        return True

    # 找到空的可下棋的位置
    def find_empty_cells(self, board):
        cells = []
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == " ":
                    cells.append((i, j))
        return cells

    def minimax(self, board, depth, is_maximizing):
        # 先检查是否胜利的情况
        score = self.evaluate(board)

        # 如果游戏结束
        if score == 10:
            return score
        if score == -10:
            return score
        if self.is_board_full(board):
            return 0

        if is_maximizing:
            best = float('-inf')
            empty_cells = self.find_empty_cells(board)
            for cell in empty_cells:
                x, y = cell
                board[x][y] = 'O'
                best = max(best, self.minimax(board, depth + 1, False))
                board[x][y] = ' '  # 回溯
            return best

        else:  # minimizing player
            best = float('inf')
            empty_cells = self.find_empty_cells(board)
            for cell in empty_cells:
                x, y = cell
                board[x][y] = 'X'
                best = min(best, self.minimax(board, depth + 1, True))
                board[x][y] = ' '  # 回溯
            return best


    # 找到最优的路径
    def find_best_move(self, board):
        best_val = float('-inf')
        best_move = None
        empty_cells = self.find_empty_cells(board)

        for cell in empty_cells:
            x, y = cell
            board[x][y] = 'O'
            move_val = self.minimax(board, 0, False)
            board[x][y] = ' '
            if move_val > best_val:
                best_move = (x, y)
                best_val = move_val
        return best_move
    
    def axis_turn_key(self, x, y):
        temp = {(0, 0):1, (0, 1):2, (0, 2):3,
               (1, 0):4, (1, 1):5, (1, 2):6,
               (2, 0):7, (2, 1):8, (2, 2):9}
        return temp[(x, y)]
    
    def key_turn_axis(self, key):
        temp = {1:(0, 0), 2:(0, 1), 3:(0, 2),
               4:(1, 0), 5:(1, 1), 6:(1, 2),
               7:(2, 0), 8:(2, 1), 9:(2, 2)}
        return temp[key]
    

if __name__ == '__main__':
    b = Backgammon()
    b.board[2][0] = 'X'
    print(b.find_best_move((b.board))) # 1, 1
    b.board[1][1] = 'O'
    b.board[0][2] = 'X'
    print(b.find_best_move((b.board))) # 0, 0
    b.board[2][2] = 'X'
    print(b.find_best_move((b.board))) # 0, 0


