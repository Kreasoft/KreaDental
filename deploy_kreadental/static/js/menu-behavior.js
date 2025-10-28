// Comportamiento personalizado del menú lateral
document.addEventListener('DOMContentLoaded', function() {
    // Expandir todos los menús al cargar la página
    expandAllMenus();
    
    // Manejar clics en elementos del menú
    handleMenuClicks();
    
    // Marcar elemento activo basado en la URL actual
    markActiveMenuItem();
});

function expandAllMenus() {
    // Los menús aparecen colapsados por defecto
    // Solo expandir el menú que contiene el elemento activo
    const activeMenuItem = document.querySelector('.sidebar-menu a.active');
    if (activeMenuItem) {
        // Para menús con Bootstrap collapse
        const parentCollapse = activeMenuItem.closest('.collapse');
        if (parentCollapse) {
            parentCollapse.classList.add('show');
            // Rotar icono del trigger
            const trigger = document.querySelector(`[data-bs-target="#${parentCollapse.id}"]`);
            if (trigger) {
                const icon = trigger.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                if (icon) {
                    icon.style.transform = 'rotate(180deg)';
                }
            }
        }
        
        // Para submenús simples
        const parentSubmenu = activeMenuItem.closest('.submenu');
        if (parentSubmenu) {
            const parentHasSubmenu = parentSubmenu.closest('.has-submenu');
            if (parentHasSubmenu) {
                parentHasSubmenu.classList.add('expanded');
                const arrow = parentHasSubmenu.querySelector('.submenu-arrow');
                if (arrow) {
                    arrow.style.transform = 'rotate(180deg)';
                }
            }
        }
    }
}

function handleMenuClicks() {
    // Manejar clics en elementos del menú principal (no submenús)
    const mainMenuItems = document.querySelectorAll('.sidebar-menu > li > a:not([data-bs-toggle="collapse"])');
    mainMenuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Marcar como activo
            markMenuItemActive(this);
            
            // No colapsar menús - mantener todo expandido
            // Solo cambiar el estado activo
        });
    });
    
    // Manejar clics en elementos de submenú con Bootstrap collapse
    const subMenuItems = document.querySelectorAll('.collapse .nav a');
    subMenuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Marcar como activo
            markMenuItemActive(this);
            
            // Mantener el submenú expandido
            const parentCollapse = this.closest('.collapse');
            if (parentCollapse) {
                parentCollapse.classList.add('show');
                // Rotar icono del trigger
                const trigger = document.querySelector(`[data-bs-target="#${parentCollapse.id}"]`);
                if (trigger) {
                    const icon = trigger.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                    if (icon) {
                        icon.style.transform = 'rotate(180deg)';
                    }
                }
            }
        });
    });
    
    // Manejar clics en elementos de submenús simples
    const simpleSubMenuItems = document.querySelectorAll('.submenu a');
    simpleSubMenuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Marcar como activo
            markMenuItemActive(this);
            
            // Mantener el submenú expandido
            const parentHasSubmenu = this.closest('.has-submenu');
            if (parentHasSubmenu) {
                parentHasSubmenu.classList.add('expanded');
                const arrow = parentHasSubmenu.querySelector('.submenu-arrow');
                if (arrow) {
                    arrow.style.transform = 'rotate(180deg)';
                }
            }
        });
    });
    
    // Manejar clics en triggers de submenús simples
    const submenuTriggers = document.querySelectorAll('.has-submenu > a');
    submenuTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const parentHasSubmenu = this.closest('.has-submenu');
            if (parentHasSubmenu) {
                // Cerrar otros submenús simples
                closeOtherSimpleSubmenus(parentHasSubmenu);
                
                // Toggle este submenú
                if (parentHasSubmenu.classList.contains('expanded')) {
                    parentHasSubmenu.classList.remove('expanded');
                    const arrow = parentHasSubmenu.querySelector('.submenu-arrow');
                    if (arrow) {
                        arrow.style.transform = 'rotate(0deg)';
                    }
                } else {
                    parentHasSubmenu.classList.add('expanded');
                    const arrow = parentHasSubmenu.querySelector('.submenu-arrow');
                    if (arrow) {
                        arrow.style.transform = 'rotate(180deg)';
                    }
                }
            }
        });
    });
    
    // Manejar clics en triggers de collapse (para cambiar entre secciones)
    const collapseTriggers = document.querySelectorAll('[data-bs-toggle="collapse"]');
    collapseTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const targetId = this.getAttribute('data-bs-target');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Si el menú está cerrado, abrirlo
                if (!targetElement.classList.contains('show')) {
                    // Cerrar otros menús abiertos
                    closeOtherMenus(targetElement);
                    
                    // Abrir este menú
                    targetElement.classList.add('show');
                    
                    // Rotar icono
                    const icon = this.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                    if (icon) {
                        icon.style.transform = 'rotate(180deg)';
                    }
                } else {
                    // Si está abierto, cerrarlo
                    targetElement.classList.remove('show');
                    
                    // Rotar icono
                    const icon = this.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                    if (icon) {
                        icon.style.transform = 'rotate(0deg)';
                    }
                }
            }
        });
    });
}

function markMenuItemActive(clickedItem) {
    // Remover clase active de todos los elementos
    document.querySelectorAll('.sidebar-menu a').forEach(item => {
        item.classList.remove('active');
    });
    
    // Agregar clase active al elemento clickeado
    clickedItem.classList.add('active');
    
    // Si es un elemento de submenú, también marcar el trigger como activo
    const parentCollapse = clickedItem.closest('.collapse');
    if (parentCollapse) {
        const trigger = document.querySelector(`[data-bs-target="#${parentCollapse.id}"]`);
        if (trigger) {
            trigger.classList.add('active');
        }
    }
}

function markActiveMenuItem() {
    const currentPath = window.location.pathname;
    
    // Buscar elemento que coincida con la ruta actual
    const menuItems = document.querySelectorAll('.sidebar-menu a[href]');
    let activeItem = null;
    
    menuItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath.includes(href.replace('/', ''))) {
            activeItem = item;
        }
    });
    
    // Si no se encuentra coincidencia exacta, buscar por patrones
    if (!activeItem) {
        const pathSegments = currentPath.split('/').filter(segment => segment);
        
        menuItems.forEach(item => {
            const href = item.getAttribute('href');
            if (href) {
                const hrefSegments = href.split('/').filter(segment => segment);
                
                // Verificar si algún segmento de la URL coincide
                if (hrefSegments.some(segment => pathSegments.includes(segment))) {
                    activeItem = item;
                }
            }
        });
    }
    
    // Marcar como activo si se encuentra
    if (activeItem) {
        markMenuItemActive(activeItem);
        
        // Asegurar que el submenú esté expandido (Bootstrap collapse)
        const parentCollapse = activeItem.closest('.collapse');
        if (parentCollapse) {
            parentCollapse.classList.add('show');
            const trigger = document.querySelector(`[data-bs-target="#${parentCollapse.id}"]`);
            if (trigger) {
                const icon = trigger.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                if (icon) {
                    icon.style.transform = 'rotate(180deg)';
                }
            }
        }
        
        // Asegurar que el submenú simple esté expandido
        const parentSubmenu = activeItem.closest('.submenu');
        if (parentSubmenu) {
            const parentHasSubmenu = parentSubmenu.closest('.has-submenu');
            if (parentHasSubmenu) {
                parentHasSubmenu.classList.add('expanded');
                const arrow = parentHasSubmenu.querySelector('.submenu-arrow');
                if (arrow) {
                    arrow.style.transform = 'rotate(180deg)';
                }
            }
        }
    }
}

function closeOtherMenus(targetElement) {
    // Cerrar todos los otros menús excepto el actual
    const allCollapses = document.querySelectorAll('.collapse');
    allCollapses.forEach(collapse => {
        if (collapse !== targetElement) {
            collapse.classList.remove('show');
            
            // Rotar iconos de vuelta
            const trigger = document.querySelector(`[data-bs-target="#${collapse.id}"]`);
            if (trigger) {
                const icon = trigger.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                if (icon) {
                    icon.style.transform = 'rotate(0deg)';
                }
            }
        }
    });
    
    // También cerrar submenús simples
    closeAllSimpleSubmenus();
}

function closeAllSimpleSubmenus() {
    // Cerrar todos los submenús simples
    const allHasSubmenus = document.querySelectorAll('.has-submenu');
    allHasSubmenus.forEach(hasSubmenu => {
        hasSubmenu.classList.remove('expanded');
        const arrow = hasSubmenu.querySelector('.submenu-arrow');
        if (arrow) {
            arrow.style.transform = 'rotate(0deg)';
        }
    });
}

function closeOtherSimpleSubmenus(targetElement) {
    // Cerrar todos los otros submenús simples excepto el actual
    const allHasSubmenus = document.querySelectorAll('.has-submenu');
    allHasSubmenus.forEach(hasSubmenu => {
        if (hasSubmenu !== targetElement) {
            hasSubmenu.classList.remove('expanded');
            const arrow = hasSubmenu.querySelector('.submenu-arrow');
            if (arrow) {
                arrow.style.transform = 'rotate(0deg)';
            }
        }
    });
    
    // También cerrar menús de Bootstrap collapse
    const allCollapses = document.querySelectorAll('.collapse');
    allCollapses.forEach(collapse => {
        collapse.classList.remove('show');
        const trigger = document.querySelector(`[data-bs-target="#${collapse.id}"]`);
        if (trigger) {
            const icon = trigger.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
            if (icon) {
                icon.style.transform = 'rotate(0deg)';
            }
        }
    });
}

// Comportamiento personalizado del menú - ya manejado arriba
