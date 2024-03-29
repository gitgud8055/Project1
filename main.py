from collections import deque
from queue import PriorityQueue

import pygame

pygame.init()

WIDTH = 500
ROWS = 50 # 50 x 50
WIN = pygame.display.set_mode((WIDTH+200, WIDTH+50))
pygame.display.set_caption("Some Pathfinding Algorithm in Maze game")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
YELLOW = (255, 0, 0)#(255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (255, 255, 0)#(255, 0, 0)
LAVENDER = (230,230,250)
DARK_BLUE = (0,0,139)

font = pygame.font.Font(None, 12)

class Node():
    def __init__(self, row, col, width, total_rows):
        """ Các thông số của một node """
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.neighbours = []
        self.neighbours8 = []
        self.total_rows = total_rows
        
        self.text = ""
        self.surface = pygame.Surface((self.width, self.width))
        self.surface.fill(WHITE)
    
    def add_text(self, value):
        self.text = str(value)

    def get_pos(self):
        """Lấy vị trí hiện tại"""
        return self.row, self.col

    def is_color(self, color):
        """ Kiểm tra màu của ô hiện tại """
        return self.color == color

    def set_color(self, color):
        """ đổi màu ô hiện tại"""
        self.color = color

    def draw(self, win):
        """Vẽ cho từng ô node """
        pygame.draw.rect(win, self.color, (self.x, self.y , self.width, self.width))
        self.surface.fill(self.color)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.width // 2))
        self.surface.blit(text_surface, text_rect)

    def update_neighbours(self, grid):
        """ cập nhật các ô có thể đến """
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_color(BLACK): # Down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_color(BLACK): # Up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_color(BLACK): # Right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_color(BLACK): # Left
            self.neighbours.append(grid[self.row][self.col - 1])
        self.neighbours8 = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1] if x != 0 else [-1, 1]:
                if 0 <= self.row + x < self.total_rows and 0 <= self.col + y < self.total_rows and not grid[self.row + x][self.col + y].is_color(BLACK):
                    self.neighbours8.append(grid[self.row + x][self.col + y])

    def __lt__(self, other):
        return False


def h(p1, p2):
    """ Halminton distance """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def get_clicked_pos(pos, rows, width):
    """ lấy vị trí của ô dựa vào click chuột """
    gap = width // rows
    x, y = pos

    row = x // gap
    col = y // gap
    
    row %= rows
    if (row < 0):
        row += rows
    col %= rows
    if (col < 0):
        col += rows

    return row, col

def reconstruct_path(came_from, current, draw):
    """Vẽ đường trace back """
    while current in came_from:
        current = came_from[current]
        current.set_color(PURPLE)
        draw()

def make_grid(rows, width):
    """ Tạo ma trận """
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows) # Adding nodes to every cell
            grid[i].append(node)

    return grid

def draw_grid(win, width, rows):
    """ Vẽ lưới của ma trận """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))

def pause():
    WIN.fill(WHITE)
    F = pygame.font.SysFont("Arial", 30)
    text = F.render('Paused', True, BLACK)
    WIN.blit(text, (250, 250))
    #print(WIN)
    
def check_event(grid, draw, came_from, start):
    """Kiểm tra các event khi sử dụng tính năng Pause"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = True
            while (paused):
                pause()
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                        paused = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for row in grid:
                            for node in row:
                                if (node.is_color(PURPLE)):
                                    node.set_color(RED)
                        draw()
                        pos = pygame.mouse.get_pos()
                        row, col = get_clicked_pos(pos, ROWS, WIDTH)
                        reconstruct_path(came_from, grid[row][col], draw)
                        start.set_color(BLUE)
                        draw()
            for row in grid:
                for node in row:
                    if (node.is_color(PURPLE)):
                        node.set_color(RED)
            draw()
                        

def dijkstra(draw, grid, start, end):
    """ Dijkstra algorithm """
    st = deque()
    st.append(start)
    vis = {}
    vis[start] = 1
    came_from = {}
    cnt = 0
    dist = {node: int("-1") for row in grid for node in row}
    dist[start] = 0
    """Khởi tạo các giá trị"""
    while st.__len__() > 0:
        check_event(grid, draw, came_from, start)
        cur = st.popleft()
        
        if (cur == end):
            reconstruct_path(came_from, end, draw)
            end.set_color(GREEN)
            start.set_color(BLUE)
            return True
        # Thực hiện thuật toán + đổi màu + cập nhật các ô kế tiếp
        for nxt in cur.neighbours:
            if nxt in vis:
                continue
            dist[nxt] = dist[cur] + 1
            nxt.add_text(dist[nxt])
            vis[nxt] = 1
            came_from[nxt] = cur
            st.append(nxt)
            nxt.set_color(YELLOW)
            cnt += 1
        draw()
        
        if (cur != start):
            cur.set_color(RED)     
            
    return False

def aStar(draw, grid, start, end):
    """ A* algorithm """
    count = 0
    open_set = PriorityQueue() 
    open_set.put((0, count, start))
    came_from = {} 

    g_score = {node: float("inf") for row in grid for node in row} # Hàm đường đi ngắn nhất F(node)
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row} # Hàm đánh giá T(node)
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} 
    paused = False
    dist = {node: int("-1") for row in grid for node in row}
    dist[start] = 0
    # Khởi tạo
    while not open_set.empty():
        #print(pygame.event.get())
        check_event(grid, draw, came_from, start)
        
        current = open_set.get()[2] 
        if current not in open_set_hash:
            continue
        open_set_hash.remove(current)

        if current == end: 
            reconstruct_path(came_from, end, draw)
            end.set_color(GREEN)
            start.set_color(BLUE)
            return True
        # Thực hiện thuật toán và cập nhật những ô liên quan
        for neighbour in current.neighbours: 
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                neighbour.add_text(temp_g_score)
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos()) * 2

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.set_color(YELLOW)

        draw()

        if current != start: 
            current.set_color(RED)
            
    return False

def thetaStar(draw, grid, start, end):
    """ Theta* algorithm """
    count = 0
    open_set = PriorityQueue() 
    
    came_from = {} 

    g_score = {node: float("inf") for row in grid for node in row} # Hàm đường đi ngắn nhất F(node)
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row} # Hàm đánh giá T(node)
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set.put((f_score[start], count, start))
    cnt = {node: int("0") for row in grid for node in row}
    cnt[start] = 1
    dist = {node: int("-1") for row in grid for node in row}
    open_set_hash = {start} 
    paused = False
    open_set_hash.remove(start)
    # Khởi tạo

    while not open_set.empty():
        #print(pygame.event.get())
        check_event(grid, draw, came_from, start)
        now = open_set.get()
        if now[0] != f_score[now[2]]:
            continue
        current = now[2] 
        if current  in open_set_hash:
            continue
        #open_set_hash.remove(current)
        open_set_hash.add(current)

        if current == end: 
            reconstruct_path(came_from, end, draw)
            end.set_color(GREEN)
            start.set_color(BLUE)
            return True
        # Thực hiện thuật toán và cập nhật những ô liên quan
        for neighbour in current.neighbours8: 
            temp_g_score = g_score[current] + 1
            cnt[neighbour] += 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                neighbour.add_text(temp_g_score)
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos()) * 2 - cnt[neighbour] * 10

                #if neighbour not in open_set_hash:
                count += 1
                open_set.put((f_score[neighbour], count, neighbour))
                
                neighbour.set_color(YELLOW)

        draw()

        if current != start: 
            current.set_color(RED)
            
    return False

def draw(win, grid, width, rows, name_algorithm):
    """ Vẽ giao diện """
    win.fill(WHITE)

    """ Vẽ các node của ma trận """
    for row in grid:
        for node in row:
            node.draw(win)
            win.blit(node.surface, (node.x, node.y))
            
    draw_grid(win, width, rows) # Vẽ lưới ma trận
    """Tạo các lựa chọn và hiện thị lựa chọn hiện tại"""
    pygame.draw.rect(WIN, LAVENDER, (525, 25, 150, 75))
    pygame.draw.rect(WIN, LAVENDER, (525, 125, 150, 75))
    pygame.draw.rect(WIN, LAVENDER, (525, 225, 150, 75))
    font = pygame.font.Font(None, 36)
    text_mode1 = font.render("Dijkstra", True, DARK_BLUE)
    text_mode2 = font.render("A star", True, DARK_BLUE)
    text_mode3 = font.render("Theta Star", True, DARK_BLUE)
    WIN.blit(text_mode1, (530, 30))
    WIN.blit(text_mode2, (530, 130))
    WIN.blit(text_mode3, (530, 230))
    selected_text = font.render(f"Selected mode: {name_algorithm}", True, BLACK)
    WIN.blit(selected_text, (200, 510))
    pygame.display.update()

def main(win):
    run = True

    # node bắt đầu và kết thúc
    start = None
    end = None

    grid = make_grid(ROWS, WIDTH)
    algorithm = dijkstra
    name_algorithm = "Dijkstra"
    # Thuật toán default là dijkstra
    while run:
        draw(win, grid, WIDTH, ROWS, name_algorithm)
        # Xử lí các event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            flag = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                row,col = pygame.mouse.get_pos()
                if 525 <= row <= 675:
                    if 25 <= col <= 100:
                        name_algorithm = "Dijkstra"
                        algorithm = dijkstra
                        flag = False
                    elif 125 <= col <= 200:
                        name_algorithm = "A star"
                        algorithm = aStar
                        flag = False
                    elif 225 <= col <= 300:
                        name_algorithm = "Theta Star"
                        algorithm = thetaStar
                        flag = False
                        
            if flag and pygame.mouse.get_pressed()[0]: # chuột trái
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.set_color(BLUE)
                elif not end and node != start:
                    end = node
                    end.set_color(GREEN)
                elif node != end and node != start:
                    node.set_color(BLACK)

            if flag and pygame.mouse.get_pressed()[2]: # chuột phải
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.set_color(WHITE)

                if node == start:
                    start = None
                elif node == end:      
                    end = None
            

            if event.type == pygame.KEYDOWN: # Thực thi thuật toán
                if event.key == pygame.K_RETURN and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    for row in grid:
                        for node in row:
                            node.add_text("")
                            if (node != start and node != end and not node.is_color(BLACK)):
                                node.set_color(WHITE)
                    algorithm(lambda: draw(win, grid, WIDTH, ROWS, name_algorithm), grid, start, end)

                if event.key == pygame.K_c: # xóa ma trận
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

    pygame.quit()

if __name__ == "__main__":
    main(WIN)
