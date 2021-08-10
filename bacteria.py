from manim import *
import numpy as np
import solarized
import math
from scipy.optimize import linprog

bacteria_data = """47.8968 301.269 m
203.398 321.238 l
60.6783 278.841 m
151.258 292.205 l
76.3443 256.66 m
149.48 267.32 l
95.7957 234.426 m
125.78 243.028 l
125.78 243.028 m
119.703 212.651 l
125.78 243.028 m
149.48 244.213 l
149.48 244.213 m
140.305 197.542 l
149.48 244.213 m
149.48 267.32 l
149.48 267.32 m
151.258 292.205 l
151.258 292.205 m
200.435 285.688 l
200.435 285.688 m
203.398 321.238 l
200.435 285.688 m
229.468 224.66 l
229.468 224.66 m
185.623 211.033 l
185.623 211.033 m
155.717 188.032 l
185.623 211.033 m
175.049 177.972 l
229.468 224.66 m
242.503 197.406 l
242.503 197.406 m
197.976 168.428 l
242.503 197.406 m
252.575 176.076 l
252.575 176.076 m
225.32 160.069 l
252.575 176.076 m
257.452 154.074 l
203.398 321.238 m
231.838 338.42 l
231.838 338.42 m
279.772 152.203 l
231.838 338.42 m
260.277 356.788 l
260.277 356.788 m
317.75 201.553 l
317.75 201.553 m
308.27 173.113 l
317.75 201.553 m
364.6 161.939 l
308.27 173.113 m
300.116 152.093 l
308.27 173.113 m
330.283 154.734 l
260.277 356.788 m
275.09 378.71 l
275.09 378.71 m
394.068 171.972 l
275.09 378.71 m
311.825 439.145 l
311.825 439.145 m
96.748 371.008 l
96.748 371.008 m
41.5514 314.621 l
96.748 371.008 m
61.1981 389.375 l
61.1981 389.375 m
29.3687 347.802 l
61.1981 389.375 m
21.9003 380.258 l
311.825 439.145 m
305.9 478.842 l
305.9 478.842 m
182.66 472.325 l
182.66 472.325 m
151.85 471.14 l
151.85 471.14 m
63.5681 425.517 l
63.5681 425.517 m
18.6799 408.685 l
63.5681 425.517 m
18.3662 435.244 l
151.85 471.14 m
132.89 497.802 l
132.89 497.802 m
106.228 478.842 l
106.228 478.842 m
20.1282 457.748 l
106.228 478.842 m
94.378 507.282 l
94.378 507.282 m
56.4581 500.172 l
56.4581 500.172 m
25.8107 489.305 l
56.4581 500.172 m
33.5049 515.404 l
94.378 507.282 m
47.5799 548.479 l
132.89 497.802 m
151.258 548.165 l
151.258 548.165 m
58.2691 567.664 l
151.258 548.165 m
153.035 572.457 l
153.035 572.457 m
73.0143 589.375 l
153.035 572.457 m
149.48 605.044 l
149.48 605.044 m
94.8894 615.013 l
149.48 605.044 m
129.648 645.386 l
182.66 472.325 m
162.809 666.261 l
305.9 478.842 m
343.227 476.472 l
343.227 476.472 m
426.15 187.486 l
343.227 476.472 m
367.52 490.1 l
367.52 490.1 m
458.172 334.273 l
458.172 334.273 m
452.247 305.24 l
452.247 305.24 m
445.762 199.727 l
452.247 305.24 m
478.909 304.648 l
478.909 304.648 m
535.748 302.891 l
478.909 304.648 m
474.762 282.133 l
474.762 282.133 m
522.328 279.126 l
474.762 282.133 m
470.614 257.84 l
470.614 257.84 m
474.413 222.291 l
470.614 257.84 m
497.658 245.97 l
458.172 334.273 m
523.939 357.38 l
523.939 357.38 m
550.811 339.348 l
523.939 357.38 m
558.082 365.661 l
367.52 490.1 m
364.557 529.797 l
364.557 529.797 m
227.69 643.557 l
227.69 643.557 m
259.721 696.575 l
227.69 643.557 m
202.805 657.184 l
202.805 657.184 m
180.515 674.901 l
202.805 657.184 m
218.803 672.589 l
218.803 672.589 m
204.456 684.212 l
218.803 672.589 m
230.954 691.646 l
364.557 529.797 m
397.737 531.575 l
397.737 531.575 m
282.653 698.278 l
397.737 531.575 m
423.807 530.982 l
423.807 530.982 m
371.075 621.042 l
371.075 621.042 m
363.372 654.222 l
363.372 654.222 m
324.267 674.959 l
324.267 674.959 m
312.658 697.592 l
324.267 674.959 m
338.76 694.285 l
363.372 654.222 m
387.072 648.889 l
387.072 648.889 m
362.018 689.139 l
387.072 648.889 m
410.18 647.704 l
410.18 647.704 m
413.688 669.532 l
410.18 647.704 m
436.055 656.994 l
371.075 621.042 m
457.067 642.476 l
423.807 530.982 m
450.469 490.1 l
450.469 490.1 m
531.049 398.262 l
531.049 398.262 m
561.545 384.143 l
531.049 398.262 m
564.379 413.121 l
450.469 490.1 m
465.282 514.392 l
465.282 514.392 m
451.654 604.452 l
451.654 604.452 m
467.682 633.957 l
451.654 604.452 m
485.189 617.818 l
465.282 514.392 m
487.204 497.21 l
487.204 497.21 m
528.087 454.55 l
528.087 454.55 m
564.542 432.685 l
528.087 454.55 m
561.748 464.867 l
487.204 497.21 m
497.869 522.687 l
497.869 522.687 m
502.086 599.177 l
497.869 522.687 m
526.309 508.467 l
526.309 508.467 m
518.014 543.425 l
518.014 543.425 m
523.106 570.011 l
518.014 543.425 m
538.057 542.756 l
526.309 508.467 m
538.752 484.767 l
538.752 484.767 m
557.619 486.753 l
538.752 484.767 m
552.918 504.374 l
119.703 212.651 m
34.6766 169.364 l
538.057 542.756 m
34.6766 169.364 l
"""

tree_data = """223.911 231.697 m
209.691 332.422 l
209.691 332.422 m
145.109 378.637 l
145.109 378.637 m
100.079 350.197 l
145.109 378.637 m
104.819 439.071 l
145.109 378.637 m
84.6738 408.854 l
84.6738 408.854 m
51.4939 453.884 l
84.6738 408.854 m
15.944 436.701 l
209.691 332.422 m
244.648 379.822 l
244.648 379.822 m
310.416 394.634 l
310.416 394.634 m
348.928 353.159 l
310.416 394.634 m
372.628 404.114 l
372.628 404.114 m
415.288 423.074 l
244.648 379.822 m
252.943 416.556 l
244.648 379.822 m
301.528 424.851 l
301.528 424.851 m
288.493 459.216 l
301.528 424.851 m
327.598 475.806 l
209.691 332.422 m
216.801 450.329 l
216.801 450.329 m
139.184 527.946 l
139.184 527.946 m
137.999 570.014 l
139.184 527.946 m
103.041 562.311 l
139.184 527.946 m
91.7838 520.836 l
91.7838 520.836 m
42.0139 507.209 l
91.7838 520.836 m
35.4965 538.019 l
103.041 562.311 m
55.6414 584.233 l
103.041 562.311 m
71.6389 630.448 l
216.801 450.329 m
258.868 498.914 l
258.868 498.914 m
289.086 541.574 l
289.086 541.574 m
308.638 584.233 l
289.086 541.574 m
351.298 565.274 l
258.868 498.914 m
333.523 519.651 l
333.523 519.651 m
376.183 517.281 l
376.183 517.281 m
409.955 499.506 l
376.183 517.281 m
408.77 522.021 l
333.523 519.651 m
381.515 542.759 l
381.515 542.759 m
406.993 578.901 l
216.801 450.329 m
225.688 523.206 l
225.688 523.206 m
207.913 577.124 l
225.688 523.206 m
284.346 602.601 l
284.346 602.601 m
265.386 648.223 l
284.346 602.601 m
329.376 665.998 l
284.346 602.601 m
343.596 628.078 l
207.913 577.124 m
217.393 612.081 l
217.393 612.081 m
235.761 612.673 l
217.393 612.081 m
187.176 634.596 l
217.393 612.081 m
208.506 671.923 l
207.913 577.124 m
151.034 611.488 l
151.034 611.488 m
149.849 681.403 l
151.034 611.488 m
102.449 626.893 l
"""

def parse_bacteria_tree():
    L = 100.0
    rot = (90.0) / (2*math.pi)
    cycle_center = [279.847/L, 427.013/L, 0]
    cycle_radius = 273.232/L
    positions = {}
    leaves = [0, 2, 4, 6, 8, 10, 14, 15, 17, 19, 20, 22, 26, 27, 28, 30, 33, 35, 36, 41, 42, 45, 48, 49, 50, 52, 54, 56, 57, 58, 60, 64, 66, 68, 70, 71, 73, 74, 77, 79, 81, 82, 84, 89, 90, 92, 94, 95, 96, 99, 100, 103, 104, 107, 108, 110, 113, 114, 116, 117]
    pos_to_vertex = {}
    edges = []
    data = [(float(d.split(" ")[0]) / L - cycle_center[0], \
            float(d.split(" ")[1]) / L - cycle_center[1], \
            0.0)\
             for d in bacteria_data.splitlines()]


    for i in range(int(len(data)/2)-2): # last 2 lines are to distinguish a and b (bad hack)
        pos_u = data[2*i]
        pos_v = data[2*i+1]
        if pos_u == pos_v:
            continue
        for pos in (pos_u, pos_v):
            if not pos in pos_to_vertex:
                node_id = len(pos_to_vertex)
                positions[node_id] = pos
                pos_to_vertex[pos] = node_id
                #if math.dist((0,0,0), pos) > 0.95 * cycle_radius:
                #    leaves.append(node_id)
        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    pos_a = data[-4]
    pos_b = data[-2]
    a = pos_to_vertex[pos_a]
    b = pos_to_vertex[pos_b]

    for pos in positions:
        positions[pos] = (\
            math.cos(rot) * positions[pos][0] + math.sin(rot) * positions[pos][1], \
            math.cos(rot) * positions[pos][1] - math.sin(rot) * positions[pos][0], 0.0)
        #positions[pos] = (positions[pos][0], positions[pos][1], 0)

    for k, v in positions.items():
        positions[k] = np.asarray(v)


    return range(len(positions)), edges, positions, a, b, leaves

def parse_tree_tree():
    L = 80.0
    positions = {}
    pos_to_vertex = {}
    edges = []
    data = [(float(d.split(" ")[0]) / L, \
            float(d.split(" ")[1]) / L, \
            0)\
             for d in tree_data.splitlines()]

    for i in range(int(len(data)/2)):
        pos_u = data[2*i]
        pos_v = data[2*i+1]
        if pos_u == pos_v:
            continue
        for pos in (pos_u, pos_v):
            if not pos in pos_to_vertex:
                node_id = len(pos_to_vertex)
                positions[node_id] = pos
                pos_to_vertex[pos] = node_id
                
        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    for k, v in positions.items():
        positions[k] = np.asarray(v)

    return range(len(positions)), edges, positions    

####################################################################

def get_adjacency_list(g):
    adj = dict([(v, []) for v in g.vertices])
    for v1, v2 in g.edges:
        adj[v1].append(v2)
        adj[v2].append(v1)

    return adj

def bfs(g: Graph, start):
    adj = get_adjacency_list(g)

    res_vertices = [[start]]
    res_edges = [[]]
    res_parents = {start: None}
    seen = set([start])

    while True:
        cur_vertices = []
        cur_edges = []

        for v1 in res_vertices[-1]:
            for v2 in adj[v1]:
                if v2 not in seen:
                    cur_vertices.append(v2)
                    seen.add(v2)
                    cur_edges.append((v1, v2))
                    res_parents[v2] = v1

        if cur_vertices:
            res_vertices.append(cur_vertices)
            res_edges.append(cur_edges)
        else:
            break

    return res_vertices, res_edges, res_parents

def get_path(g: Graph, start, end):
    _, _, parents = bfs(g, end)
    path = [start]

    while path[-1] != end:
        path.append(parents[path[-1]])

    return path

def hanging_position(g: Graph, start, end, shift=(0.0, 0.0, 0.0), Delta=0.3, scale = 0.5):
    positions = {}
    top = get_path(g, start, end)

    adj = get_adjacency_list(g)
    weights = {}
    level_order = {}
    pi = {}
    parent = {}
    i = 0
    for u in g.vertices:
        pi[u] = i
        i = i+1

    def weight(v, parents, depth):
        w = 1
        for v2 in adj[v]:
            if v2 not in parents:
                w += weight(v2, [v], depth+1)
        weights[v] = w
        if depth > 0:
            parent[v] = parents[0]
            positions[v] = np.array([0.0, -depth, 0])
            if not depth in level_order:
                level_order[depth] = []
            level_order[depth].append(v)
        return w

    for i, v1 in enumerate(top):
        positions[v1] = np.array([i * 1.0 - len(top) / 2.0 + 0.5, 0.0, 0.0])
        weight(v1, top, 0)


    # LP
    # variably:    n* x_i ... pozice na x-ove ose
    #              n* c_i ... rozdil na x-ove ose me a meho otce
    #              vektor promennych je konkatenace x_i a c_i
    # constrainty: pro rooty je x_i = jejich pozice
    #              jinak kdyz x_i a x_j vedle sebe tak x_j > x_i + Delta
    #              a nakonec c_i >= |x_i - x_p(i)|
    # MIN sum w_i * c_i kde w_i je velikost podstromu

    n = len(g.vertices)
    num_var = 2 * n
    
    A = []
    b = []
    c = np.zeros(num_var)  
    
    for u in g.vertices:
        if u in top: # je-li to root tak x_i = současná pozice i
            l = np.zeros(num_var)
            l[pi[u]] = 1
            A.append(l) 
            A.append(-l)
            b.append(positions[u][0])
            b.append(-positions[u][0])
        else: # jinak c_i >= |x_i - x_p(i)|
            c[n+pi[u]] = weights[u]
            l = np.zeros(num_var)
            l[pi[u]] = 1
            l[pi[parent[u]]] = -1
            l[n+pi[u]] = -1
            A.append(l)
            l = -l
            l[n+pi[u]] = -1
            A.append(l)
            b.append(0)
            b.append(0)

    for i in level_order:
        lev = level_order[i]
        for i in range(1, len(lev)): # pro ty vedle plati x_j > x_i + Delta
            l = np.zeros(num_var)
            l[pi[lev[i]]] = -1
            l[pi[lev[i-1]]] = 1

            A.append(l)
            b.append(-Delta)
    
    
    constraints = []
    for i in range(num_var):
        constraints.append((None, None))

    res = linprog(c, A_ub=A, b_ub=b, bounds=constraints)
    
    for u in g.vertices:
        positions[u][0] = 1.0 * res.x[pi[u]]


    for k in positions:
        positions[k] *= scale
        positions[k] += shift

    return positions


####################################################################

example_edges = [
    (0, 1),
    (1, 10),
    #(1, 11),
    (1, 2),
    (2, 20),
    (20, 21),
    (2, 3),
    #(3, 30),
    #(30, 31),
    (3, 4),
    (4, 40),
    (40, 41),
    (41, 42),
    (41, 43),
    (42, 44),
    #(42, 45),
    (43, 46),
    (4, 5),
    (5, 50),
    #(51, 50),
    (52, 50),
    #(51, 53),
    (52, 54),
    (54, 55),
    (54, 56),
    (5, 6),
    (6, 60),
    (60, 61),
    (60, 62),
    (61, 63),
    (61, 64),
    (62, 65),
    (6, 7),
    (8, 7),
    (8, 80),
    (8, 9)]
example_vertices = np.unique(np.array([item for sublist in example_edges for item in sublist]))

####################################################################


config.background_color = solarized.BASE2


class Intro(Scene):
    def construct(self):
        erdos = ImageMobject("img/erdos.jpg")
        straight = Text("Straight from the Book!")
        erdos.shift(5*RIGHT)
        self.add(erdos)
        self.add(straight)
        self.wait(1)
        self.remove(erdos, straight)

#https://illustoon.com/?dl=383
class Definice_stromu(Scene):
    def construct(self):
        tree = ImageMobject("img/tree.png")
        self.add(tree)
        self.wait(1)

        vertices, edges, positions = parse_tree_tree()

        self.g = Graph(
            vertices,
            edges,
            layout="kamada_kawai",
            labels=False,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(self.g))
        
        self.wait(1)

        vec = tree.get_center() - tree.get_start()
        delta = positions[0] - tree.get_center() - np.array([0.0, 0.8*vec[1], 0.0])
        #(-2.5, -6.0, 0.0)
        for k, v in positions.items():
            v -= delta

        self.play(self.g.animate.change_layout(positions))
        
        self.wait(1)

        self.g.add_edges((6, 22))

        self.wait(1)

        self.g.remove_edges((1, 8))

        self.wait(10)


class Kutaleci_strom(Scene):
    def construct(self):
        self.g = Graph(example_vertices,example_edges)
        sh = (-2,3,0)
        hanging1 = hanging_position(self.g, 4, 4, shift=sh)
        self.g = Graph(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale = 2,
            labels=False,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(self.g))  
        self.wait(1)

        delta = (-2.0, 0.0, 0.0)
        for k, v in hanging1.items():
            v += delta

        self.play(self.g.animate.change_layout(hanging1))
        self.wait(1)


        hanging2 = hanging_position(self.g, 4, 9, shift=sh)
        delta = hanging1[4] - hanging2[4]
        for k, v in hanging2.items():
            v += delta


        self.play(self.g.animate.change_layout(hanging2))

        self.wait(1)

        hanging3 = hanging_position(self.g, 9, 9)
        delta = hanging2[9] - hanging3[9]
        for k, v in hanging3.items():
            v += delta

        self.play(self.g.animate.change_layout(hanging3))

        self.wait(1)

        hanging4 = hanging_position(self.g, 9, 0)
        delta = hanging3[9] - hanging4[9]
        for k, v in hanging4.items():
            v += delta

        self.play(self.g.animate.change_layout(hanging4))

        self.wait(1)


        self.wait(1)
              

class LongestPath(Scene):

    def construct(self):
         
        self.g = Graph(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=4.0,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
        )

        self.play(Create(self.g))

        self.wait(1)
        
        sh = (0,1,0)
        hanging1 = hanging_position(self.g, 0, 9, shift=sh)

        self.play(self.g.animate.change_layout(hanging1))

        self.wait(1)


        tleft = hanging1[0]
        tright= hanging1[9]
        tmid  = (tleft + tright)/2.0
        tbot  = tmid - [(tmid-tleft)[1], (tmid-tleft)[0], 0]

        ltop  = Line(tleft, tright)
        lleft = Line(tleft, tbot)
        lright= Line(tbot, tright)
        self.add(ltop)
        self.add(lleft)
        self.add(lright)

        self.wait(1)

        self.remove(ltop, lleft, lright)

        self.wait(10)

        
        self.play(self.g.animate.change_layout(hanging_position(self.g, 44, 65, shift=sh)))

        self.wait(1)




class Bacteria(Scene):

    def construct(self):


        vertices, edges, positions, a, b, leaves = parse_bacteria_tree()
        vconfig = {"color": solarized.BASE00}
        
        self.g = Graph(
            vertices,
            edges,
            layout=positions, #"kamada_kawai",
            vertex_config=vconfig,
            edge_config={"color": solarized.BASE00},
        )

        longest = get_path(self.g, a, b)

        for u in longest:
            vconfig[u] = {"fill_color": RED}
        for u in leaves:
            vconfig[u] = {"fill_color": GREEN}

        self.play(Create(self.g))

        self.wait(1)

        self.remove(self.g)

        
        self.g = Graph(
            vertices,
            edges,
            layout=positions, #"kamada_kawai",
            layout_scale=4.0,
            #labels = True,
            vertex_config=vconfig,
            edge_config={"color": solarized.BASE00},
        )

        self.play(self.g.animate.change_layout("kamada_kawai"))

        self.wait(1)
      
