from queue import PriorityQueue

class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0

    def __lt__(self, other):
        return self.f_score < other.f_score

def a_star(start_pos, end_pos, grid):
    def heuristic(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(node, grid):
        neighbors = []
        for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            r, c = node.pos[0] + drow, node.pos[1] + dcol
            if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
                continue
            if grid[r][c] == 1:
                continue
            neighbors.append((r, c))
        return [Node(neighbor, node) for neighbor in neighbors]

    start_node = Node(start_pos)
    end_node = Node(end_pos)

    open_list = PriorityQueue()
    open_list.put(start_node)
    closed_list = set()
    g_score = {start_node.pos: 0}
    f_score = {start_node.pos: heuristic(start_node.pos, end_node.pos)}

    while not open_list.empty():
        current_node = open_list.get()

        if current_node.pos == end_node.pos:
            return reconstruct_path(current_node)

        closed_list.add(current_node)

        for neighbor_node in get_neighbors(current_node, grid):
            if neighbor_node in closed_list:
                continue

            tentative_g_score = g_score[current_node.pos] + heuristic(current_node.pos, neighbor_node.pos)

            if neighbor_node not in open_list.queue or tentative_g_score < g_score[neighbor_node.pos]:
                neighbor_node.g_score = tentative_g_score
                neighbor_node.h_score = heuristic(neighbor_node.pos, end_node.pos)
                neighbor_node.f_score = neighbor_node.g_score + neighbor_node.h_score
                g_score[neighbor_node.pos] = tentative_g_score
                f_score[neighbor_node.pos] = neighbor_node.f_score
                neighbor_node.parent = current_node

                if neighbor_node not in open_list.queue:
                    open_list.put(neighbor_node)

    return None

def reconstruct_path(current_node):
    path = []
    while current_node is not None:
        path.append(current_node.pos)
        current_node = current_node.parent
    path.reverse()
    return path
