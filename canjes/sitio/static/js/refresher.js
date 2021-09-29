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
        `<div class="col-md-6 col-lg-4">
            <div class="card text-center card-product">
                <div class="card-product__img">
                    <img class="card-img" src="` + text.image + `" alt="` + text.link + `">
                </div>
                <div class="card-body">
                    <p>` + text.category + `</p>
                    <h4 class="card-product__title"><a href="` + text.link + `">` + text.title + `</a></h4>
                    <p>` + text.user + `</p>
                </div>
            </div>
        </div>`;
    });
    $("#articles").html(articles);
  }