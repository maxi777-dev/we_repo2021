$(document).ready(function() {
  fetch('/article_categories/0')
    .then(response => response.json())
    .then(data => add_categories(data));
})

function fill_sub_category(id){
  fetch("/article_categories/"+id)
    .then(response => response.json())
    .then(data => add_sub_categories(data));
}

function add_categories(data) {
  var categorias = '';
  var i = 0;
  $.each(data, function(val, text) {    
    if(i==0){
      categorias += `<option id="item-dropdown`+ text.id +`" value="` + text.id + `" selected>` + text.title + `</option>`;
      fill_sub_category(text.id);
    }else{
      categorias += `<option id="item-dropdown`+ text.id +`" value="` + text.id + `">` + text.title + `</option>`;
    }
    i++;
  });
  $("#dropdownMenuLink1").html(categorias);
}


function add_sub_categories(data) {
  var categorias = '';
  var i = 0;
  $.each(data, function(val, text) {    
    if(i==0){
      categorias += `<option id="item-dropdown2" value="` + text.id + `" selected>` + text.title + `</option>`;
    }else{
      categorias += `<option id="item-dropdown2" value="` + text.id + `">` + text.title + `</option>`;
    }
    i++;
  });
  $("#dropdownMenuLink2").html(categorias);
}