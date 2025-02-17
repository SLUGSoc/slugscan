// The spreadsheet used to store information on who is signed in or out
// where SHEET_ID is the file id. There must be a Sheet1 sheet
// and registered users must have their card ID in column A
var sheet = SpreadsheetApp.openById('SHEET_ID').getSheetByName('Sheet1');

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
  var date = Utilities.formatDate(new Date(), "GMT", "yyyy-MM-dd"); 
  var time = Utilities.formatDate(new Date(), "GMT", "HH:mm:ss");
  Logger.log(date + " " + time);	
  
  var data = sheet.getDataRange().getValues();
  var foundCard = 0;
  for (var i = 0; i < data.length; i++) {
    if (card == data[i][0]) {
      foundCard = 1;
      Logger.log("found card " + card + " in row " + (i + 1));
      if (data[i][2] == 'in') {
        data[i][2] = 'out';
      }
      else {
        data[i][2] = 'in';
      }
      data[i][3] = date;
      data[i][4] = time;
      var row = data[i];
      sheet.getRange(i+1,1,1,5).setValues([row]);
      break;
    }
  }
  if (foundCard == 0) {
    Logger.log("unknown card: " + card);
    return ContentService.createTextOutput('????');
  }
  
  if (row[2] == 'in') {
    return ContentService.createTextOutput(row[1] + '1');
  }
  else {
    return ContentService.createTextOutput(row[1] + '0');
  }
}
