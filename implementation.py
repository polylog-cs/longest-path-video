from collections import deque

import tree_data

def bfs(g, start):
    q = deque()
    q.append(start)
    dist = {start: 0}

    while q:
        a = q.popleft()
        for b in g[a]:
            if b not in dist:
                q.append(b)
                dist[b] = dist[a] + 1

    return dist

def main():
    # edges = tree_data.parse_linux_tree("fictional_filesystem.txt")
    edges = tree_data.parse_linux_tree("sandbox/vv_filesystem_dirs.txt")
    g = {}
    print(f"Loaded {len(edges)} edges")

    for a, b in edges:
        for x in a, b:
            if x not in g:
                g[x] = []
        
        g[a].append(b)
        g[b].append(a)

    dist = bfs(g, "/")
    farthest = ["/", 0]
    for k, v in dist.items():
        if v > farthest[1]:
            farthest = [k, v]
    
    print("Step 1:", farthest)

    dist = bfs(g, farthest[0])
    farthest[1] = 0
    for k, v in dist.items():
        if v > farthest[1]:
            farthest = k, v
    
    print(farthest)



main()