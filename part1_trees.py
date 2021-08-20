from manim import *
from manim.utils import tex
import numpy as np
import math
import textwrap

import solarized
import tree_data
from util import *


class TheBook(Scene):
    def construct(self):
        text_color = solarized.BASE00
        erdos_img = ImageMobject("img/erdos.jpg")  # wiki
        erdos_img.height = 4
        erdos_desc = Tex(r"Paul Erd\"{o}s", color=text_color)
        erdos = Group(erdos_img, erdos_desc).arrange(DOWN)

        erdos.shift(5 * LEFT)
        erdos.shift(1.5 * UP)

        self.play(FadeIn(erdos))
        self.wait(1)

        #################################################################

        # book reveal
        offset = np.array((2.0, -0.5, -1))
        offset_start = np.array((5.0, -2.0, -1))
        offset_finish = offset_start - np.array((10, 0.5, 0))
        book_height_large = 6.0
        book_height_small = 2.5
        book = OSVGMobject("img/open-book.svg", height=book_height_small)
        # http://www.clker.com/cliparts/I/O/x/x/4/8/open-book.svg
        book.move_to(offset_start)

        self.play(FadeIn(book))

        self.play(
            ApplyMethod(
                book.move_and_resize, offset, book_height_large / book_height_small
            )
        )
        # book travel

        # first square

        a = 5.0
        b = 12.0
        scale = 0.5 * book_height_large / (a + b)
        a *= scale
        b *= scale
        c = math.sqrt(a * a + b * b)

        # nejdriv vnejsi ctverce
        outer_shift = np.array((0.28 * book_height_large, 0.0 * book_height_large, 0))
        outer_color = GREEN
        outer_square = Square(side_length=(a + b), color=outer_color)
        outer_square.move_to(np.array(offset) - outer_shift)

        outer_square2 = outer_square.copy()
        outer_square2.move_to(np.array(offset) + outer_shift)

        # self.wait(1)

        # pak vnitrni
        inner_color = BLUE
        inner_square = Square(side_length=c, color=inner_color)
        inner_square.set_fill(inner_color, opacity=1.0)
        inner_square.rotate(math.asin(a / c))
        inner_square.align_to(outer_square, LEFT)
        inner_square.align_to(outer_square, DOWN)

        self.play(FadeIn(outer_square), FadeIn(outer_square2), FadeIn(inner_square))

        # self.wait(1)

        # pak trojuhelniky
        tr_color = RED

        pointedness = 0.00

        tr_botleft = RotPolygon([0, 0, 0], [a, 0, 0], [0, b, 0], color=tr_color)
        tr_botleft.align(outer_square, LEFT, DOWN)

        tr_botright = RotPolygon([0, 0, 0], [0, a, 0], [-b, 0, 0], color=tr_color)
        tr_botright.align(outer_square, RIGHT, DOWN)

        tr_topright = RotPolygon([0, 0, 0], [-a, 0, 0], [0, -b, 0], color=tr_color)
        tr_topright.align(outer_square, RIGHT, UP)

        tr_topleft = RotPolygon([0, 0, 0], [0, -a, 0], [b, 0, 0], color=tr_color)
        tr_topleft.align(outer_square, LEFT, UP)

        self.play(
            Create(tr_botleft),
            Create(tr_botright),
            Create(tr_topright),
            Create(tr_topleft),
        )
        # self.wait(1)

        # pak se presunou
        self.play(
            ApplyMethod(tr_botleft.align_and_rotate, outer_square2, LEFT, DOWN, 0),
            ApplyMethod(
                tr_botright.align_and_rotate,
                outer_square2,
                LEFT,
                DOWN,
                math.pi / 2,
                pointedness * UP,
            ),
            ApplyMethod(
                tr_topright.align_and_rotate, outer_square2, RIGHT, UP, -math.pi / 2
            ),
            ApplyMethod(
                tr_topleft.align_and_rotate,
                outer_square2,
                RIGHT,
                UP,
                0,
                pointedness * LEFT,
            ),
        )
        # self.play(MoveToTarget(tr_botright))

        # nakonec male ctverce
        thickness = 0.04
        a_square = Square(side_length=a - thickness, color=inner_color)
        a_square.align_to(outer_square2, LEFT)
        a_square.align_to(outer_square2, UP)
        a_square.shift((0, 0, -1))
        a_square.set_fill(inner_color, opacity=1.0)
        b_square = Square(side_length=b - thickness, color=inner_color)
        b_square.align_to(outer_square2, RIGHT)
        b_square.align_to(outer_square2, DOWN)
        a_square.shift((0, 0, 1))
        b_square.set_fill(inner_color, opacity=1.0)

        self.play(FadeIn(a_square), FadeIn(b_square))

        pythagoras = OGroup(
            outer_square,
            outer_square2,
            inner_square,
            tr_botright,
            tr_botleft,
            tr_topleft,
            tr_topright,
            a_square,
            b_square,
        )

        math_book = OGroup(book, pythagoras)

        ########################################################
        # erdos mluvi, knizka zaleze
        ########################################################

        straight = Tex(r"Straight from the Book!", color=text_color)
        straight.shift(3 * UP)

        self.play(Create(straight))
        # self.play(FadeOut(erdos), FadeOut(straight))

        self.play(
            ApplyMethod(
                math_book.move_and_resize,
                offset_finish,
                book_height_small / book_height_large,
            )
        )

        ########################################################
        # objevi se druha knizka, naleze doprostred, udela se v ni animace
        ########################################################

        # kniha
        offset2_start = offset_start
        book2 = OSVGMobject("img/open-book.svg", height=book_height_small)
        # http://www.clker.com/cliparts/I/O/x/x/4/8/open-book.svg
        book2.move_to(offset2_start)
        self.play(FadeIn(book2))

        offset2 = offset + np.array((0, 0, 0))
        self.play(
            ApplyMethod(
                book2.move_and_resize, offset2, book_height_large / book_height_small
            )
        )

        # strom
        time_scale = 2.0
        tree_scale = 2.0
        edge_scale = 0.5
        node_radius = 0.1
        base_color = solarized.BASE00
        highlight_color = RED

        ex_tree = Tree(
            tree_data.misof_example_vertices,
            tree_data.misof_example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": base_color},
            labels=False,
            edge_config={"color": base_color}
            # labels=True
        )

        # self.add_foreground_mobjects(ex_tree)
        offset2_tree_start = offset2 + np.array((-0.5 * book_height_large, 0, 0))
        ex_tree.move_to(offset2_tree_start)
        ex_tree.rot(offset2_tree_start, math.pi / 2.0)
        ex_tree.shift(1 * RIGHT)

        # self.play(Create(ex_tree))
        self.play(DrawBorderThenFill(ex_tree))
        return

        a = 5
        b = 10
        c = 20

        self.play(ex_tree.animate.set_path_color(a, a, GREEN))
        a_hanging = ex_tree.hanging_position(
            a,
            a,
            shift=offset2
            + np.array((-0.3 * book_height_large, 0.2 * book_height_large, 0)),
            scale=edge_scale,
            delta=5 * node_radius,
            custom_layers={2: [12, 3, 13, 7, 15, 18]},
        )

        self.play(ex_tree.animate.change_layout(a_hanging), run_time=time_scale)
        self.play(ex_tree.animate.set_path_color(b, b, highlight_color))

        ex_tree2 = ex_tree.copy()
        b_hanging = ex_tree.hanging_position(
            b,
            b,
            shift=offset2
            + np.array((+0.26 * book_height_large, 0.46 * book_height_large, 0)),
            scale=edge_scale,
            delta=5 * node_radius,
            custom_layers={},
        )

        # takle se to asi nema delat?
        self.play(ex_tree2.animate.set_path_color(a, a, base_color), run_time=0)
        self.play(ex_tree2.animate.set_path_color(b, b, highlight_color), run_time=0)
        self.play(ex_tree2.animate.change_layout(b_hanging), run_time=time_scale)
        self.wait(0.5)
        # self.play(ex_tree2.animate.set_path_color(c, c, highlight_color))
        self.play(ex_tree2.animate.set_path_color(b, c, highlight_color))

        # TODO: animace s našimi jmény - Vašek ® a Václav (V),
        #   pokud bude separátní channel, tak jméno channelu,
        #   naznačit že mluví vašek v?, taky někde napsáno SoME challenge

        ################################################################
        # everything fades out, then names are displayed
        ################################################################

        self.play(
            FadeOut(erdos),
            FadeOut(math_book),
            FadeOut(book2),
            FadeOut(straight),
            FadeOut(ex_tree),
            FadeOut(ex_tree2),
        )

        volhejn = Tex(r"Vaclav Volhejn", color=text_color)
        rozhon = Tex(r"Vasek Rozhon", color=text_color)
        names = Group(rozhon, volhejn).arrange(DOWN)
        names.shift(2 * DOWN + 4 * RIGHT)
        volhejn.align_to(names, RIGHT)
        rozhon.align_to(names, RIGHT)

        some_highlight_color = RED
        some_challenge = MarkupText(
            f'<span fgcolor="{some_highlight_color}">S</span>ummer <span fgcolor="{some_highlight_color}">o</span>f <span fgcolor="{some_highlight_color}">M</span>ath<span fgcolor="{some_highlight_color}"> E</span>xposition <span fgcolor="{some_highlight_color}">1</span>',
            color=text_color,
        )
        some_challenge.shift(1 * LEFT)

        self.play(FadeIn(names), Write(some_challenge))

        self.wait(1)

        self.play(FadeOut(names), Unwrite(some_challenge), run_time=1)

        self.wait(10)


class TreeIntro(OScene):
    def construct(self):
        base_color = solarized.BASE00
        node_radius = 0.2

        self.outline(1)

        # https://illustoon.com/?dl=383
        tree = ImageMobject("img/tree.png")
        tree.shift(np.array((100, 0, 0)))
        self.add(tree)

        # tree.set_opacity(0.5)
        vertices, edges, positions = parse_tree_tree()

        self.T = Tree(
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

        # for k,v in self.T.positions:
        #    self.T.layout[k] = v * 0.5 + np.array((3,0,0))

        self.play(Create(self.T))

        self.wait(1)

        tree.shift(np.array((-100 + 3, 0, 0)))
        self.play(FadeIn(tree))

        self.wait(1)

        vec = tree.get_center() - tree.get_start()
        delta = positions[0] - tree.get_center() - np.array([0.0, 0.8 * vec[1], 0.0])
        # (-2.5, -6.0, 0.0)
        for k, v in positions.items():
            v -= delta

        self.play(self.T.animate.change_layout(positions))
        self.play(self.T.animate.change_layout(positions), run_time=3)

        self.play(FadeOut(tree))

        # This means that in a tree, you can walk from every node to every other node
        # using the connections between nodes,
        # but there is always just one way of doing that.
        # [vyznačí se dva vrcholy a pak cesta mezi nimi]

        extra_edge = Line(
            self.T[6].get_center(), self.T[22].get_center(), color=solarized.RED
        )

        self.play(Create(extra_edge))
        self.wait(1)

        self.wait(1)
        self.play(self.T.animate.set_path_color(6, 22, solarized.RED))

        self.wait(1)
        self.play(
            Uncreate(extra_edge), self.T.animate.set_path_color(6, 22, solarized.BASE00)
        )
        self.wait(1)

        self.play(self.T.animate.remove_edges((1, 8)))

        self.play(
            self.T.animate.set_colors(vertex_colors = {1: solarized.RED, 8: solarized.RED})
        )

        self.wait(1)
        self.play(
            self.T.animate.set_colors(vertex_colors = {1: solarized.BASE00, 8: solarized.BASE00})
        )

        self.wait(10)
        self.play(FadeOut(tree, self.T))


class TreeExamples(Scene):
    def construct(self):
        # x = Dot()
        # self.add(x)

        # def foo(a):
        #     a.shift(RIGHT)
        #     a.scale(4)
        #     return a

        # self.play(ApplyFunction(foo, x))

        # self.play(x.animate.shift(RIGHT).scale(4))
        # self.play(x.animate)
        # self.wait()
        # return

        text_color = solarized.BASE00
        edges = tree_data.parse_linux_tree("fictional_filesystem.txt")

        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])

        # vertex order influences layout
        vertices = sorted(list(vertices))
        # import os
        # seed = int(os.environ["seed"])
        # self.add(Text(str(seed), color=RED))
        """
        # seed search (Fish shell):
        for seed in (seq 100)
            env seed={$seed} manim -pql part1_trees.py TreeExamples -s
            sleep 1
        end
        """
        seed = 1
        rng: np.random.Generator = np.random.default_rng(seed=seed)
        rng.shuffle(vertices)

        file_tree = Tree(
            vertices,
            edges,
            layout="kamada_kawai",
            layout_scale=3,
            vertex_config={"color": solarized.BASE00},
            edge_config={"color": solarized.BASE00},
            # labels=labels,
            vertex_type=ExternalLabeledDot,
            labels=True,
            label_class=Tex,
        )

        for v in file_tree.vertices:
            file_tree[v].reposition_label(file_tree, v)

        # self.play(DrawBorderThenFill(Gbacteria))
        self.play(Create(file_tree))
        self.wait(1)

        self.play(file_tree.animate.shift(LEFT * 4).scale(0.6))

        filesystem_str = textwrap.dedent(
            """
            ├── Documents
            │   ├── Books
            │   ├── ETH
            │   │   ├── Notes
            │   │   └── Thesis
            │   └── SoME1
            ├── Downloads
            ├── Movies
            └── Pictures
            """
        )

        filesystem_text = (
            Text(filesystem_str, color=solarized.BASE00).scale(0.8).shift(RIGHT * 3)
        )

        self.wait()
        self.play(Create(filesystem_text))
        self.wait(3)
        return
        self.play(Uncreate(filesystem_text))
        self.wait()

        # bacteria

        bacteria_mid_point = np.array((3, 0, 0))
        vertices, edges, positions, a, b, a2, b2, leaves = parse_bacteria_tree(
            shift=bacteria_mid_point
        )
        base_color = solarized.BASE00
        bac_highlight_color = RED
        node_radius = 0.05
        # labels = dict((v, Text(str(v), fill_color=BLACK, size=0.15)) for v in vertices)
        Gbacteria = Tree(
            vertices,
            edges,
            layout=positions,  # "kamada_kawai",
            labels=False,
            vertex_config={"radius": node_radius, "color": base_color},
            edge_config={"color": base_color},
        )

        self.play(Create(Gbacteria))
        self.wait(1)

        c = 67
        d = 68

        self.wait(1)

        self.play(
            Gbacteria.animate.set_colors(dict((v, solarized.GREEN) for v in leaves))
        )
        self.wait(1)
        self.play(Gbacteria.animate.set_colors(dict((v, base_color) for v in leaves)))
        self.wait(1)
        """
        
        """
        self.play(
            Gbacteria.animate.set_colors(
                {c: bac_highlight_color, d: bac_highlight_color}
            )
        )
        self.play(Gbacteria.animate.set_path_color(c, d, bac_highlight_color))
        self.play(Gbacteria.animate.set_path_color(c, d, base_color))
        """        

        """
        self.play(Gbacteria.animate.set_path_color(a, b))
        self.wait(1)

        self.play(
            Gbacteria.animate.rot(bacteria_mid_point, 47.0 / 360.0 * (2 * math.pi))
        )

        sc = 0.3
        dlt = 0.3
        self.wait(1)
        bact_hanging_position = Gbacteria.hanging_position(
            start=a, end=b, shift=bacteria_mid_point, delta=dlt, scale=sc
        )
        self.play(Gbacteria.animate.change_layout(bact_hanging_position), run_time=2)
        self.wait(1)

        txt_diameter = Tex(r"Diameter", color=text_color)
        txt_diameter.move_to(np.array((3, 1.5, 0)))
        seg_mid = Line(
            Gbacteria.vertices[a].get_center() + np.array((0, 1, 0)),
            Gbacteria.vertices[b].get_center() + np.array((0, 1, 0)),
            color=text_color,
        )
        l = 0.3
        seg_left = Line(
            seg_mid.get_start() + np.array((0, l, 0)),
            seg_mid.get_start() + np.array((0, -l, 0)),
            color=text_color,
        )
        seg_right = Line(
            seg_mid.get_end() + np.array((0, l, 0)),
            seg_mid.get_end() + np.array((0, -l, 0)),
            color=text_color,
        )
        seg = Group(seg_left, seg_mid, seg_right)

        self.play(Write(txt_diameter), FadeIn(seg))

        self.play(Gbacteria.animate.set_path_color(a2, b2, solarized.BLUE))

        self.wait(1)
        bact_hanging_position2 = Gbacteria.hanging_position(
            start=a2, end=b2, shift=bacteria_mid_point, delta=dlt, scale=sc
        )
        self.play(Gbacteria.animate.change_layout(bact_hanging_position2), run_time=2)

        file_a = "/Documents/ETH/Thesis"
        file_b = "/Downloads"

        anim1, anim2 = file_tree.path_animation(file_a, file_b, color=RED)
        self.play(anim1)
        self.wait(1)
        self.play(anim2)

        self.wait(1)
        self.play(
            FadeOut(Gbacteria), FadeOut(file_tree), FadeOut(txt_diameter), FadeOut(seg)
        )
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


def parse_bacteria_tree(rot=0.0, shift=np.array((0, 0, 0))):
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
                # if math.dist((0,0,0), pos) > 0.95 * cycle_radius:
                #    leaves.append(node_id)
        edges.append((pos_to_vertex[pos_u], pos_to_vertex[pos_v]))

    """    
    leaves = []
    for k, v in positions.items():
        if math.dist((0,0,0), v) - cycle_radius > -0.2:
            leaves.append(k)
    print(leaves)
    """

    """
    for pos in positions:
        positions[pos] = (
            math.cos(rot) * positions[pos][0] + math.sin(rot) * positions[pos][1],
            math.cos(rot) * positions[pos][1] - math.sin(rot) * positions[pos][0],
            0.0,
        )
        # positions[pos] = (positions[pos][0], positions[pos][1], 0)
    """

    for k, v in positions.items():
        positions[k] = np.asarray(v) + shift

    return range(len(positions)), edges, positions, a, b, a2, b2, leaves
