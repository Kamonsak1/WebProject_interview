  function upload(round_id) {
    var optionsDiv = document.getElementById(`upload_popup_${round_id}`);
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }