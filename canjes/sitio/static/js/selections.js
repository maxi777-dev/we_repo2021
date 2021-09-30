function select_item(id, value){
    if ($("#" + id).hasClass("list-group-item list-group-item-action active")){
        $("#" + id).removeClass("active");
        $("#" + id).css('color', 'grey');
    }else{
        $("#" + id).addClass("list-group-item list-group-item-action active");
        $("#" + id).css('color', 'white');
    }
}