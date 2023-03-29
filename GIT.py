from intervaltree import Interval, IntervalTree
from shapely.geometry import box
import numpy as np

import numpy as np
from intervaltree import Interval, IntervalTree
from shapely.geometry import box

class GIT:
    """ Grid Index for Trajectories (GIT)
    A grid index for trajectories that supports the following operations:
    - Insertion of a trajectory
    - Deletion of a trajectory
    - Spatial window query
    - Temporal window query
    - Spatiotemporal window query
    :param sf_xmin: float
    :param sf_xmax: float
    :param sf_ymin: float
    :param sf_ymax: float
    :param delta_x: float
    :param delta_y: float
    """
    def __init__(self, sf_xmin, sf_xmax, sf_ymin, sf_ymax, delta_x, delta_y):
        self.sf_xmin = sf_xmin
        self.sf_xmax = sf_xmax
        self.sf_ymin = sf_ymin
        self.sf_ymax = sf_ymax
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.nx = int(np.ceil((sf_xmax - sf_xmin) / delta_x))
        self.ny = int(np.ceil((sf_ymax - sf_ymin) / delta_y))
        self.grid = [[IntervalTree() for _ in range(self.ny)] for _ in range(self.nx)]

    def _get_intersecting_cells(self, geometry):
        """
        Returns a list of cell coordinates (x, y) that intersect with the given geometry.
        :param geometry: shapely.geometry
        :return: list of tuples (x, y)
        """
        cells = []
        for i in range(self.nx):
            for j in range(self.ny):
                cell_bbox = box(self.sf_xmin + i * self.delta_x, self.sf_ymin + j * self.delta_y,
                                self.sf_xmin + (i + 1) * self.delta_x, self.sf_ymin + (j + 1) * self.delta_y)
                if geometry.intersects(cell_bbox):
                    cells.append((i, j))
        return cells


    def insert(self, trajectory):
        """
        Inserts a trajectory into the grid index.
        :param trajectory: Trajectory
        """
        for i in range(len(trajectory.tgpairs) - 1):
            tgi_start, tgi_end = trajectory.tgpairs[i], trajectory.tgpairs[i + 1]
            ti_start, gi_start = tgi_start
            ti_end, gi_end = tgi_end
            intersecting_cells = self._get_intersecting_cells(gi_start.union(gi_end))

            for cell_coords in intersecting_cells:
                x, y = cell_coords
                self.grid[x][y].add(Interval(ti_start, ti_end, trajectory.traj_id))

    def delete(self, trajectory_id):
        """
        Deletes a trajectory from the grid index.
        :param trajectory_id: int
        """
        for i in range(self.nx):
            for j in range(self.ny):
                intervals_to_remove = [interval for interval in self.grid[i][j] if interval.data == trajectory_id]
                for interval in intervals_to_remove:
                    self.grid[i][j].remove(interval)

    def spatial_window_query(self, x1, y1, x2, y2):
        """
        Returns a set of trajectory ids that intersect with the given spatial window.
        :param x1: float
        :param y1: float
        :param x2: float
        :param y2: float
        :return: set of int
        """
        query_bbox = box(x1, y1, x2, y2)
        result = set()

        for i in range(self.nx):
            for j in range(self.ny):
                cell_bbox = box(self.sf_xmin + i * self.delta_x, self.sf_ymin + j * self.delta_y,
                                self.sf_xmin + (i + 1) * self.delta_x, self.sf_ymin + (j + 1) * self.delta_y)
                if query_bbox.intersects(cell_bbox):
                    for interval in self.grid[i][j]:
                        result.add(interval.data)
        return result

    def temporal_window_query(self, t1, t2):
        """
        Returns a set of trajectory ids that intersect with the given temporal window.
        :param t1: timestamp
        :param t2: timestamp
        :return: set of int
        """
        result = set()
        for i in range(self.nx):
            for j in range(self.ny):
                intervals = self.grid[i][j][t1:t2]
                for interval in intervals:
                    result.add(interval.data)
        return result

    def spatiotemporal_window_query(self, x1, y1, x2, y2, t1, t2):
        """ 
        Returns a set of trajectory ids that intersect with the given spatiotemporal window.
        :param x1: float
        :param y1: float
        :param x2: float
        :param y2: float
        :param t1: timestamp
        :param t2: timestamp
        :return: set of int
        """
        spatial_result = self.spatial_window_query(x1, y1, x2, y2)
        temporal_result = self.temporal_window_query(t1, t2)
        return spatial_result.intersection(temporal_result)
