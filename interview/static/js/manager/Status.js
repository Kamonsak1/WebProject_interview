function kick_round(interviewer_id) {
    var optionsDiv = document.getElementById("exit_round");
    document.getElementById('interviewer_id').value = interviewer_id;

    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }
