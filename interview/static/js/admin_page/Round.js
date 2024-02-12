function add_Round() {
    var optionsDiv = document.getElementById("add_RoundForm");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }

  function doc(id) {
    var optionsDiv = document.getElementById(`add_doc_${id}`);
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }

  function edit_popup(id, name, year, major, manager, time) {
    var optionsDiv = document.getElementById("edit_popup");
    console.log(manager)
    document.getElementById('round_id').value = id;
    document.getElementById('round_name_e').value = name;
    document.getElementById('academic_year_e').value = year;
    document.getElementById('majorSelect_e').value = major;
    document.getElementById('manager_name_e').value = manager;
    document.getElementById('interview_time_e').value = time;

    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
    }