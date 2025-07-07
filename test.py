from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os

# Ruta del archivo NGI
#archivo = "C:/Users/facui/Desktop/Proyectos/tallerIntegrador1/Taller-integrador-1/Datos/227/ionogram/TMJ20_2015227000805.ngi"

carpeta = "C:/Users/facui/Desktop/Proyectos/tallerIntegrador1/Taller-Integrador-1/Datos/archivosPrueba"
archivos = [f for f in os.listdir(carpeta) if f.endswith(".ngi")]
# Carpeta temporal para guardar los frames
carpeta_frames = "frames_temp"
os.makedirs(carpeta_frames, exist_ok=True)
frames_paths = []






# Abrir el archivo
#dataset = Dataset(archivo, "r")

# Constantes físicas
eps0 = 8.854 ** (-12)  # permitividad del vacío (F/m)
m = 9.109 ** (-31)  # masa del electrón (kg)
e = 1.602 ** (-19)  # carga del electrón (C)

plt.figure(figsize=(8, 10))

for archivo in archivos:
    ruta = os.path.join(carpeta, archivo)
    with Dataset(ruta, mode="r") as dataset:
        rangos_raw = dataset.variables["Range"][:]  # Altitudes (km o m)
        frecuencias_raw = dataset.variables["Frequency"][:]  # Frecuencias (MHz)
        potencia_om = dataset.variables["O-mode_power"][:]  # Potencia O-mode (dB)
        min_length = min(len(rangos_raw), len(frecuencias_raw))
        rangos_trunc = rangos_raw[:min_length]
        frecuencias_trunc = frecuencias_raw[:min_length]
        # Filtro de datos vacios
        valid_mask = ~np.isnan(rangos_trunc) & ~np.isnan(frecuencias_trunc)
        rangos = rangos_trunc[valid_mask]
        frecuencias = frecuencias_trunc[valid_mask]
        # Calcular la densidad de electrones con la fórmula
        Ne = (((2 * np.pi * frecuencias) ** 2) * eps0 * m) / e**2
        # Grafica x=Ne , y=rango
        plt.figure(figsize=(6, 8))
        plt.plot(Ne, rangos)
        plt.xlabel("Densidad Electrónica Ne (electrones/m³)")
        plt.ylabel("Altitud (km)")
        plt.title("Perfil de Densidad Electrónica (datos filtrados)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        
        # Control de longitud
        # print("Cantidad de rangos limpios", len(rangos))
        # print("Cantidad de frecuencias limpias:", len(frecuencias))
        # print("Cantidad de Ne:", len(Ne))
        # Controles pares frecuencia,rango
        # for i in range(min(10, len(frecuencias))):  # Print first 10 pairs
        #    print(f"Frecuencia: {frecuencias[i]} MHz, Rango: {rangos[i]} km")
        # Graficar potencia O-mode como imagen
        plt.figure(figsize=(10, 6))
        plt.imshow(
            potencia_om,
            extent=[rangos.min(), rangos.max(), frecuencias.min(), frecuencias.max()],
            aspect="auto",
            origin="lower",
            cmap="viridis",
        )

        plt.colorbar(label="Potencia O-mode")
        plt.xlabel("Altura (km)")
        plt.ylabel("Frecuencia (Hz)")
        plt.title(f"Archivo: {os.path.basename(archivo)}")
        plt.tight_layout()
        plt.show()


    # Obtener variables
    #rangos_raw = dataset.variables["Range"][:]  # Altitudes (km o m)
    #frecuencias_raw = dataset.variables["Frequency"][:]  # Frecuencias (MHz)
    #potencia_om = dataset.variables["O-mode_power"][:]  # Potencia O-mode (dB)

    # CONTROL POR DIFERENCIA DE CANTIDAD
    # for i in range(0, 104):
    #    print("Primeros 104 rangos:", rangos_raw[i])
    #    print("Primeras 104 frecuencias", frecuencias_raw[i])
    # for i in range(408, 512):
    # print("Ultimos 104 rangos:", rangos_raw[i])
    # print("Ultimas 104 frecuencias", frecuencias_raw[i])

    # for i in range(390, 407):
    #    print("Ultimas frecuencias posibles", frecuencias_raw[i])

    # Imprimir longitud inicial
    # print("Longitud de rangos:", len(rangos_raw))
    # print("Longitud de frecuencias:", len(frecuencias_raw))

    # Achicar ambos arreglos al mas pequeño de ambos
