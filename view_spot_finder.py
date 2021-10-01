class ViewSpotFinder:
    def __init__(self, data, n_maxima):
        self.data = data
        self.n_maxima = n_maxima
        self.heights = self.__make_heights()
        self.nodes_elements_mapping = self.__make_nodes_elements_mapping()

    def get_local_maxima(self):
        maxima = []
        # sort elements by height descending
        elements = sorted(self.data["elements"], reverse=True, key=lambda e: self.heights[e["id"]])

        for e in elements:
            if len(maxima) >= self.n_maxima:
                break

            if len(maxima) > 0 and self.__is_neighbour_with_same_height(e, maxima[-1]):
                # A neighbour of this element with the same height has already been added to the list
                continue

            neighbours = self.__get_neighbours(e)
            height = self.heights[e["id"]]
            if all([self.heights[element_id] <= height for element_id in neighbours]):
                # all neighbours are lower or have same height. This is a maximum.
                maxima.append(e)

        return self.__format_maxima(maxima)

    def __make_heights(self):
        "Builds a dictionary for fast access that maps element ids to heights."
        return dict((e["element_id"], e["value"]) for e in self.data["values"])

    def __make_nodes_elements_mapping(self):
        "Builds a dictionary that maps node ids to a list of element ids. This way we have fast access to all elements that a node belongs to."
        nodes = {}
        for e in self.data["elements"]:
            for node in e["nodes"]:
                if node in nodes:
                    nodes[node].append(e["id"])
                else:
                    nodes[node] = [e["id"]]

        return nodes

    def __format_maxima(self, maxima):
        return [{ "element_id": e["id"], "value": self.heights[e["id"]] } for e in maxima]

    def __get_neighbours(self, element):
        "Returns all neighbouring element ids for an element."
        neighbours = set()
        for node in element["nodes"]:
            for element_id in self.nodes_elements_mapping[node]:
                # Don't add itself to the neighbours
                if element_id != element["id"]:
                    neighbours.add(element_id)

        return neighbours

    def __is_neighbour_with_same_height(self, element, other_element):
        "Returns true if both elements have the same height and are neighbours"
        if self.heights[element["id"]] != self.heights[other_element["id"]]:
            return False

        # They are neighbours if they have at least one node in common
        return len(set(element["nodes"]) & set(other_element["nodes"])) > 0

