from manim import *


class Naive(Scene):
    def construct(self):
        pass
        # TODO: osnova: Algorithm

        # TODO: animace nkrát zkopírovaného grafu (už je to náš příkladový graf),
        #   na každém běží bfs z jednoho vrcholu, důležité, aby jednotlivá bfs
        #   běžela sekvenčně a každé bfs běželo sekvenčně, nakonec tam bude n^2
        #   čísel a z nich se vyznačí jedno z největších, pak odpovídající
        #   nejdelší cesta, pak to samé se zbylými největšími

        # (animace, jak vašek klikne v terminálu na enter, pak se zapne TQDM progress bar
        #   a bude vidět na pozadí při mluvení, aby se ukázalo, jak pomalé to je)

        # After waiting for like an hour, our calculation seems to be about right.
        # TODO: animace výpočtu nxn/10^6 = …, pak jak vypadá tqdm bar po hodině?


class QuadraticVsLinear(Scene):
    def construct(self):
        pass
        # TODO: animace lineární a kvadratické křivky: n^2 vs n vs 10n


class Algorithm(Scene):
    def construct(self):
        pass
        # Fortunately, there is a much faster algorithm whose number of steps is about 2n.
        # Here is how it works. We start by picking one node in our tree, it doesn't matter which one. We call it, say, a.
        # Next, we find the distance from it to all other nodes.

        # TODO: animace toho, jak se vybere a a jede bfs

        # TODO: zvýraznit b

        # TODO: animace bfs, vyznačí se cesta mezi b a c

        # TODO: zase animace, stejný strom ale jiné a, vyjde jiná nejdelší cesta

        # TODO: animace terminálu, kde vašek klikne a hned vidí výsledek