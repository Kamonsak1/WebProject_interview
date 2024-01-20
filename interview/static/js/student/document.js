  function upload(docs, round_id) {
    document.getElementById('round_id').value = round_id;
    var doc = [];
    doc.push(docs.split(','));
    var select = document.getElementById("doc_name");
    select.innerHTML = "";
    doc[0].forEach(function(item) {
      var option = document.createElement("option");
      option.value = item;
      option.text = item;
      select.appendChild(option);
    });
    var optionsDiv = document.getElementById("upload_popup");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }