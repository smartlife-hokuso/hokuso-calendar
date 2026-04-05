// ====================================================
// Google Apps Script - Webカレンダーからの実績報告受付
// ====================================================
// 【設置方法】
// 1. Googleスプレッドシートを開く
// 2. メニュー「拡張機能」→「Apps Script」
// 3. このコードを貼り付けて保存
// 4. 「デプロイ」→「新しいデプロイ」→ 種類:「ウェブアプリ」
//    - 実行するユーザー: 「自分」
//    - アクセスできるユーザー: 「全員」
// 5. デプロイ後に表示されるURLをコピー
// 6. index.html内の GAS_URL を↑のURLに置き換える
// ====================================================

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('フォームの回答 1');
    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    }

    var data = JSON.parse(e.postData.contents);

    // スプレッドシートに追記
    sheet.appendRow([
      new Date(),                          // A: タイムスタンプ
      data.instructor || '',               // B: イベント講師
      data.plannerCount || '',             // C: 講師プランナー人数
      data.plannerCost || '',              // D: 講師プランナー人件費
      data.groupCount || '',               // E: 参加組数
      data.participantCount || '',         // F: 参加人数
      data.achievement || '',              // G: 実績
      data.issues || '',                   // H: 課題と対策
      '',                                  // I: 列7
      '',                                  // J: 実績[2行目]
      data.eventDate || '',                // K: イベント日付（追加）
      data.eventVenue || '',               // L: 会場（追加）
      data.eventTitle || '',               // M: イベントタイトル（追加）
      data.eventCircle || '',              // N: サークル名（追加）
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'success' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  // テスト用 & データ取得用
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('フォームの回答 1');
    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    }

    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1).map(function(row) {
      var obj = {};
      headers.forEach(function(h, i) {
        obj[h] = row[i];
      });
      return obj;
    });

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'success', data: rows }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
