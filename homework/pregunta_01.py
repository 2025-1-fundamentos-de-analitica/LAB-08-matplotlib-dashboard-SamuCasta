# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

# Importación de librerías necesarias
import matplotlib.pyplot as plt  # Para crear gráficos y visualizaciones
import pandas as pd              # Para manipulación y análisis de datos
import os                        # Para operaciones del sistema operativo (crear carpetas)

def cargar_datos():
    """
    Función para cargar los datos del archivo CSV de envíos.
    
    Returns:
        DataFrame: Datos de envíos cargados desde el archivo CSV
    """
    # Leer el archivo CSV con los datos de envíos
    datos = pd.read_csv('files/input/shipping-data.csv')
    return datos

def crear_visual_envios_por_almacen(datos):
    """
    Crea un gráfico de barras mostrando la cantidad de envíos por almacén.
    
    Args:
        datos (DataFrame): Datos de envíos
    """
    # Crear una copia de los datos para evitar modificar el original
    datos = datos.copy()
    
    # Crear una nueva figura de matplotlib
    plt.figure()
    
    # Contar la frecuencia de cada bloque de almacén
    conteos = datos.Warehouse_block.value_counts()
    
    # Crear gráfico de barras con configuraciones específicas
    conteos.plot.bar(
        title='Shipping per Warehouse',  # Título del gráfico
        xlabel='Warehouse Block',        # Etiqueta del eje X
        ylabel='Record Count',           # Etiqueta del eje Y
        color='tab:blue',               # Color de las barras
        fontsize=8,                     # Tamaño de fuente
    )

    # Personalizar el estilo del gráfico
    plt.gca().spines['top'].set_visible(False)    # Ocultar borde superior
    plt.gca().spines['right'].set_visible(False)  # Ocultar borde derecho
    
    # Guardar el gráfico como imagen PNG en la carpeta docs
    plt.savefig('docs/shipping_per_warehouse.png')

def crear_visual_modo_envio(datos):
    """
    Crea un gráfico de pastel (dona) mostrando la distribución de los modos de envío.
    
    Args:
        datos (DataFrame): Datos de envíos
    """
    # Crear una copia de los datos para evitar modificar el original
    datos = datos.copy()
    
    # Crear una nueva figura de matplotlib
    plt.figure()
    
    # Contar la frecuencia de cada modo de envío
    conteos = datos.Mode_of_Shipment.value_counts()
    
    # Crear gráfico de pastel con forma de dona
    conteos.plot.pie(
        title='Mode of Shipment',                               # Título del gráfico
        wedgeprops=dict(width=0.35),                           # Grosor de la dona
        ylabel='',                                              # Sin etiqueta en eje Y
        colors=['tab:blue', 'tab:orange', 'tab:green'],        # Colores personalizados
    )
    
    # Guardar el gráfico como imagen PNG en la carpeta docs
    plt.savefig('docs/mode_of_shipment.png')

def crear_visual_calificacion_promedio_cliente(datos):
    """
    Crea un gráfico de barras horizontales mostrando el rango y promedio 
    de calificaciones de clientes por modo de envío.
    
    Args:
        datos (DataFrame): Datos de envíos
    """
    # Crear una copia de los datos para evitar modificar el original
    datos = datos.copy()
    
    # Crear una nueva figura de matplotlib
    plt.figure()
    
    # Agrupar por modo de envío y calcular estadísticas descriptivas de calificaciones
    datos = (
        datos[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    
    # Simplificar las columnas del DataFrame (quitar nivel superior)
    datos.columns = datos.columns.droplevel()
    
    # Seleccionar solo las columnas necesarias: promedio, mínimo y máximo
    datos = datos[["mean", "min", "max"]]
    
    # Crear barras horizontales grises para mostrar el rango completo (min-max)
    plt.barh(
        y=datos.index.values,           # Modos de envío en el eje Y
        width=datos["max"].values - 1,  # Ancho de barra = máximo - 1
        left=datos["min"].values,       # Inicio de barra = valor mínimo
        height=0.9,                     # Altura de las barras
        color='lightgray',             # Color gris claro
        alpha=0.8,                     # Transparencia
    )
    
    # Definir colores para las barras del promedio basado en la calificación
    # Verde si es >= 3.0, naranja si es menor
    colores = [
        "tab:green" if valor >= 3.0 else "tab:orange" for valor in datos["mean"].values
    ]

    # Crear barras horizontales coloreadas para mostrar el promedio
    plt.barh(
        y=datos.index.values,           # Modos de envío en el eje Y
        width=datos["mean"].values - 1, # Ancho de barra = promedio - 1
        left=datos["min"].values,       # Inicio de barra = valor mínimo
        color=colores,                  # Colores definidos anteriormente
        height=0.5,                     # Altura menor que las barras grises
        alpha=1.0,                      # Sin transparencia
    )

    # Configurar título y estilo del gráfico
    plt.title("Average Customer Rating")
    plt.gca().spines['top'].set_visible(False)      # Ocultar borde superior
    plt.gca().spines['right'].set_visible(False)    # Ocultar borde derecho
    plt.gca().spines['left'].set_color("gray")      # Color gris para borde izquierdo
    plt.gca().spines['bottom'].set_color("gray")    # Color gris para borde inferior
    
    # Guardar el gráfico como imagen PNG en la carpeta docs
    plt.savefig('docs/average_customer_rating.png')

def crear_visual_distribucion_peso(datos):
    """
    Crea un histograma mostrando la distribución de pesos de los envíos.
    
    Args:
        datos (DataFrame): Datos de envíos
    """
    # Crear una copia de los datos para evitar modificar el original
    datos = datos.copy()
    
    # Crear una nueva figura de matplotlib
    plt.figure()
    
    # Crear histograma de la distribución de pesos
    datos.Weight_in_gms.plot.hist(
        title='Weight Distribution',    # Título del gráfico
        color='tab:orange',            # Color naranja para las barras
        edgecolor='white',             # Bordes blancos en las barras
    )
    
    # Personalizar el estilo del gráfico
    plt.gca().spines['top'].set_visible(False)    # Ocultar borde superior
    plt.gca().spines['right'].set_visible(False)  # Ocultar borde derecho
    
    # Guardar el gráfico como imagen PNG en la carpeta docs
    plt.savefig('docs/weight_distribution.png')

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    # PASO 1: Verificar y crear la carpeta de destino
    # Comprobar si la carpeta 'docs' existe, si no existe la crea
    if not os.path.exists("docs"):
        os.makedirs("docs")

    # PASO 2: Cargar los datos del archivo CSV
    # Llamar a la función para cargar los datos de envíos
    datos = cargar_datos()
    
    # PASO 3: Generar todas las visualizaciones
    # Crear gráfico de barras para envíos por almacén
    crear_visual_envios_por_almacen(datos)
    
    # Crear gráfico de pastel para modos de envío
    crear_visual_modo_envio(datos)
    
    # Crear gráfico de barras horizontales para calificaciones promedio
    crear_visual_calificacion_promedio_cliente(datos)
    
    # Crear histograma para distribución de pesos
    crear_visual_distribucion_peso(datos)

    # PASO 4: Generar el dashboard HTML
    # Crear y escribir el archivo HTML que contiene el dashboard
    with open("docs/index.html", "w") as archivo:
        # Escribir el contenido HTML con estructura de dashboard
        archivo.write("""
        <!DOCTYPE html>
        <html>
            <body>
                <h1>Shipping Dashboard Example</h1>
                <!-- Columna izquierda con dos gráficos -->
                <div style="width:45%; float:left">
                    <img src="shipping_per_warehouse.png" alt="Fig 1">
                    <img src="mode_of_shipment.png" alt="Fig 2">
                </div>
                <!-- Columna derecha con dos gráficos -->
                <div style="width:45%; float:right">
                    <img src="average_customer_rating.png" alt="Fig 3">
                    <img src="weight_distribution.png" alt="Fig 4">
                </div>
            </body>
        </html>
        """)

# EJECUCIÓN PRINCIPAL: Ejecutar la función solo cuando el script se ejecuta directamente
if __name__ == "__main__":
    pregunta_01()
