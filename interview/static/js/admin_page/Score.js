function add_Score(pattern_id) {
  console.log(pattern_id);
    var optionsDiv = document.getElementById("add_ScoreTopic");
    document.getElementById('template_num').value = pattern_id;
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }

  function add_Pattern() {
    var optionsDiv = document.getElementById("add_ScorePattern");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }

  function edit_popup(topic_id, topic_name, max_score, detail) {
    console.log(topic_id);
    var optionsDiv = document.getElementById("edit_popup");
    document.getElementById('topic_id').value = topic_id;
    document.getElementById('topic_name_edit').value = topic_name;
    document.getElementById('max_score_edit').value = max_score;
    document.getElementById('score_detail_edit').value = detail;

    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
    }