# Proyecto Web GO TRAVEL

Este proyecto es una página web que incluye un slider de imágenes, una galería de imagenes, un formulario de contacto, una sección de destinos (editables y eliminables por roles específicos), un espacio para comentarios y la posibilidad de personalizar el perfil. Además, trae la posibilidad de poder filtrar y buscar entre los diferentes destinos, aparte de crear nuevos. Todo esto implementado en Django


## Configuración y Uso

### 1. Configurar settings.py
Asegurarse que el settings.py tenga estas 3 lineas:
```settings.py
    BASE_DIR = Path(__file__).resolve().parent.parent

    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL  = '/media/'
```

### 2. Iniciar el entorno virtual
```bash
python -m venv venv

.\venv\Scripts\activate
```

### 3. Instalar Django
Se hace mediante
```bash
pip install django
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Referentes y Material Adicional


- [Guía rápida de Markdown](https://www.markdownguide.org/)

---
