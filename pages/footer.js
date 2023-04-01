document.addEventListener("DOMContentLoaded", function() {
  const footerContainer = document.getElementById("footer-container");
  const footerUrl = "footer.html";
  fetch(footerUrl)
    .then(response => response.text())
    .then(data => {
      footerContainer.innerHTML = data;
    });
});