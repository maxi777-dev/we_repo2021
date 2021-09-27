$(document).ready(function() {
  fetch_info(true, '/article_categories/0');
})

document.getElementById("item-dropdown1").addEventListener("click", fetch_info(false, ));

function fetch_info(bool, url){
  if (bool){
    fetch(url)
    .then(response => response.json())
    .then(data => add_categories1(data));
  }else{
    fetch(url)
    .then(response => response.json())
    .then(data => add_sub_categories(data));
  }
}

function add_categories1(data) {
  $.each(data, function(val, text) {
    $(dropdownMenuLink1).append(
        $('<option id="item-dropdown1" class="dropdown-item" onclick="return fetch_info(false, /article_categories/'+ text.id +')"></option>').val(val).html(text.title)
    );
  });
}

function add_sub_categories(data) {
  $.each(data, function(val, text) {
    $(dropdownMenuLink2).append(
        $('<option class="dropdown-item"></option>').val(val).html(text.title)
    );
  });
}