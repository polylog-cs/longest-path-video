from manim import *
import numpy as np
import math

import solarized
import tree_data
from util import Tree
from util import OScene

class RotPolygon(Polygon):
    def align_and_rotate(self, obj, leftright, bottomtop, rot):
        self.rotate(rot)
        self.align_to(obj, leftright)
        self.align_to(obj, bottomtop)

    def align(self, obj, leftright, bottomtop):
        self.align_to(obj, leftright)
        self.align_to(obj, bottomtop)

class TheBook(Scene):
    def construct(self):
        # TODO: obrázek knížky?
        erdos = ImageMobject("img/erdos.jpg")  #wiki
        erdos.shift(5 * LEFT)
        
        straight = Tex(r"Straight from the Book!", color=solarized.BASE00)
        straight.shift(2 * UP)

        self.play(FadeIn(erdos))
        self.play(Create(straight))
        self.wait(1)
        #self.play(FadeOut(erdos), FadeOut(straight))
        


        #################################################################

        #kniha
        offset = np.array((-2.0,-2.0,-1))
        book_height = 2.5
        book = SVGMobject("img/open-book.svg", height = book_height)
        #http://www.clker.com/cliparts/I/O/x/x/4/8/open-book.svg
        book.move_to(offset)
        
        self.play(FadeIn(book))

        #first square

        a = 5.0
        b = 12.0
        scale = 0.5 * book_height / (a+b)
        a *= scale
        b *= scale
        c = math.sqrt(a*a + b*b)
        
        #nejdriv vnejsi ctverce
        outer_shift = np.array((0.28 * book_height, 0.0 * book_height, 0))
        outer_color = GREEN
        outer_square = Square(side_length = (a+b), color = outer_color)
        outer_square.move_to(np.array(offset) - outer_shift)

        outer_square2 = outer_square.copy()
        outer_square2.move_to(np.array(offset) + outer_shift)

        
        #self.wait(1)
        
        #pak vnitrni
        inner_color = BLUE
        inner_square = Square(side_length = c, color = inner_color)
        inner_square.set_fill(inner_color, opacity = 1.0)
        inner_square.rotate(math.asin(a / c))
        inner_square.align_to(outer_square, LEFT)
        inner_square.align_to(outer_square, DOWN)

        self.play(FadeIn(outer_square), FadeIn(outer_square2), FadeIn(inner_square))
        
        #self.wait(1)
        

        #pak trojuhelniky
        tr_color = RED

        tr_botleft = RotPolygon([0,0,0], [a, 0, 0], [0, b, 0], color = tr_color) 
        tr_botleft.align(outer_square, LEFT, DOWN)

        tr_botright = RotPolygon([0,0,0], [0, a, 0], [-b, 0, 0], color = tr_color)
        tr_botright.align(outer_square, RIGHT, DOWN)

        tr_topright = RotPolygon([0,0,0], [-a, 0, 0], [0, -b, 0], color = tr_color)
        tr_topright.align(outer_square, RIGHT, UP)

        tr_topleft = RotPolygon([0,0,0], [0, -a, 0], [b, 0, 0], color = tr_color)
        tr_topleft.align(outer_square, LEFT, UP)



        self.play(Create(tr_botleft), \
                Create(tr_botright), \
                Create(tr_topright), \
                Create(tr_topleft))
        #self.wait(1)


        #pak se presunou
        self.play(ApplyMethod(tr_botleft.align_and_rotate, outer_square2, LEFT, DOWN, 0), \
            ApplyMethod(tr_botright.align_and_rotate, outer_square2, LEFT, DOWN, math.pi/2), \
            ApplyMethod(tr_topright.align_and_rotate, outer_square2, RIGHT, UP, -math.pi/2), \
            ApplyMethod(tr_topleft.align_and_rotate, outer_square2, RIGHT, UP, 0))
        #self.play(MoveToTarget(tr_botright))


        #nakonec male ctverce
        a_square = Square(side_length = a, color = inner_color)
        a_square.align_to(outer_square2, LEFT)
        a_square.align_to(outer_square2, UP)
        a_square.set_fill(inner_color, opacity = 1.0)
        b_square = Square(side_length = b, color = inner_color)
        b_square.align_to(outer_square2, RIGHT)
        b_square.align_to(outer_square2, DOWN)
        b_square.set_fill(inner_color, opacity = 1.0)

        self.play(FadeIn(a_square), FadeIn(b_square))
        


        ########################################################

        #kniha
        offset2 = offset + np.array((6, 0, 0))
        book2 = SVGMobject("img/open-book.svg", height = book_height)
        #http://www.clker.com/cliparts/I/O/x/x/4/8/open-book.svg
        book2.move_to(offset2)
        self.play(FadeIn(book2))

        #strom
        tree_scale = 0.95
        edge_scale = 0.2
        node_radius = 0.05
        base_color = solarized.BASE00
        highlight_color = RED

        ex_tree = Tree(
            tree_data.misof_example_vertices,
            tree_data.misof_example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={
                "radius": node_radius,
                "color": base_color
            },
            labels = False,
            edge_config={"color": base_color},
            # labels=True
        )
        self.add_foreground_mobjects(ex_tree)
        ex_tree.move_to(offset2+np.array((-0.5*book_height, 0, 0)))
        self.play(Create(ex_tree))


        a = 4
        b = 10
        c = 20

        self.play(ex_tree.animate.set_path_color(a, a, GREEN))
        a_hanging = ex_tree.hanging_position(a, a, \
            shift = offset2 + np.array((-0.25 * book_height, 0.4 * book_height, 0)),\
            scale = edge_scale, \
            delta = 10*node_radius)
        
        self.play(ex_tree.animate.change_layout(a_hanging))
        self.play(ex_tree.animate.set_path_color(b, b, highlight_color))

        ex_tree2 = ex_tree.copy()
        b_hanging = ex_tree.hanging_position(b, b, \
            shift = offset2 + np.array((+0.25 * book_height, 0.4 * book_height, 0)),\
            scale = edge_scale, \
            delta = 10*node_radius)

        self.play(ex_tree2.animate.set_path_color(a, a, base_color), \
            ex_tree2.animate.set_path_color(b, b, highlight_color), \
            ex_tree2.animate.change_layout(b_hanging))

        #self.play(ex_tree2.animate.set_path_color(c, c, highlight_color))
        self.play(ex_tree2.animate.set_path_color(b, c, highlight_color))

        # TODO: animace s našimi jmény - Vašek ® a Václav (V),
        #   pokud bude separátní channel, tak jméno channelu,
        #   naznačit že mluví vašek v?, taky někde napsáno SoME challenge

        self.play(FadeOut(erdos), FadeOut(straight), FadeOut(book), FadeOut(book2), \
            FadeOut(outer_square), FadeOut(outer_square2), FadeOut(inner_square), \
            FadeOut(tr_botright), FadeOut(tr_botleft), FadeOut(tr_topleft), FadeOut(tr_topright), \
            FadeOut(ex_tree), FadeOut(ex_tree2), FadeOut(a_square), FadeOut(b_square))


        volhejn = Tex(r"Vaclav Volhejn", color=solarized.BASE00)
        rozhon = Tex(r"Vaclav Rozhon", color=solarized.BASE00)
        rozhon.shift(2*DOWN+4*RIGHT)
        volhejn.shift(3*DOWN+4*RIGHT)
        # dodelat right bottom align

        self.play(FadeIn(rozhon), FadeIn(volhejn))

        self.wait(10)



class TreeIntro(OScene):
    def construct(self):
        # TODO: vyznačí se osnova TREES, THE ALGORITHM, WHY IT WORKS?, zvýrazní se TREES
        base_color = solarized.BASE00
        node_radius = 0.2

        self.outline(1)
        

        # https://illustoon.com/?dl=383
        tree = ImageMobject("img/tree.png")
        tree.shift(np.array((3, 0, 0)))
        vertices, edges, positions = parse_tree_tree()

        self.g = Tree(
            vertices,
            edges,
            layout="kamada_kawai",
            labels=False,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # Passed to:
            # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html
            layout_config={"center": (-5, 0)},
        )
        
        #for k,v in self.g.positions:
        #    self.g.layout[k] = v * 0.5 + np.array((3,0,0))

        # TODO: vytvorit v puvodnim layoutu napred vedle (bio)stromu, ne pres nej
        self.play(Create(self.g))

        self.wait(1)

        self.play(FadeIn(tree))

        self.wait(1)

        vec = tree.get_center() - tree.get_start()
        delta = positions[0] - tree.get_center() - np.array([0.0, 0.8 * vec[1], 0.0])
        # (-2.5, -6.0, 0.0)
        for k, v in positions.items():
            v -= delta

        self.play(self.g.animate.change_layout(positions))
        self.wait(1)
        # TODO: vyresit ze hrany (abstraktniho) stromu jsou za vetvemi skutecneho
        #   a problikavaji
        # self.bring_to_back(tree)
        self.play(FadeOut(tree))

        # This means that in a tree, you can walk from every node to every other node
        # using the connections between nodes,
        # but there is always just one way of doing that.
        # TODO: animace typu vyznačí se dva vrcholy a pak cesta mezi nimi

        extra_edge = Line(
            self.g[6].get_center(), self.g[22].get_center(), color=solarized.RED
        )

        self.play(Create(extra_edge))
        self.wait(1)

        # TODO: vyznacit vytvoreny cyklus
        self.wait(1)
        self.play(self.g.animate.set_path_color(6, 22, solarized.RED))

        self.wait(1)
        self.play(Uncreate(extra_edge), self.g.animate.set_path_color(6, 22, solarized.BASE00))
        self.wait(1)

        self.play(self.g.animate.remove_edges((1, 8)))
        
        self.play(self.g.animate.set_path_color(1,1, solarized.RED), self.g.animate.set_path_color(8,8, solarized.RED))
        
        self.wait(1)
        self.play(self.g.animate.set_path_color(1,1, base_color), self.g.animate.set_path_color(8,8, base_color))

        self.wait(10)
        self.play(FadeOut(tree, self.g))

class Filesystem(Scene):
    def construct(self):
        # TODO: labely u vrcholu? reprezentativnejsi subset?
        #   mozna by bylo lepsi udelat nejakej umelej priklad jako
        #   ~/, ~/Documents, ~/Documents/school/thesis.tex, ~/Documents/manim/,
        #   ~/Pictures/vacation/...
        #   etc a ukazat to podobne jako to dela prikaz `tree`
        edges = tree_data.parse_linux_tree("vv_filesystem_L2_edited.txt")

        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])

        # labels = dict((v, Text(v, fill_color=solarized.ORANGE)) for v in vertices)
        # labels["/Applications"] = Text("/Applications", fill_color=solarized.ORANGE)

        file_tree = Tree(
            vertices,
            edges,
            layout="kamada_kawai",
            layout_scale=3,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # labels=labels,
        )

        # self.play(DrawBorderThenFill(g))
        self.play(Create(file_tree))
        self.wait(1)

        #bacteria

        vertices, edges, positions, a, b, a2, b2, leaves = parse_bacteria_tree(shift = (3, 0, 0))
        base_color = solarized.BASE00
        node_radius = 0.05
        # labels = dict((v, Text(str(v), fill_color=BLACK, size=0.15)) for v in vertices)
        g = Tree(
            vertices,
            edges,
            layout=positions,  # "kamada_kawai",
            labels=True,
            vertex_config={
                "radius": node_radius,
                "color": base_color
            },
            edge_config={"color": base_color},
            # labels=labels,
        )

        self.play(Create(g))
        self.wait(1)

        c = 67
        d = 85
        self.wait(1)
        self.play(g.animate.set_path_color(c, d, RED))
        self.play(g.animate.set_path_color(c, d, base_color))


        self.wait(1)

        self.play(g.animate.set_colors(dict((v, solarized.GREEN) for v in leaves)))
        self.wait(1)

        self.play(g.animate.set_path_color(a, b))
        self.wait(1)

        self.play(g.animate.set_path_color(a2, b2, solarized.BLUE))
        
        self.wait(1)
        self.play(FadeOut(g), FadeOut(file_tree))
        self.wait(10)

def parse_tree_tree():
    L = 80.0
    positions = {}
    pos_to_vertex = {}
    edges = []
    data = [
        (float(d.split(" ")[0]) / L, float(d.split(" ")[1]) / L, 0)
        for d in tree_data.tree_data.splitlines()
    ]

    for i in range(int(len(data) / 2)):
        pos_u = data[2 * i]
        pos_v = data[2 * i + 1]
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


def parse_bacteria_tree(rot = 0.0, shift = np.array((0,0,0))):
    a = 6
    b = 111
    a2 = 16
    b2 = 105
    L = 90.0
    cycle_center = [279.847 / L, 427.013 / L, 0]
    cycle_radius = 273.232 / L
    positions = {}
    leaves = tree_data.bacteria_leaves
    pos_to_vertex = {}
    edges = []
    data = [
        (
            float(d.split(" ")[0]) / L - cycle_center[0],
            float(d.split(" ")[1]) / L - cycle_center[1],
            0.0,
        )
        for d in tree_data.bacteria_data.splitlines()
    ]

    for i in range(
        int(len(data) / 2)
    ):  
        pos_u = data[2 * i]
        pos_v = data[2 * i + 1]
        if pos_u == pos_v:
            continue
        for pos in (pos_u, pos_v):
            if not pos in pos_to_vertex:
                node_id = len(pos_to_vertex)
                positions[node_id] = pos
                pos_to_vertex[pos] = node_id
                # if math.dist((0,0,0), pos) > 0.95 * cycle_radius:
                #    leaves.append(node_id)
        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    '''    
    leaves = []
    for k, v in positions.items():
        if math.dist((0,0,0), v) - cycle_radius > -0.2:
            leaves.append(k)
    print(leaves)
    '''

    '''
    for pos in positions:
        positions[pos] = (
            math.cos(rot) * positions[pos][0] + math.sin(rot) * positions[pos][1],
            math.cos(rot) * positions[pos][1] - math.sin(rot) * positions[pos][0],
            0.0,
        )
        # positions[pos] = (positions[pos][0], positions[pos][1], 0)
    '''

    for k, v in positions.items():
        positions[k] = np.asarray(v) + shift

    return range(len(positions)), edges, positions, a, b, a2, b2, leaves
