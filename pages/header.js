document.addEventListener("DOMContentLoaded", function() {
  const headerContainer = document.getElementById("header-container");
  const headerUrl = "header.html";
  fetch(headerUrl)
    .then(response => response.text())
    .then(data => {
      headerContainer.innerHTML = data;
    });
});
