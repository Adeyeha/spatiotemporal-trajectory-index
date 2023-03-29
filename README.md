# Grid-mapped Interval Trees (G-IT) for Spatiotemporal Trajectories
This project implements a spatiotemporal trajectory index called Grid-mapped Interval Trees (G-IT) in Python. It provides a simple trajectory access mechanism primarily designated for historical persistent spatiotemporal data. The project contains three main files: GIT.py, which implements the G-IT index, and Trajectory.py, which implements the trajectory data type and testGIT.py, which implements test cases.

## Getting Started
### Prerequisites
The following Python libraries are required to run this project:

- Shapely
- Intervaltree

You can install them using pip:

``` python
pip install shapely
pip install intervaltree
```

### Files
1. GIT.py: Implementation of the G-IT index.
2. Trajectory.py: Implementation of the trajectory data type.
3. TestGIT.py: A script that inserts a toy dataset into a G-IT index instance and tests different query types.

### Running the Code
To run the TestGIT.py script, simply execute the following command:

``` python
python TestGIT.py
```
This will create a G-IT index instance, insert a toy dataset into the index, and perform various queries. The output will show the results of the queries, which include spatial window query, temporal window query, and spatio-temporal window query.

### Usage
To use the G-IT index and trajectory classes in your own project, you can import them as follows:

``` python
from GIT import GIT
from Trajectory import Trajectory
```

Create a G-IT index instance by specifying the parameters for the spatial grid:

``` python
git_index = GIT(sf_xmin=0, sf_xmax=100, sf_ymin=0, sf_ymax=100, delta_x=10, delta_y=10)
```
Create a trajectory instance and insert it into the G-IT index:

```
from shapely.geometry import Point

traj = Trajectory(1, [(1, Point(5, 5)), (2, Point(5, 15)), (3, Point(15, 15)), (4, Point(25, 5))])
git_index.insert(traj)
```
Perform various queries on the G-IT index:

``` python
# Spatial window query
result = git_index.spatial_window_query(x1, y1, x2, y2)

# Temporal window query 
result = git_index.temporal_window_query(t1, t2)

# Spatio-temporal window query 
result = git_index.spatio_temporal_window_query(x1, y1, x2, y2, t1, t2)
```