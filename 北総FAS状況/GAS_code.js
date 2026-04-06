var SHEET_ID = "1wjKFnzeKQe6StoIHXcE08qC2bZgzgJWfywHk32o0BSw";
var SHEET_NAME = "SL富里のコピー";

function doGet(e) {
  var callback = e.parameter.callback || "";
  var action = e.parameter.action || "";
  var json = "";

  if (action === "save") {
    json = JSON.stringify(saveData(e));
  } else if (action === "totals") {
    json = JSON.stringify(readTotals());
  } else {
    json = JSON.stringify(readData(e));
  }

  if (callback) {
    return ContentService.createTextOutput(callback + "(" + json + ")").setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var data = JSON.parse(e.postData.contents);
  var result = saveDataDirect(data.name, data.values);
  return ContentService.createTextOutput(JSON.stringify(result)).setMimeType(ContentService.MimeType.JSON);
}

function readData(e) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var ws = ss.getSheetByName(SHEET_NAME);
  var allData = ws.getDataRange().getValues();
  var targetName = e.parameter.name || "";
  var nameRow = allData[2];
  var itemCol = 2;
  var result = {};
  for (var c = 3; c < nameRow.length; c++) {
    var name = nameRow[c] ? nameRow[c].toString().trim() : "";
    if (!name) continue;
    if (targetName && name.replace(/\s/g, "") !== targetName.replace(/\s/g, "")) continue;
    var person = {};
    for (var r = 3; r < allData.length; r++) {
      var item = allData[r][itemCol] ? allData[r][itemCol].toString().trim() : "";
      if (item) {
        person[item] = allData[r][c] !== null && allData[r][c] !== "" ? allData[r][c] : 0;
      }
    }
    result[name] = person;
  }
  return result;
}

function readTotals() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var ws = ss.getSheetByName(SHEET_NAME);
  var allData = ws.getDataRange().getValues();
  var nameRow = allData[2]; // 3行目 = 名前行
  var itemCol = 2;          // C列 = 項目名

  // 項目名→行番号のマッピング
  var itemRows = {};
  for (var r = 3; r < allData.length; r++) {
    var item = allData[r][itemCol] ? allData[r][itemCol].toString().trim() : "";
    if (item) itemRows[item] = r;
  }

  var totalCust = 0, totalVC = 0;
  var planners = {};

  for (var c = 3; c < nameRow.length; c++) {
    var name = nameRow[c] ? nameRow[c].toString().trim() : "";
    if (!name) continue;
    var nameKey = name.replace(/\s/g, "");
    var cust = Number(allData[itemRows["担当軒数"]] ? allData[itemRows["担当軒数"]][c] : 0) || 0;
    var people = Number(allData[itemRows["担当人数"]] ? allData[itemRows["担当人数"]][c] : 0) || 0;
    var ao = Number(allData[itemRows["内AO生"]] ? allData[itemRows["内AO生"]][c] : 0) || 0;
    var vc = Number(allData[itemRows["VC"]] ? allData[itemRows["VC"]][c] : 0) || 0;

    totalCust += cust;
    totalVC += vc;
    planners[nameKey] = { cust: cust, people: people, ao: ao, dx: vc };
  }

  return { totalCust: totalCust, totalVC: totalVC, planners: planners };
}

function saveData(e) {
  var name = e.parameter.name || "";
  var dataStr = e.parameter.data || "{}";
  var values = JSON.parse(dataStr);
  return saveDataDirect(name, values);
}

function saveDataDirect(name, values) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var ws = ss.getSheetByName(SHEET_NAME);
  var names = ws.getRange(3, 1, 1, ws.getLastColumn()).getValues()[0];
  var col = -1;
  for (var i = 0; i < names.length; i++) {
    if (names[i] && names[i].toString().replace(/\s/g, "") === name.replace(/\s/g, "")) {
      col = i + 1;
      break;
    }
  }
  if (col === -1) {
    return {status: "error", message: "name not found: " + name};
  }
  var items = ws.getRange(1, 3, ws.getLastRow(), 1).getValues();
  var updates = [];
  var keys = Object.keys(values);
  for (var k = 0; k < keys.length; k++) {
    var key = keys[k];
    var value = values[key];
    for (var r = 0; r < items.length; r++) {
      if (items[r][0] && items[r][0].toString().trim() === key.trim()) {
        ws.getRange(r + 1, col).setValue(Number(value) || 0);
        updates.push(key);
        break;
      }
    }
  }
  ws.getRange(2, 2).setValue("更新日:" + Utilities.formatDate(new Date(), "Asia/Tokyo", "yyyy年M月d日"));
  return {status: "ok", updated: updates, name: name};
}
