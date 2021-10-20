
function refresh(id){
    fetch("/get_images/"+id)
        .then(response => response.json())
        .then(data => add_photos(data));
}

var Fotos = [];
var aux = 0;

function add_photos(data) {
    Fotos = data.photos
    V_max = Fotos.length - 1;
}

function siguiente () {        
    if (aux == V_max){    
        aux = 0;    
    }
    else{
        aux = aux+1;
    }
    document.images.Diapositiva.src = Fotos[aux];
}

function anterior () {    
    if (aux == 0){    
        aux = V_max;    
    }
    else{
        aux = aux-1;
    }
    document.images.Diapositiva.src = Fotos[aux];
}