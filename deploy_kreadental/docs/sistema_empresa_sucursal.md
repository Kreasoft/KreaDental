# Sistema de Empresa y Sucursal - Flujo Lógico

## 🎯 **Problema Resuelto**

Se ha corregido la confusión conceptual en el sistema de selección de empresa/sucursal. Ahora el flujo es más lógico y apropiado para el contexto dental.

## 🔄 **Flujo Anterior (Confuso)**
```
Usuario se registra → Se le asigna empresa → Puede "cambiar empresa" → Confusión
```

## ✅ **Flujo Nuevo (Lógico)**
```
Super Admin crea empresas y sucursales
↓
Super Admin asigna usuarios a empresas específicas
↓
Usuario se loguea → Ve su empresa asignada
↓
Usuario selecciona sucursal de trabajo (si hay múltiples)
↓
Usuario trabaja en esa sucursal específica
```

## 🏗️ **Arquitectura del Sistema**

### **Roles de Usuario:**
1. **Super Administrador**: Crea empresas, sucursales y asigna usuarios
2. **Administrador de Empresa**: Gestiona su empresa y sucursales
3. **Administrador de Sucursal**: Gestiona su sucursal específica
4. **Profesional/Recepción/Auxiliar**: Trabaja en sucursal asignada

### **Jerarquía:**
```
Empresa (Clínica Dental)
├── Sucursal Principal
├── Sucursal Norte
├── Sucursal Sur
└── Usuarios asignados
```

## 🔧 **Cambios Implementados**

### **1. Context Processors Nuevos:**
- `sucursal_actual`: Obtiene la sucursal actual del usuario
- `sucursales_disponibles`: Lista todas las sucursales de la empresa

### **2. Vista Nueva:**
- `cambiar_sucursal`: Permite cambiar de sucursal dentro de la misma empresa

### **3. Interfaz Actualizada:**

#### **Sidebar:**
- ❌ **Eliminado**: Selector de "Cambiar Clínica"
- ✅ **Agregado**: Información de clínica y sucursal actual
- ✅ **Agregado**: Selector de sucursal (solo si hay múltiples)

#### **Barra Superior:**
- ✅ **Actualizado**: Muestra clínica + sucursal actual
- ✅ **Agregado**: Dropdown con información detallada
- ✅ **Agregado**: Opción para cambiar sucursal

#### **Perfil de Usuario:**
- ✅ **Actualizado**: Muestra clínica y sucursal asignada

## 📋 **Funcionalidades**

### **Para Usuarios Regulares:**
1. **Ver clínica asignada**: Siempre visible en el sidebar
2. **Ver sucursal actual**: Mostrada debajo del nombre de la clínica
3. **Cambiar sucursal**: Solo si tiene acceso a múltiples sucursales
4. **Información detallada**: En dropdowns de la barra superior

### **Para Administradores:**
1. **Gestión de empresas**: Crear y configurar clínicas
2. **Gestión de sucursales**: Crear y configurar sucursales
3. **Asignación de usuarios**: Asignar usuarios a empresas y sucursales

## 🎨 **Interfaz de Usuario**

### **Sidebar Principal:**
```
🏥 Clínica Dental ABC
   📍 Sucursal Centro

📍 Cambiar Sucursal ▼
   ✅ Sucursal Centro
   🏢 Sucursal Norte
   🏢 Sucursal Sur
```

### **Barra Superior:**
```
🏥 Clínica Dental ABC
📍 Sucursal Centro

Dropdown:
📋 Información de Clínica
   Clínica Dental ABC
   Av. Principal 123

📍 Sucursal: Sucursal Centro
   Calle Secundaria 456

🔄 Cambiar sucursal
   ✅ Sucursal Centro
   🏢 Sucursal Norte
   🏢 Sucursal Sur
```

## 🔒 **Seguridad y Permisos**

### **Validaciones:**
- Usuario solo puede ver su empresa asignada
- Usuario solo puede cambiar a sucursales de su empresa
- Verificación de permisos en cada operación

### **Sesión:**
- `empresa_actual_id`: ID de la empresa en sesión
- Sucursal actual: Almacenada en `UsuarioEmpresa.sucursal`

## 📁 **Archivos Modificados**

### **Backend:**
- `empresa/context_processors.py`: Nuevos context processors
- `empresa/views.py`: Nueva vista `cambiar_sucursal`
- `empresa/urls.py`: Nueva URL para cambiar sucursal
- `config/settings.py`: Registro de context processors

### **Frontend:**
- `templates/base.html`: Interfaz actualizada
- `static/css/sidebar.css`: Estilos para nuevos elementos
- `static/js/sidebar.js`: JavaScript para animaciones

## 🚀 **Beneficios**

1. **Claridad conceptual**: El usuario entiende que trabaja en una clínica específica
2. **Simplicidad**: No hay confusión sobre "cambiar empresa"
3. **Flexibilidad**: Puede cambiar de sucursal si es necesario
4. **Información clara**: Siempre sabe en qué clínica y sucursal está
5. **Escalabilidad**: Fácil agregar más sucursales

## 🔮 **Próximos Pasos**

1. **Migración de datos**: Asignar sucursales a usuarios existentes
2. **Pruebas**: Verificar funcionamiento con múltiples sucursales
3. **Documentación**: Manual de usuario para administradores
4. **Optimización**: Cache para context processors si es necesario 