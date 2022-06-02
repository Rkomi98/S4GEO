const getCellValue = (tr, idx) =>
  tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) =>
  ((v1, v2) =>
    v1 !== "" && v2 !== "" && !isNaN(v1) && !isNaN(v2)
      ? v1 - v2
      : v1.toString().localeCompare(v2))(
    getCellValue(asc ? a : b, idx),
    getCellValue(asc ? b : a, idx)
  );

var desc = true;

document.querySelectorAll("th").forEach((th) =>
  th.addEventListener("click", () => {
    document.querySelectorAll("th").forEach((el) => {
      if (el.textContent != th.textContent) {
        el.textContent = el.textContent.replace("⬆", "").replace("⬇", "");
      }
    });
    if (desc) {
      th.textContent = th.textContent.replace("⬆", "");
      th.textContent = th.textContent + "⬇";
      desc = false;
    } else {
      th.textContent = th.textContent.replace("⬇", "");
      th.textContent = th.textContent + "⬆";
      desc = true;
    }

    const table = th.closest("table");
    const tbody = table.querySelector("tbody");
    Array.from(tbody.querySelectorAll("tr"))
      .sort(
        comparer(
          Array.from(th.parentNode.children).indexOf(th),
          (this.asc = !this.asc)
        )
      )
      .forEach((tr) => tbody.appendChild(tr));
  })
);

function check(){
  var ftype = document.getElementById("ftype").value;
  var fcolumn = document.getElementById("fcolumn").value;
  if (ftype != "" && fcolumn != "")
    document.getElementById("filterInput").disabled = false;
  else 
    document.getElementById("filterInput").disabled = true;
}
function filter(event) {
  var filter = event.target.value.toUpperCase();
  var rows = document.querySelector("#forecastTable tbody").rows;
  var ftype = document.getElementById("ftype").value;
  var fcolumn = document.getElementById("fcolumn").value;

  var column = {
    day: 0,
    avg_o3: 1,
    max_o3: 2,
    min_o3: 3,
    avg_pm10: 4,
    max_pm10: 5,
    min_pm10: 6,
    avg_pm25: 7,
    max_pm25: 8,
    min_pm25: 9,
    avg_uvi: 10,
    max_uvi: 11,
    min_uvi: 12,
  };

  for (var i = 0; i < rows.length; i++) {
    var col = rows[i].cells[column[fcolumn]].textContent.toUpperCase();
    if (column[fcolumn] == 0) {
      col = Date(col);
      filter = Date(filter) 
    } else {
      col = parseFloat(col);
      filter = parseFloat(filter) 
    }
    console.log(ftype)
    switch (ftype) {
      case 'equal':
        if (col == filter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        console.log("equal");
        break;
      case 'gt':
        if (col > filter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        console.log("gt");
        break;
      case 'lt':
        if (col < filter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        console.log("lt");
        break;
      case 'egt':
        if (col >= filter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        console.log("egt");
        break;
      case 'elt':
        if (col <= filter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        console.log("elt");
        break;
      default:
        console.log("NOPE");
        rows[i].style.display = "";
        break;
    }
  }
}

document.querySelector("#filterInput").addEventListener("keyup", filter, false);
