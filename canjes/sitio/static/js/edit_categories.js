
function fill_sub_category(id){
  fetch("/article_categories/"+id)
    .then(response => response.json())
    .then(data => add_sub_categories(data));
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