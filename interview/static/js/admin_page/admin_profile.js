function changepassword(user_id) {
    var optionsDiv = document.getElementById("changepassword");
    document.getElementById('user_id').value = user_id;
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }

  function changename(user_id) {
    var edit_name = document.getElementById("edit_name");
    var show_name = document.getElementById("show_name");
    document.getElementById('user_id').value = user_id;
  
    if (edit_name.style.display === "block") {
      edit_name.style.display = "none";
      show_name.style.display = "block";
    } else {
      edit_name.style.display = "block";
      show_name.style.display = "none";
    }
  }

  function changeemail(user_id) {
    var edit_email = document.getElementById("edit_email");
    var show_email = document.getElementById("show_email");
    document.getElementById('user_id').value = user_id;
  
    if (edit_email.style.display === "block") {
      edit_email.style.display = "none";
      show_email.style.display = "block";
    } else {
      edit_email.style.display = "block";
      show_email.style.display = "none";
    }
  }

  
  function changecitizen_id(user_id) {
    var edit_citizen_id = document.getElementById("edit_citizen_id");
    var show_citizen_id = document.getElementById("show_citizen_id");
    document.getElementById('user_id').value = user_id;
  
    if (edit_citizen_id.style.display === "block") {
      edit_citizen_id.style.display = "none";
      show_citizen_id.style.display = "block";
    } else {
      edit_citizen_id.style.display = "block";
      show_citizen_id.style.display = "none";
    }
  }

  function changephone_number(user_id) {
    var edit_phone_number = document.getElementById("edit_phone_number");
    var show_phone_number = document.getElementById("show_phone_number");
    document.getElementById('user_id').value = user_id;
  
    if (edit_phone_number.style.display === "block") {
      edit_phone_number.style.display = "none";
      show_phone_number.style.display = "block";
    } else {
      edit_phone_number.style.display = "block";
      show_phone_number.style.display = "none";
    }
  }

  function changeaddress(user_id) {
    var edit_address = document.getElementById("edit_address");
    var show_address = document.getElementById("show_address");
    document.getElementById('user_id').value = user_id;
  
    if (edit_address.style.display === "block") {
      edit_address.style.display = "none";
      show_address.style.display = "block";
    } else {
      edit_address.style.display = "block";
      show_address.style.display = "none";
    }
  }
  


function checkemail(){
    var optionsDiv = document.getElementById("check_hide");
    var meail_done = document.getElementById("meail_done");
    meail_done.readOnly = true;
    meail_done.style.backgroundColor = "#f0f0f0";
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }



function changehbd(user_id) {
  var edit_hbd = document.getElementById("edit_hbd");
  var show_hbd = document.getElementById("show_hbd");
  document.getElementById('user_id').value = user_id;

  if (edit_hbd.style.display === "block") {
    edit_hbd.style.display = "none";
    show_hbd.style.display = "block";
  } else {
    edit_hbd.style.display = "block";
    show_hbd.style.display = "none";
  }
}