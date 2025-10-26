'''
import random
import heapq
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import streamlit as st

# --- Pathfinding Algorithms ---
def make_grid(rows, cols, random_walls=0.2, seed=None):
    if seed is not None:
        random.seed(seed)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if random.random() < random_walls:
                grid[r][c] = 1
    return grid

def neighbors(pos, rows, cols):
    r, c = pos
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield (nr, nc)

def dijkstra(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]
    visited_order = []
    while pq:
        d, node = heapq.heappop(pq)
        if d != dist.get(node, float('inf')):
            continue
        visited_order.append(node)
        if node == goal:
            break
        for nb in neighbors(node, rows, cols):
            if grid[nb[0]][nb[1]] == 1:
                continue
            nd = d + 1
            if nd < dist.get(nb, float('inf')):
                dist[nb] = nd
                prev[nb] = node
                heapq.heappush(pq, (nd, nb))
    # reconstruct path
    path = []
    cur = goal
    if cur in prev or cur == start:
        while cur != start:
            path.append(cur)
            cur = prev[cur]
        path.append(start)
        path.reverse()
    return visited_order, path

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    prev = {}
    pq = [(fscore[start], start)]
    visited_order = []
    while pq:
        f, node = heapq.heappop(pq)
        if f != fscore.get(node, float('inf')):
            continue
        visited_order.append(node)
        if node == goal:
            break
        for nb in neighbors(node, rows, cols):
            if grid[nb[0]][nb[1]] == 1:
                continue
            tentative_g = gscore[node] + 1
            if tentative_g < gscore.get(nb, float('inf')):
                prev[nb] = node
                gscore[nb] = tentative_g
                fscore[nb] = tentative_g + heuristic(nb, goal)
                heapq.heappush(pq, (fscore[nb], nb))
    path = []
    cur = goal
    if cur in prev or cur == start:
        while cur != start:
            path.append(cur)
            cur = prev[cur]
        path.append(start)
        path.reverse()
    return visited_order, path

# --- Visualization for Streamlit ---
def draw_grid(grid, start=None, goal=None, visited=None, path=None, title=''):
    arr = np.array(grid)
    rows, cols = arr.shape
    cmap = plt.cm.get_cmap('gray_r')
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(arr, cmap=cmap, origin='upper')
    # overlay visited
    if visited:
        vs = np.zeros_like(arr, dtype=float)
        for (r, c) in visited:
            vs[r, c] = 0.6
        ax.imshow(vs, cmap='Blues', alpha=0.6, origin='upper')
    # overlay path
    if path:
        pts = np.array(path)
        ax.plot(pts[:, 1], pts[:, 0], linewidth=3, color='red')
    # start/goal markers
    if start:
        ax.scatter([start[1]], [start[0]], marker='o', s=100, label='start', zorder=5, color='lime')
    if goal:
        ax.scatter([goal[1]], [goal[0]], marker='X', s=100, label='goal', zorder=5, color='red')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

# --- Streamlit UI ---
st.title("Pathfinding Visualization")

rows = st.number_input("Grid rows", min_value=5, max_value=50, value=18)
cols = st.number_input("Grid columns", min_value=5, max_value=50, value=18)
wall_density = st.slider("Wall density", 0.0, 0.5, 0.25)
seed = st.number_input("Random seed (optional)", step=1, value=42)

start_r = st.number_input("Start row", min_value=0, max_value=rows-1, value=0)
start_c = st.number_input("Start column", min_value=0, max_value=cols-1, value=0)
goal_r = st.number_input("Goal row", min_value=0, max_value=rows-1, value=rows-1)
goal_c = st.number_input("Goal column", min_value=0, max_value=cols-1, value=cols-1)

algorithm = st.selectbox("Select algorithm", ["Dijkstra", "A*"])

if st.button("Generate and Run"):
    grid = make_grid(rows, cols, wall_density, seed)
    start = (int(start_r), int(start_c))
    goal = (int(goal_r), int(goal_c))

    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0

    if algorithm == "Dijkstra":
        visited, path = dijkstra(grid, start, goal)
    else:
        visited, path = astar(grid, start, goal)

    image_buf = draw_grid(grid, start=start, goal=goal, visited=visited, path=path, title="Grid with path and visited nodes")
    st.image(image_buf, caption="Grid with path and visited nodes")
    st.write(f"Visited nodes: {len(visited)}")
    st.write(f"Path length: {len(path)}")

'''

import random
import heapq
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import streamlit as st
import time

# --- Utility Functions ---
def make_grid(rows, cols, random_walls=0.2, seed=None):
    if seed is not None:
        random.seed(seed)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if random.random() < random_walls:
                grid[r][c] = 1
    return grid

def neighbors(pos, rows, cols):
    r, c = pos
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield (nr, nc)

# --- Dijkstra Algorithm ---
def dijkstra(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]
    visited_order = []

    while pq:
        d, node = heapq.heappop(pq)
        if d != dist.get(node, float('inf')):
            continue
        visited_order.append(node)
        if node == goal:
            break
        for nb in neighbors(node, rows, cols):
            if grid[nb[0]][nb[1]] == 1:
                continue
            nd = d + 1
            if nd < dist.get(nb, float('inf')):
                dist[nb] = nd
                prev[nb] = node
                heapq.heappush(pq, (nd, nb))
    # reconstruct path
    path = []
    cur = goal
    if cur in prev or cur == start:
        while cur != start:
            path.append(cur)
            cur = prev[cur]
        path.append(start)
        path.reverse()
    return visited_order, path

# --- A* Algorithm ---
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    prev = {}
    pq = [(fscore[start], start)]
    visited_order = []

    while pq:
        f, node = heapq.heappop(pq)
        if f != fscore.get(node, float('inf')):
            continue
        visited_order.append(node)
        if node == goal:
            break
        for nb in neighbors(node, rows, cols):
            if grid[nb[0]][nb[1]] == 1:
                continue
            tentative_g = gscore[node] + 1
            if tentative_g < gscore.get(nb, float('inf')):
                prev[nb] = node
                gscore[nb] = tentative_g
                fscore[nb] = tentative_g + heuristic(nb, goal)
                heapq.heappush(pq, (fscore[nb], nb))
    # reconstruct path
    path = []
    cur = goal
    if cur in prev or cur == start:
        while cur != start:
            path.append(cur)
            cur = prev[cur]
        path.append(start)
        path.reverse()
    return visited_order, path

# --- Visualization Function ---
def draw_grid(grid, start=None, goal=None, visited=None, path=None, title=''):
    arr = np.array(grid)
    rows, cols = arr.shape
    cmap = plt.cm.get_cmap('gray_r')
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(arr, cmap=cmap, origin='upper')
    
    if visited:
        vs = np.zeros_like(arr, dtype=float)
        for (r, c) in visited:
            vs[r, c] = 0.6
        ax.imshow(vs, cmap='Blues', alpha=0.6, origin='upper')
    if path:
        pts = np.array(path)
        ax.plot(pts[:, 1], pts[:, 0], linewidth=2.5, color='red')
    if start:
        ax.scatter([start[1]], [start[0]], marker='o', s=80, color='lime')
    if goal:
        ax.scatter([goal[1]], [goal[0]], marker='X', s=80, color='red')
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

# --- Streamlit Frontend ---
st.set_page_config(page_title="Grid Navigator", layout="wide")
st.title("Grid Navigator")

rows = st.number_input("Grid rows", min_value=5, max_value=50, value=18)
cols = st.number_input("Grid columns", min_value=5, max_value=50, value=18)
wall_density = st.slider("Wall density", 0.0, 0.5, 0.25)
seed = st.number_input("Random seed (optional)", step=1, value=42)

start_r = st.number_input("Start row", min_value=0, max_value=rows-1, value=0)
start_c = st.number_input("Start column", min_value=0, max_value=cols-1, value=0)
goal_r = st.number_input("Goal row", min_value=0, max_value=rows-1, value=rows-1)
goal_c = st.number_input("Goal column", min_value=0, max_value=cols-1, value=cols-1)

if st.button("Generate and Run"):
    grid = make_grid(rows, cols, wall_density, seed)
    start = (int(start_r), int(start_c))
    goal = (int(goal_r), int(goal_c))
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dijkstra Algorithm Steps")
        visited_dij, path_dij = dijkstra(grid, start, goal)
        for i in range(0, len(visited_dij), max(1, len(visited_dij)//10)):
            partial = visited_dij[:i+1]
            img = draw_grid(grid, start, goal, visited=partial, title=f"Dijkstra Steps ({i+1}/{len(visited_dij)})")
            st.image(img)
            time.sleep(0.2)
        final_img_dij = draw_grid(grid, start, goal, visited=visited_dij, path=path_dij, title="Dijkstra Final Path")
        st.image(final_img_dij)
        st.write(f"Visited Nodes: {len(visited_dij)} | Path Length: {len(path_dij)}")
    
    with col2:
        st.subheader("A* Algorithm Steps")
        visited_astar, path_astar = astar(grid, start, goal)
        for i in range(0, len(visited_astar), max(1, len(visited_astar)//10)):
            partial = visited_astar[:i+1]
            img = draw_grid(grid, start, goal, visited=partial, title=f"A* Steps ({i+1}/{len(visited_astar)})")
            st.image(img)
            time.sleep(0.2)
        final_img_astar = draw_grid(grid, start, goal, visited=visited_astar, path=path_astar, title="A* Final Path")
        st.image(final_img_astar)
        st.write(f"Visited Nodes: {len(visited_astar)} | Path Length: {len(path_astar)}")

st.markdown("---")
st.subheader("Final Comparison Output")

col3, col4 = st.columns(2)
with col3:
    st.image(final_img_dij, caption="Dijkstra Final Path")
with col4:
    st.image(final_img_astar, caption="A* Final Path")
