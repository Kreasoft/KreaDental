# Iconos de Submenú en el Sidebar

## Descripción
Se han agregado iconos de flecha a todos los menús expandibles del sidebar para indicar visualmente que tienen submenús. Los iconos están alineados a la derecha y tienen animación de rotación cuando se expande/contrae el menú.

## Cambios Realizados

### 1. Estructura HTML (templates/base.html)
- Se modificó la estructura de los enlaces con submenús para usar `d-flex align-items-center justify-content-between`
- Se envolvió el contenido principal (icono + texto) en un `<div>`
- Se agregó el icono de flecha con la clase `submenu-icon` al final del enlace

### 2. Estilos CSS (static/css/sidebar.css)
- Se mejoraron los estilos para los iconos de submenú:
  - `margin-left: auto` para alinearlos a la derecha
  - `flex-shrink: 0` para evitar que se compriman
  - `transition: transform 0.3s ease` para animación suave
- Se agregaron estilos específicos para enlaces con submenús:
  - `justify-content: space-between` para distribuir el contenido
  - Estilos para el contenedor del icono principal

### 3. JavaScript (static/js/sidebar.js)
- Se agregó funcionalidad para manejar la animación de los iconos:
  - Rotación de 180° cuando el menú se expande
  - Rotación de 0° cuando el menú se contrae
  - Inicialización del estado correcto al cargar la página

## Menús Afectados
Los siguientes menús ahora tienen iconos de flecha:
- **Laboratorios** (Control)
- **Tablas del Sistema** (Tablas del Sistema)
- **Informes** (Reportes)
- **Configuración** (Configuración)
- **Usuario** (Usuario)

## Comportamiento
1. **Estado inicial**: Los iconos apuntan hacia abajo (▼)
2. **Al expandir**: Los iconos rotan 180° y apuntan hacia arriba (▲)
3. **Al contraer**: Los iconos vuelven a su posición original (▼)
4. **Animación**: Transición suave de 0.3 segundos

## Clases CSS Utilizadas
- `.submenu-icon`: Clase principal para los iconos de submenú
- `.fa-chevron-down`, `.fa-angle-down`: Clases de FontAwesome para las flechas
- `[data-bs-toggle="collapse"]`: Selector para enlaces con submenús

## Compatibilidad
- Funciona con Bootstrap 5
- Compatible con FontAwesome 5+
- Responsive design mantenido
- Funciona en todos los navegadores modernos 