from manim import *


class TheBook(Scene):
    def construct(self):
        pass
        # TODO: animace, obrázek erdose, možná text citace aby bylo
        #   vidět capital B, obrázek knížky?

        # TODO: animace s našimi jmény - Vašek ® a Václav (V),
        #   pokud bude separátní channel, tak jméno channelu,
        #   naznačit že mluví vašek v?, taky někde napsáno SoME challenge


class TreeIntro(Scene):
    def construct(self):
        pass
        # TODO: vyznačí se osnova TREES, THE ALGORITHM, WHY IT WORKS?, zvýrazní se TREES

        # TODO: obrázek abstraktního stromu, objeví se opravdový strom
        #   a abstraktní strom se na něj nasune

        # This means that in a tree, you can walk from every node to every other node
        # using the connections between nodes,
        # but there is always just one way of doing that.
        # TODO: animace typu vyznačí se dva vrcholy a pak cesta mezi nimi

        # TODO: animace disconnected grafu a grafu s cyklem


class TreeExamples(Scene):
    def construct(self):
        pass
        # TODO: ukázat filesystem strom, labely u vrcholů označující názvy složek

        # TODO: ukázat strom s bakteriemi

        # TODO: animace vyznačí v bakteria stromě nejdelší cestu

        # TODO: animace vyznačí jinou nejdelší cestu, jakože to není unique