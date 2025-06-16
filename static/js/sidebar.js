// Toggle the side navigation
const sidebarToggle = document.body.querySelector('#sidebarToggle');
const sidebar = document.body.querySelector('#wrapper');
const content = document.body.querySelector('#content');

if (sidebarToggle) {
    // Mostrar/ocultar el menú en dispositivos móviles
    sidebarToggle.addEventListener('click', function(e) {
        e.preventDefault();
        document.body.classList.toggle('sidebar-toggled');
        sidebar.classList.toggle('toggled');
        
        // Si el menú está abierto, agregar padding al contenido
        if (sidebar.classList.contains('toggled')) {
            content.style.paddingLeft = '0';
        } else {
            content.style.paddingLeft = '250px';
        }
    });
}

// Cerrar el menú al hacer clic fuera de él
document.addEventListener('click', function(e) {
    const isClickInsideSidebar = sidebar.contains(e.target);
    const isClickOnToggle = sidebarToggle.contains(e.target);
    
    if (!isClickInsideSidebar && !isClickOnToggle && window.innerWidth < 768) {
        document.body.classList.remove('sidebar-toggled');
        sidebar.classList.remove('toggled');
        content.style.paddingLeft = '0';
    }
});

// Ajustar el padding del contenido cuando se redimensiona la ventana
window.addEventListener('resize', function() {
    if (window.innerWidth >= 768) {
        content.style.paddingLeft = '250px';
    } else {
        if (!sidebar.classList.contains('toggled')) {
            content.style.paddingLeft = '0';
        }
    }
});

// Inicializar tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
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
});
