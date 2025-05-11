import csv
import os
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import mimetypes
from GoTravel.models import Destinos

CSV_PATH = 'GoTravel/data/100destinos.csv'

created_count = 0
updated_count = 0
saved_count = 0
failed_urls = []  # Lista para almacenar URLs problemáticas

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.ico', '.heic', '.heif'}

def clean_url(url):
    """Limpia la URL eliminando caracteres inválidos y corrigiendo errores comunes."""
    # Eliminar caracteres finales como ;;; o espacios
    url = url.strip(' ;')
    # Corregir dobles puntos en el dominio
    url = url.replace('cloudfront..net', 'cloudfront.net')
    return url

def get_file_extension(url, response):
    """Determina la extensión del archivo basado en la URL o el Content-Type."""
    parsed_url = urlparse(url)
    ext = os.path.splitext(parsed_url.path)[1].lower()
    
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return ext
    
    content_type = response.headers.get('Content-Type', '')
    if content_type:
        ext_from_mime = mimetypes.guess_extension(content_type.split(';')[0].strip())
        if ext_from_mime and ext_from_mime.lower() in ALLOWED_IMAGE_EXTENSIONS:
            return ext_from_mime
    
    print(f"⚠️ No se pudo determinar la extensión para {url}, usando .jpg como fallback.")
    return '.jpg'

with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    possible_keys = [k for k in reader.fieldnames if 'image_url' in k.lower()]
    image_key = possible_keys[0] if possible_keys else None

    if not image_key:
        print("❌ No se encontró ninguna columna con 'image_url' en el CSV.")
    else:
        print(f"ℹ️ Usando la columna '{image_key}' para las URLs de imagen.")

    for row in reader:
        nombre = row.get('Destino', '').strip()
        pais = row.get('País', '').strip()
        continente = row.get('Continente', '').strip()
        idioma = row.get('Idioma', '').strip()
        moneda = row.get('Moneda', '').strip()
        image_url = row.get(image_key, '').strip() if image_key else ''

        destino_obj, created = Destinos.objects.update_or_create(
            destino=nombre,
            defaults={
                'pais': pais,
                'continente': continente,
                'idioma': idioma,
                'moneda': moneda,
            }
        )
        if created:
            created_count += 1
            print(f"✅ Creado destino: {nombre}")
        else:
            updated_count += 1
            print(f"🔄 Actualizado destino: {nombre}")

        if image_url:
            try:
                # Limpiar la URL
                cleaned_url = clean_url(image_url)
                print(f"📥 Descargando imagen para {nombre} desde {cleaned_url} …")
                response = requests.get(cleaned_url, timeout=15)
                print(f"   Código HTTP: {response.status_code}")
                response.raise_for_status()

                content_type = response.headers.get('Content-Type', '')
                if not content_type.startswith('image/'):
                    raise ValueError(f"El contenido no es una imagen: {content_type}")

                ext = get_file_extension(cleaned_url, response)
                filename = f"{nombre.lower().replace(' ', '_')}{ext}"
                
                destino_obj.imagen.save(filename, ContentFile(response.content), save=True)
                filepath = destino_obj.imagen.path
                print(f"✅ Guardada imagen para {nombre} en: {filepath}")
                saved_count += 1
            except Exception as e:
                error_msg = f"⚠️ Error descargando o guardando imagen para {nombre}: {e}"
                print(error_msg)
                failed_urls.append({'destino': nombre, 'url': image_url, 'error': str(e)})

print("\n--- Resumen ---")
print(f"Destinos creados:     {created_count}")
print(f"Destinos actualizados:{updated_count}")
print(f"Imágenes guardadas:   {saved_count}")
if failed_urls:
    print("\n--- URLs con errores ---")
    for item in failed_urls:
        print(f"Destino: {item['destino']}, URL: {item['url']}, Error: {item['error']}")