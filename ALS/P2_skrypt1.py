import laspy
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def get_input(prompt):
    value = input(prompt)
    return value.strip()

point_cloud_path = get_input("Podaj ścieżkę do chmury punktów w formacie LAS/LAZ: ")
point_cloud = laspy.read(point_cloud_path)
x, y, z = point_cloud.x, point_cloud.y, point_cloud.z
points = np.vstack((x, y, z)).T
classification = point_cloud.classification

unique_classes, counts = np.unique(classification, return_counts=True)


plt.figure(figsize=(10, 6))
plt.bar(unique_classes, counts, color='skyblue', edgecolor='black')
plt.title("Liczba punktów w każdej klasie")
plt.xlabel("Klasa")
plt.ylabel("Liczba punktów")
plt.xticks(unique_classes)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

colors = {
    1: [8, 37, 103],      # Nieklasyfikowane 
    2: [8, 114, 143],     # Grunt 
    3: [0, 128, 0],       # Niska roślinność 
    4: [34, 139, 34],     # Średnia roślinność 
    5: [127, 255, 0],     # Wysoka roślinność 
    6: [0, 255, 0],       # Budynki 
    7: [128, 128, 128],   # Szumy 
    8: [0, 255, 255],     # Wodny 
    9: [255, 222, 173],   # Drogi 
}


default_color = [255, 248, 220]

point_colors = np.array([colors.get(cls, default_color) for cls in classification])/ 255.0
# point_colors = point_colors.astype(np.float64)
o3d_cloud = o3d.geometry.PointCloud()
o3d_cloud.points = o3d.utility.Vector3dVector(points)
o3d_cloud.colors = o3d.utility.Vector3dVector(point_colors)

o3d.visualization.draw_geometries([o3d_cloud], window_name="Chmura punktów - Kolorowanie wg klasy",
                                   width=800, height=600, point_show_normal=False)