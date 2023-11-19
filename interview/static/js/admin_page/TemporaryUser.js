function add_TemporaryUser() {
  var optionsDiv = document.getElementById("add_TemporaryUser");
  if (optionsDiv.style.display === "block") {
    optionsDiv.style.display = "none";
  } else {
    optionsDiv.style.display = "block";
  }
}

function updateMajorOptions() {
  var facultyId = $("#facultySelect").val();

  $.ajax({
      url: '/get_majors/',  // กำหนด URL ที่จะรับข้อมูลสาขา
      type: 'GET',
      data: {
          'faculty_id': facultyId
      },
      dataType: 'json',
      success: function (data) {
          var majorSelect = $("#majorSelect");
          majorSelect.empty();
          majorSelect.append('<option>สาขา</option>');
          
          for (var i = 0; i < data.length; i++) {
              majorSelect.append('<option value="' + data[i].id + '">' + data[i].major + '</option>');
          }
      }
  });
}
function edit_popup(user_id, first_name, last_name, faculty, major,citizen_id,birth_date) {
var optionsDiv = document.getElementById("edit_popup");
document.getElementById('user_id').value = user_id;
document.getElementById('first_name').value = first_name;
document.getElementById('last_name').value = last_name;
document.getElementById('citizen_id').value = citizen_id;
document.getElementById('birth_date').value = birth_date;
var a = [];
a.push(faculty.split(':'));
var faculty_split = [];
for (var i = 0; i < a[0].length; i++) {
    var a2 = a[0][i].split(">");
    a2[0] = a2[0].trim();
    faculty_split.push(a2[0]);
}
var aa = [];
aa.push(major.split(':'));
var major_split = [];
for (var i = 0; i < aa[0].length; i++) {
    var a2 = aa[0][i].split(">");
    a2[0] = a2[0].trim();
    major_split.push(a2[0]);
}

//document.getElementById('faculty').value = faculty_split.slice(1);
//document.getElementById('major').value = major_split.slice(1);

if (optionsDiv.style.display === "block") {
  optionsDiv.style.display = "none";
} else {
  optionsDiv.style.display = "block";
}
}



