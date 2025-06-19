# Bitácora de Desarrollo

## Instrucciones Importantes

1. **Formato de Respuestas**
   - Ser conciso en las respuestas
   - Solo mostrar cambios específicos cuando sea necesario
   - Describir los cambios realizados en lugar de mostrar todo el código
   - Mantener un lenguaje claro y directo

2. **Estilo de Código**
   - Usar la paleta de colores definida
   - Mantener consistencia en los nombres de clases
   - Seguir las convenciones de Django

3. **Buenas Prácticas**
   - Documentar cambios importantes
   - Mantener el código limpio y organizado
   - Optimizar consultas a la base de datos
   - Manejar errores de forma adecuada

4. **Reglas para Modificaciones**
   - Solo hacer cambios específicos que se soliciten
   - No modificar nada sin autorización
   - No eliminar o alterar archivos que puedan afectar otras funcionalidades
   - Mantener los cambios enfocados en resolver el problema específico que se plantea

## Paleta de Colores
```css
:root {
    --dental-primary: #00A0B0;
    --dental-secondary: #008C9A;
    --dental-accent: #00B4C8;
    --dental-light: #E6F7F9;
    --dental-dark: #006D78;
}
```

## Convenciones de Nombres
- Clases CSS: `btn-dental-primary`, `bg-dental-primary`
- Variables: `empresa_actual`, `profesional_activo`
- Funciones: `get_empresa_actual`, `validar_rut`

## Estructura de Archivos
- Templates: `templates/profesionales/`
- Vistas: `profesionales/views.py`
- Formularios: `profesionales/forms.py`
- Modelos: `profesionales/models.py`
- URLs: `profesionales/urls.py`

## Registro de Cambios

### [2024-03-21]
- Creación inicial de la bitácora
- Definición de convenciones y estructura
- Establecimiento de paleta de colores
- Documentación de buenas prácticas 