const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) => 
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));

var desc = true
// do the work...
document.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
    document.querySelectorAll('th').forEach(el => {
        if (el.textContent != th.textContent){
            el.textContent = el.textContent.replace("⬆","").replace("⬇","")
        }
    })
    if (desc) {
        th.textContent = th.textContent.replace("⬆","")
        th.textContent = th.textContent + "⬇"
        desc = false
    } else {
        th.textContent = th.textContent.replace("⬇","")
        th.textContent = th.textContent + "⬆"
        desc = true
    }


    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    Array.from(tbody.querySelectorAll('tr'))
      .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
      .forEach(tr => tbody.appendChild(tr) );
})));


function filter() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("filterInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("forecastTable");
    tr = table.getElementsByTagName("tr");
    console.log(tr)
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }