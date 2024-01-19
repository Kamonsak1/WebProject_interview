function skip_confirm() {
    var optionsDiv = document.getElementById("skip_confirm");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
}

function next_confirm() {
    var optionsDiv = document.getElementById("next_confirm");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
}

function exit_confirm() {
  var optionsDiv = document.getElementById("exit_round");
  if (optionsDiv.style.display === "block") {
    optionsDiv.style.display = "none";
  } else {
    optionsDiv.style.display = "block";
  }
}
