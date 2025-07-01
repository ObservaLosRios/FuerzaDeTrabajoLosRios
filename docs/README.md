# Documentación del Proyecto

Esta carpeta contiene la documentación técnica y de usuario del proyecto.

## Estructura

- `api/` - Documentación de la API (si aplica)
- `architecture.md` - Arquitectura del sistema
- `data_dictionary.md` - Diccionario de datos
- `methodology.md` - Metodología de análisis
- `deployment.md` - Guía de despliegue

## Documentación Disponible

### Para Desarrolladores
- **Arquitectura**: Explicación de la estructura modular
- **API Reference**: Documentación de funciones y clases
- **Contribution Guide**: Guía para contribuir al proyecto

### Para Usuarios
- **User Guide**: Guía de uso del proyecto
- **Data Dictionary**: Descripción de variables y datasets
- **Methodology**: Explicación de metodologías aplicadas

### Para Stakeholders
- **Executive Summary**: Resumen ejecutivo del proyecto
- **Business Impact**: Impacto y valor del análisis
- **Roadmap**: Futuras mejoras y expansiones

## Generar Documentación

La documentación se puede generar automáticamente usando:

```bash
# Sphinx para documentación técnica
sphinx-build -b html docs/ docs/_build/

# Jupyter Book para documentación interactiva
jupyter-book build docs/
```
