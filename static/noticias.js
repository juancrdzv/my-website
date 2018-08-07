document.addEventListener("DOMContentLoaded", function(event) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/noticias', true);
  xhr.onload = function () {
    if (xhr.status === 200) {
    // File(s) uploaded.

      var data = JSON.parse(xhr.response);
      var content = document.querySelector('.content');

      for(var i=0,il = data.length; i<il; i++) {
        var div = document.createElement("div");
        var hr = document.createElement("hr");

        if(data[i].text.length === 0)
          continue;

        div.className="row";
        div.innerHTML = "<div class= col-sm-12 scrapp-division>"+
                            "<div><h4>"+data[i].title+"</h4></div>"+
                            "<a href="+data[i].url+">Noticia original</a>"+
                            "<div>"+data[i].text+"</div>"+
                        "</div>";

        content.appendChild(div)
        content.appendChild(hr);

      }

    } else {
      document.querySelector('.content').innerHTML = '<h1>Un error ha ocurrido</h1>';
    }
  };
  xhr.send();
});
