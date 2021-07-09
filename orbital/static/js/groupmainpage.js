(function () {
  "use strict";
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll(".needs-validation");
  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      },
      false
    );
  });
})();

// Get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function sortTable(n) {
  var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    switchcount = 0;
  table = document.getElementById("group_data");
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
    for (i = 1; i < rows.length - 1; i++) {
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
      switchcount++;
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

var $sortable = $(".sortable");
$sortable.on("click", function () {
  var $this = $(this);
  var asc = $this.hasClass("asc");
  var desc = $this.hasClass("desc");
  $sortable.removeClass("asc").removeClass("desc");
  if (desc || (!asc && !desc)) {
    $this.addClass("asc");
  } else {
    $this.addClass("desc");
  }
});

// Delete button AJAX Request
$(document).on("click", ".delete_item", function () {
  $(this).parents("tr").remove();
  index = $(this).parent().parent().siblings().closest(".index").text();
  $.ajax({
    type: "POST",
    url: "/accounts/deleteItem",
    data: {
      index: index,
      name: $("#group_name").text(),
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },
    success: function (response) {
      location.href = "/accounts/ship/" + $("#group_name").text();
    },
  });
});

function redirect_locked(group_name) {
  location.href = "/accounts/ship/" + group_name + "/locked";
}

(function () {
  // DON'T EDIT BELOW THIS LINE
  var d = document,
    s = d.createElement("script");
  s.src = "https://shopbud.disqus.com/embed.js";
  s.setAttribute("data-timestamp", +new Date());
  (d.head || d.body).appendChild(s);
})();

$(document).on("click", ".delete", function () {
  $.ajax({
    type: "GET",
    url: "/accounts/deleteGroup",
    data: {
      name: $("#group_name").text(),
    },
    success: function (response) {
      location.href = "/accounts/ship";
    },
  });
});

$(document).on("click", ".leave", function () {
  $.ajax({
    type: "GET",
    url: "/accounts/leaveGroup",
    data: {
      name: $("#group_name").text(),
    },
    success: function (response) {
      location.href = "/accounts/ship";
    },
  });
});

$(document).on("click", ".lock", function () {
  $.ajax({
    type: "GET",
    url: "/accounts/lockGroup",
    data: {
      name: $("#group_name").text(),
    },
    success: function (response) {
      // redirect_locked($("#group_name").text());
    },
  });
  $.ajax({
    type: "GET",
    url: "/accounts/sendNotification_locked",
    data: {
      name: $("#group_name").text(),
    },
  });
});
