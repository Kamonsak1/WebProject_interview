function add_Announcement() {
    var optionsDiv = document.getElementById("add_Announcement");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }
  var edit_selectedRounds = [];
  var edit_Roundid = [];
  function edit_Announcement(id,title,post_date,content,role,round) {
    document.getElementById('edit_topic').value = title;
    document.getElementById('round_id').value = id;
    document.getElementById('deleteLink_Announcement').href = 'delete_Announcement/' + id;
    document.getElementById('edit_content').value = content;
    document.getElementById('edit_selectedRoundsInput').value = round;
    var role_new = role.split(',').map(function(item) {
      return item.trim();
    });
    var checkbox1 = document.getElementById('checkbox1');
    var checkbox2 = document.getElementById('checkbox2');
    var checkbox3 = document.getElementById('checkbox3');
    var checkbox4 = document.getElementById('checkbox4');
    checkbox1.checked = false;
    checkbox2.checked = false;
    checkbox3.checked = false;
    checkbox4.checked = false;
    
    for (let i = 0; i < role_new.length; i++) {
      if (role_new[i] === 'Admin') {
        checkbox1.checked = true;
      }
      if (role_new[i] === 'Manager') {
        checkbox2.checked = true;
      }
      if (role_new[i] === 'Interviewer') {
        checkbox3.checked = true;
      }
      if (role_new[i] === 'Student') {
        checkbox4.checked = true;
      }
    }
    

    
    if (post_date) {
      var birth_date_split =  post_date.split(' ');
      if (birth_date_split.length > 1) {
        var hbd_day =  birth_date_split[1].split(',')[0];
        var new_year =  parseInt(birth_date_split[2])+543;
        var new_HBD;
      } 
    }
    
    if (birth_date_split[0] == 'Jan.') {
      new_HBD = hbd_day + '/01/' + new_year
    } else if (birth_date_split[0] == 'Feb.') {
      new_HBD = hbd_day + '/02/' + new_year
    } else if (birth_date_split[0] == 'March') {
      new_HBD = hbd_day + '/03/' + new_year
    } else if (birth_date_split[0] == 'April') {
      new_HBD = hbd_day + '/04/' + new_year
    } else if (birth_date_split[0] == 'May.') {
      new_HBD = hbd_day + '/05/' + new_year
    } else if (birth_date_split[0] == 'June') {
      new_HBD = hbd_day + '/06/' + new_year
    } else if (birth_date_split[0] == 'July') {
      new_HBD = hbd_day + '/07/' + new_year
    } else if (birth_date_split[0] == 'Aug.') {
      new_HBD = hbd_day + '/08/' + new_year
    } else if (birth_date_split[0] == 'Sept.') {
      new_HBD = hbd_day + '/09/' + new_year
    } else if (birth_date_split[0] == 'Oct.') {
      new_HBD = hbd_day + '/10/' + new_year
    } else if (birth_date_split[0] == 'Nov.') {
      new_HBD = hbd_day + '/11/' + new_year
    } else if (birth_date_split[0] == 'Dec.') {
      new_HBD = hbd_day + '/12/' + new_year
    }
    
    document.getElementById('edit_post_date').value = new_HBD || " ";
    edit_selectedRounds = [];
    var round_new = round.split(',').map(function(item) {
      return item.trim();
    });
    round_new.forEach(function(item) {
      if (item !== "") { 
        edit_selectedRounds.push(item);
      }
    });
    
    document.getElementById('edit_round').innerHTML = edit_selectedRounds.map(function(item) {
      return '<span style="color: black; font-weight: bold;">' + item + '</span> <button onclick="deleteItem(\'' + item + '\')" style="font-size: 20px; color: red; background: none; border: none;">-</button>';
  }).join('<br>');
  

    var edit_An = document.getElementById("edit_Announcement");
    if (edit_An.style.display === "block") {
      edit_An.style.display = "none";
    } else {
      edit_An.style.display = "block";
    }
  }

  function editRoundInfo() {
    var select = document.getElementById('edit_selectRound');
    var text = select.options[select.selectedIndex].value;
    if (text !== "" && !edit_selectedRounds.includes(text)) {
      edit_selectedRounds.push(text);
  }
  document.getElementById('edit_round').innerHTML = edit_selectedRounds.map(function(item) {
    return '<span style="color: black; font-weight: bold;">' + item + '</span> <button onclick="deleteItem(\'' + item + '\')" style="font-size: 20px; color: red; background: none; border: none;">-</button>';
}).join('<br>');
    document.getElementById('edit_selectedRoundsInput').value = edit_selectedRounds
  
}

function deleteItem(itemName) {
  var index = edit_selectedRounds.indexOf(itemName);
  if (index > -1) {
    edit_selectedRounds.splice(index, 1);
  }
  document.getElementById('edit_round').innerHTML = edit_selectedRounds.map(function(item) {
    return '<span style="color: black; font-weight: bold;">' + item + '</span> <button onclick="deleteItem(\'' + item + '\')" style="font-size: 20px; color: red; background: none; border: none;">-</button>';
}).join('<br>');
  document.getElementById('edit_selectedRoundsInput').value = edit_selectedRounds

}



  var selectedRounds = [];
  var Roundid = [];
  function updateRoundInfo() {
      var select = document.getElementById('selectRound');
      var value = select.options[select.selectedIndex].value;
      var text = select.options[select.selectedIndex].text;


      if (value && !selectedRounds.some(round => round.id === value)) {
          selectedRounds.push({id: value, name: text}); 
          Roundid.push(value);
      }

      var displayText = '<ul>';
      for (var i = 0; i < selectedRounds.length; i++) {
          displayText += '<li style="color: black; font-weight: bold;">';
          displayText += selectedRounds[i].name;
          displayText += ' <button style="font-size: 20px; color: red; background: none; border: none;"  onclick="deleteRound(' + i + ')">-</button></li>';
      }
      displayText += '</ul>';
      
      document.getElementById('round').innerHTML = displayText;
      
      document.getElementById('selectedRoundsInput').value = Roundid
  }
  function deleteRound(index) {
    // Remove the round from the array
    selectedRounds.splice(index, 1);

    // Update the display
    var updatedDisplayText = '<ul>';
    for (var i = 0; i < selectedRounds.length; i++) {
        updatedDisplayText += '<li style="color: black; font-weight: bold;">';
        updatedDisplayText += selectedRounds[i].name;
        updatedDisplayText += ' <button style="font-size: 20px; color: red; background: none; border: none;"  onclick="deleteRound(' + i + ')">-</button></li>';
    }
    updatedDisplayText += '</ul>';
    document.getElementById('round').innerHTML = updatedDisplayText;
}


function add_Schedule() {
  var add_Schedule = document.getElementById("add_Schedule");
  if (add_Schedule.style.display === "block") {
    add_Schedule.style.display = "none";
  } else {
    add_Schedule.style.display = "block";
  }
}

var edit_selectedRounds_Schedule = [];
var edit_Roundid_Schedule = [];
function edit_Schedule(id,schedule_name,end_date,schedule_content,role,round) {
  document.getElementById('Schedule_id').value = id;
  document.getElementById('deleteLink_Schedule').href = 'delete_Schedule/' + id;
  document.getElementById('schedule_name').value = schedule_name;
  document.getElementById('schedule_content').value = schedule_content;
  document.getElementById('edit_selectedRoundsInput_schedule').value = round;

  document.getElementById('schedule_name').value = schedule_name;
  var edit_Schedule = document.getElementById("edit_Schedule");
  var role_new = role.split(',').map(function(item) {
    return item.trim();
  });
  var checkbox1 = document.getElementById('checkbox_1');
  var checkbox2 = document.getElementById('checkbox_2');
  var checkbox3 = document.getElementById('checkbox_3');
  var checkbox4 = document.getElementById('checkbox_4');
  checkbox1.checked = false;
  checkbox2.checked = false;
  checkbox3.checked = false;
  checkbox4.checked = false;
  
  for (let i = 0; i < role_new.length; i++) {
    if (role_new[i] === 'Admin') {
      checkbox1.checked = true;
    }
    if (role_new[i] === 'Manager') {
      checkbox2.checked = true;
    }
    if (role_new[i] === 'Interviewer') {
      checkbox3.checked = true;
    }
    if (role_new[i] === 'Student') {
      checkbox4.checked = true;
    }
  }

  if (end_date) {
    var birth_date_split =  end_date.split(' ');
    if (birth_date_split.length > 1) {
      var hbd_day =  birth_date_split[1].split(',')[0];
      var new_year =  parseInt(birth_date_split[2])+543;
      var new_HBD;
      var old_date;
    } 
  }
  
  if (birth_date_split[0] == 'Jan.') {
    new_HBD = hbd_day + '/01/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'Feb.') {
    new_HBD = hbd_day + '/02/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'March') {
    new_HBD = hbd_day + '/03/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'April') {
    new_HBD = hbd_day + '/04/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'May.') {
    new_HBD = hbd_day + '/05/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'June') {
    new_HBD = hbd_day + '/06/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'July') {
    new_HBD = hbd_day + '/07/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'Aug.') {
    new_HBD = hbd_day + '/08/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'Sept.') {
    new_HBD = hbd_day + '/09/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'Oct.') {
    new_HBD = hbd_day + '/10/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'Nov.') {
    new_HBD = hbd_day + '/11/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  } else if (birth_date_split[0] == 'Dec.') {
    new_HBD = hbd_day + '/12/' + new_year
    old_date = hbd_day + '/01/' + birth_date_split[2]
  }
  
  document.getElementById('selectedDate_edit').innerHTML = "วันที่เลือก:" +new_HBD;
  document.getElementById('inputselectedDate_edit').value = old_date;

  edit_selectedRounds_Schedule = [];
  var round_new = round.split(',').map(function(item) {
    return item.trim();
  });
  round_new.forEach(function(item) {
    if (item !== "") { 
      edit_selectedRounds_Schedule.push(item);
    }
  });
  document.getElementById('edit_round_schedule').innerHTML = edit_selectedRounds_Schedule.map(function(item) {
    return '<span style="color: black; font-weight: bold;">' + item + '</span> <button onclick="delete_Round_Schedule(\'' + item + '\')" style="font-size: 20px; color: red; background: none; border: none;">-</button>';
}).join('<br>');


  if (edit_Schedule.style.display === "block") {
    edit_Schedule.style.display = "none";
  } else {
    edit_Schedule.style.display = "block";
  }

}
  function edit_ScheduleRoundInfo() {
    var select = document.getElementById('edit_selectRound_schedule');
    var text = select.options[select.selectedIndex].value;
    if (text !== "" && !edit_selectedRounds_Schedule.includes(text)) {
      edit_selectedRounds_Schedule.push(text);
  }
  document.getElementById('edit_round_schedule').innerHTML = edit_selectedRounds_Schedule.map(function(item) {
    return '<span style="color: black; font-weight: bold;">' + item + '</span> <button onclick="delete_Round_Schedule(\'' + item + '\')" style="font-size: 20px; color: red; background: none; border: none;">-</button>';
  }).join('<br>');
    document.getElementById('edit_selectedRoundsInput_schedule').value = edit_selectedRounds_Schedule

  }
function delete_Round_Schedule(itemName) {
  var index = edit_selectedRounds_Schedule.indexOf(itemName);
  if (index > -1) {
    edit_selectedRounds_Schedule.splice(index, 1);
  }
  document.getElementById('edit_round_schedule').innerHTML = edit_selectedRounds_Schedule.map(function(item) {
    return '<span style="color: black; font-weight: bold;">' + item + '</span> <button onclick="delete_Round_Schedule(\'' + item + '\')" style="font-size: 20px; color: red; background: none; border: none;">-</button>';
}).join('<br>');
  document.getElementById('edit_selectedRoundsInput_schedule').value = edit_selectedRounds_Schedule
}

var selectedRounds_Schedule = [];
var Roundid_Schedule = [];
function update_ScheduleInfo() {
    var select = document.getElementById('selectRound_Schedule_add');
    var value = select.options[select.selectedIndex].value;
    var text = select.options[select.selectedIndex].text;
    

    if (value && !selectedRounds_Schedule.some(round => round.id === value)) {
      selectedRounds_Schedule.push({id: value, name: text}); 
      Roundid_Schedule.push(value);
    }

    var displayText = '<ul>';
    for (var i = 0; i < selectedRounds_Schedule.length; i++) {
        displayText += '<li style="color: black; font-weight: bold;">';
        displayText += selectedRounds_Schedule[i].name;
        displayText += ' <button style="font-size: 20px; color: red; background: none; border: none;"  onclick="delete_Schedule(' + i + ')">-</button></li>';
    }
    displayText += '</ul>';
    
    document.getElementById('round_Schedule').innerHTML = displayText;
    document.getElementById('selectedRoundsInput_Schedule').value = Roundid_Schedule
}
function delete_Schedule(index) {
  selectedRounds_Schedule.splice(index, 1);
  var updatedDisplayText = '<ul>';
  for (var i = 0; i < selectedRounds_Schedule.length; i++) {
      updatedDisplayText += '<li style="color: black; font-weight: bold;">';
      updatedDisplayText += selectedRounds_Schedule[i].name;
      updatedDisplayText += ' <button style="font-size: 20px; color: red; background: none; border: none;"  onclick="delete_Schedule(' + i + ')">-</button></li>';
  }
  updatedDisplayText += '</ul>';
  document.getElementById('round_Schedule').innerHTML = updatedDisplayText;
}



function select_calendar() {
  var add_Schedule = document.getElementById("select_calendar");
  if (add_Schedule.style.display === "block") {
    add_Schedule.style.display = "none";
  } else {
    add_Schedule.style.display = "block";
  }
}


var previousSelectedTd; 
function createYearOptions() {
    var yearSelect = document.getElementById('year');
    var currentYear = new Date().getFullYear();
    for (var i = currentYear + 2; i >= currentYear - 2; i--) {
        var option = document.createElement('option');
        option.value = i; 
        option.textContent = (i + 543).toString(); 
        if (i === currentYear) {
            option.selected = true; 
        }
        yearSelect.appendChild(option);
    }
}


function createMonthOptions() {
    var months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'];
    var monthSelect = document.getElementById('month');
    months.forEach(function(month, index) {
        var option = document.createElement('option');
        option.value = index + 1;
        option.textContent = month;
        monthSelect.appendChild(option);
    });
}

function selectDate(td, day) {
    var year = parseInt(document.getElementById('year').value);
    var month = document.getElementById('month').value;
    var formatyear =  year + 543
    var formattedDate = ('0' + day).slice(-2) + '/' + ('0' + month).slice(-2) + '/' + formatyear.toString();
    var inputformattedDate = ('0' + day).slice(-2) + '/' + ('0' + month).slice(-2) + '/' + year.toString();
    document.getElementById('selectedDate').textContent = 'วันที่เลือก: ' + formattedDate;
    document.getElementById('selectedDate_edit').innerHTML = 'วันที่เลือก: ' + formattedDate;
    document.getElementById('inputselectedDate_edit').value = inputformattedDate;
    document.getElementById('inputselectedDate').value = inputformattedDate;

    if (previousSelectedTd) {
        previousSelectedTd.classList.remove('selected');
    }
    td.classList.add('selected');
    previousSelectedTd = td;
    document.getElementById('select_calendar').style.display = 'none';
}

function getFirstDayOfMonth(year, month) {
    return new Date(year, month - 1, 1).getDay();
}

function updateCalendar() {
    var year = parseInt(document.getElementById('year').value);
    var month = parseInt(document.getElementById('month').value);
    var daysInMonth = new Date(year, month, 0).getDate();
    var firstDay = getFirstDayOfMonth(year, month);

    var calendarHtml = '<table><thead><tr>';
    var daysOfWeek = ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส'];
    for (var i = 0; i < 7; i++) {
        calendarHtml += '<th>' + daysOfWeek[i] + '</th>';
    }
    calendarHtml += '</tr></thead><tbody>';

    var day = 1;
    var cellCount = 0;
    for (var i = 0; i < 6; i++) {
        calendarHtml += '<tr>';
        for (var j = 0; j < 7; j++, cellCount++) {
            if (cellCount >= firstDay && day <= daysInMonth) {
                calendarHtml += `<td onclick="selectDate(this, ${day})">${day}</td>`;
                day++;
            } else {
                calendarHtml += '<td></td>';
            }
        }
        calendarHtml += '</tr>';
        if (day > daysInMonth) {
            break;
        }
    }
    calendarHtml += '</tbody></table>';

    document.getElementById('calendar').innerHTML = calendarHtml;
}