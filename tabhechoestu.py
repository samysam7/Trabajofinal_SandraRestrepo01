import os
import shutil
import pandas as pd

# Carpetas
carpeta_pendientes = "pendientes"
carpeta_leidos = "leidos"
carpeta_dimensiones = "dimensiones_maestras"
carpeta_errores ="errores"


# Dimensiones que se van a gestionar
dimensiones_nombres = [
    "NACIONALIDAD", "ESTADO DE ORÍGEN", "NIVEL ANTERIOR", "NIVEL ACADÉMICO", "NIVEL ACTUAL", "CATEGORÍA",
    "UNIDAD ACADÉMICA", "SEDE", "SEDE EDO", "PROGRAMA EDUCATIVO", "NUEVO INGRESO", "LENGUA",
    "AFRODESCENDIENTE", "DISCAPACIDAD", "TIPO DISCAPACIDAD"
]

def crear_carpetas_si_no_existen():
    os.makedirs(carpeta_pendientes, exist_ok=True)
    os.makedirs(carpeta_leidos, exist_ok=True)
    os.makedirs(carpeta_dimensiones, exist_ok=True)
    os.makedirs(carpeta_errores, exist_ok=True)

def obtener_archivos_pendientes():
    archivos = os.listdir(carpeta_pendientes)
    return [f for f in archivos if f.lower().endswith(('.xlsx', '.xls', '.csv'))]

# Cargar o inicializar las tablas maestras
def cargar_tablas_maestras():
    tablas_maestras = {}
    for dim in dimensiones_nombres:
        path = os.path.join(carpeta_dimensiones, f"{dim}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path, dtype=str)
            tablas_maestras[dim] = df
        else:
            tablas_maestras[dim] = pd.DataFrame(columns=[f"ID_{dim}", dim])
    return tablas_maestras

# Guardar tablas maestras actualizadas
def guardar_tablas_maestras(tablas_maestras):
    for dim, df in tablas_maestras.items():
        path = os.path.join(carpeta_dimensiones, f"{dim}.csv")
        df.to_csv(path, index=False)

def procesar_archivo(nombre_archivo):
    ruta_archivo = os.path.join(carpeta_pendientes, nombre_archivo)
    try:
        if nombre_archivo.lower().endswith('.csv'):
            df_origen = pd.read_csv(ruta_archivo)
        else:
            df_origen = pd.read_excel(ruta_archivo)

        # Reemplazos para valores nulos
        df_origen["DISCAPACIDAD"] = df_origen["DISCAPACIDAD"].fillna("No")
        df_origen["AFRODESCENDIENTE"] = df_origen["AFRODESCENDIENTE"].fillna("No")
        df_origen["TIPO DISCAPACIDAD"] = df_origen["TIPO DISCAPACIDAD"].fillna("No aplica")
        df_origen["LENGUA"] = df_origen["LENGUA"].fillna("Español")

        # Cargar dimensiones maestras
        tablas_maestras = cargar_tablas_maestras()
        dimensiones_ids = {}  # diccionarios de valor -> ID

        for dim in dimensiones_nombres:
            valores_actuales = set(tablas_maestras[dim][dim].dropna().unique())
            nuevos_valores = set(df_origen[dim].dropna().unique()) - valores_actuales
            ultimo_id = tablas_maestras[dim][f"ID_{dim}"].astype(int).max() if not tablas_maestras[dim].empty else 0
            nuevos_registros = []
            for i, val in enumerate(sorted(nuevos_valores), start=1):
                nuevos_registros.append([ultimo_id + i, val])
            if nuevos_registros:
                nuevos_df = pd.DataFrame(nuevos_registros, columns=[f"ID_{dim}", dim])
                tablas_maestras[dim] = pd.concat([tablas_maestras[dim], nuevos_df], ignore_index=True)

            # Crear diccionario para mapear
            dimensiones_ids[dim] = dict(zip(tablas_maestras[dim][dim], tablas_maestras[dim][f"ID_{dim}"]))

        guardar_tablas_maestras(tablas_maestras)

        # Crear tabla de hechos
        registros = []
        for _, row in df_origen.iterrows():
            registros.append([
                row["NÚM."], row["AÑO"], row["GÉNERO"], row["GRADO"], row["GRUPO"],
                row["FECHA DE NACIMIENTO"], pd.to_datetime(row["FECHA DE NACIMIENTO"]).year,
                pd.to_datetime(row["FECHA DE NACIMIENTO"]).month, pd.to_datetime(row["FECHA DE NACIMIENTO"]).day, row["EDAD"]
            ] + sum([[dimensiones_ids[dim].get(row[dim], None), row[dim]] for dim in dimensiones_nombres], []))

        columnas_hechos = [
            "NÚM.", "AÑO", "GÉNERO", "GRADO", "GRUPO", "FECHA DE NACIMIENTO", "Año", "Mes", "Día", "EDAD"
        ] + sum([[f"ID_{dim}", dim] for dim in dimensiones_nombres], [])

        df_hechos = pd.DataFrame(registros, columns=columnas_hechos)

        # Guardar resultado
        nombre_archivo_destino = ruta_archivo
        with pd.ExcelWriter(nombre_archivo_destino, engine="openpyxl") as writer:
            df_hechos.to_excel(writer, sheet_name="Tabla_Hechos", index=False)
            for dim in dimensiones_nombres:
                tablas_maestras[dim].to_excel(writer, sheet_name=f"Dim_{dim}", index=False)

        print(f"Modelo de datos generado en: {nombre_archivo_destino}")
    except Exception as e:
        print(f"Error al procesar {nombre_archivo}: {e}")
        mover_archivo(nombre_archivo, carpeta_errores)  
        return False
    return True

def mover_archivo(nombre_archivo,carpeta):
    origen = os.path.join(carpeta_pendientes, nombre_archivo)
    destino = os.path.join(carpeta, nombre_archivo)
    shutil.move(origen, destino)
    print(f"Archivo movido a 'leidos': {nombre_archivo}")

def procesar_archivos():
    crear_carpetas_si_no_existen()
    while True:
        archivos = obtener_archivos_pendientes()
        if not archivos:
            print("No hay más archivos por procesar.")
            break
        for archivo in archivos:
            if procesar_archivo(archivo):
                mover_archivo(archivo,carpeta_leidos)

if __name__ == "__main__":
    procesar_archivos()
