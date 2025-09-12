# Bitácora de Estándares de Diseño - KreaDental Cloud

## Paleta de Colores Principal
### Azul Dental
- **Base (Principal)**: #1A5276
  - Uso: Títulos, botones principales, elementos destacados
- **Suave**: #2874A6
  - Uso: Hover de botones, elementos secundarios
- **Claro**: #AED6F1
  - Uso: Bordes, separadores
- **Muy Claro**: #E8F4FC
  - Uso: Fondo de headers, elementos de fondo

## Estándares de Listados
### Header de Panel
- **Fondo**: #E8F4FC (Azul Dental Muy Claro)
- **Borde Inferior**: #AED6F1 (Azul Dental Claro)
- **Título**: 
  - Color: #1A5276 (Azul Dental Base)
  - Tamaño: 1.5rem
  - Fuente: Poppins, sans-serif
  - Peso: 600
  - **IMPORTANTE**: Siempre incluir icono antes del título
  - Ejemplo: `<i class="fas fa-users me-2"></i>Pacientes`
- **Subtítulo**:
  - Color: #2874A6 (Azul Dental Suave)
  - Tamaño: 0.95rem
  - Peso: 400
  - Debe incluir descripción de funcionalidades

### Tabla
- **Encabezados**:
  - Color: #1A5276 (Azul Dental Base)
  - Borde inferior: #AED6F1 (Azul Dental Claro)
  - Texto en mayúsculas
  - Letra espaciada
- **Filas**:
  - Separador: #E8F4FC (Azul Dental Muy Claro)
  - Hover: #F8F9FA
- **Borde de Tarjeta**: #AED6F1 (Azul Dental Claro)

### Botones
- **Principal**:
  - Fondo: #1A5276 (Azul Dental Base)
  - Hover: #2874A6 (Azul Dental Suave)
- **Danger**:
  - Fondo: #e74c3c
  - Hover: #c0392b

## Estándares de Alertas y Confirmaciones
### SweetAlert2
- **IMPORTANTE**: Usar SweetAlert2 para todas las alertas y confirmaciones
- **Configuración Base**:
  ```javascript
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true
  });
  ```

### Tipos de Alertas
1. **Mensajes de Éxito**
   ```javascript
   Toast.fire({
     icon: 'success',
     title: 'Operación exitosa'
   });
   ```

2. **Mensajes de Error**
   ```javascript
   Toast.fire({
     icon: 'error',
     title: 'Ha ocurrido un error'
   });
   ```

3. **Confirmaciones**
   ```javascript
   Swal.fire({
     title: '¿Está seguro?',
     text: "Esta acción no se puede deshacer",
     icon: 'warning',
     showCancelButton: true,
     confirmButtonColor: '#1A5276',
     cancelButtonColor: '#95a5a6',
     confirmButtonText: 'Sí, continuar',
     cancelButtonText: 'Cancelar'
   });
   ```

4. **Mensajes de Información**
   ```javascript
   Toast.fire({
     icon: 'info',
     title: 'Información importante'
   });
   ```

### Colores de SweetAlert
- **Éxito**: #2ecc71
- **Error**: #e74c3c
- **Advertencia**: #f39c12
- **Info**: #3498db
- **Confirmación**: #1A5276 (Azul Dental Base)
- **Cancelación**: #95a5a6

## Estructura de Listados
1. **Header del Panel**
   - Icono + Título y botón de acción en primera línea
   - Subtítulo explicativo debajo
   - Fondo claro con borde sutil

2. **Contenido**
   - Tabla responsive
   - Acciones en última columna
   - Mensaje cuando no hay datos

## Notas Importantes
- Mantener consistencia en todos los listados del sistema
- Usar la misma estructura y paleta de colores
- Incluir subtítulos explicativos en todas las secciones
- Mantener la jerarquía visual con los colores establecidos
- **IMPORTANTE**: Siempre incluir iconos antes de los títulos
- **IMPORTANTE**: Mantener altura consistente en títulos y subtítulos
- **IMPORTANTE**: Usar SweetAlert2 para todas las alertas y confirmaciones

## Fecha de Implementación
- Implementado: 2024-03-19
- Última actualización: 2024-03-19

## Próximos Pasos
- [ ] Aplicar estándares a todos los listados del sistema
- [ ] Crear componentes reutilizables
- [ ] Documentar componentes en Storybook
- [ ] Crear guía de estilo completa
- [ ] Implementar SweetAlert2 en todas las vistas 