document.addEventListener('DOMContentLoaded', function() {
    // Función para calcular el subtotal
    function calcularSubtotal(row) {
        const procedimiento = row.querySelector('.procedimiento-select');
        const cantidad = row.querySelector('.cantidad-input');
        const descuento = row.querySelector('.descuento-input');
        const subtotal = row.querySelector('.subtotal-input');
        
        if (procedimiento.value) {
            const valor = parseFloat(procedimiento.options[procedimiento.selectedIndex].dataset.valor);
            const cant = parseInt(cantidad.value) || 0;
            const desc = parseFloat(descuento.value) || 0;
            
            let total = valor * cant;
            if (desc > 0) {
                total = total * (1 - desc / 100);
            }
            
            subtotal.value = '$' + total.toFixed(0);
        } else {
            subtotal.value = '$0';
        }
        
        calcularTotal();
    }

    // Función para calcular el total
    function calcularTotal() {
        const subtotales = document.querySelectorAll('.subtotal-input');
        let total = 0;
        
        subtotales.forEach(input => {
            const valor = parseFloat(input.value.replace('$', '')) || 0;
            total += valor;
        });
        
        const totalElement = document.getElementById('total-tratamiento');
        if (totalElement) {
            totalElement.textContent = '$' + total.toFixed(0);
        }
    }

    // Función para actualizar el contador de formularios
    function actualizarContadorFormularios() {
        const totalForms = document.querySelector('#id_procedimientos-TOTAL_FORMS');
        if (totalForms) {
            const formCount = document.querySelectorAll('.formset-row').length;
            totalForms.value = formCount;
        }
    }

    // Función para agregar nuevo procedimiento
    function agregarProcedimiento() {
        const totalForms = document.querySelector('#id_procedimientos-TOTAL_FORMS');
        if (!totalForms) return;

        const formCount = parseInt(totalForms.value);
        const container = document.getElementById('formset-container');
        if (!container) return;

        const template = container.querySelector('.formset-row');
        if (!template) return;

        const newRow = template.cloneNode(true);
        
        // Actualizar IDs y nombres
        newRow.querySelectorAll('[name*="-"]').forEach(input => {
            const newName = input.name.replace(/\d+/, formCount);
            input.name = newName;
            input.id = newName;
            input.value = '';
        });
        
        // Limpiar selecciones y valores
        newRow.querySelector('.procedimiento-select').selectedIndex = 0;
        newRow.querySelector('.cantidad-input').value = '1';
        newRow.querySelector('.descuento-input').value = '0';
        newRow.querySelector('.subtotal-input').value = '$0';
        
        // Agregar eventos
        newRow.querySelectorAll('.procedimiento-select, .cantidad-input, .descuento-input').forEach(input => {
            input.addEventListener('change', () => calcularSubtotal(newRow));
        });
        
        // Agregar evento para eliminar
        newRow.querySelector('.remove-formset').addEventListener('click', function() {
            newRow.remove();
            actualizarContadorFormularios();
            calcularTotal();
        });
        
        container.appendChild(newRow);
        totalForms.value = formCount + 1;
    }

    // Agregar eventos a los procedimientos existentes
    document.querySelectorAll('.formset-row').forEach(row => {
        // Eventos para cálculos
        row.querySelectorAll('.procedimiento-select, .cantidad-input, .descuento-input').forEach(input => {
            input.addEventListener('change', () => calcularSubtotal(row));
        });

        // Evento para eliminar
        const removeButton = row.querySelector('.remove-formset');
        if (removeButton) {
            removeButton.addEventListener('click', function() {
                row.remove();
                actualizarContadorFormularios();
                calcularTotal();
            });
        }
    });

    // Agregar evento al botón de agregar procedimiento
    const addButton = document.getElementById('add-formset');
    if (addButton) {
        addButton.addEventListener('click', agregarProcedimiento);
    }

    // Calcular subtotales iniciales
    document.querySelectorAll('.formset-row').forEach(row => {
        calcularSubtotal(row);
    });

    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}); 