function refresh(id){
    console.log(id)
    fetch("/get_articles_by_category/"+id)
        .then(response => response.json())
        .then(data => add_articles(data));
}

function add_articles(data) {
    var articles = '';
    $.each(data, function(val, text) {
        articles +=
        `<div class="wrapper">                    
            <a href="` + text.link + `">
                <img src="` + text.image + `">
                <div class="content">
                    <p>` + text.category + `</p>
                    <h3>` + text.title + `</h3>
                    <p class="p1">` + text.user + `</p>
                </div>
            </a>                  
        </div>`;
    });
    $("#articles").html(articles);
  }