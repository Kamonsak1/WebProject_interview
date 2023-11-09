
function toggleOptions(optionsId) {
    var optionsDiv = document.getElementById(optionsId);
    if (optionsDiv.style.display === "block") {
      optionsDiv.style.display = "none";
    } else {
      optionsDiv.style.display = "block";
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
  
  document.addEventListener("DOMContentLoaded", function() {
      document.getElementById('addLink').addEventListener('click', function(event) {
          event.preventDefault(); // ยกเลิกการทำงานปกติของลิงก์
  
          // กำหนดความกว้างและความสูงของหน้าต่าง pop-up
          var popupWidth = 800;
          var popupHeight = 800;
  
          // คำนวณตำแหน่งกึ่งกลางของหน้าจอ
          var left = (screen.width - popupWidth) / 2;
          var top = (screen.height - popupHeight) / 2;
  
          // กำหนดคุณสมบัติของหน้าต่าง pop-up
          var popupOptions = 'width=' + popupWidth + ',height=' + popupHeight + ',left=' + left + ',top=' + top;
  
          // เปิดหน้าต่าง pop-up โดยใช้ URL ที่คุณต้องการแสดง
          window.open('form_interview', 'เพิ่มรายละเอียดรอบสัมภาษณ์', popupOptions);
      });
  });
  
  document.addEventListener("DOMContentLoaded", function () {
      // คำนวณปีปัจจุบัน
      var currentYear = new Date().getFullYear();
  
      // เลือกองค์ประกอบ HTML โดยใช้ ID
      var academicYearSelect = document.getElementById("academic_year");
  
      // เพิ่มปีการศึกษาในรายการเลือก
      for (var year = currentYear; year <= currentYear + 5; year++) {
          var option = document.createElement("option");
          option.value = year;
          option.textContent = year;
          academicYearSelect.appendChild(option);
      }
  });
  
  
  document.addEventListener("DOMContentLoaded", function() {
      const addButton = document.getElementById("addButton");
      const inputContainer = document.querySelector(".input-container");
  
      addButton.addEventListener("click", function() {
          // สร้างแถวของช่อง input และปุ่มลบ
          const inputRow = document.createElement("div");
          inputRow.classList.add("input-row");
  
          const newInput = document.createElement("input");
          newInput.setAttribute("type", "text");
  
          const deleteButton = document.createElement("button");
          deleteButton.innerText = "ลบ";
          deleteButton.classList.add("delete-button");
  
          // เพิ่มช่อง input และปุ่มลบลงในแถวใหม่
          inputRow.appendChild(newInput);
          inputRow.appendChild(deleteButton);
  
          // เพิ่มแถวใหม่ลงใน input container
          inputContainer.appendChild(inputRow);
  
          // ใส่การลบแถวเมื่อคลิกปุ่ม "ลบ"
          deleteButton.addEventListener("click", function() {
              inputContainer.removeChild(inputRow);
          });
      });
  });
  
  function addRow_Score() {
      var table = document.querySelector("table tbody");
      var newRow = document.createElement("tr");
      newRow.innerHTML = `
          <td><input type="text" name="topic${table.children.length + 1}"></td>
          <td><input type="number" name="fullScore${table.children.length + 1}" min="0" max="100"></td>
          <td><button onclick="removeRow_Score(this)">ลบ</button></td>
      `;
      table.appendChild(newRow);
  }
  
  function removeRow_Score(button) {
      var table = document.querySelector("table tbody");
      var rowToRemove = button.parentNode.parentNode; // หาแถวที่ต้องการลบ
      if (rowToRemove) {
          table.removeChild(rowToRemove);
      }
  }
  
  
  