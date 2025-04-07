import csv
from GoTravel.models import Destinos

with open('GoTravel/data/100destinos.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    objetos = [Destinos(destino=row['destino'], pais=row['pais'], continente=row['continente'], idioma=row['idioma'], moneda=row['moneda']) for row in reader]

Destinos.objects.bulk_create(objetos)
print(f"Se cargaron {len(objetos)} destinos.")
