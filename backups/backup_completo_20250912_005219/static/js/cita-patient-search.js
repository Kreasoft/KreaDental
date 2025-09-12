jQuery(document).ready(function($) {
    // Destruir instancia previa si existe
    if ($('#id_paciente').data('select2')) {
        $('#id_paciente').select2('destroy');
    }

    // Inicializar Select2
    $('#id_paciente').select2({
        language: 'es',
        dropdownParent: $('#citaModal'),
        placeholder: 'Buscar paciente...',
        allowClear: true,
        minimumInputLength: 2,
        readonly: false,
        disabled: false,
        searchInputPlaceholder: 'Buscar paciente...',
        ajax: {
            url: '/pacientes/buscar/',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    q: params.term,
                    page: params.page || 1
                };
            },
            processResults: function(data) {
                return {
                    results: data.results.map(function(patient) {
                        return {
                            id: patient.id,
                            text: patient.nombre + ' ' + patient.apellidos + 
                                  ' - Doc: ' + patient.documento
                        };
                    })
                };
            },
            cache: true
        }
    });
});
