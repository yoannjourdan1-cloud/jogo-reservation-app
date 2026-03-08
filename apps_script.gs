// ============================================================
// Google Apps Script - CHEZ JOGO Réservation
// À déployer comme "Application Web" dans Google Apps Script
// ============================================================

var SPREADSHEET_ID = "1Al1Z4tCYYe_8OmecrTzHdtpwjf5cWALQ";
var SHEET_NAME = "Feuil1";

function doPost(e) {
  var lock = LockService.getScriptLock();
  
  try {
    // Tentative d'acquisition du verrou (gestion des accès concurrents)
    lock.waitLock(10000); // attend jusqu'à 10 secondes
    
    var params = JSON.parse(e.postData.contents);
    var row = parseInt(params.row);
    var col = parseInt(params.col);
    var value = params.value;
    
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME);
    
    // Vérification anti-doublon : la cellule est-elle encore "Libre" ?
    var currentValue = sheet.getRange(row, col).getValue();
    
    if (currentValue !== "Libre") {
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          message: "Cette place vient d'être réservée par quelqu'un d'autre."
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Écriture du nom dans la cellule
    sheet.getRange(row, col).setValue(value);
    SpreadsheetApp.flush();
    
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: "Réservation confirmée !"
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        message: "Erreur : " + err.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: "JOGO Script actif" }))
    .setMimeType(ContentService.MimeType.JSON);
}
