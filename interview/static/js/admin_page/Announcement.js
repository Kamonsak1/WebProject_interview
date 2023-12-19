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
    document.getElementById('deleteLink').href = 'delete_Announcement/' + id;
    document.getElementById('edit_content').value = content;
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
  
    

    console.log(round_new)

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