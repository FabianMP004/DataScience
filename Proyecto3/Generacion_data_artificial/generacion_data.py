import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuración inicial
num_clientes = 100000  # Total de clientes únicos
num_meses = 12  # Número de meses de observación
features = ['ingresos_mensuales', 'deuda_total', 'limite_credito', 'antiguedad_laboral', 'numero_tarjetas']

# Generar IDs de clientes
clientes_ids = np.arange(1, num_clientes + 1)

# Fechas de observación (último día de cada mes)
fechas = [datetime(2022, 1, 31) + timedelta(days=31 * i) for i in range(num_meses)]
fechas = [fecha.strftime('%Y-%m-%d') for fecha in fechas]

# Crear DataFrame vacío
df = pd.DataFrame()

# Generar datos de forma variable por fecha
for fecha in fechas:
    # Número aleatorio de observaciones para esta fecha (entre 1,000 y 10,000)
    num_observaciones = np.random.randint(1000, 10001)

    # Seleccionar clientes aleatorios para esta fecha
    clientes_observados = np.random.choice(clientes_ids, size=num_observaciones, replace=False)

    # Crear DataFrame temporal para esta fecha
    temp_df = pd.DataFrame({
        'id_cliente': clientes_observados,
        'fecha_observacion': fecha
    })

    # Generar features aleatorios para los clientes observados
    for feature in features:
        if feature == 'ingresos_mensuales':
            temp_df[feature] = np.random.normal(3000, 500, num_observaciones)  # Media 3000, desviación 500
        elif feature == 'deuda_total':
            temp_df[feature] = np.random.normal(10000, 2000, num_observaciones)  # Media 10000, desviación 2000
        elif feature == 'limite_credito':
            temp_df[feature] = np.random.normal(15000, 3000, num_observaciones)  # Media 15000, desviación 3000
        elif feature == 'antiguedad_laboral':
            temp_df[feature] = np.random.randint(1, 20, num_observaciones)  # Entre 1 y 20 años
        elif feature == 'numero_tarjetas':
            temp_df[feature] = np.random.randint(1, 6, num_observaciones)  # Entre 1 y 5 tarjetas

    # Concatenar al DataFrame principal
    df = pd.concat([df, temp_df], ignore_index=True)

# Guardar el DataFrame en un archivo CSV
df.to_csv('datos_clientes_variable.csv', index=False)

print(f"Datos generados y guardados en 'datos_clientes.csv'. Tamaño del archivo: {len(df)} registros.")