/**
 * Funciones personalizadas de SweetAlert2 para KreaDental Cloud
 */

// Configuración global de SweetAlert2
const SwalConfig = {
    confirmButtonColor: '#1A5276',
    cancelButtonColor: '#6c757d',
    background: '#ffffff',
    backdrop: 'rgba(0,0,0,0.4)',
    customClass: {
        popup: 'swal2-popup-dental',
        confirmButton: 'swal2-confirm-dental',
        cancelButton: 'swal2-cancel-dental',
        title: 'swal2-title-dental',
        content: 'swal2-content-dental'
    }
};

/**
 * Mostrar mensaje de éxito
 * @param {string} title - Título del mensaje
 * @param {string} message - Mensaje a mostrar
 * @param {number} timer - Tiempo en ms (opcional)
 */
function showSuccess(title, message, timer = 3000) {
    return Swal.fire({
        icon: 'success',
        title: title,
        text: message,
        timer: timer,
        timerProgressBar: true,
        showConfirmButton: false,
        ...SwalConfig
    });
}

/**
 * Mostrar mensaje de error
 * @param {string} title - Título del mensaje
 * @param {string} message - Mensaje a mostrar
 */
function showError(title, message) {
    return Swal.fire({
        icon: 'error',
        title: title,
        text: message,
        confirmButtonText: 'Entendido',
        ...SwalConfig
    });
}

/**
 * Mostrar mensaje de advertencia
 * @param {string} title - Título del mensaje
 * @param {string} message - Mensaje a mostrar
 */
function showWarning(title, message) {
    return Swal.fire({
        icon: 'warning',
        title: title,
        text: message,
        confirmButtonText: 'Entendido',
        ...SwalConfig
    });
}

/**
 * Mostrar mensaje de información
 * @param {string} title - Título del mensaje
 * @param {string} message - Mensaje a mostrar
 */
function showInfo(title, message) {
    return Swal.fire({
        icon: 'info',
        title: title,
        text: message,
        confirmButtonText: 'Entendido',
        ...SwalConfig
    });
}

/**
 * Confirmar eliminación
 * @param {string} title - Título de la confirmación
 * @param {string} message - Mensaje de confirmación
 * @param {string} confirmText - Texto del botón confirmar
 * @param {string} cancelText - Texto del botón cancelar
 */
function confirmDelete(title, message, confirmText = 'Sí, eliminar', cancelText = 'Cancelar') {
    return Swal.fire({
        icon: 'warning',
        title: title,
        text: message,
        showCancelButton: true,
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        reverseButtons: true,
        ...SwalConfig
    });
}

/**
 * Confirmar desactivación
 * @param {string} title - Título de la confirmación
 * @param {string} message - Mensaje de confirmación
 * @param {string} confirmText - Texto del botón confirmar
 * @param {string} cancelText - Texto del botón cancelar
 */
function confirmDeactivate(title, message, confirmText = 'Sí, desactivar', cancelText = 'Cancelar') {
    return Swal.fire({
        icon: 'question',
        title: title,
        text: message,
        showCancelButton: true,
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        confirmButtonColor: '#fd7e14',
        cancelButtonColor: '#6c757d',
        reverseButtons: true,
        ...SwalConfig
    });
}

/**
 * Confirmar acción general
 * @param {string} title - Título de la confirmación
 * @param {string} message - Mensaje de confirmación
 * @param {string} confirmText - Texto del botón confirmar
 * @param {string} cancelText - Texto del botón cancelar
 */
function confirmAction(title, message, confirmText = 'Confirmar', cancelText = 'Cancelar') {
    return Swal.fire({
        icon: 'question',
        title: title,
        text: message,
        showCancelButton: true,
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        reverseButtons: true,
        ...SwalConfig
    });
}

/**
 * Mostrar loading
 * @param {string} title - Título del loading
 * @param {string} message - Mensaje del loading
 */
function showLoading(title = 'Procesando...', message = 'Por favor espera') {
    return Swal.fire({
        title: title,
        text: message,
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
}

/**
 * Mostrar formulario de entrada
 * @param {string} title - Título del formulario
 * @param {string} message - Mensaje del formulario
 * @param {string} inputType - Tipo de input (text, email, password, etc.)
 * @param {string} placeholder - Placeholder del input
 * @param {string} confirmText - Texto del botón confirmar
 * @param {string} cancelText - Texto del botón cancelar
 */
function showInput(title, message, inputType = 'text', placeholder = '', confirmText = 'Confirmar', cancelText = 'Cancelar') {
    return Swal.fire({
        title: title,
        text: message,
        input: inputType,
        inputPlaceholder: placeholder,
        showCancelButton: true,
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        reverseButtons: true,
        inputValidator: (value) => {
            if (!value) {
                return 'Debes ingresar un valor';
            }
        },
        ...SwalConfig
    });
}

/**
 * Mostrar mensaje de éxito con redirección
 * @param {string} title - Título del mensaje
 * @param {string} message - Mensaje a mostrar
 * @param {string} url - URL a la que redirigir
 * @param {number} timer - Tiempo en ms antes de redirigir
 */
function showSuccessAndRedirect(title, message, url, timer = 2000) {
    return Swal.fire({
        icon: 'success',
        title: title,
        text: message,
        timer: timer,
        timerProgressBar: true,
        showConfirmButton: false,
        ...SwalConfig
    }).then(() => {
        window.location.href = url;
    });
}

/**
 * Mostrar mensaje de error con redirección
 * @param {string} title - Título del mensaje
 * @param {string} message - Mensaje a mostrar
 * @param {string} url - URL a la que redirigir
 * @param {number} timer - Tiempo en ms antes de redirigir
 */
function showErrorAndRedirect(title, message, url, timer = 3000) {
    return Swal.fire({
        icon: 'error',
        title: title,
        text: message,
        timer: timer,
        timerProgressBar: true,
        showConfirmButton: false,
        ...SwalConfig
    }).then(() => {
        window.location.href = url;
    });
}

/**
 * Función para confirmar eliminación de elementos
 * @param {string} url - URL del formulario de eliminación
 * @param {string} title - Título de la confirmación
 * @param {string} message - Mensaje de confirmación
 */
function confirmDeleteAndSubmit(url, title = '¿Estás seguro?', message = 'Esta acción no se puede deshacer') {
    confirmDelete(title, message).then((result) => {
        if (result.isConfirmed) {
            // Crear formulario temporal
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = url;
            
            // Agregar CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
            
            // Enviar formulario
            document.body.appendChild(form);
            form.submit();
        }
    });
}

/**
 * Función para confirmar desactivación de elementos
 * @param {string} url - URL del formulario de desactivación
 * @param {string} title - Título de la confirmación
 * @param {string} message - Mensaje de confirmación
 */
function confirmDeactivateAndSubmit(url, title = '¿Estás seguro?', message = '¿Deseas desactivar este elemento?') {
    confirmDeactivate(title, message).then((result) => {
        if (result.isConfirmed) {
            // Crear formulario temporal
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = url;
            
            // Agregar CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
            
            // Enviar formulario
            document.body.appendChild(form);
            form.submit();
        }
    });
}

// Agregar estilos personalizados para SweetAlert
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .swal2-popup-dental {
            font-family: 'Poppins', sans-serif !important;
            border-radius: 15px !important;
        }
        
        .swal2-title-dental {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            color: #1A5276 !important;
        }
        
        .swal2-content-dental {
            font-family: 'Poppins', sans-serif !important;
            color: #6c757d !important;
        }
        
        .swal2-confirm-dental {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 500 !important;
            border-radius: 10px !important;
            padding: 0.75rem 2rem !important;
        }
        
        .swal2-cancel-dental {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 500 !important;
            border-radius: 10px !important;
            padding: 0.75rem 2rem !important;
        }
    `;
    document.head.appendChild(style);
}); 