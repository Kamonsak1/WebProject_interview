function changepassword(user_id) {
    var optionsDiv = document.getElementById("changepassword");
    document.getElementById('user_id').value = user_id;
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }