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
