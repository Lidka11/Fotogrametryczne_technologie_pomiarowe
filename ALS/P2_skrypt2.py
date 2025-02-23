import numpy as np
from scipy.spatial import cKDTree
import laspy
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

point_cloud_path = input("Podaj ścieżkę do pliku chmury punktów (np. C:/sciezka/do/pliku.laz): ")
las_data = laspy.read(point_cloud_path)

class_filter_input = input("Wybierz, czy chcesz analizować punkty (wszystkie/grunt). Domyślnie 'grunt': ").strip().lower()
class_filter = 2 

if class_filter_input == 'wszystkie':
    mask = np.ones(las_data.classification.shape, dtype=bool)
    class_filter = 'wszystkie' 
elif class_filter_input == 'grunt' or class_filter_input == '':
    classification = las_data.classification
    mask = (classification == class_filter)
else:
    print("Nieznany wybór, domyślnie analizuję 'grunt'.")
    classification = las_data.classification
    mask = (classification == class_filter)

filtered_xyz = np.float64([las_data.x[mask], las_data.y[mask], las_data.z[mask]]).T

r = 2.0
block_size = 10000
total_points = filtered_xyz.shape[0]
kdtree = cKDTree(filtered_xyz)

densities_2d = []
densities_3d = []
area_2d = np.pi * r**2
volume_3d = 4 / 3 * np.pi * r**3

for start_idx in range(0, total_points, block_size):
    end_idx = min(start_idx + block_size, total_points)
    block = filtered_xyz[start_idx:end_idx]
    neighbors = kdtree.query_ball_point(block, r)

    for neighbor_list in neighbors:
        num_neighbors = len(neighbor_list) - 1  
        density_2d = num_neighbors / area_2d
        density_3d = num_neighbors / volume_3d
        densities_2d.append(density_2d)
        densities_3d.append(density_3d)

    print(f"Przetworzono punkty od {start_idx} do {end_idx} z {total_points}.")

densities_2d = np.array(densities_2d)
densities_3d = np.array(densities_3d)

def plot_density(density_data, dimension, color, label):
    plt.figure(figsize=(8, 6))
    plt.hist(density_data, bins=256, color=color, alpha=0.7, edgecolor='black')
    if class_filter == 'wszystkie':
        plt.title(f'Histogram gęstości ({dimension}) dla wszystkich klas')
    else:
        plt.title(f'Histogram gęstości ({dimension}) dla gruntu')
    if dimension == '2D':
        plt.xlabel(f'Gęstość [punkty/jednostka^2]')
    else:
        plt.xlabel(f'Gęstość [punkty/jednostka^3]')
    plt.ylabel('Liczba punktów')
    formatter = FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' '))
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_choice = input("Wybierz wykres (2D lub 3D). Domyślnie 2D: ").strip().lower()

if plot_choice == '3d':
    plot_density(densities_3d, '3D', 'green', 'punkty/jednostka^3')
else:
    plot_density(densities_2d, '2D', 'blue', 'punkty/jednostka^2')

# Zapytanie, czy wygenerować drugi wykres
second_choice = input("Czy chcesz wyświetlić drugi wykres? (tak/nie): ").strip().lower()
if second_choice == 'tak':
    if plot_choice == '3d':
        plot_density(densities_2d, '2D', 'blue', 'punkty/jednostka^2')
    else:
        plot_density(densities_3d, '3D', 'green', 'punkty/jednostka^3')