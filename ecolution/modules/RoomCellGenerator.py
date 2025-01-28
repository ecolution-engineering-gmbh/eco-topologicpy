from topologicpy.Vertex import Vertex
from topologicpy.Face import Face
from topologicpy.Cell import Cell


def create_room_cells(polygons, room_height=2.7):
    """
    Creates 3D room cells (Cells) from a list of 2D polygons.

    Each polygon is a list of (x, y) tuples lying in the XY-plane (z=0),
    which will be extruded upward using Cell.ByThickenedFace.

    Parameters
    ----------
    polygons : list of list of tuple
        A list of polygons, each polygon is a list of (x, y) coordinate pairs.
    room_height : float, optional
        The extrusion height for each polygon. Default is 2.7 meters.

    Returns
    -------
    list of topologic_core.Cell
        A list of extruded cells, one per polygon.

    Example
    -------
    from RoomCellGenerator import create_room_cells
    polygons = [
    ...     [(0,0), (4,0), (4,3), (0,3)],
    ...     [(7,0), (9,0), (9,2), (7,2)]
    ... ]
    my_cells = create_room_cells(polygons, room_height=3.0)
    """
    room_cells = []

    # Convert each polygon to a Face, then extrude to a Cell
    for idx, polygon in enumerate(polygons):
        vertex_list = [Vertex.ByCoordinates(x, y, 0) for (x, y) in polygon]
        face = Face.ByVertices(vertex_list)
        cell = Cell.ByThickenedFace(
            face=face,
            thickness=room_height,
            bothSides=False,  # only extrude in +normal direction
            reverse=False,  # if face normal is inverted, set this to True
            planarize=False
        )
        room_cells.append(cell)

    return room_cells
