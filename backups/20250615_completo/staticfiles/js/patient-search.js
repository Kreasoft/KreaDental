$(document).ready(function() {
    // Inicializar Select2 en el select de pacientes
    $('#id_paciente').select2({
        theme: 'bootstrap-5',
        language: 'es',
        placeholder: 'Buscar paciente...',
        allowClear: true,
        minimumInputLength: 2,
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
