(function () {
  'use strict';
  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation');
  // Loop over them and prevent submission
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      'submit',
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      },
      false
    );
  });
})();

function capitalize(word) {
  return word.replace(/^\w/, (c) => c.toUpperCase());
}

// Get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Delete button AJAX Request
$(document).on('click', '.delete', function () {
  $(this).parents('tr').remove();
  $.ajax({
    type: 'POST',
    url: '/accounts/deleteTransaction',
    data: {
      name: $(this).parent().parent().siblings().closest('.name').text(),
      price: $(this).parent().parent().siblings().closest('.price').text(),
      date: $(this).parent().parent().siblings().closest('.date').text(),
      company: $(this).parent().parent().siblings().closest('.company').text(),
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
    success: function (response) {
      location.href = "/accounts/transaction";
    },
  });
});

function displayExpenses() {
  $.ajax({
    type: 'GET',
    url: '/accounts/displayExpenses',
    success: function (response) {
      let platforms = Object.keys(response);
      let dataset = [];
      let totalspent = 0;
      for (var i = 0, len = platforms.length; i < len; i++) {
        dataset.push(response[platforms[i]]);
        totalspent += parseFloat(response[platforms[i]]);
        $(`.${platforms[i]}`).text(`$${response[platforms[i]]}`);
        platforms[i] = capitalize(platforms[i]);
      }
      new Chart(document.getElementById('chartjs-dashboard-pie'), {
        type: 'pie',
        data: {
          labels: platforms,
          datasets: [
            {
              data: dataset,
              borderWidth: 5,
            },
          ],
        },
        options: {
          responsive: !window.MSInputMethodContext,
          maintainAspectRatio: false,
          legend: {
            display: true,
          },
          cutoutPercentage: 75,
          plugins: {
            colorschemes: {
              scheme: 'tableau.ClassicMedium10'
            }
          }
        },
      });

      var formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      });

      $('.total').text(formatter.format(totalspent).toString());
    },
  });
}

// Display expenses
$(document).ready(displayExpenses());

// Edit functions
let items;
function Save() {
  var par = $(this).parents('tr'); //tr
  var tdItem = par.children('td.name');
  var tdDate = par.children('td.date');
  var tdCompany = par.children('td.company');
  var tdPrice = par.children('td.price');
  var tdEdit = par.find('.btnSave');
  var tdDelete = par.find('.cancel');

  // New values
  nItem = tdItem.children('input[type=text]').val();
  nDate = tdDate.children('input[type=date]').val().split('-');
  nDate = nDate[2] + '/' + nDate[1] + '/' + nDate[0];
  nCom = tdCompany.children('input[type=text]').val();
  nPrice = tdPrice.children('input[type=number]').val();

  tdItem.html(nItem[0].toUpperCase() + nItem.substring(1));
  tdDate.html(nDate);
  tdCompany.html(nCom);
  tdPrice.html('$' + parseFloat(nPrice).toFixed(2));
  tdEdit.replaceWith(
    "<a class='edit' title='Edit' data-bs-toggle='tooltip' data-bs-placement='top'>" +
      "<i class='bi bi-pencil-square me-3'></i>" +
      '</a>'
  );
  tdDelete.replaceWith(
    "<a class='delete' title='Delete' data-bs-toggle='tooltip' data-bs-placement='top'>" +
      "<i class='bi bi-trash-fill me-3'></i>" +
      '</a>'
  );

  $('.edit').bind('click', Edit);

  // AJAX
  $.ajax({
    type: 'POST',
    url: '/accounts/editTransaction',
    data: {
      oItem: items[0],
      oDate: items[1],
      oCom: items[2],
      oPrice: items[3],
      nItem: nItem,
      nDate: nDate,
      nCom: nCom,
      nPrice: nPrice,
      csrfmiddlewaretoken: getCookie('csrftoken'),
    },
    success: function (response) {
      location.href = '/accounts/transaction'
    },
  });
}

function Edit() {
  var par = $(this).parents('tr'); //tr
  var tdItem = par.children('td.name');
  var tdDate = par.children('td.date');
  var tdCompany = par.children('td.company');
  var tdPrice = par.children('td.price');
  var tdSave = par.find('.edit');
  var tdCancel = par.find('.delete');

  // Extract and format original date
  let date = tdDate.html().split('/');
  date = date[2] + '-' + date[1] + '-' + date[0];

  items = [tdItem.html(), tdDate.html(), tdCompany.html(), tdPrice.html()];

  tdItem.html(
    "<input type='text' class='name form-control' value='" +
      tdItem.html() +
      "'/>"
  );
  tdDate.html("<input class='form-control' type='date' value='" + date + "'/>");
  tdCompany.html(
    "<input type='text' class='company form-control' value='" +
      tdCompany.html() +
      "'/>"
  );
  tdPrice.html(
    "<input class='form-control' type='number' value='" +
      tdPrice.html().substring(1) +
      "' min='0' step='.01' />"
  );
  tdSave.replaceWith(
    "<a class='btnSave' title='Save' data-bs-toggle='tooltip' data-bs-placement='top'>" +
      "<i class='bi bi-check-square me-3'></i>" +
      '</a>'
  );
  tdCancel.replaceWith(
    "<a class='cancel' title='Cancel' data-bs-toggle='tooltip' data-bs-placement='top'>" +
      "<i class='bi bi-x-square me-3'></i>" +
      '</a>'
  );

  $('.btnSave').bind('click', Save);
  $('.cancel').bind('click', function () {
    var par = $(this).parents('tr'); //tr
    var tdItem = par.children('td.name');
    var tdDate = par.children('td.date');
    var tdCompany = par.children('td.company');
    var tdPrice = par.children('td.price');
    var tdEdit = par.find('.btnSave');
    var tdDelete = par.find('.cancel');

    tdItem.html(items[0]);
    tdDate.html(items[1]);
    tdCompany.html(items[2]);
    tdPrice.html(items[3]);
    tdEdit.replaceWith(
      "<a class='edit' title='Edit' data-bs-toggle='tooltip' data-bs-placement='top'>" +
        "<i class='bi bi-pencil-square me-3'></i>" +
        '</a>'
    );
    tdDelete.replaceWith(
      "<a class='delete' title='Delete' data-bs-toggle='tooltip' data-bs-placement='top'>" +
        "<i class='bi bi-trash-fill me-3'></i>" +
        '</a>'
    );

    $('.edit').bind('click', Edit);
  });
}

$(function () {
  $('.edit').bind('click', Edit);
});

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
  table = document.getElementById('transaction_data');
  switching = true;
  // Set the sorting direction to ascending:
  dir = 'asc';
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
      x = rows[i].getElementsByTagName('TD')[n];
      y = rows[i + 1].getElementsByTagName('TD')[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == 'asc') {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == 'desc') {
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
      if (switchcount == 0 && dir == 'asc') {
        dir = 'desc';
        switching = true;
      }
    }
  }
}

function sortPrice(n) {
  var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    switchcount = 0;
  table = document.getElementById('transaction_data');
  switching = true;
  // Set the sorting direction to ascending:
  dir = 'asc';
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
      x = rows[i].getElementsByTagName('TD')[n];
      y = rows[i + 1].getElementsByTagName('TD')[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      var xprice = parseFloat(x.innerHTML.slice(1));
      var yprice = parseFloat(y.innerHTML.slice(1));
      if (dir == 'asc') {
        if (xprice > yprice) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == 'desc') {
        if (xprice < yprice) {
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
      if (switchcount == 0 && dir == 'asc') {
        dir = 'desc';
        switching = true;
      }
    }
  }
}

function sortDate(n) {
  var table,
    rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    dir,
    switchcount = 0;
  table = document.getElementById('transaction_data');
  switching = true;
  // Set the sorting direction to ascending:
  dir = 'asc';
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
      x = rows[i].getElementsByTagName('TD')[n];
      y = rows[i + 1].getElementsByTagName('TD')[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      var xDate = x.innerHTML.split('/');
      var yDate = y.innerHTML.split('/');
      if (dir == 'asc') {
        if (xDate[2] > yDate[2]) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
        if (xDate[2] == yDate[2]) {
          if (xDate[1] > yDate[1]) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
          if (xDate[1] == yDate[1]) {
            if (xDate[0] > yDate[0]) {
              // If so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
        }
      } else if (dir == 'desc') {
        if (xDate[2] < yDate[2]) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
        if (xDate[2] == yDate[2]) {
          if (xDate[1] < yDate[1]) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
          }
          if (xDate[1] == yDate[1]) {
            if (xDate[0] < yDate[0]) {
              // If so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
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
      if (switchcount == 0 && dir == 'asc') {
        dir = 'desc';
        switching = true;
      }
    }
  }
}

var $sortable = $('.sortable');

$sortable.on('click', function () {
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
