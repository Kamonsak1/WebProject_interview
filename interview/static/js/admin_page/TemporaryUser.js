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

  
