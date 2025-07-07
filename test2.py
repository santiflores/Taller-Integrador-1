from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
import imageio.v2 as imageio

# Carpeta donde están tus archivos
carpeta = "C:/Users/facui/Desktop/Proyectos/tallerIntegrador1/Taller-Integrador-1/Datos/227/ionogram"
archivos = [f for f in os.listdir(carpeta) if f.endswith(".ngi")]

#Carpeta para imagenes grafica tipo 1
salida_img = "C:/Users/facui/Desktop/Proyectos/tallerIntegrador1/Taller-Integrador-1/Datos/227/imagenesTipo1"
os.makedirs(salida_img, exist_ok=True)

# Crear carpetas temporales para los frames
#os.makedirs("frames_ne", exist_ok=True)
os.makedirs("frames_potencia", exist_ok=True)

#frames_ne = []
frames_potencia = []

# Constantes físicas
eps0 = 8.854e-12  # permitividad del vacío (F/m)
m = 9.109e-31  # masa del electrón (kg)
e = 1.602e-19  # carga del electrón (C)

for i, archivo in enumerate(archivos):
    ruta = os.path.join(carpeta, archivo)
    with Dataset(ruta, mode="r") as dataset:
        rangos_raw = dataset.variables["Range"][:]
        frecuencias_raw = dataset.variables["Frequency"][:]
        potencia_om = dataset.variables["O-mode_power"][:]

        min_length = min(len(rangos_raw), len(frecuencias_raw))
        rangos_trunc = rangos_raw[:min_length]
        frecuencias_trunc = frecuencias_raw[:min_length]

        valid_mask = ~np.isnan(rangos_trunc) & ~np.isnan(frecuencias_trunc)
        rangos = rangos_trunc[valid_mask]
        frecuencias = frecuencias_trunc[valid_mask]

        Ne = (((2 * np.pi * frecuencias) ** 2) * eps0 * m) / e**2

        # --------- GRÁFICA 1: Ne vs Altura ---------
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(Ne, rangos)
        ax1.set_xlabel("Densidad Electrónica Ne (electrones/m³)")
        ax1.set_ylabel("Altitud (km)")
        ax1.set_title(f"Perfil de Densidad Electrónica\nArchivo: {archivo}")
        ax1.grid(True)
        fig1.tight_layout()

        # Guardar imagen
        nombre_salida = os.path.join(salida_img, f"grafica_ne_{i:03}.png")
        fig1.savefig(nombre_salida)
        plt.close(fig1)
        # Guardar frames 1
        #filename_ne = f"frames_ne/frame_ne_{i:03}.png"
        #fig1.savefig(filename_ne)
        #frames_ne.append(filename_ne)
        #plt.close(fig1)

        # --------- GRÁFICA 2: Potencia O-mode ---------
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        im = ax2.imshow(
            potencia_om,
            extent=[rangos.min(), rangos.max(), frecuencias.min(), frecuencias.max()],
            aspect="auto",
            origin="lower",
            cmap="viridis",
        )
        fig2.colorbar(im, ax=ax2, label="Potencia O-mode")
        ax2.set_xlabel("Altura (km)")
        ax2.set_ylabel("Frecuencia (Hz)")
        ax2.set_title(f"Potencia O-mode\nArchivo: {archivo}")
        fig2.tight_layout()

        # Guardar frames 2
        filename_pot = f"frames_potencia/frame_pot_{i:03}.png"
        fig2.savefig(filename_pot)
        frames_potencia.append(filename_pot)
        plt.close(fig2)

# --------- VIDEO 1: Densidad Electrónica ---------
#with imageio.get_writer(
#    "C:/Users/facui/Desktop/video_ne.mp4", fps=2, macro_block_size=None
#) as writer:
#    for path in frames_ne:
#        writer.append_data(imageio.imread(path))

# --------- VIDEO 2: Potencia O-mode ---------
with imageio.get_writer(
    "C:/Users/facui/Desktop/Proyectos/tallerIntegrador1/Taller-Integrador-1/Datos/227/video_potencia.mp4", fps=2, macro_block_size=None
) as writer:
    for path in frames_potencia:
        writer.append_data(imageio.imread(path))

# --------- Limpieza (opcional) ---------
#for path in frames_ne:
#    os.remove(path)
#os.rmdir("frames_ne")

for path in frames_potencia:
    os.remove(path)
os.rmdir("frames_potencia")

print("Se generaron los videos: video_ne.mp4 y video_potencia.mp4")
