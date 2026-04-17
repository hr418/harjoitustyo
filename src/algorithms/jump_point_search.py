import heapq
from algorithms.a_star import AStar, AStarNode


class JumpPointSearchNode(AStarNode):
    """
    Node class for Jump Point Search algorithm.

    Attributes:
        position (tuple): The (x, y) position of the node.
        g_cost (int): The cost from the start node to this node.
        h_cost (int): The heuristic cost from this node to the goal node.
        f_cost (int): The total cost (g_cost + h_cost).
        parent (JumpPointSearchNode): The parent node in the path.
    """


class JumpPointSearch(AStar):
    """
    Jump Point Search pathfinding algorithm implementation.

    Attributes:
        open_set (list): A priority queue of nodes to be evaluated.
        current_node (JumpPointSearchNode): The current node being evaluated.
        closed_set (set): A set of positions that have been evaluated.
        g_scores (dict): A dictionary mapping positions to their current best g_costs.
    """

    def _direction(self, start, end):
        return (
            (end[0] > start[0]) - (end[0] < start[0]),
            (end[1] > start[1]) - (end[1] < start[1]),
        )

    def _distance(self, start, end):
        return max(abs(end[0] - start[0]), abs(end[1] - start[1]))

    def _is_walkable(self, position):
        return self.pixel_map.is_walkable(position)

    def _forced_directions(self, position, direction):
        x, y = position
        dx, dy = direction

        forced = []

        if dx != 0 and dy != 0:
            if not self._is_walkable((x - dx, y + dy)) and self._is_walkable(
                (x - dx, y)
            ):
                forced.append((-dx, dy))
            if not self._is_walkable((x + dx, y - dy)) and self._is_walkable(
                (x, y - dy)
            ):
                forced.append((dx, -dy))
            return forced

        if dx != 0:
            if not self._is_walkable((x, y + 1)) and self._is_walkable((x + dx, y + 1)):
                forced.append((dx, 1))
            if not self._is_walkable((x, y - 1)) and self._is_walkable((x + dx, y - 1)):
                forced.append((dx, -1))
            return forced

        if dy != 0:
            if not self._is_walkable((x + 1, y)) and self._is_walkable((x + 1, y + dy)):
                forced.append((1, dy))
            if not self._is_walkable((x - 1, y)) and self._is_walkable((x - 1, y + dy)):
                forced.append((-1, dy))

        return forced

    def _pruned_directions(self, node):
        if not node.parent:
            return [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]

        direction = self._direction(node.parent.position, node.position)
        dx, dy = direction
        directions = [direction]

        if dx != 0 and dy != 0:
            directions.extend([(dx, 0), (0, dy)])
        elif dx != 0:
            directions.append((dx, 0))
        else:
            directions.append((0, dy))

        directions.extend(self._forced_directions(node.position, direction))

        unique_directions = []
        for candidate in directions:
            if candidate not in unique_directions:
                unique_directions.append(candidate)

        return unique_directions

    def _jump(self, position, direction):
        next_position = (position[0] + direction[0], position[1] + direction[1])

        if not self._is_walkable(next_position):
            return None

        if next_position == self.pixel_map.end:
            return next_position

        if self._forced_directions(next_position, direction):
            return next_position

        dx, dy = direction
        if dx != 0 and dy != 0:
            if self._jump(next_position, (dx, 0)) or self._jump(next_position, (0, dy)):
                return next_position

        return self._jump(next_position, direction)

    def search_step(self):
        while self.open_set:
            positions_added_to_closed = []
            positions_added_to_open = []

            self.current_node = heapq.heappop(self.open_set)

            if self.current_node.position in self.closed_set:
                continue

            self.closed_set.add(self.current_node.position)
            positions_added_to_closed.append(self.current_node.position)

            if self.current_node.position == self.pixel_map.end:
                self.done = True
                raise StopIteration

            for direction in self._pruned_directions(self.current_node):
                jump_position = self._jump(self.current_node.position, direction)

                if jump_position is None or jump_position in self.closed_set:
                    continue

                g_cost = self.current_node.g_cost + self._distance(
                    self.current_node.position, jump_position
                )

                if g_cost >= self.g_scores.get(jump_position, float("inf")):
                    continue

                self.g_scores[jump_position] = g_cost
                jump_node = JumpPointSearchNode(
                    jump_position,
                    g_cost=g_cost,
                    h_cost=self._heuristic(jump_position),
                    parent=self.current_node,
                )
                positions_added_to_open.append(jump_position)
                heapq.heappush(self.open_set, jump_node)

            yield (positions_added_to_open, positions_added_to_closed)
