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

function search() {
  // Declare variables
  var input, tr, table, i;
  input = document.getElementById('search').value.toLowerCase();
  table = document.getElementById('group_data');
  tr = table.getElementsByTagName('tr');

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td_name = tr[i].getElementsByTagName("td")[0];
    td_location = tr[i].getElementsByTagName("td")[3];
    if (td_name || td_location) {
      txtValue = td_name.textContent || td_name.innerText
      txtValue_Location = td_location.textContent || td_location.innerText
      if (txtValue.toLowerCase().indexOf(input) > -1 || txtValue_Location.toLowerCase().indexOf(input) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function redirect(group_name) {
  location.href = "/accounts/ship/" + group_name;
}

function redirect_locked(group_name) {
  location.href = "/accounts/ship/" + group_name + "/locked";
}

(function () {  // DON'T EDIT BELOW THIS LINE
  var d = document, s = d.createElement('script');

  s.src = 'https://shopbud.disqus.com/embed.js';

  s.setAttribute('data-timestamp', +new Date());
  (d.head || d.body).appendChild(s);
})();

$(document).on("click", ".delete", function () {
  $.ajax({
    type: 'GET',
    url: "/accounts/deleteGroup",
    data: {
      "name": $('#group_name').text(),
    },
    success: function (response) {
      location.href = '/accounts/ship'
    }
  })
});

$(document).on("click", ".leave", function () {
  $.ajax({
    type: 'GET',
    url: "/accounts/leaveGroup",
    data: {
      "name": $('#group_name').text(),
    },
    success: function (response) {
      location.href = '/accounts/ship'
    }
  })
});

$(document).on("click", ".lock", function () {
  $.ajax({
    type: 'GET',
    url: "/accounts/lockGroup",
    data: {
      "name": $('#group_name').text(),
    },
    success: function (response) {
      redirect_locked($('#group_name').text());
    }
  })
});

$(".paid").change(function() {
  index = $(this).parent().parent().index()
  checkbox = $('.data').eq(index).find('input')
  if ($(checkbox).is(':checked')) {
    $.ajax({
      type: 'GET',
      url: "/accounts/changePaidStatus",
      data: {
        "name": $('#group_name').text(),
        'index': index,
        'paid': 'true'
      },
    })
  } else {
    $.ajax({
      type: 'GET',
      url: "/accounts/changePaidStatus",
      data: {
        "name": $('#group_name').text(),
        'index': index,
        'paid': 'false'
      },
    })
  }
});