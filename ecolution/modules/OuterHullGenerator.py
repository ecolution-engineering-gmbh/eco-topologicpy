from topologicpy.Cluster import Cluster
from topologicpy.Vertex import Vertex
from topologicpy.Wire import Wire
from topologicpy.Face import Face
from topologicpy.Cell import Cell
from topologicpy.Topology import Topology


def create_outer_hull(polygons, thickness=2.7, hull_type="concave", k=3):
    """
    Creates an outer 3D shell (Cell) around the given polygons by computing
    either a concave or a convex hull of all polygon vertices, then extruding
    that hull face.

    Parameters
    ----------
    polygons : list of list of tuple
        A list of polygons, each polygon is a list of (x, y) coordinate pairs.
        All are assumed to be in the XY-plane (z=0).
    thickness : float, optional
        The extrusion thickness/height for the hull. Default is 2.7 meters.
    hull_type : str, optional
        The type of hull to compute, either "concave" or "convex". Default is "concave".
    k : int, optional
        Concavity parameter if hull_type="concave". Controls how deeply the hull
        indents around interior vertices by nearest neighbors to consider for each point when building the hull.
        Default is 3.

    Returns
    -------
    topologic_core.Cell
        The extruded hull cell that encloses all the polygon vertices.

    Example
    -------
    from OuterHullGenerator import create_outer_hull
    polygons = [
    ...     [(0,0), (4,0), (4,3), (0,3)],
    ...     [(7,0), (9,0), (9,2), (7,2)]
    ... ]
    hull_cell = create_outer_hull(polygons, thickness=3.0, hull_type="concave", k=3)
    """
    vertex_list = []
    for polygon in polygons:
        for (x, y) in polygon:
            vertex_list.append(Vertex.ByCoordinates(x, y, 0))

    cluster_of_vertices = Cluster.ByTopologies(vertex_list)

    if hull_type.lower() == "concave":
        outer_wire = Wire.ConcaveHull(cluster_of_vertices, k=k)
    else:
        outer_wire = Wire.ConvexHull(cluster_of_vertices)

    outer_face = Face.ByWire(outer_wire)
    outer_shell = Cell.ByThickenedFace(
        face=outer_face,
        thickness=thickness,
        bothSides=False,
        reverse=False,
        planarize=False
    )

    return outer_shell, cluster_of_vertices
