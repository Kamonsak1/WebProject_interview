function add_Announcement() {
    var optionsDiv = document.getElementById("add_Announcement");
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
    }
  }

  function edit_Announcement() {
    var edit_An = document.getElementById("edit_Announcement");
    console.log('asd')
    if (edit_An.style.display === "block") {
      edit_An.style.display = "none";
    } else {
      edit_An.style.display = "block";
    }
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


      var displayText = 'Selected Rounds:<ul>';
      for (var i = 0; i < selectedRounds.length; i++) {
          displayText += '<li>' + selectedRounds[i].name + ' (ID: ' + selectedRounds[i].id + ')</li>';
      }
      displayText += '</ul>';

      document.getElementById('round').innerHTML = displayText;
      document.getElementById('selectedRoundsInput').value = Roundid
  }