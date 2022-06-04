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

document.getElementById("forecastTable").querySelectorAll("th").forEach((th) =>
  th.addEventListener("click", () => {
    document.getElementById("forecastTable").querySelectorAll("th").forEach((el) => {
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
  var rows = document.querySelector("#forecastTable tbody").rows;
  var column = {
    day: 1,
    avg_o3: 2,
    max_o3: 3,
    min_o3: 4,
    avg_pm10: 5,
    max_pm10: 6,
    min_pm10: 7,
    avg_pm25: 8,
    max_pm25: 9,
    min_pm25: 10,
    avg_uvi: 11,
    max_uvi: 12,
    min_uvi: 13,
  };

  document.getElementById("filterInput").value = "";
  for (var i = 0; i < rows.length; i++) {
    rows[i].style.display = "";
  }
  if (ftype != "" && fcolumn != "")
    document.getElementById("filterInput").disabled = false;
  else 
    document.getElementById("filterInput").disabled = true;
}

function checkCity(){
  var city = document.getElementById("city").value;
  if (city != "")
    document.getElementById("dtype").disabled = false;
  else 
    document.getElementById("dtype").disabled = true;
}

function filter(event) {
  var filter = event.target.value.toUpperCase();
  var rows = document.querySelector("#forecastTable tbody").rows;
  var ftype = document.getElementById("ftype").value;
  var fcolumn = document.getElementById("fcolumn").value;

  var column = {
    day: 1,
    avg_o3: 2,
    max_o3: 3,
    min_o3: 4,
    avg_pm10: 5,
    max_pm10: 6,
    min_pm10: 7,
    avg_pm25: 8,
    max_pm25: 9,
    min_pm25: 10,
    avg_uvi: 11,
    max_uvi: 12,
    min_uvi: 13,
  };

  for (var i = 0; i < rows.length; i++) {
    var col = rows[i].cells[column[fcolumn]].textContent.toUpperCase();
    var compcol,compfilter
    if (column[fcolumn] == 1) {
      console.log("TUTAJ")
      if (filter.length != 10){
        console.log(filter.length)
        rows[i].style.display = ""
      } else {
        compfilter = filter.split("-")
        compcol = col.split("-")
        compcol = new Date(parseInt(compcol[0]), parseInt(compcol[1] - 1), parseInt(compcol[2]));
        compfilter = new Date(parseInt(compfilter[0]), parseInt(compfilter[1] - 1), parseInt(compfilter[2]));
      }
    } else {
      compcol = parseFloat(col);
      compfilter = parseFloat(filter);
    }

    switch (ftype) {
      case 'equal':
        if (compcol == compfilter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        break;
      case 'gt':
        if (compcol > compfilter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        break;
      case 'lt':
        if (compcol < compfilter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        break;
      case 'egt':
        if (compcol >= compfilter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        console.log("egt");
        break;
      case 'elt':
        if (compcol <= compfilter) {
          rows[i].style.display = "";
        } else {
          rows[i].style.display = "none";
        }
        break;
      default:
        rows[i].style.display = "";
        break;
    }
  }
}

document.querySelector("#filterInput").addEventListener("keyup", filter, false);
