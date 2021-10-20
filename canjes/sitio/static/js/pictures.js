// Inicio de la configuración de diapositivas.

	// Declaración de variables.
    var Fotos; // Lugar donde se almacenara la ruta de la imagen.
    var V_max; // Longitud máxima del vector "Fotos".
    var aux;   // Auxiliar para configuración.
    var aux_2; // Auxiliar para programación.

// Inicio de variables.
    Fotos = new Array(); // Crea el vector para las fotos.
    aux_2 = 0; // Inicia la variable auxiliar de programación con valor 0.

    function refresh(id){
        console.log(id)
        fetch("/get_images/"+id)
            .then(response => response.json())
            .then(data => add_photos(data));
    }

    function add_photos(data) {
        $.each(data, function(val, text) {
            Fotos.push(text)
        });
      }

// Rutas de imagenes.
   
    /* Para añadir nuevas imagenes simplemente adicionas "Fotos[] = "ruta imagen" */

    V_max = Fotos.length; // Obtiene la longitud del vector.
    V_max = V_max-1; // Diminuye uno su valor dado que V_max coge un valor a más.

// Fin de la configuración de diapositivas.

// Inicio de la programación de diapositivas.

// Pasar a la siguiente imagen.
    function siguiente () {
        
        if (aux_2 == V_max){
        
            aux_2 = 0;
        
        }

        else{

            aux_2 = aux_2+1;

        }

        document.images.Diapositiva.src = Fotos[aux_2];
    }

// Pasar a la siguiente imagen.
    function anterior () {
        
        if (aux_2 == 0){
        
            aux_2 = V_max;
        
        }

        else{

            aux_2 = aux_2-1;

        }

        document.images.Diapositiva.src = Fotos[aux_2];
    }

// Fin de la programación de diapositivas.