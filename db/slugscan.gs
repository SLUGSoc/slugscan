// The spreadsheet used to store information on who is signed in or out
// where SHEET_ID is the file id. There must be a Sheet1 sheet
// and registered users must have their card ID in column A
var sheet = SpreadsheetApp.openById('SHEET_ID').getSheetByName('Members');

function testHandleGet() {
  return handleGet('1337');
}

function doGet(e) {
  var card = e.parameter.card;
  return handleGet(card);
}

// call the app with url/?card=scanned card number
// will return out for a sign out, in for a sign in
// or unknown card if it's not already in the spreadsheet
function handleGet(card) {  
  var datetime = Utilities.formatDate(new Date(), "GMT", "dd/MM/yyy HH:mm:ss");
  Logger.log(datetime);

  var data = sheet.getDataRange().getValues();
  var foundCard = 0;
  for (var i = 1; i < data.length; i++) {
    if (card == data[i][4]) {
      foundCard = 1;
      Logger.log(`Found card ${card} belonging to ${data[i][1]} in row ${i}`);
      if (data[i][5] == 'in') {
        data[i][5] = 'out';
      }
      else {
        data[i][5] = 'in';
      }

      data[i][6] = datetime;

      var row = data[i];
      sheet.getRange(i,1,1,7).setValues([row]);
      break;
    }
  }

  if (foundCard == 0) {
    Logger.log(`Unknown card: ${card} - is this a new member?`);
    return ContentService.createTextOutput("????");
  }

  if (row[5] == 'in') {
    return ContentService.createTextOutput(row[1] + '1');
  }
  else {
    return ContentService.createTextOutput(row[1] + '0');
  }
}
