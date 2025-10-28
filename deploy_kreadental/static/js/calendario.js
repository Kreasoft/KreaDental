document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: function(info, successCallback, failureCallback) {
            var profesionalId = document.getElementById('filtro_profesional').value;
            var url = "/citas/api/citas/";
            if (profesionalId) {
                url += '?profesional=' + profesionalId + '&estado=true';
            }
            fetch(url)
                .then(response => response.json())
                .then(data => successCallback(data))
                .catch(error => failureCallback(error));
        },
        eventClick: function(info) {
            window.location.href = "/citas/editar/" + info.event.id + "/";
        }
    });
    calendar.render();

    // Manejar cambios en el filtro de profesionales
    document.getElementById('filtro_profesional').addEventListener('change', function() {
        calendar.refetchEvents();
    });
}); 