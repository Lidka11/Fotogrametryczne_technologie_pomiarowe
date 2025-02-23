import laspy
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt


def get_input(prompt):
    value = input(prompt)
    return value.strip()

point_cloud_path = get_input("Podaj ścieżkę do pierwszego pliku LAZ: ")
las_data=laspy.read(point_cloud_path)
ground=las_data[las_data["classification"]==2]
points_ground=np.float64([ground.x, ground.y, ground.z]).T
point_ground= points_ground-points_ground.mean(axis=0)
ground_cloud = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points_ground))


ground_color = np.tile([0.2, 0.8, 0.2], (points_ground.shape[0], 1)) 
ground_cloud.colors = o3d.utility.Vector3dVector(ground_color)


buildings=las_data[las_data["classification"]==6]
points=np.float64([buildings.x, buildings.y, buildings.z]).T
point= points-points.mean(axis=0)
points=o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))

clusters=points.cluster_dbscan(eps=2.0, min_points=100, print_progress=True)
labels=np.array(clusters)

max_label=labels.max()
colors=plt.get_cmap("tab20")(labels/max_label)
colors[labels<0]=0
points.colors=o3d.utility.Vector3dVector(colors[:, :3])
o3d.visualization.draw_geometries([points, ground_cloud])
