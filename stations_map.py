import folium, json, math

def desplazar_coords(lat, lon, index, total, radius=0.0003):
    angle = (index / total) * 2 * math.pi
    delta_lat = math.cos(angle) * radius
    delta_lon = math.sin(angle) * radius
    return lat + delta_lat, lon + delta_lon

# Función para detectar y modificar las coordenadas de estaciones superpuestas
def ajustar_coordenadas_superpuestas(datos):
    coord_dict = {}

    # Agrupar estaciones por coordenadas
    for linea, info in datos.items():
        for estacion in info['estaciones']:
            lat, lon = estacion['coords']
            coord_key = (lat, lon)

            if coord_key in coord_dict:
                coord_dict[coord_key].append(estacion)
            else:
                coord_dict[coord_key] = [estacion]

    # Ajustar las coordenadas de las estaciones superpuestas
    for coord_key, estaciones in coord_dict.items():
        total_estaciones = len(estaciones)

        if total_estaciones > 1:
            for index, estacion in enumerate(estaciones):
                lat, lon = coord_key
                lat_desplazado, lon_desplazado = desplazar_coords(lat, lon, index, total_estaciones)
                estacion['coords'] = [lat_desplazado, lon_desplazado]
    return datos

def create_map():
    m = folium.Map((40.4167635, -3.7036371), zoom_start=12)

    with open('lineas.json', 'r', encoding='utf-8') as json_file:
        lineas = json.load(json_file)
        
    informacion = ajustar_coordenadas_superpuestas(lineas)
    
    groups =[folium.FeatureGroup("Línea 1").add_to(m),
        folium.FeatureGroup("Línea 2").add_to(m),
        folium.FeatureGroup("Línea 3").add_to(m),
        folium.FeatureGroup("Línea 4").add_to(m),
        folium.FeatureGroup("Línea 5").add_to(m),
        folium.FeatureGroup("Línea 6").add_to(m),
        folium.FeatureGroup("Línea 7").add_to(m),
        folium.FeatureGroup("Línea 8").add_to(m),
        folium.FeatureGroup("Línea 9").add_to(m),
        folium.FeatureGroup("Línea 10").add_to(m),
        folium.FeatureGroup("Línea 11").add_to(m),
        folium.FeatureGroup("Línea 12").add_to(m),
        folium.FeatureGroup("Línea 13").add_to(m),
        ]

    for nom_linea in informacion:
        nombre_estacion = informacion[nom_linea]['nombre']
        color_linea = informacion[nom_linea]['color']
        for station in informacion[nom_linea]['estaciones']:
            icon_html2 = f'''
                <div style="
                background-color: {color_linea};
                color: #ffffff;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                text-align: center;
                line-height: 24px;
                font-size: 16px;
                font-family: Arial, sans-serif;
                border: 2px solid {color_linea};
                position: relative;
                top: -8px;
                left: -8px;
                ">{nom_linea.split()[-1]}</div>
                '''

            folium.Marker(
                location=station['coords'],
                tooltip=station['nombre'],
                popup=f"Línea 1: {nombre_estacion}\nEstación: {station['nombre']}",
                icon=folium.DivIcon(html=icon_html2)
                ).add_to(groups[int(nom_linea.split()[-1])-1])

    folium.LayerControl().add_to(m)
    
    return m

if __name__ == '__main__':
    map = create_map()
    map.save('mapa.html')