class Trajectory:
  """
  A trajectory is a list of time-geopoint pairs.
  """
  def __init__(self, traj_id, tgpairs):
    self.traj_id = traj_id
    self.tgpairs = tgpairs

  def __str__(self):
    #return f"{self.traj_id}" # replace as needed
    return f"Trajectory {self.traj_id}: {len(self.tgpairs)} points"