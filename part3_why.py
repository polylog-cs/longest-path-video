from manim import *


class PhysicalModel(Scene):
    def construct(self):
        pass
        # TODO: osnova: Why it works

        # TODO: obrázek knížky a jména autorů

        # TODO: fyzická demonstrace odteď dál, bude to ten stejný strom a run algoritmu jako předtím,
        #   jen fyzicky, klidně vedle toho může být obrázek té původní animace aby to šlo srovnat

        # TODO: vedle vaška se udělá animace, která zopakuje breadth first search z vrcholu.
        #   Pak animace strom zavěsí za stejnou nodu jako vašek

        # TODO: drží to horizontálně jako trojúhelník


class Triangle(Scene):
    def construct(self):
        pass
        # TODO: tady někde se přejde zpátky k animaci, vyznačí se trojúhelník

        # TODO: strom se složí do nějakého výchozího postavení, pak se prohodí nejdelší cesta

        # TODO: animace, zvýraznit třetí vrchol horní cesty a pak vzdálenost k levému
        #   kraji a ke spodku podstromu (vzdálenost je stejná)

        # TODO: důkaz trojúhelníkovosti sporem - animace sporné cesty


class Proof(Scene):
    def construct(self):
        pass
        # TODO: animace, ukázat trojúhelník, zvýrazit a

        # So, recall that we start by finding some node farthest away from a.
        # Let's think about where this farthest node can be. We start computing
        # distances from a to other nodes. Let us pause the algorithm now, just
        # one step before we reach the leftmost node. By this time, we have
        # already reached all nodes on the left side, except the nodes lying on
        # the edge of the triangle. We have also reached the node on the right
        # that is closest to the bottom tip of the triangle. That means we
        # already reached all the nodes in the right side of the triangle to the
        # left of a. Finally, we have reached all the nodes to the right of a,
        # because the furthest one, in the right tip of the triangle, is
        # definitely strictly closer than the node in the furthest left tip.
        # TODO: animace toho, jak algoritmus postupuje, stopne krok před cílem, pak
        #   se tam občas objeví nějaké čáry, když se porovnávají vzdálenosti

        # TODO: nějak se vyznačí vrcholy na levé hraně trojúhelníka

        # TODO: animace ohne cestu co jsme našli na tu horní, aby se ukázalo, že jsou
        #   stejně dlouhé


class EvenCase(Scene):
    def construct(self):
        pass
        # TODO: obrázek druhého casu, bude napravo od prvního (příprava na nadcházející animaci)
        # TODO: nechat to viewera rozdejchat


class OtherUses(Scene):
    def construct(self):
        pass
        # This is not the only thing the picture is useful for. For example, it
        # also shows that all longest paths in a tree will either share their
        # middle edge, if the diameter is even, or they share the middle node if
        # the diameter is odd. This middle edge or a node is called the center
        # of the tree and it is also the only place in the tree from which you
        # can reach all other nodes in smallest number of steps, namely half of
        # the tree’s diameter. Or to be precise, its half of the tree’s
        # diameter, rounded up  [+1 u sudých]

        # TODO: animace - běhají různé nejdelší cesty, uprostřed je highlightnutá
        #   hrana (nalevo) nebo vrchol (napravo), vyznačí se centrum  a z něj se
        #   spustí bfs
