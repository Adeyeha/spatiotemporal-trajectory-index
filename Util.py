import pandas as pd
import geopandas
from shapely import wkt

def read_toy_dataset(path, column_names):
    traj_df = pd.read_csv(filepath_or_buffer=path, compression='gzip', header=None, sep='\t', names=column_names)
    traj_df['ts'] = pd.to_datetime(traj_df['ts'], unit='ms')
    traj_df['geom'] = traj_df['geom'].apply(wkt.loads)
    traj_df = geopandas.GeoDataFrame(traj_df, geometry='geom')
    return traj_df

path = './toy_traj.csv.gz'
columns = ['id', 'ts', 'geom']
tdf = read_toy_dataset(path, columns)
print(tdf.info())
