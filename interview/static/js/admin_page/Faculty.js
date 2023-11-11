

  
  function add_Faculty() {
      var optionsDiv = document.getElementById("add_Faculty");
      if (optionsDiv.style.display === "block") {
        optionsDiv.style.display = "none";
      } else {
        optionsDiv.style.display = "block";
      }
    }
    function add_Major(facultyName,id_faculty) {
      var addMajorDiv = document.getElementById("add_Major");
      var facultyParagraph = addMajorDiv.querySelector('p');
      var facultyIdField = document.getElementById("facultyIdField");
      
      if (addMajorDiv.style.display === "block") {
        addMajorDiv.style.display = "none";
      } else {
        addMajorDiv.style.display = "block";
        facultyParagraph.textContent = facultyName;
        facultyIdField.value = id_faculty;
      }
    }
  


  
  
  