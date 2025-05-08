from heapq import heappush, heappop

start_state = (10,8,14,7,6,9,2,5,1,12,4,3,11,15,13,0)
goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
goal_positions = {val: (i // 4, i % 4) for i, val in enumerate(goal_state)}
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan(state):
    distance = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        current_row, current_col = i // 4, i % 4
        goal_row, goal_col = goal_positions[val]
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    zero_index = state.index(0)
    row, col = zero_index // 4, zero_index % 4
    neighbors = []

    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_index = new_row * 4 + new_col
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append(tuple(new_state))
    return neighbors

def greedy_best_first(start, goal):
    visited = set()
    heap = []
    heappush(heap, (manhattan(start), start, []))  # (priority, state, path)

    while heap:
        _, current, path = heappop(heap)
        if current == goal:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                heappush(heap, (manhattan(neighbor), neighbor, path + [current]))
    return None

def get_direction(prev_state, next_state):
    zero_prev = prev_state.index(0)
    zero_next = next_state.index(0)
    dr = (zero_next // 4) - (zero_prev // 4)
    dc = (zero_next % 4) - (zero_prev % 4)

    if dr == -1 and dc == 0:
        return "bas", "\033[31m"  
    elif dr == 1 and dc == 0:
        return "haut", "\033[32m"  
    elif dr == 0 and dc == 1:
        return "gauche", "\033[33m"  
    elif dr == 0 and dc == -1:
        return "droite", "\033[34m"  
    return "inconnu", "\033[0m" 

solution_path = greedy_best_first(start_state, goal_state)
if solution_path:
    directions = []
    for i in range(1, len(solution_path)):
        direction, color = get_direction(solution_path[i - 1], solution_path[i])
        directions.append(f"{color}{direction}\033[0m")  
    print("Mouvements à suivre :")
    print(", ".join(directions))
    print(f"\nNombre total de mouvements : {len(directions)}")
else:
    print("Aucune solution trouvée.")
