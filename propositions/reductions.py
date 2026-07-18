# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2025
# File name: propositions/reductions.py

"""Reduction between computational search problems."""

from __future__ import annotations
from typing import AbstractSet, Mapping, Tuple, Union
from itertools import product

from propositions.syntax import *
from propositions.semantics import *

#: A graph on a vertex set of the form ``(1,``...\ ``,``\ `n_vertices`\ ``)``,
#: represented by the number of vertices `n_vertices` and a set of edges over
#: the vertices.
Graph = Tuple[int, AbstractSet[Tuple[int, int]]] 

def is_graph(graph: Graph) -> bool:
    """Checks if the given data structure is a valid representation of a graph.

    Parameters:
        graph: data structure to check.

    Returns:
        ``True`` if the given data structure is a valid representation of a
        graph, ``False`` otherwise.
    """
    (n_vertices, edges) = graph
    for edge in edges:
        for vertex in edge:
            if not 1 <= vertex <= n_vertices:
                return False
        if edge[0] == edge[1]:
            return False
    return True

def is_valid_3coloring(graph: Graph, coloring: Mapping[int, int]) -> bool:
    """Checks whether the given coloring is a valid coloring of the given graph
    by the colors 1, 2, and 3.

    Parameters:
        graph: graph to check.
        coloring: mapping from the vertices of the given graph to colors,
            to check.

    Returns:
        ``True`` if the given coloring is a valid coloring of the given graph by
        the colors 1, 2, and 3; ``False`` otherwise.
    """
    assert is_graph(graph)
    (n_vertices, edges) = graph
    for vertex in range(1, n_vertices + 1):
        if vertex not in coloring.keys() or coloring[vertex] not in {1, 2, 3}:
            return False
    for edge in edges:
        if coloring[edge[0]] == coloring[edge[1]]:
            return False
    return True

def graph3coloring_to_formula(graph: Graph) -> Formula:
    """Efficiently reduces the 3-coloring problem of the given graph into a
    satisfiability problem.

    Parameters:
        graph: graph whose 3-coloring problem to reduce.
       
    Returns:
        A propositional formula that is satisfiable if and only if the given
        graph is 3-colorable.
    """
    assert is_graph(graph)
    # Optional Task 2.10a

    # Each coloring corresponds to a model (encoding)
    # Only some colorings are valid
    # So only some models are valid
    # Let's represent valid as "True"
    # So each coloring's model gets a truth value
    # Just previously, we converted a model into a formula
    # using _synthesize_for_model()
    # that gave us a formula that evaluates that model to True
    # Represent graph coloring validity as the existence of a formula
    # that evaluates to true under the model that represents that coloring

    def coloringFromModel(model:Model) -> Mapping[int,int]:
        vars = list(variables(model))
        vars.sort()
        n_vertices = len(vars) // 3
        invalidColoring = dict([(vtx,1) for vtx in range(n_vertices)])
        mapping = {}
        for v in range(n_vertices):
            v1 = vars[v*3]
            v2 = vars[v*3 + 1]
            v3 = vars[v*3 + 2]
            if sum([model[v1],model[v2],model[v3]]) != 1:
                # Each vertex needs exactly 1 color
                return invalidColoring
            if   model[v1]: mapping[v+1] = 1 # vertices are numbered from 1
            elif model[v2]: mapping[v+1] = 2
            elif model[v3]: mapping[v+1] = 3
            else: return invalidColoring
        return mapping

    n_vertices,edges = graph

    # From the book:
    # "A coloring of the graph can be encoded by having, for every vertex v
    # and possible color c, a Boolean variable x_{vc} that represents that
    # vertex v is colored by color c,"
    vars = []
    for v in range(n_vertices):
        vars.extend([
            f'v{v+1:04d}1',
            f'v{v+1:04d}2',
            f'v{v+1:04d}3',
        ])

    all_models(vars)

    valids = (
        is_valid_3coloring(
            graph,
            coloringFromModel(model)
        )
        for model
        in all_models(vars)
    )

    return synthesize(vars,valids)

def assignment_to_3coloring(graph: Graph, assignment: Model) -> \
        Mapping[int, int]:
    """Efficiently transforms an assignment to the formula corresponding to the
    3-coloring problem of the given graph, to a 3-coloring of the given graph so
    that the 3-coloring is valid if and only if the given assignment is
    satisfying.

    Parameters:
        graph: graph to produce a 3-coloring for.
        assignment: assignment to the variable names of the formula returned by
            `graph3coloring_to_formula`\\ ``(``\\ `graph`\\ ``)``.

    Returns:
        A 3-coloring of the given graph by the colors 1, 2, and 3 that is valid
        if and only if the given assignment satisfies the formula
        `graph3coloring_to_formula`\\ ``(``\\ `graph`\\ ``)``.
    """
    assert is_graph(graph)
    formula = graph3coloring_to_formula(graph)
    assert evaluate(formula, assignment)
    # Optional Task 2.10b

    # We basically want to "decode" the model into a graph coloring here...
    # Well, each vertex needs a color...
    n_vertices,edges = graph
    mapping = {}
    for v in range(n_vertices):
        # But first we need to find that color in the model
        if   assignment[f'v{v+1:04d}1']: mapping[v+1] = 1
        elif assignment[f'v{v+1:04d}2']: mapping[v+1] = 2
        elif assignment[f'v{v+1:04d}3']: mapping[v+1] = 3
        else: raise ValueError(f'Vertex must have a color')
    return mapping

def tricolor_graph(graph: Graph) -> Union[Mapping[int, int], None]:
    """Computes a 3-coloring of the given graph.

    Parameters:
        graph: graph to 3-color.

    Returns:
        An arbitrary 3-coloring of the given graph if it is 3-colorable,
        ``None`` otherwise.
    """
    assert is_graph(graph)
    formula = graph3coloring_to_formula(graph)
    for assignment in all_models(list(formula.variables())):
        if evaluate(formula, assignment):
            return assignment_to_3coloring(graph, assignment)
    return None
