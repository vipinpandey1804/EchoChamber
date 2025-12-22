from django.conf import settings
import random

def generate_maze(width, height, level=1):
    if width < 3 or height < 3:
        raise ValueError("Maze dimensions must be at least 3x3")
    
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    for i in range(1, height-1):
        for j in range(1, width-1):
            maze[i][j] = 0
    
    complexity = max(0.1, 0.4 - (level * 0.05))
    
    for i in range(2, height-2, 2):
        for j in range(2, width-2, 2):
            if random.random() < complexity:
                maze[i][j] = 1
                if random.random() > 0.5 and j < width-3:
                    maze[i][j+1] = 1
                elif i < height-3:
                    maze[i+1][j] = 1
    
    maze[1][1] = 0
    maze[1][2] = 0
    maze[2][1] = 0
    maze[2][2] = 0
    
    maze[height-2][width-2] = 0
    if width > 3:
        maze[height-2][width-3] = 0
        maze[height-3][width-3] = 0
    if height > 3:
        maze[height-3][width-2] = 0
    
    return maze

def get_maze_size(level):
    sizes = {1: 7, 2: 10, 3: 15, 4: 15, 5: 20}
    return sizes.get(level, 25)

def spawn_power_ups(width, height, maze, count=3):
    power_ups = []
    types = ['speed', 'phase', 'freeze', 'vision']
    
    for _ in range(count):
        attempts = 0
        while attempts < 50:
            x, y = random.randint(2, width-3), random.randint(2, height-3)
            if maze[y][x] == 0:
                power_ups.append({
                    'type': random.choice(types),
                    'pos': [x, y],
                    'expire': random.randint(30, 60)
                })
                break
            attempts += 1
    
    return power_ups

def spawn_mines(width, height, maze, level):
    mines = []
    mine_count = min(level, 2) if level <= 5 else min(2 + (level - 5), 10)
    mine_penalty = getattr(settings, 'GAME_MINE_PENALTY', 50)
    
    for _ in range(mine_count):
        attempts = 0
        while attempts < 50:
            x, y = random.randint(1, width-2), random.randint(1, height-2)
            if maze[y][x] == 0 and [x, y] != [1, 1] and [x, y] != [width-2, height-2]:
                mines.append({'pos': [x, y], 'penalty': mine_penalty})
                break
            attempts += 1
    
    return mines

def spawn_score_powerups(width, height, maze, level):
    score_ups = []
    score_types = [
        {'type': 'coin', 'points': getattr(settings, 'GAME_COIN_BONUS', 25), 'color': '#ffd700'},
        {'type': 'gem', 'points': getattr(settings, 'GAME_GEM_BONUS', 50), 'color': '#00ff00'},
        {'type': 'star', 'points': getattr(settings, 'GAME_STAR_BONUS', 100), 'color': '#ff69b4'}
    ]
    
    count = random.randint(2, 4)
    
    for _ in range(count):
        attempts = 0
        while attempts < 50:
            x, y = random.randint(1, width-2), random.randint(1, height-2)
            if maze[y][x] == 0 and [x, y] != [1, 1] and [x, y] != [width-2, height-2]:
                score_type = random.choice(score_types)
                score_ups.append({
                    'pos': [x, y],
                    'type': score_type['type'],
                    'points': score_type['points'],
                    'color': score_type['color'],
                    'collected': False
                })
                break
            attempts += 1
    
    return score_ups

def generate_movable_walls(width, height, maze, level):
    patterns = [
        [[0, 0], [1, 0], [2, 0], [3, 0]],
        [[0, 0], [0, 1], [0, 2], [0, 3]],
        [[0, 0], [1, 0], [2, 0], [1, 1]],
        [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2]],
        [[0, 0], [1, 0], [2, 0], [0, 1], [2, 1], [0, 2], [1, 2], [2, 2]],
        [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]],
        [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0]],
        [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2], [0, 2], [2, 2]],
        [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
        [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2]]
    ]
    
    movable_walls = []
    num_patterns = min(level * 2, 15)
    
    for i in range(num_patterns):
        pattern = random.choice(patterns)
        attempts = 0
        
        while attempts < 30:
            base_x = random.randint(4, width - 8)
            base_y = random.randint(4, height - 8)
            
            can_place = True
            pattern_cells = []
            
            for dx, dy in pattern:
                x = base_x + dx
                y = base_y + dy
                
                if x < 2 or x >= width - 2 or y < 2 or y >= height - 2:
                    can_place = False
                    break
                
                if maze[y][x] != 0:
                    can_place = False
                    break
                
                if (x < 4 and y < 4) or (x > width - 5 and y > height - 5):
                    can_place = False
                    break
                
                pattern_cells.append([x, y])
            
            if can_place and len(pattern_cells) > 0:
                movable_walls.extend(pattern_cells)
                break
            
            attempts += 1
    
    return movable_walls

def generate_echo_personality(action, position):
    personalities = ['chaotic', 'helpful', 'mirror', 'delayed']
    return random.choice(personalities)

def calculate_echo_position(original, new_pos, personality, max_width, max_height):
    if personality == 'chaotic':
        x = max(0, min(new_pos[0] + random.randint(-2, 2), max_width - 1))
        y = max(0, min(new_pos[1] + random.randint(-2, 2), max_height - 1))
        return [x, y]
    elif personality == 'helpful':
        x = max(0, min(new_pos[0] + 1, max_width - 1))
        return [x, new_pos[1]]
    elif personality == 'mirror':
        x = max(0, min(original[0] - (new_pos[0] - original[0]), max_width - 1))
        y = max(0, min(original[1] - (new_pos[1] - original[1]), max_height - 1))
        return [x, y]
    else:
        return new_pos

def calculate_score(game_tick, echoes_count, wall_hits):
    starting_score = getattr(settings, 'GAME_STARTING_SCORE', 100)
    wall_penalty = getattr(settings, 'GAME_WALL_HIT_PENALTY', 10)
    echo_penalty = getattr(settings, 'GAME_ECHO_PENALTY', 2)
    return max(0, starting_score - (echoes_count * echo_penalty) - (wall_hits * wall_penalty))
