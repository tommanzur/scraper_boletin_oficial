import requests
import pandas as pd
from bs4 import BeautifulSoup
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

def obtener_fecha_publicacion(soup):
    """Función para obtener la fecha de publicación"""
    fecha_texto = soup.find('div', class_='margin-bottom-20 fecha-ultima-edicion').find_all('h6')[1].text.strip()
    for mes_es, mes_en in meses.items():
        fecha_texto = fecha_texto.replace(mes_es, mes_en)
    return datetime.strptime(fecha_texto, '%d de %B de %Y').strftime('%d/%m/%Y')

def obtener_detalles_aviso(url_detalle):
    """Función para obtener detalles de un aviso"""
    try:
        response_detalle = session.get(url_detalle)
        response_detalle.raise_for_status()
        soup_detalle = BeautifulSoup(response_detalle.text, 'html.parser')
        titulo = soup_detalle.find(id='tituloDetalleAviso').text.strip()
        texto = soup_detalle.find(id='cuerpoDetalleAviso').text.strip()
        return {'Título': titulo, 'Texto': texto, 'Enlace': url_detalle}
    except Exception as e:
        print(f"Error al obtener detalles del aviso: {e}")
        return None

url_base = 'https://www.boletinoficial.gob.ar'
url_seccion = f'{url_base}/seccion/primera'

datos = []

with requests.Session() as session:
    try:
        response = session.get(url_seccion)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        fecha_publicacion = obtener_fecha_publicacion(soup)

        avisos = soup.find_all('div', class_='col-md-12 avisosSeccionDiv')
        for aviso in avisos:
            enlaces = [a['href'] for a in aviso.find_all('a', href=True)]
            for enlace in enlaces:
                url_detalle = f'{url_base}{enlace}'
                detalle_aviso = obtener_detalles_aviso(url_detalle)
                if detalle_aviso:
                    detalle_aviso['Fecha Publicación'] = fecha_publicacion
                    datos.append(detalle_aviso)
        df = pd.DataFrame(datos)
        df.to_csv(f'./{str(fecha_publicacion).replace("/", "-")}.csv', index=False)
    except Exception as e:
        print(f"Error al obtener datos de la sección: {e}")
