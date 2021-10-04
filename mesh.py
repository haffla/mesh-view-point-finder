def get_view_spots(data, nr_view_spots):
    view_spots = []
    heights = __make_elements_heights_mapping(data)
    nodes_elements_mapping = __make_nodes_elements_mapping(data)
    elements = __get_sorted_elements(data, heights)

    for e in elements:
        if len(view_spots) >= nr_view_spots:
            break

        if len(view_spots) > 0 and __are_neighbours_with_same_height(e, view_spots[-1], heights):
            # A neighbour of this element with the same height has already been added to the list
            continue

        neighbours = __get_neighbours_for(e, nodes_elements_mapping)
        height = heights[e["id"]]
        if all([heights[element_id] <= height for element_id in neighbours]):
            # all neighbours are lower or have same height. This is a maximum (view spot).
            view_spots.append(e)

    return __format_view_spots(view_spots, heights)

def __get_sorted_elements(data, heights):
    "Sorts elements by heights descending"

    return sorted(data["elements"], reverse=True, key=lambda e: heights[e["id"]])

def __make_elements_heights_mapping(data):
    "Builds a dictionary for fast access that maps element ids to heights."

    return dict((e["element_id"], e["value"]) for e in data["values"])

def __make_nodes_elements_mapping(data):
    """
    Builds a dictionary that maps node ids to a list of element ids.
    This way we have fast access to all elements that a node belongs to.
    """

    nodes = {}
    for e in data["elements"]:
        for node in e["nodes"]:
            if node in nodes:
                nodes[node].append(e["id"])
            else:
                nodes[node] = [e["id"]]

    return nodes

def __format_view_spots(view_spots, heights):
    return [{ "element_id": e["id"], "value": heights[e["id"]] } for e in view_spots]

def __get_neighbours_for(element, nodes_elements_mapping):
    "Returns all neighbouring element ids for an element."

    neighbours = set()
    for node in element["nodes"]:
        for element_id in nodes_elements_mapping[node]:
            # Don't add itself to the neighbours
            if element_id != element["id"]:
                neighbours.add(element_id)

    return neighbours

def __are_neighbours_with_same_height(element, other_element, heights):

    "Returns true if both elements have the same height and are neighbours"
    if heights[element["id"]] != heights[other_element["id"]]:
        return False

    # They are neighbours if they have at least one node in common
    return len(set(element["nodes"]) & set(other_element["nodes"])) > 0

