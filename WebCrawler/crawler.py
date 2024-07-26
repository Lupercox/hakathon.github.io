import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# Directorio donde se guardarán los archivos descargados
download_directory = "downloads"

# Crear el directorio si no existe
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

def is_valid_url(url):
    """
    Verifica si una URL es válida y completa.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_links(url):
    """
    Extrae y devuelve todos los enlaces válidos de una página web.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a"):
            href = a_tag.get("href")
            if href:
                full_url = urljoin(url, href)
                if is_valid_url(full_url):
                    links.add(full_url)
        return links
    except Exception as e:
        print(f"{Fore.RED}Error al obtener enlaces de {url}: {e}")
        return set()

def download_file(url):
    """
    Descarga un archivo desde una URL y lo guarda en el directorio especificado.
    """
    try:
        local_filename = os.path.join(download_directory, url.split("/")[-1])
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"{Fore.GREEN}Archivo descargado: {local_filename}")
        return local_filename
    except Exception as e:
        print(f"{Fore.RED}Error al descargar {url}: {e}")

def crawl(url, visited=set()):
    """
    Función recursiva que rastrea un sitio web, descarga archivos y sigue enlaces.
    """
    # Verificar si la URL ya ha sido visitada
    if url in visited:
        return
    visited.add(url)
    
    print(f"{Fore.GREEN}Rastreando: {url}")
    
    # Obtener todos los enlaces de la página actual
    links = get_all_links(url)
    for link in links:
        try:
            # Descargar archivos si tienen una extensión conocida
            if link.endswith(('pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'txt')):
                print(f"{Fore.GREEN}Descargando archivo: {link}")
                download_file(link)
            else:
                # Pausa entre solicitudes para no sobrecargar el servidor
                time.sleep(1)
                # Rastrear el enlace recursivamente
                crawl(link, visited)
        except Exception as e:
            print(f"{Fore.RED}Error al procesar {link}: {e}")

def main():
    """
    Función principal que inicializa el rastreo del sitio web.
    """
    # URL inicial para comenzar el rastreo
    start_url = "https://example.com"  # Reemplaza con la URL del sitio que deseas rastrear
    print(f"{Fore.GREEN}Iniciando rastreo en: {start_url}")
    crawl(start_url)
    print(f"{Fore.GREEN}Rastreo completado")

if __name__ == "__main__":
    main()
