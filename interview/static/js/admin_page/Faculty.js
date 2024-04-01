function add_Major_manager(Major_manager,id_Major_manager) {
  var optionsDiv = document.getElementById("add_Major_manager");
  var facultyParagraph = optionsDiv.querySelector('p');
  var facultyIdField = document.getElementById("major_id");
  if (optionsDiv.style.display === "block") {
    optionsDiv.style.display = "none";
  } else {
    optionsDiv.style.display = "block";
    facultyParagraph.textContent = Major_manager;
    facultyIdField.value = id_Major_manager;
  }
}

  
  function add_Faculty() {
      var optionsDiv = document.getElementById("add_Faculty");
      if (optionsDiv.style.display === "block") {
        optionsDiv.style.display = "none";
      } else {
        optionsDiv.style.display = "block";
      }
    }

    function display_manager(majorId) {
      var managerDiv = document.getElementById('display_manager_' + majorId);
      if (managerDiv.style.display === 'none') {
          managerDiv.style.display = 'block';
      } else {
          managerDiv.style.display = 'none';
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
  
  
function display_popup_del(major_name,major_id){
  var optionsDiv = document.getElementById("display_popup_del");
  document.getElementById('major_name_tag').innerHTML = major_name;
  var deleteLink = document.querySelector('.bt_del a[href^="delete_Major"]');
  deleteLink.setAttribute('href', 'delete_Major/' + major_id);
  if (optionsDiv.style.display === "block") {
    optionsDiv.style.display = "none";
  } else {
    optionsDiv.style.display = "block";
  }
}

function display_popup_del_faculty(faculty_name,faculty_id){
  var optionsDiv = document.getElementById("display_popup_del_faculty");
  document.getElementById('faculty_name_tag').innerHTML = faculty_name;
  var deleteLink = document.querySelector('.bt_del_faculty a[href^="delete_Faculty"]');
  deleteLink.setAttribute('href', 'delete_Faculty/' + faculty_id);
  if (optionsDiv.style.display === "block") {
    optionsDiv.style.display = "none";
  } else {
    optionsDiv.style.display = "block";
  }
}