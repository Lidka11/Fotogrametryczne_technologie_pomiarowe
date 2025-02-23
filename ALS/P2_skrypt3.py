import arcpy

def get_input(prompt):
    value = input(prompt)
    return value.strip()

path_las1 = get_input("Podaj ścieżkę do pierwszego pliku LAS I: ")
path_las2 = get_input("Podaj ścieżkę do drugiego pliku LAS II: ")


output_nmpt_I = get_input("Podaj ścieżkę do zapisu rastra NMPT dla LAS I: ")
output_nmpt_II = get_input("Podaj ścieżkę do zapisu rastra NMPT dla LAS II: ")
output_difference = get_input("Podaj ścieżkę do zapisu rastra różnicowego: ")


# Utworzenie LAS Dataset
las_dataset1 = arcpy.management.CreateLasDataset(path_las1)
las_dataset2 = arcpy.management.CreateLasDataset(path_las2)

# Definicja klas do filtrowania
allowed_classes_1 = [2, 3, 4, 5, 6]            
allowed_class_2 = [2]   
arcpy.management.MakeLasDatasetLayer(
    in_las_dataset=las_dataset1,
    out_layer="nmpt_I",
    class_code=allowed_classes_1
)
arcpy.LasDatasetToRaster_conversion(
    in_las_dataset="nmpt_I",
    out_raster=output_nmpt_I,
    value_field="ELEVATION",
    sampling_type="CELLSIZE",
    sampling_value=2.0
)


arcpy.management.MakeLasDatasetLayer(
    in_las_dataset=las_dataset2,
    out_layer="nmpt_II",
    class_code=allowed_classes_1
)
arcpy.LasDatasetToRaster_conversion(
    in_las_dataset="nmpt_II",
    out_raster=output_nmpt_II,
    value_field="ELEVATION",
    sampling_type="CELLSIZE",
    sampling_value=2.0
)

# Tworzenie rastra różnicowego (NMPT I - NMPT II)
raster_roznicowy=arcpy.Raster(output_nmpt_II)-arcpy.Raster(output_nmpt_I)
raster_roznicowy.save(output_difference)

print("Raster różnicowy zapisano w: ", output_difference)

arcpy.management.MakeLasDatasetLayer(
    in_las_dataset=las_dataset1,
    out_layer="nmt_I",
    class_code=allowed_class_2
)
arcpy.LasDatasetToRaster_conversion(
    in_las_dataset="nmt_I",
    out_raster=output_nmpt_I,
    value_field="ELEVATION",
    sampling_type="CELLSIZE",
    sampling_value=2.0
)


arcpy.management.MakeLasDatasetLayer(
    in_las_dataset=las_dataset2,
    out_layer="nmpt_I",
    class_code=allowed_class_2
)
arcpy.LasDatasetToRaster_conversion(
    in_las_dataset="nmt_II",
    out_raster=output_nmpt_II,
    value_field="ELEVATION",
    sampling_type="CELLSIZE",
    sampling_value=2.0
)
print("Stworzono NMT")