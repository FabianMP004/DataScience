import csv
import requests
from bs4 import BeautifulSoup
import re
import time


# Función para extraer valores numéricos de un texto
def extract_value(text):
    match = re.search(r'(\d[\d,]*)', text)
    return match.group(1) if match else "N/A"


# Función para extraer el texto después de los dos puntos ":"
def extract_full_text(text):
    return text.split(':')[-1].strip()


# Función para obtener los datos de una propiedad específica
def data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # Evita bloqueos por protección anti-bots
        req = requests.get(url, headers=headers, timeout=10)
        req.raise_for_status()  # Lanza una excepción si hay errores HTTP

        soup = BeautifulSoup(req.content, "html.parser")

        # Extraer detalles de la propiedad
        results = soup.find(id="accordion_prop_details")
        detalles_list = results.find_all("div", class_="listing_detail col-md-4") if results else []

        results2 = soup.find(id="accordion_prop_addr")
        addr_list = results2.find_all("div", class_="listing_detail") if results2 else []

        results3 = soup.find(id="all_wrapper")
        cat_list = results3.find_all("div", class_="property_title_label") if results3 else []

        # Diccionario para almacenar los datos
        property_data = {
            "ID de la propiedad": "N/A",
            "Precio": "N/A",
            "Dormitorios": "N/A",
            "Banos": "N/A",
            "Parqueos": "N/A",
            "Tamano de la propiedad": "N/A",
            "Area": "N/A",
            "Categoria": "N/A",
            "URL": url
        }

        # Recorrer los elementos de detalles_list y asignar los valores correctos
        for detail in detalles_list:
            text = detail.text.strip()
            if "Código" in text or "ID" in text:
                property_data["ID de la propiedad"] = extract_full_text(text)
            elif "Precio" in text:
                property_data["Precio"] = extract_value(text)
            elif "Dormitorios" in text or "Habitaciones" in text:
                property_data["Dormitorios"] = extract_value(text)
            elif "Baños" in text:
                property_data["Banos"] = extract_value(text)
            elif "Parqueos" in text:
                property_data["Parqueos"] = extract_value(text)
            elif "Tamaño" in text or "Área" in text:
                property_data["Tamano de la propiedad"] = extract_value(text)

        # Extraer la información de la dirección (Área)
        for addr in addr_list:
            text = addr.text.strip()
            if "Zona" in text or "Área" in text:
                property_data["Area"] = extract_full_text(text)

        # Extraer la categoría
        if cat_list:
            property_data["Categoria"] = cat_list[0].text.strip()

        return property_data

    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return None


# Función para obtener todas las URLs de propiedades desde la página principal
def get_property_urls(main_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        req = requests.get(main_url, headers=headers, timeout=10)
        req.raise_for_status()

        soup = BeautifulSoup(req.content, "html.parser")

        property_links = []
        for link in soup.find_all("div", class_="carousel property_unit_carousel slide"):  # Ajusta si es necesario
            a_tag = link.find("a")
            if a_tag and a_tag.get("href"):
                href = a_tag.get("href")
                if "http" not in href:
                    href = main_url.rstrip("/") + "/" + href
                property_links.append(href)

        return property_links

    except requests.RequestException as e:
        print(f"Error al acceder a {main_url}: {e}")
        return []


# Función para guardar los datos en un archivo CSV
def save_to_csv(property_data, filename='datos3.csv'):
    headers = ["ID de la propiedad", "Precio", "Dormitorios", "Banos", "Parqueos",
               "Tamano de la propiedad", "Area", "Categoria", "URL"]

    file_exists = False
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        if not file_exists:
            writer.writeheader()  # Escribe encabezados si el archivo no existe

        writer.writerow(property_data)  # Guarda la propiedad en el CSV


# URL de la página principal donde están listadas las propiedades
main_url = "https://mapainmueble.com/casas-en-alquiler-zona-14/page/4/"  # Reemplázala si es necesario

# Obtener todas las URLs de las propiedades
property_urls = get_property_urls(main_url)

# Procesar cada propiedad y guardar los datos en CSV
for idx, url in enumerate(property_urls):
    print(f"Procesando {idx + 1}/{len(property_urls)}: {url}")
    property_data = data(url)

    if property_data:
        save_to_csv(property_data)
        time.sleep(1)  # Pausa para evitar bloqueos por parte del servidor

print("✅ Extracción completada. Los datos han sido guardados en 'datos3.csv'.")
