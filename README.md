# Proyecto Final - Modelo de Datos con Dimensiones Maestras

Este proyecto en Python automatiza la construcción de un modelo de datos tipo estrella, procesando archivos Excel/CSV con información educativa. A partir de los datos, genera:

- Una tabla de hechos con columnas derivadas (como año, mes, día de nacimiento)
- Tablas de dimensiones maestras (e.g., nacionalidad, lengua, discapacidad)
- Archivos de salida en Excel con todos los datos integrados

## 📁 Estructura de carpetas

- `pendientes/` → Aquí se colocan los archivos a procesar.
- `leidos/` → Se mueven los archivos que se procesaron correctamente.
- `errores/` → Se mueven los archivos que causaron errores.
- `dimensiones_maestras/` → Aquí se guardan las dimensiones maestras actualizadas en CSV.

## ⚙️ Requisitos

- Python 3.7+
- Paquetes: `pandas`, `openpyxl`

Instalación de dependencias (opcional si usas un entorno virtual):

```bash
pip install pandas openpyxl

## 📌 Dimensiones gestionadas
NACIONALIDAD
ESTADO DE ORÍGEN
NIVEL ANTERIOR
NIVEL ACADÉMICO
NIVEL ACTUAL
CATEGORÍA
UNIDAD ACADÉMICA
SEDE
SEDE EDO
PROGRAMA EDUCATIVO
NUEVO INGRESO
LENGUA
AFRODESCENDIENTE
DISCAPACIDAD
TIPO DISCAPACIDAD

## ❓¿Qué preguntas permite responder?
¿Cuántos estudiantes hay por nacionalidad, sede, programa, etc.?
¿Cuántos estudiantes tienen discapacidad o pertenecen a una comunidad afrodescendiente?
¿Cuál es la distribución por edad, género o lengua?
¿Cómo evolucionan las categorías o niveles académicos en el tiempo?
