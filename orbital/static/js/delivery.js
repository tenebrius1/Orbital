(function () {
  'use strict'
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')
  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })
})()

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function displayDeliveries() {
  $.ajax({
    type: 'GET',
    url: "/accounts/displayDeliveries",
    success: function (response) {
      var rows = $('.data');
      var columns;
      for (var i = 0; i < rows.length; i++) {
        columns = $(rows[i]).find('td');
        state = response['response'][i]['delivery_status'];
        if (state == "delivered") {
          $(columns[3]).children("span").addClass("badge bg-success");
          $(columns[3]).children("span").html(state);
        } else if (state == "transit" || state == "pickup") {
          $(columns[3]).children("span").addClass("badge bg-warning");
          $(columns[3]).children("span").html(state);
        } else if (state == "pendding") {
          $(columns[3]).children("span").addClass("badge bg-secondary");
          $(columns[3]).children("span").html("pending");
        } else {
          $(columns[3]).children("span").addClass("badge bg-danger");
          $(columns[3]).children("span").html(state);
        }
        t = response['response'][i]['lastest_checkpoint_time'] ? response['response'][i]['lastest_checkpoint_time'].split("T") : "";
        tt = t == "" ? "" : t[1].split("+");
        $(columns[4]).html(tt == "" ? "---" : t[0] + " " + tt[0]);
      }
    },
  })
}

// Display deliveries
$(document).ready(displayDeliveries());

// Delete button AJAX Request
$(document).on("click", ".delete", function () {
  $(this).parents("tr").remove();
  $.ajax({
    type: 'POST',
    url: "/accounts/deleteDelivery",
    data: {
      "name": $(this).parent().parent().siblings().closest(".name").text(),
      "tkg_number": $(this).parent().parent().siblings().closest(".tkg_number").text(),
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
    success: function (response) {
      displayDeliveries();
    }
  })
});

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("transaction_data");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

var $sortable = $('.sortable');

$sortable.on('click', function(){
  
  var $this = $(this);
  var asc = $this.hasClass('asc');
  var desc = $this.hasClass('desc');
  $sortable.removeClass('asc').removeClass('desc');
  if (desc || (!asc && !desc)) {
    $this.addClass('asc');
  } else {
    $this.addClass('desc');
  }
  
});