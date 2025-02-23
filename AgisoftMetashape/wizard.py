import Metashape
import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QCheckBox, QFileDialog, QMessageBox

def show_path_selector_dialog():
    app = QApplication.instance() or QApplication([])
    parent = app.activeWindow()

    dialog = QDialog(parent)
    dialog.setWindowTitle("Program")
    dialog.resize(400, 500)

    layout = QVBoxLayout(dialog)

    path_input = QLineEdit()
    layout.addWidget(path_input)

    browse_button = QPushButton("Wybierz folder ze zdjęciami")
    layout.addWidget(browse_button)

    osnowa_input = QLineEdit()
    layout.addWidget(osnowa_input)

    osnowa_browse_button = QPushButton("Wybierz plik osnowy")
    layout.addWidget(osnowa_browse_button)

    downscale_label = QLabel("Wybierz dokładność:")
    layout.addWidget(downscale_label)

    downscale_combobox = QComboBox()
    # downscale_combobox.addItem("16 (Lowest)", 16)
    downscale_combobox.addItem("8 (Low)", 8)
    downscale_combobox.addItem("4 (Medium)", 4)
    downscale_combobox.addItem("2 (High)", 2)
    downscale_combobox.addItem("1 (Ultra)", 1)
    downscale_combobox.setCurrentIndex(1)
    layout.addWidget(downscale_combobox)

    points_cloud_checkbox = QCheckBox("Generować chmurę punktów?")
    points_cloud_checkbox.setChecked(True)
    layout.addWidget(points_cloud_checkbox)

    model_checkbox = QCheckBox("Generować model 3D?")
    model_checkbox.setChecked(True)
    layout.addWidget(model_checkbox)

    crs_label = QLabel("Wybierz docelowy CRS:")
    layout.addWidget(crs_label)

    crs_combobox = QComboBox()
    crs_combobox.addItem("EPSG:2178 (Polska 1992)", "EPSG::2178")
    crs_combobox.addItem("EPSG:4326 (WGS 84)", "EPSG::4326")
    crs_combobox.addItem("EPSG:3857 (Pseudo-Mercator)", "EPSG::3857")
    crs_combobox.setCurrentIndex(0)
    layout.addWidget(crs_combobox)

    ok_button = QPushButton("OK")
    layout.addWidget(ok_button)

    def browse_folder():
        folder = QFileDialog.getExistingDirectory(dialog, "Wybierz folder")
        if folder:
            path_input.setText(folder)

    def browse_osnowa():
        file, _ = QFileDialog.getOpenFileName(dialog, "Wybierz plik osnowy", "", "Text Files (*.txt);;All Files (*)")
        if file:
            osnowa_input.setText(file)

    def accept_dialog():
        photo_path = path_input.text()
        osnowa_path = osnowa_input.text()
        downscale_value = downscale_combobox.currentData()
        generate_points_cloud = points_cloud_checkbox.isChecked()
        generate_model = model_checkbox.isChecked()
        selected_crs = crs_combobox.currentData()

        if photo_path and os.path.exists(osnowa_path):
            process_images(photo_path, osnowa_path, downscale_value, generate_points_cloud, generate_model, selected_crs)
        else:
            QMessageBox.warning(dialog, "Błąd", "Wybierz poprawną ścieżkę.")
        dialog.accept()

    browse_button.clicked.connect(browse_folder)
    osnowa_browse_button.clicked.connect(browse_osnowa)
    ok_button.clicked.connect(accept_dialog)

    dialog.exec()

def process_images(photo_folder, osnowa_path, downscale_value, generate_points_cloud, generate_model, selected_crs):
    document = Metashape.app.document
    chunk=document.chunk
    if chunk:
        document.remove(chunk)
        chunk=None
    chunk = document.addChunk()
    chunk.crs = Metashape.CoordinateSystem("EPSG::2178")
    chunk.camera_crs = Metashape.CoordinateSystem("EPSG::4326")
    chunk.marker_crs = Metashape.CoordinateSystem(selected_crs)

    def find_files(folder, types):
        return [entry.path for entry in os.scandir(folder) if entry.is_file() and os.path.splitext(entry.name)[1].lower() in types]

    chunk.addPhotos(find_files(photo_folder, [".jpg"]))

    with open(osnowa_path) as file:
        for line in file:
            name, y, x, z = line.split()
            y, x, z = float(y), float(x), float(z)
            marker = chunk.addMarker()
            marker.reference.location = Metashape.Vector([x, y, z])

    chunk.updateTransform()
    chunk.matchPhotos(downscale=downscale_value, generic_preselection=True, reference_preselection=True)
    chunk.alignCameras()
    if generate_points_cloud:
        chunk.buildDepthMaps(downscale=4, filter_mode=Metashape.AggressiveFiltering)
        chunk.buildPointCloud()
    if generate_model:
        chunk.buildModel(
            source_data=Metashape.DepthMapsData,
            surface_type=Metashape.Arbitrary,
            interpolation=Metashape.EnabledInterpolation,
            face_count=Metashape.HighFaceCount
        )

Metashape.app.addMenuItem("Scripts/Program_1", show_path_selector_dialog)
print("W celu uruchomienia programu otwórz Scripts -> Program_1")
