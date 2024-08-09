from bs4 import BeautifulSoup
import requests, json

def find_stations():
    url = 'https://en.wikipedia.org/wiki/List_of_Madrid_Metro_stations'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    nombres_tags = soup.find_all('div', class_='legend')
    color_spans = soup.find_all('span', class_='legend-color mw-no-invert')
    nombres = [n.text.strip() for n in nombres_tags]
    colors = []
    
    for cs in color_spans:
        style = cs.get('style', '')
        start_index = style.find('background-color:')
        if start_index != -1:
            start_index += len('background-color:')
            end_index = style.find(';', start_index)
         
        if end_index == -1:
            end_index = len(style)
            
        background_color = style[start_index:end_index].strip()
        colors.append(background_color)
           
    div = soup.find_all('div', class_='mw-content-ltr mw-parser-output')[0]
    uls = div.find_all('ul')[0:13] ##### 13
    linea = 1
    lineas = {}
    for ul in uls:
        list_stations = []
        for li in ul:
            a_tag = li.find('a')
            try:
                a_tag = li.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    station_link = a_tag['href']
                    station_name = a_tag.text
                    response_station = requests.get('https://en.wikipedia.org'+ station_link)
                    soup_station = BeautifulSoup(response_station.text, 'html.parser')
                    coords_str = soup_station.find('span', class_='geo-dec').text.strip()
                    lat, lon = [c[:-2] for c in coords_str.split()]
                    coords = (float(lat), -float(lon))
                    list_stations.append({
                    'nombre': station_name,
                    'coords': coords,
                    })
            except AttributeError as e:
                pass
 
        lineas[f'Línea {linea}'] = {
            'nombre': nombres[linea - 1],
            'color': colors[linea - 1],
            'estaciones': list_stations
            }
        print(lineas[f'Línea {linea}'])
        linea += 1

    if lineas:
        lineas = add_other_stations(lineas)
        with open('lineas.json', 'w', encoding='utf-8') as json_file:
            json.dump(lineas, json_file, ensure_ascii=False, indent=4)
        return lineas
    
def add_other_stations(data):
    estacion_a_lineas = {}

    # Recorrer cada línea y sus estaciones
    for linea, contenido in data.items():
        for estacion in contenido['estaciones']:
            coords = tuple(estacion['coords'])
            if coords not in estacion_a_lineas:
                estacion_a_lineas[coords] = []
            estacion_a_lineas[coords].append(linea)

    # Añadir el campo `other_lines` a cada estación
    for linea, contenido in data.items():
        for estacion in contenido['estaciones']:
            coords = tuple(estacion['coords'])
            estacion['other_lines'] = [l for l in estacion_a_lineas[coords] if l != linea]

    return data
    
    



if __name__ == '__main__':
    find_stations()