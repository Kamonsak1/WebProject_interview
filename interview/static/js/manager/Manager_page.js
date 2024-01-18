function read_Announcement(title, content) {
    var optionsDiv = document.getElementById("readAnnouncement");
    document.getElementById('topic').innerHTML = title;
    var formattedContent = content.replace(/\n/g, '<br>');
    document.getElementById('content').innerHTML = formattedContent;
  
    if (optionsDiv.style.display === "block") {
        optionsDiv.style.display = "none";
    } else {
        optionsDiv.style.display = "block";
    }
  }
  
  
  function read_schedule(title, content) {
    var optionsDiv = document.getElementById("readschedule");
    document.getElementById('schedule_topic').innerHTML = title;
    var formattedContent = content.replace(/\n/g, '<br>');
    document.getElementById('schedule_content').innerHTML = formattedContent;
  
    if (optionsDiv.style.display === "block") {
        optionsDiv.style.display = "none";
    } else {
        optionsDiv.style.display = "block";
    }
  }
  


  function close_Announcement() {
    var optionsDiv = document.getElementById("readAnnouncement");
    if (optionsDiv.style.display === "block") {
        optionsDiv.style.display = "none";
    } else {
        optionsDiv.style.display = "block";
    }
  }
  
  
  function close_schedule() {
    var optionsDiv = document.getElementById("readschedule");
    if (optionsDiv.style.display === "block") {
        optionsDiv.style.display = "none";
    } else {
        optionsDiv.style.display = "block";
    }
  }
  