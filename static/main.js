document.addEventListener("DOMContentLoaded", function(event) {
    document.querySelector('.noticias').addEventListener('click', function(event) {
      window.location.href = '/noticias';
    });

    document.querySelector('.resumidor').addEventListener('click', function(event) {
      window.location.href = '/resumidor';
    });

    document.querySelector('.clustering').addEventListener('click', function(event) {
      window.location.href = '/clustering';
    });
});
