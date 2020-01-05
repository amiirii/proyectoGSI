$(document).ready(function() {
    // Ocultar los formularios al inicio
    $("#form_edificio, #form_vehiculo").hide();

    // Ignorar acción por defecto de los botones
    $("#form_edificio, #form_vehiculo").submit(function(e){
        return false;
    });

    // Mostrar el formulario correspondiente a cada botón
    $("#mostrar_form_edificio").click(function() {
        $("#form_edificio").fadeIn();
        $("#form_vehiculo").hide();
    });
    $("#mostrar_form_vehiculo").click(function() {
        $("#form_vehiculo").fadeIn();
        $("#form_edificio").hide();	
    });

    // Enviar los datos del formulario
    $("#form_edificio input[type=submit]").click(function() {
        var res = {};
        $("#form_edificio input, #form_edificio select, #form_edificio textarea").each(function(i, obj) {
            res[obj.name] = $(obj).val();
        });
        $.post("/add/", res).done(function(data) {
            $("#form_edificio .message").text(data);
            $("#form_edificio .message").show();
            $("#form_edificio")[0].reset();

            setTimeout(function() {
                $("#form_edificio .message").fadeOut();
            }, 3000);
        });
    });

    $("#form_vehiculo input[type=submit]").click(function() {
        var res = {};
        $("#form_vehiculo input, #form_vehiculo select, #form_vehiculo textarea").each(function(i, obj) {
            res[obj.name] = $(obj).val();
        });
        $.post("/add/", res).done(function(data) {
            $("#form_vehiculo .message").text(data);
            $("#form_vehiculo .message").show();
            $("#form_vehiculo")[0].reset();

            setTimeout(function() {
                $("#form_vehiculo .message").fadeOut();
            }, 3000);
        });
    });
});