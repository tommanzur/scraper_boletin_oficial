import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Diccionario para mapear los meses en español a inglés
meses = {
    'Enero': 'January',
    'Febrero': 'February',
    'Marzo': 'March',
    'Abril': 'April',
    'Mayo': 'May',
    'Junio': 'June',
    'Julio': 'July',
    'Agosto': 'August',
    'Septiembre': 'September',
    'Octubre': 'October',
    'Noviembre': 'November',
    'Diciembre': 'December'
}

# URL de la primera sección del Boletín Oficial de Argentina
url = 'https://www.boletinoficial.gob.ar/seccion/primera'

# Hacemos la solicitud a la página de la primera sección
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extraer y convertir la fecha de publicación
fecha_texto = soup.find('div', class_='margin-bottom-20 fecha-ultima-edicion').find_all('h6')[1].text.strip()
for mes_es, mes_en in meses.items():
    fecha_texto = fecha_texto.replace(mes_es, mes_en)
fecha_publicacion = datetime.strptime(fecha_texto, '%d de %B de %Y').strftime('%d/%m/%Y')

datos = []

# Buscamos todos los avisos en la primera sección
for aviso in soup.find_all('div', class_='col-md-12 avisosSeccionDiv'):
    for enlace in aviso.find_all('a', href=True):
        url_detalle = 'https://www.boletinoficial.gob.ar' + enlace['href']
        response_detalle = requests.get(url_detalle)
        soup_detalle = BeautifulSoup(response_detalle.text, 'html.parser')

        titulo = soup_detalle.find(id='tituloDetalleAviso').text.strip()
        texto = soup_detalle.find(id='cuerpoDetalleAviso').text.strip()
        
        datos.append({'Fecha Publicación': fecha_publicacion, 'Título': titulo, 'Texto': texto, 'Enlace': url_detalle})

# Crear el DataFrame
df = pd.DataFrame(datos)

# Guardar el DataFrame
df.to_csv('/ruta/donde/guardar/el/archivo.csv', index=False)
