// Toggle the side navigation
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
});

// Cerrar el menú al hacer clic fuera de él
document.addEventListener('click', function(e) {
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('#sidebarToggle');
    const content = document.querySelector('.content');
    
    if (sidebar && sidebarToggle && content) {
        const isClickInsideSidebar = sidebar.contains(e.target);
        const isClickOnToggle = sidebarToggle.contains(e.target);
        
        if (!isClickInsideSidebar && !isClickOnToggle && window.innerWidth < 768) {
            document.body.classList.remove('sidebar-toggled');
            sidebar.classList.remove('toggled');
            content.style.paddingLeft = '0';
        }
    }
});

// Ajustar el padding del contenido cuando se redimensiona la ventana
window.addEventListener('resize', function() {
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');
    
    if (content) {
        if (window.innerWidth >= 768) {
            content.style.paddingLeft = '250px';
        } else {
            if (sidebar && !sidebar.classList.contains('toggled')) {
                content.style.paddingLeft = '0';
            }
        }
    }
});

// Inicializar tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Función para actualizar el indicador de empresa actual
function updateCurrentCompanyIndicator() {
    const currentPath = window.location.pathname;
    const companyLinks = document.querySelectorAll('.company-selector');
    
    companyLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            link.innerHTML = '<i class="fas fa-check-circle me-2"></i>' + link.textContent;
        } else {
            link.classList.remove('active');
            link.innerHTML = '<i class="fas fa-building me-2"></i>' + link.textContent.replace('<i class="fas fa-check-circle me-2"></i>', '');
        }
    });
}

// Llamar a la función cuando se cargue la página
document.addEventListener('DOMContentLoaded', function() {
    updateCurrentCompanyIndicator();
    
    // Inicializar el menú desplegable de Bootstrap
    var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
    });
    
    // Cerrar el menú desplegable al hacer clic en un elemento
    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', function() {
            const dropdown = this.closest('.dropdown');
            if (dropdown) {
                const dropdownInstance = bootstrap.Dropdown.getInstance(dropdown.querySelector('.dropdown-toggle'));
                if (dropdownInstance) {
                    dropdownInstance.hide();
                }
            }
        });
    });
    
    // Manejar la animación de los iconos de submenú
    const collapseElements = document.querySelectorAll('[data-bs-toggle="collapse"]');
    collapseElements.forEach(element => {
        element.addEventListener('click', function() {
            const targetId = this.getAttribute('data-bs-target');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Esperar a que la animación de Bootstrap termine
                targetElement.addEventListener('shown.bs.collapse', function() {
                    const icon = element.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                    if (icon) {
                        icon.style.transform = 'rotate(180deg)';
                    }
                }, { once: true });
                
                targetElement.addEventListener('hidden.bs.collapse', function() {
                    const icon = element.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
                    if (icon) {
                        icon.style.transform = 'rotate(0deg)';
                    }
                }, { once: true });
            }
        });
    });
    
    // Inicializar el estado de los iconos basado en los menús ya expandidos
    collapseElements.forEach(element => {
        const targetId = element.getAttribute('data-bs-target');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement && targetElement.classList.contains('show')) {
            const icon = element.querySelector('.submenu-icon, .fa-chevron-down, .fa-angle-down');
            if (icon) {
                icon.style.transform = 'rotate(180deg)';
            }
        }
    });
});
