function add_TemporaryUser() {
    var optionsDiv = document.getElementById("add_TemporaryUser");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }
  function add_TemporaryUser_by_file() {
    var optionsDiv = document.getElementById("add_TemporaryUser_by_file");
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
  function edit_popup(user_id, first_name, last_name, faculty, major,citizen_id,birth_date,role) {
  var optionsDiv = document.getElementById("edit_popup");
  document.getElementById('user_id').value = user_id;
  document.getElementById('first_name').value = first_name;
  document.getElementById('last_name').value = last_name;
  document.getElementById('citizen_id').value = citizen_id;
  var birth_date_split =  birth_date.split(' ');
  var hbd_day =  birth_date_split[1].split(',')[0];
  var new_HBD;
  if (birth_date_split[0] == 'Jan.'){
    new_HBD = hbd_day+'/01/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Feb.'){
    new_HBD = hbd_day+'/02/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'March'){
    new_HBD = hbd_day+'/03/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'April'){
    new_HBD = hbd_day+'/04/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'May'){
    new_HBD = hbd_day+'/05/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'June'){
    new_HBD = hbd_day+'/06/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'July'){
    new_HBD = hbd_day+'/07/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Aug.'){
    new_HBD = hbd_day+'/08/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Sept.'){
    new_HBD = hbd_day+'/09/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Oct.'){
    new_HBD = hbd_day+'/10/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Nov.'){
    new_HBD = hbd_day+'/11/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Dec.'){
    new_HBD = hbd_day+'/12/'+birth_date_split[2];
    
  }
  document.getElementById('birth_date').value = new_HBD;
  
  //document.getElementById('birth_date').value = birth_date;
  var faculty_new = [];
  faculty_new.push(faculty.split(':'));
  var faculty_split = [];
  for (var i = 0; i < faculty_new[0].length; i++) {
      var a2 = faculty_new[0][i].split(">");
      a2[0] = a2[0].trim();
      faculty_split.push(a2[0]);
  }
  var major_new = [];
  major_new.push(major.split(':'));
  var major_split = [];
  for (var i = 0; i < major_new[0].length; i++) {
      var a2 = major_new[0][i].split(">");
      a2[0] = a2[0].trim();
      major_split.push(a2[0]);
  }
  var role_new = [];
  role_new.push(role.split(':'));
  var role_split = [];
  for (var i = 0; i < role_new[0].length; i++) {
      var a2 = role_new[0][i].split(">");
      a2[0] = a2[0].trim();
      role_split.push(a2[0]);
  }
  var checkbox1 = document.getElementById('checkbox1');
  var checkbox2 = document.getElementById('checkbox2');
  var checkbox3 = document.getElementById('checkbox3');
  var checkbox4 = document.getElementById('checkbox4');
  checkbox1.checked = false;
  checkbox2.checked = false;
  checkbox3.checked = false;
  checkbox4.checked = false;
  
  for (let i = 0 ; i < (role_split.length);i++){
    if (role_split[i] === 'Admin') {
      checkbox1.checked = true;
    }
    if (role_split[i] === 'Manager') {
      checkbox2.checked = true;
    }
    if (role_split[i] === 'Interviewer') {
      checkbox3.checked = true;
    }
    if (role_split[i] === 'Student') {
      checkbox4.checked = true;
    }
    
      
  }
  //document.getElementById('faculty').value = faculty_split.slice(1);
  //document.getElementById('major').value = major_split.slice(1);
  
  if (optionsDiv.style.display === "block") {
    optionsDiv.style.display = "none";
  } else {
    optionsDiv.style.display = "block";
  }
  }
  
  function display_popup(user_id, first_name, last_name, faculty, major,citizen_id,birth_date,role) {
  var optionsDiv = document.getElementById("display_popup");
  document.getElementById('user_id').value = user_id;
  document.getElementById('display_first_name').value = first_name;
  document.getElementById('display_last_name').value = last_name;
  document.getElementById('display_citizen_id').value = citizen_id;
  var birth_date_split =  birth_date.split(' ');
  var hbd_day =  birth_date_split[1].split(',')[0];
  var new_HBD;
  if (birth_date_split[0] == 'Jan.'){
    new_HBD = hbd_day+'/01/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Feb.'){
    new_HBD = hbd_day+'/02/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'March'){
    new_HBD = hbd_day+'/03/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'April'){
    new_HBD = hbd_day+'/04/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'May.'){
    new_HBD = hbd_day+'/05/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'June'){
    new_HBD = hbd_day+'/06/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'July'){
    new_HBD = hbd_day+'/07/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Aug.'){
    new_HBD = hbd_day+'/08/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Sept.'){
    new_HBD = hbd_day+'/09/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Oct.'){
    new_HBD = hbd_day+'/10/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Nov.'){
    new_HBD = hbd_day+'/11/'+birth_date_split[2];
    
  }
  if (birth_date_split[0] == 'Dec.'){
    new_HBD = hbd_day+'/12/'+birth_date_split[2];
    
  }
  document.getElementById('display_birth_date').value = new_HBD;
  var faculty_new = [];
  faculty_new.push(faculty.split(':'));
  var faculty_split = [];
  for (var i = 0; i < faculty_new[0].length; i++) {
      var a2 = faculty_new[0][i].split(">");
      a2[0] = a2[0].trim();
      faculty_split.push(a2[0]);
  }
  var major_new = [];
  major_new.push(major.split(':'));
  var major_split = [];
  for (var i = 0; i < major_new[0].length; i++) {
      var a2 = major_new[0][i].split(">");
      a2[0] = a2[0].trim();
      major_split.push(a2[0]);
  }
  var role_new = [];
  role_new.push(role.split(':'));
  var role_split = [];
  for (var i = 0; i < role_new[0].length; i++) {
      var a2 = role_new[0][i].split(">");
      a2[0] = a2[0].trim();
      role_split.push(a2[0]);
  }
  
  var checkbox1 = document.getElementById('checkbox5');
  var checkbox2 = document.getElementById('checkbox6');
  var checkbox3 = document.getElementById('checkbox7');
  var checkbox4 = document.getElementById('checkbox8');
  checkbox1.checked = false;
  checkbox2.checked = false;
  checkbox3.checked = false;
  checkbox4.checked = false;
  
  for (let i = 0 ; i < (role_split.length);i++){
    if (role_split[i] === 'Admin') {
      checkbox1.checked = true;
    }
    if (role_split[i] === 'Manager') {
      checkbox2.checked = true;
    }
    if (role_split[i] === 'Interviewer') {
      checkbox3.checked = true;
    }
    if (role_split[i] === 'Student') {
      checkbox4.checked = true;
    }
  }
  //document.getElementById('faculty').value = faculty_split.slice(1);
  //document.getElementById('major').value = major_split.slice(1);
  
  if (optionsDiv.style.display === "block") {
    optionsDiv.style.display = "none";
  } else {
    optionsDiv.style.display = "block";
  }
  }
  
  
  