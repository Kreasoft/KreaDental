// Toggle the side navigation
const sidebarToggle = document.body.querySelector('#sidebarToggle');
if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener('click', event => {
        event.preventDefault();
        document.body.classList.toggle('sb-sidenav-toggled');
        localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
    });
}

// Initialize DataTables
$(document).ready(function() {
    if ($.fn.DataTable) {
        $('.datatable').DataTable({
            responsive: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json'
            }
        });
    }
});

// Initialize Select2
$(document).ready(function() {
    if ($.fn.select2) {
        $('.select2').select2({
            language: 'es',
            theme: 'bootstrap-5'
        });
    }
});

// Initialize tooltips
$(document).ready(function() {
    if ($.fn.tooltip) {
        $('[data-bs-toggle="tooltip"]').tooltip();
    }
});

// Initialize popovers
$(document).ready(function() {
    if ($.fn.popover) {
        $('[data-bs-toggle="popover"]').popover();
    }
});

// Setup procedimiento listeners
$(document).ready(function() {
    function setupProcedimientoListeners() {
        $('.procedimiento-row').each(function() {
            const row = $(this);
            const removeBtn = row.find('.procedimiento-remove');
            
            if (removeBtn.length) {
                removeBtn.on('click', function() {
                    row.remove();
                    updateTotals();
                });
            }
        });
    }

    function updateTotals() {
        let total = 0;
        $('.procedimiento-row').each(function() {
            const cantidad = parseFloat($(this).find('.cantidad').val()) || 0;
            const precio = parseFloat($(this).find('.precio').val()) || 0;
            const descuento = parseFloat($(this).find('.descuento').val()) || 0;
            
            const subtotal = cantidad * precio;
            const descuentoMonto = (subtotal * descuento) / 100;
            const totalRow = subtotal - descuentoMonto;
            
            $(this).find('.subtotal').val(subtotal.toFixed(2));
            $(this).find('.descuento-monto').val(descuentoMonto.toFixed(2));
            $(this).find('.total').val(totalRow.toFixed(2));
            
            total += totalRow;
        });
        
        $('#costo-total').val(total.toFixed(2));
    }

    // Setup initial listeners
    setupProcedimientoListeners();

    // Add new procedimiento
    $('#add-procedimiento').on('click', function() {
        const formset = $('#id_detalles-TOTAL_FORMS');
        const totalForms = parseInt(formset.val());
        
        // Clone the first procedimiento row
        const newRow = $('.procedimiento-row:first').clone();
        
        // Update form index
        newRow.find('input, select').each(function() {
            const name = $(this).attr('name');
            if (name) {
                $(this).attr('name', name.replace('-0-', `-${totalForms}-`));
                $(this).attr('id', $(this).attr('id').replace('-0-', `-${totalForms}-`));
            }
        });
        
        // Clear values
        newRow.find('input[type="text"], input[type="number"]').val('');
        newRow.find('select').val('');
        
        // Add to form
        $('.procedimientos-container').append(newRow);
        
        // Update form count
        formset.val(totalForms + 1);
        
        // Setup listeners for new row
        setupProcedimientoListeners();
    });

    // Update totals when values change
    $(document).on('change', '.cantidad, .precio, .descuento', function() {
        updateTotals();
    });
});
