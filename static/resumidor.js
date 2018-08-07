document.addEventListener("DOMContentLoaded", function(event) {
  var form = document.getElementById('file-form');
  var fileSelect = document.getElementById('subir-archivo');
  var uploadButton = document.getElementById('upload-button');
  form.onsubmit = function(event) {
    event.preventDefault();
    var files = fileSelect.files;
    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      // Add the file to the request.
      formData.append('file', file, file.name);
    }
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/resumidor', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
      // File(s) uploaded.
        alert("uploaded")

        var data = JSON.parse(xhr.response);

        data["no_summarized"] = data["no_summarized"].replace(/(?:\r\n|\r|\n)/g, '<br />');
				data["summarized"] = data["summarized"].replace(/(?:\r\n|\r|\n)/g, '<br /><br />');

        document.getElementById("no-resumido").innerHTML = data["no_summarized"];
        document.getElementById("resumido").innerHTML = data["summarized"];
      } else {
        alert('An error occurred!');
      }
    };
    xhr.send(formData);
    // The rest of the code will go here...
  }
});
