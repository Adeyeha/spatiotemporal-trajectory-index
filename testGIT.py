from shapely.geometry import Point
import time
import pandas as pd
import geopandas
from shapely import wkt
import numpy as np
from Trajectory import Trajectory
from GIT import GIT

def read_toy_dataset(path, column_names):
    traj_df = pd.read_csv(filepath_or_buffer=path, compression='gzip', header=None, sep='\t', names=column_names)
    traj_df['ts'] = pd.to_datetime(traj_df['ts'], unit='ms')
    traj_df['geom'] = traj_df['geom'].apply(wkt.loads)
    traj_df = geopandas.GeoDataFrame(traj_df, geometry='geom')
    return traj_df

# function to output two randomly ordered timestamps from ts column in dataframe tdf
def get_random_timestamps(tdf):
    ts = tdf.ts.unique()
    ts1 = np.random.choice(ts)
    ts2 = np.random.choice(ts)
    while ts1 == ts2:
        ts2 = np.random.choice(ts)
    return ts1, ts2


#function to generate two random coordinates (i.e., (x1, y1), (x2, y2)) that will represent a bounding box (envelope) from GIT.grid
def get_random_bbox(git_index):
    x1 = np.random.uniform(git_index.sf_xmin, git_index.sf_xmax)
    x2 = np.random.uniform(git_index.sf_xmin, git_index.sf_xmax)
    y1 = np.random.uniform(git_index.sf_ymin, git_index.sf_ymax)
    y2 = np.random.uniform(git_index.sf_ymin, git_index.sf_ymax)
    return x1, y1, x2, y2
    
def main():
    # Read toy dataset
    path = './toy_traj.csv.gz'
    columns = ['id', 'ts', 'geom']

    print("Reading toy dataset...")
    tdf = read_toy_dataset(path, columns)

    # Create G-IT index instance and insert toy dataset
    print("Creating GIT index...")
    sf_xmin, sf_xmax, sf_ymin, sf_ymax = tdf.bounds.minx.min(), tdf.bounds.maxx.max(), tdf.bounds.miny.min(), tdf.bounds.maxy.max()
    git_index = GIT(sf_xmin=sf_xmin, sf_xmax=sf_xmax, sf_ymin=sf_ymin, sf_ymax=sf_ymax, delta_x=10, delta_y=10)

    # Insert toy dataset
    print("Inserting toy dataset...")
    tdf['g_pair'] = list(zip(tdf.ts, tdf.geom))
    cc = 0
    tdf_minimized = tdf[1:1000]
    for x in tdf_minimized.id.unique():
        tic = time.time()
        traj = Trajectory(x, tdf_minimized[tdf_minimized.id == x].sort_values(ascending=True,by='ts').g_pair.to_list())
        git_index.insert(traj)
        cc += tdf_minimized[tdf_minimized.id == x].shape[0]
        tac = time.time()
        print(f"processed - {(cc / tdf_minimized.shape[0]) * 100}% - {tac - tic} seconds - {tdf_minimized[tdf_minimized.id == x].shape[0]} trajectories")

    # Test cases for each query
    # Spatial window query
    x1, y1, x2, y2 = get_random_bbox(git_index)
    print("Spatial window query:")
    print(git_index.spatial_window_query(x1, y1, x2, y2))

    # Temporal window query
    ts1,ts2 = get_random_timestamps(tdf_minimized)
    print("Temporal window query:")
    print(git_index.temporal_window_query(ts1,ts2))

    # Spatiotemporal window query
    # ts1,ts2 = get_random_timestamps(tdf_minimized)
    # x1, y1, x2, y2 = get_random_bbox(git_index)
    print("Spatiotemporal window query:")
    print(git_index.spatiotemporal_window_query(x1, y1, x2, y2, ts1,ts2))

if __name__ == "__main__":
    main()