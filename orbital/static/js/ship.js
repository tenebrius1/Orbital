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

function myFunction() {
  // Declare variables
  var input, tr, table, i, group_name;
  input = document.getElementById('search').value.toLowerCase();
  table = document.getElementById('group_data');
  tr = table.getElementsByTagName('tr');
  console.log(input)
  console.log(table)
  console.log(tr)
}