import pandas as pd
import numbers

def cleaning_columns_names(df):
    """
    Limpia y estandariza los nombres de las columnas de un DataFrame.

    Operaciones realizadas:
    ------------------------
    1. Convierte todos los nombres de las columnas a minúsculas.
    2. Reemplaza los espacios en los nombres de columnas por guiones bajos ('_').
    3. Renombra específicamente la columna 'st' para que pase a llamarse 'state'.
    4. Actualiza el DataFrame con los nuevos nombres de columnas.

    Parámetros:
    ------------
    df : pandas.DataFrame
        El DataFrame cuyos nombres de columnas serán limpiados y estandarizados.

    Retorna:
    --------
    pandas.DataFrame
        El mismo DataFrame de entrada pero con los nombres de las columnas modificados.

    """
    # Ponemos los nombres de columnas en minúsculas y reemplazamos espacios por guiones
    new_columns = [column.lower().replace(' ','_') for column in df.columns]

    df.columns = new_columns

    # Renombrarmos la columna 'st' como 'state'
    df.rename(columns={'st':'state'},inplace=True)

    return df

def cleaning_invalid_values(df):
    """
    Limpia y normaliza valores inconsistentes en varias columnas de un DataFrame.

    Operaciones realizadas:
    ------------------------
    1. Convierte todos los valores de la columna 'gender' a minúsculas.
    2. Normaliza los valores de 'gender' para que sólo existan 'M' (masculino) y 'F' (femenino).
    3. Reemplaza abreviaturas de estados ('AZ', 'Cali', 'WA') por sus nombres completos ('Arizona', 'California', 'Washington').
    4. Corrige el valor 'Bachelors' en la columna 'education' para uniformizarlo como 'Bachelor'.
    5. Elimina el símbolo '%' en los valores de la columna 'customer_lifetime_value' y los deja en formato numérico como texto (sin convertir todavía a float).
    6. Agrupa las categorías de vehículos de alta gama ('Sports Car', 'Luxury SUV', 'Luxury Car') en una única categoría: 'Luxury'.

    Parámetros:
    ------------
    df : pandas.DataFrame
        El DataFrame que contiene los datos a limpiar y normalizar.

    Retorna:
    --------
    pandas.DataFrame
        El mismo DataFrame, pero con los valores corregidos y estandarizados.

    """
    # Pasamos a minusculas todos los valores de la columna 'gender'
    df['gender']=df['gender'].str.lower()

    # Normalizamos los valores para tener sólo 'M' y 'F'
    df['gender'] = df['gender'].replace({
        'm': 'M',
        'f': 'F',
        'femal': 'F',
        'male': 'M',
        'female': 'F'
    })

    # Reemplazmos los valores de estados como AZ, Cali y WA por sus valores completos
    df['state'] = df['state'].replace({
        'AZ': 'Arizona',
        'Cali':'California',
        'WA':'Washington'
    })

    # En la columna de 'Education', reemplazamos 'Bachelors' por 'Bacherlor'
    df['education'] = df['education'].replace({
        'Bachelors':'Bachelor'
    })

    # Transformamos los valores de la columna 'customer_lifetime_value' para eliminar el carácter '%'
    # Primero, convertimos todo a string para evitar problemas (ya que hay valores NaN)
    df['customer_lifetime_value'] = df['customer_lifetime_value'].astype(str)

    # Luego, eliminanos el símbolo % y convertimos a número, ignorando los 'nan' que se crearon
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '', regex=False)

    # Trasnsformamos los valores de la columna 'vehicle_class' para agrupar a todos los coches de alta gama como 'Luxury'
    df['vehicle_class'] = df['vehicle_class'].replace({
        'Sports Car': 'Luxury',
        'Luxury SUV':'Luxury',
        'Luxury Car':'Luxury'
    })

    return df

def extraer_mayor(valor):
    """
    Extrae el mayor número de una cadena de números separados por '/'.

    Parámetros:
    -----------
    valor : str o None
        Cadena de texto con números enteros separados por barras ("/"), 
        o un valor nulo (NaN).

    Retorna:
    --------
    int o None
        El número entero más grande encontrado en la cadena.
        Si el valor es NaN, devuelve None.

    Ejemplos:
    ---------
    >>> extraer_mayor("1/3/5")
    5

    >>> extraer_mayor("2/2/2")
    2

    >>> extraer_mayor(None)
    None
    """
   
    if pd.isna(valor):
        return None
    if isinstance(valor, numbers.Number):  # Si ya es número, lo devolvemos
        return valor
   
    numeros = list(map(int, valor.split('/')))
    return max(numeros)
   



def formatting_data_types(df):
    """
    Formatea y corrige tipos de datos específicos en un DataFrame.

    Operaciones realizadas:
    ------------------------
    1. Convierte los valores de la columna 'customer_lifetime_value' de texto (que pueden incluir errores o valores no numéricos) a valores numéricos tipo float.
       - Los valores que no se puedan convertir se transformarán en NaN (Not a Number).

    2. Aplica la función `extraer_mayor` sobre la columna 'number_of_open_complaints', 
       que transforma cadenas de números separados por '/' en el número mayor de la secuencia.
    
    3. Devuelve el DataFrame modificado.

    Parámetros:
    ------------
    df : pandas.DataFrame
        El DataFrame que contiene las columnas 'customer_lifetime_value' y 'number_of_open_complaints' a formatear.

    Retorna:
    --------
    pandas.DataFrame
        El mismo DataFrame de entrada pero con los tipos de datos corregidos en las columnas mencionadas.

    """
    # Convertimos las cadenas de la columna 'customer_lifetime_value' a float, convirtiendo los 'nan' en NaN reales
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')
   
    # Aplicamos extraer_mayor a la columna 'number_of_open_complaints'
    df['number_of_open_complaints'] = df['number_of_open_complaints'].apply(extraer_mayor)
   
    return df 

def dealing_with_null_values(df):
    """
    Elimina los valores nulos del DataFrame y convierte las columnas numéricas a tipo entero.

    Pasos:
    1. Elimina todas las filas que contienen valores nulos en cualquier columna.
    2. Realiza una copia explícita del DataFrame resultante para evitar el warning SettingWithCopyWarning.
    3. Identifica todas las columnas de tipo numérico (float o int).
    4. Convierte las columnas numéricas a tipo entero (int), eliminando así posibles decimales residuales.

    Parámetros:
    ----------
    df : pandas.DataFrame
        El DataFrame original que puede contener valores nulos y columnas numéricas flotantes.

    Retorna:
    -------
    pandas.DataFrame
        Un nuevo DataFrame sin valores nulos y con las columnas numéricas convertidas a enteros.
    """

    # Quitamos todas las filas con valores nulos
    df = df.dropna().copy()

    # Seleccionamos las columnas numéricas
    columnas_numericas = df.select_dtypes(include=['float', 'int']).columns

    # Convertimos las columnas numéricas a int
    df[columnas_numericas] = df[columnas_numericas].astype(int)

    return df

def dealing_with_duplicates(df):
    """
    Elimina las filas duplicadas de un DataFrame.

    Pasos:
    1. Identifica las filas duplicadas en el DataFrame.
    2. Elimina las filas duplicadas, conservando únicamente la primera aparición de cada registro único.
    3. Devuelve un nuevo DataFrame limpio, sin duplicados.

    Parámetros:
    ----------
    df : pandas.DataFrame
        El DataFrame original que puede contener filas duplicadas.

    Retorna:
    -------
    pandas.DataFrame
        Un nuevo DataFrame en el que se han eliminado todas las filas duplicadas.
    """
    
    # Optamos por borrar las filas con duplicados conservando la primera aparición
    df_sin_duplicados = df.drop_duplicates()

    return df_sin_duplicados

def save_dataframe(df,file_url):
    """
    Guarda un DataFrame en un archivo CSV.

    Pasos:
    1. Convierte el DataFrame en un archivo CSV.
    2. Guarda el archivo en la ubicación especificada, sin incluir los índices de las filas.

    Parámetros:
    ----------
    df : pandas.DataFrame
        El DataFrame que se desea guardar en un archivo.
    
    file_url : str
        Ruta y nombre del archivo donde se guardará el DataFrame en formato CSV.

    Retorna:
    -------
    None
        Esta función no retorna ningún valor. Solo guarda el archivo en la ubicación indicada.
    """
    
    # Grabamos el nuevo DataFrame en un nuevo fichero
    df.to_csv(file_url,index=False)

