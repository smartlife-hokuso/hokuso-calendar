#!/usr/bin/env python3
"""お客様向けWEBカレンダーを生成するスクリプト"""
import json
import sys

# 既存index.htmlからイベントデータを抽出
with open('/tmp/events_data.json', 'r') as f:
    events = json.loads(f.read())

events_json = json.dumps(events, ensure_ascii=False, separators=(',',':'))

html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SMARTLIFE AO 北総校｜2026年度 イベントカレンダー</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@300;400;500;700&family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{
    font-family:"Zen Maru Gothic","Hiragino Maru Gothic ProN",sans-serif;
    background:#faf8f5;
    color:#4a4a4a;
    line-height:1.6;
    min-height:100vh;
}}

/* ========== ヘッダー ========== */
.header{{
    background:#fff;
    padding:20px 24px;
    text-align:center;
    border-bottom:1px solid #eee;
    position:sticky;
    top:0;
    z-index:100;
    box-shadow:0 1px 8px rgba(0,0,0,0.04);
}}
.header-inner{{
    max-width:1100px;
    margin:0 auto;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:16px;
    flex-wrap:wrap;
}}
.brand{{
    display:flex;
    align-items:center;
    gap:10px;
}}
.brand-year{{
    font-family:"Quicksand",sans-serif;
    font-size:28px;
    font-weight:700;
    color:#2a7b9b;
    line-height:1;
}}
.brand-name{{
    font-size:13px;
    color:#5a5a5a;
    line-height:1.3;
}}
.brand-name strong{{
    font-size:20px;
    color:#2a7b9b;
    display:block;
    letter-spacing:1px;
}}
.brand-sub{{
    font-size:12px;
    color:#888;
    letter-spacing:0.5px;
}}

/* ========== 会場凡例 ========== */
.venue-legend{{
    display:flex;
    justify-content:center;
    gap:16px;
    padding:12px 20px;
    background:#f8f6f3;
    flex-wrap:wrap;
    font-size:12px;
    color:#666;
}}
.venue-legend-item{{
    display:flex;
    align-items:center;
    gap:6px;
}}
.venue-dot{{
    width:10px;
    height:10px;
    border-radius:50%;
}}

/* ========== メインコンテナ ========== */
.container{{
    max-width:1100px;
    margin:0 auto;
    padding:20px 16px 40px;
}}

/* ========== 月ナビ ========== */
.month-nav{{
    display:flex;
    justify-content:center;
    gap:6px;
    margin-bottom:24px;
    flex-wrap:wrap;
}}
.month-btn{{
    padding:10px 18px;
    border:1.5px solid #d8d0c8;
    border-radius:24px;
    background:#fff;
    color:#888;
    cursor:pointer;
    font-family:"Quicksand","Zen Maru Gothic",sans-serif;
    font-size:14px;
    font-weight:600;
    transition:all 0.25s ease;
    letter-spacing:0.5px;
}}
.month-btn:hover{{
    background:#2a7b9b;
    color:#fff;
    border-color:#2a7b9b;
    transform:translateY(-1px);
    box-shadow:0 3px 12px rgba(42,123,155,0.25);
}}
.month-btn.active{{
    background:#2a7b9b;
    color:#fff;
    border-color:#2a7b9b;
    box-shadow:0 2px 10px rgba(42,123,155,0.2);
}}

/* ========== カレンダーグリッド ========== */
.calendar-section{{display:none;}}
.calendar-section.active{{display:block;animation:fadeIn 0.35s ease;}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(8px);}}to{{opacity:1;transform:translateY(0);}}}}

.calendar-month-title{{
    text-align:center;
    margin-bottom:16px;
}}
.month-year{{
    font-family:"Quicksand",sans-serif;
    font-size:36px;
    font-weight:700;
    color:#2a7b9b;
    letter-spacing:2px;
}}
.month-ja{{
    font-size:14px;
    color:#999;
    letter-spacing:3px;
}}

.calendar-grid{{
    display:grid;
    grid-template-columns:repeat(7,1fr);
    gap:1px;
    background:#e8e4e0;
    border-radius:14px;
    overflow:hidden;
    box-shadow:0 2px 16px rgba(0,0,0,0.06);
}}
.day-header{{
    background:#f5f2ef;
    text-align:center;
    padding:10px 4px;
    font-size:12px;
    font-weight:700;
    color:#999;
    letter-spacing:2px;
}}
.day-header.mon{{color:#999;}}
.day-header.sat{{color:#5a8fb8;background:#f0f5fa;}}
.day-header.sun{{color:#c87070;background:#faf0f0;}}

.day-cell{{
    background:#fff;
    min-height:120px;
    padding:6px;
    cursor:default;
    transition:background 0.15s;
    position:relative;
}}
.day-cell:hover{{background:#fdfcfb;}}
.day-cell.empty{{background:#faf9f7;min-height:40px;}}
.day-cell.today{{background:#fffde8;}}
.day-cell.sat-bg{{background:#f8fbff;}}
.day-cell.sun-bg{{background:#fff8f8;}}

.day-number{{
    font-family:"Quicksand",sans-serif;
    font-size:13px;
    font-weight:700;
    color:#bbb;
    text-align:right;
    padding-right:4px;
    margin-bottom:4px;
}}
.day-cell.sat-bg .day-number{{color:#5a8fb8;}}
.day-cell.sun-bg .day-number{{color:#c87070;}}
.day-cell.today .day-number{{
    color:#fff;
    background:#2a7b9b;
    display:inline-block;
    width:24px;
    height:24px;
    line-height:24px;
    text-align:center;
    border-radius:50%;
    float:right;
}}

/* ========== イベントチップ ========== */
.ev-chip{{
    display:block;
    padding:3px 6px;
    margin-bottom:2px;
    border-radius:6px;
    font-size:10.5px;
    line-height:1.4;
    cursor:pointer;
    transition:all 0.15s;
    border-left:3px solid transparent;
    text-decoration:none;
    color:inherit;
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
}}
.ev-chip:hover{{
    transform:scale(1.02);
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
    white-space:normal;
    z-index:10;
    position:relative;
}}

/* 会場別カラー */
.ev-chip.v-tomisato{{background:#fce8ed;border-left-color:#e8889e;}}
.ev-chip.v-narita{{background:#e4f0fc;border-left-color:#6aa8d8;}}
.ev-chip.v-kamagaya{{background:#e6f5e4;border-left-color:#88bb70;}}

/* セミナー */
.ev-chip.seminar{{
    border-left:none;
    border:1.5px solid #d4a017;
    border-radius:20px;
    background:linear-gradient(135deg,#fff8eb,#fef0d0);
    color:#8a6010;
    font-weight:600;
    text-align:center;
    padding:4px 8px;
}}
.ev-chip.seminar.v-tomisato{{border-color:#e8889e;background:linear-gradient(135deg,#fff0f3,#fce8ed);color:#a0506a;}}
.ev-chip.seminar.v-narita{{border-color:#6aa8d8;background:linear-gradient(135deg,#f0f6ff,#e4f0fc);color:#3a6a9a;}}
.ev-chip.seminar.v-kamagaya{{border-color:#88bb70;background:linear-gradient(135deg,#f2faf0,#e6f5e4);color:#3a7a30;}}

.ev-time{{
    font-family:"Quicksand",sans-serif;
    font-size:9px;
    font-weight:700;
    opacity:0.6;
    margin-right:3px;
}}

/* ========== モーダル ========== */
.modal-overlay{{
    display:none;
    position:fixed;
    top:0;left:0;right:0;bottom:0;
    background:rgba(0,0,0,0.3);
    backdrop-filter:blur(3px);
    z-index:1000;
    justify-content:center;
    align-items:center;
    padding:20px;
}}
.modal-overlay.show{{display:flex;}}
.modal{{
    background:#fff;
    border-radius:20px;
    padding:0;
    max-width:480px;
    width:100%;
    max-height:85vh;
    overflow-y:auto;
    box-shadow:0 16px 48px rgba(0,0,0,0.15);
    animation:modalIn 0.3s ease;
}}
@keyframes modalIn{{from{{opacity:0;transform:scale(0.95) translateY(10px);}}to{{opacity:1;transform:scale(1) translateY(0);}}}}
.modal-header{{
    padding:24px 24px 16px;
    position:relative;
}}
.modal-close{{
    position:absolute;
    top:16px;
    right:16px;
    font-size:20px;
    cursor:pointer;
    color:#ccc;
    background:none;
    border:none;
    width:32px;
    height:32px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    transition:all 0.2s;
}}
.modal-close:hover{{background:#f5f5f5;color:#888;}}
.modal-genre-tag{{
    display:inline-block;
    padding:4px 12px;
    border-radius:20px;
    font-size:11px;
    font-weight:600;
    margin-bottom:10px;
}}
.modal-genre-tag.g-ai{{background:#e8f4fd;color:#2868a8;}}
.modal-genre-tag.g-security{{background:#fce8e8;color:#b83838;}}
.modal-genre-tag.g-business{{background:#e4f5e8;color:#1a7a40;}}
.modal-genre-tag.g-photo{{background:#fef3e4;color:#b87818;}}
.modal-genre-tag.g-esports{{background:#f0e8f8;color:#7838a8;}}
.modal-genre-tag.g-seminar{{background:#fff8eb;color:#8a6010;border:1px solid #e8d8a0;}}
.modal-title{{
    font-size:18px;
    font-weight:700;
    color:#3a3a3a;
    line-height:1.5;
    padding-right:30px;
}}
.modal-body{{
    padding:0 24px 24px;
}}
.modal-info{{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
    background:#f8f6f3;
    padding:16px;
    border-radius:14px;
    margin-bottom:16px;
}}
.info-item{{}}
.info-label{{
    font-size:10px;
    color:#aaa;
    font-weight:600;
    letter-spacing:0.5px;
    margin-bottom:2px;
}}
.info-value{{
    font-size:14px;
    color:#4a4a4a;
    font-weight:500;
}}
.modal-venue-badge{{
    display:inline-flex;
    align-items:center;
    gap:4px;
}}
.modal-venue-dot{{
    width:8px;
    height:8px;
    border-radius:50%;
    display:inline-block;
}}

/* お申込み案内 */
.modal-cta{{
    background:linear-gradient(135deg,#f0f8ff,#e8f4fd);
    border:1.5px solid #c8dff0;
    border-radius:14px;
    padding:16px;
    text-align:center;
    margin-top:16px;
}}
.modal-cta p{{
    font-size:12px;
    color:#5a8a9a;
    margin-bottom:8px;
}}
.modal-cta .cta-phone{{
    font-family:"Quicksand",sans-serif;
    font-size:22px;
    font-weight:700;
    color:#2a7b9b;
    letter-spacing:1px;
}}
.modal-cta .cta-location{{
    font-size:11px;
    color:#888;
    margin-top:4px;
}}

/* ========== リスト表示 ========== */
.view-toggle{{
    display:flex;
    justify-content:center;
    gap:8px;
    margin-bottom:20px;
}}
.view-btn{{
    padding:8px 16px;
    border:1.5px solid #d8d0c8;
    border-radius:20px;
    background:#fff;
    color:#888;
    cursor:pointer;
    font-family:inherit;
    font-size:12px;
    font-weight:600;
    transition:all 0.2s;
}}
.view-btn.active{{
    background:#2a7b9b;
    color:#fff;
    border-color:#2a7b9b;
}}
.list-view{{display:none;}}
.list-view.active{{display:block;}}
.calendar-view{{display:none;}}
.calendar-view.active{{display:block;}}

.event-list{{
    display:flex;
    flex-direction:column;
    gap:8px;
}}
.event-card{{
    display:flex;
    align-items:flex-start;
    gap:14px;
    background:#fff;
    padding:16px;
    border-radius:14px;
    box-shadow:0 1px 6px rgba(0,0,0,0.04);
    cursor:pointer;
    transition:all 0.2s;
    border:1px solid #f0ede8;
}}
.event-card:hover{{
    box-shadow:0 4px 16px rgba(0,0,0,0.08);
    transform:translateY(-1px);
}}
.event-card-date{{
    flex-shrink:0;
    width:52px;
    text-align:center;
    padding:6px 0;
}}
.event-card-day{{
    font-family:"Quicksand",sans-serif;
    font-size:26px;
    font-weight:700;
    color:#2a7b9b;
    line-height:1;
}}
.event-card-dow{{
    font-size:10px;
    color:#aaa;
    font-weight:600;
    margin-top:2px;
}}
.event-card-dow.sun{{color:#c87070;}}
.event-card-dow.sat{{color:#5a8fb8;}}
.event-card-body{{
    flex:1;
    min-width:0;
}}
.event-card-title{{
    font-size:14px;
    font-weight:600;
    color:#3a3a3a;
    margin-bottom:4px;
    line-height:1.4;
}}
.event-card-meta{{
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    font-size:11px;
    color:#999;
}}
.event-card-meta span{{
    display:flex;
    align-items:center;
    gap:3px;
}}

/* ========== フッター ========== */
.footer{{
    background:#fff;
    border-top:1px solid #eee;
    padding:30px 20px;
    text-align:center;
    margin-top:40px;
}}
.footer-brand{{
    font-size:16px;
    font-weight:700;
    color:#2a7b9b;
    margin-bottom:6px;
}}
.footer-address{{
    font-size:12px;
    color:#888;
    margin-bottom:10px;
    line-height:1.6;
}}
.footer-phone{{
    font-family:"Quicksand",sans-serif;
    font-size:24px;
    font-weight:700;
    color:#2a7b9b;
    letter-spacing:1px;
}}
.footer-note{{
    font-size:11px;
    color:#bbb;
    margin-top:12px;
    line-height:1.6;
}}

/* ========== フィルター ========== */
.filter-bar{{
    display:flex;
    justify-content:center;
    gap:6px;
    margin-bottom:16px;
    flex-wrap:wrap;
}}
.filter-btn{{
    padding:6px 14px;
    border:1.5px solid #e0dcd8;
    border-radius:20px;
    background:#fff;
    color:#999;
    cursor:pointer;
    font-family:inherit;
    font-size:11px;
    font-weight:600;
    transition:all 0.2s;
}}
.filter-btn.active{{
    border-color:#2a7b9b;
    color:#2a7b9b;
    background:#f0f8ff;
}}
.filter-btn:hover{{
    border-color:#2a7b9b;
    color:#2a7b9b;
}}

/* ========== レスポンシブ ========== */
@media(max-width:768px){{
    .header-inner{{gap:10px;}}
    .brand-year{{font-size:22px;}}
    .brand-name strong{{font-size:16px;}}
    .month-year{{font-size:28px;}}
    .day-cell{{min-height:80px;padding:3px;}}
    .ev-chip{{font-size:9px;padding:2px 4px;}}
    .ev-time{{display:none;}}
    .day-number{{font-size:11px;}}
    .modal{{max-width:100%;border-radius:16px;}}
    .modal-title{{font-size:16px;}}
    .container{{padding:12px 8px 30px;}}
    .month-btn{{padding:8px 14px;font-size:12px;}}
    .event-card{{padding:12px;gap:10px;}}
    .event-card-title{{font-size:13px;}}
}}
@media(max-width:480px){{
    .day-cell{{min-height:65px;padding:2px;}}
    .ev-chip{{font-size:8px;padding:1px 3px;border-left-width:2px;}}
    .day-number{{font-size:10px;}}
    .calendar-grid{{border-radius:10px;}}
    .day-header{{padding:6px 2px;font-size:10px;}}
}}
</style>
</head>
<body>

<!-- ヘッダー -->
<div class="header">
    <div class="header-inner">
        <div class="brand">
            <div class="brand-year">2026</div>
            <div class="brand-name">
                SMARTLIFE
                <strong>AO 北総校</strong>
            </div>
        </div>
        <div class="brand-sub">イベントカレンダー｜富里キャンパス・成田キャンパス・鎌ヶ谷</div>
    </div>
</div>

<!-- 会場凡例 -->
<div class="venue-legend">
    <div class="venue-legend-item"><div class="venue-dot" style="background:#e8889e;"></div>富里キャンパス</div>
    <div class="venue-legend-item"><div class="venue-dot" style="background:#6aa8d8;"></div>成田キャンパス</div>
    <div class="venue-legend-item"><div class="venue-dot" style="background:#88bb70;"></div>鎌ヶ谷</div>
    <div class="venue-legend-item" style="margin-left:8px;"><span style="display:inline-block;width:28px;height:14px;border-radius:10px;border:1.5px solid #d4a017;background:linear-gradient(135deg,#fff8eb,#fef0d0);vertical-align:middle;"></span>&nbsp;セミナー・体験会</div>
</div>

<!-- メインコンテナ -->
<div class="container">

    <!-- 表示切替 -->
    <div class="view-toggle">
        <button class="view-btn active" onclick="setView('calendar')">カレンダー</button>
        <button class="view-btn" onclick="setView('list')">リスト</button>
    </div>

    <!-- 会場フィルター -->
    <div class="filter-bar" id="filterBar">
        <button class="filter-btn active" data-venue="all" onclick="setFilter('all',this)">すべて</button>
        <button class="filter-btn" data-venue="富里" onclick="setFilter('富里',this)">富里</button>
        <button class="filter-btn" data-venue="成田" onclick="setFilter('成田',this)">成田</button>
        <button class="filter-btn" data-venue="鎌ヶ谷" onclick="setFilter('鎌ヶ谷',this)">鎌ヶ谷</button>
    </div>

    <!-- 月ナビ -->
    <div class="month-nav" id="monthNav"></div>

    <!-- カレンダー表示 -->
    <div class="calendar-view active" id="calendarView"></div>

    <!-- リスト表示 -->
    <div class="list-view" id="listView"></div>

</div>

<!-- フッター -->
<div class="footer">
    <div class="footer-brand">SMARTLIFE AO 北総校</div>
    <div class="footer-address">
        富里キャンパス：SLMC富里インターBASE内<br>
        成田キャンパス・オンライン配信あり
    </div>
    <div class="footer-phone">0476-90-6667</div>
    <div class="footer-note">
        ※天候等により、開催内容やスケジュールが変更となる可能性がございます。最新情報は随時ご確認ください。<br>
        ※各講座のお申込みは、店頭またはお電話にて承ります。ご予約はいつもの担当プランナーまで。
    </div>
</div>

<!-- モーダル -->
<div class="modal-overlay" id="modal" onclick="if(event.target===this)closeModal()">
    <div class="modal">
        <div class="modal-header">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div id="modalGenre"></div>
            <div class="modal-title" id="modalTitle"></div>
        </div>
        <div class="modal-body">
            <div class="modal-info" id="modalInfo"></div>
            <div class="modal-cta">
                <p>お申込み・お問い合わせ</p>
                <div class="cta-phone">0476-90-6667</div>
                <div class="cta-location">SMARTLIFE AO 北総校<br>富里キャンパス SLMC富里インターBASE内</div>
            </div>
        </div>
    </div>
</div>

<script>
const events = {events_json};

const months = ['2026-04','2026-05','2026-06','2026-07','2026-08','2026-09'];
const monthNames = {{
    '2026-04':['APRIL','4月'],'2026-05':['MAY','5月'],'2026-06':['JUNE','6月'],
    '2026-07':['JULY','7月'],'2026-08':['AUGUST','8月'],'2026-09':['SEPTEMBER','9月']
}};
const dowJa = ['日','月','火','水','木','金','土'];
let currentFilter = 'all';
let currentView = 'calendar';

function venueClass(v) {{
    if(v.includes('富里')) return 'v-tomisato';
    if(v.includes('成田')) return 'v-narita';
    if(v.includes('鎌ヶ谷')) return 'v-kamagaya';
    return '';
}}
function venueColor(v) {{
    if(v.includes('富里')) return '#e8889e';
    if(v.includes('成田')) return '#6aa8d8';
    if(v.includes('鎌ヶ谷')) return '#88bb70';
    return '#ccc';
}}
function genreTag(circle) {{
    if(circle.includes('AI') && !circle.includes('セミナー') && !circle.includes('体験')) return ['AI活用','g-ai'];
    if(circle.includes('安全') || circle.includes('セキュリティ')) return ['セキュリティ','g-security'];
    if(circle.includes('商店') || circle.includes('事業')) return ['ビジネス・DX','g-business'];
    if(circle.includes('写真') || circle.includes('メディア')) return ['写真・メディア','g-photo'];
    if(circle.includes('Sports') || circle.includes('スポーツ')) return ['E-Sports','g-esports'];
    if(circle.includes('セミナー') || circle.includes('体験')) return ['セミナー・体験会','g-seminar'];
    return ['講座','g-ai'];
}}

function filteredEvents() {{
    if(currentFilter==='all') return events;
    return events.filter(e=>e.venue===currentFilter);
}}

// 月ナビ生成
function buildMonthNav() {{
    const nav = document.getElementById('monthNav');
    nav.innerHTML = months.map((m,i)=>
        `<button class="month-btn${{i===0?' active':''}}" onclick="showMonth('${{m}}')">${{monthNames[m][0]}}<span style="font-size:10px;opacity:0.6;margin-left:4px;">${{monthNames[m][1]}}</span></button>`
    ).join('');
}}

// カレンダー生成
function buildCalendars() {{
    const container = document.getElementById('calendarView');
    const fe = filteredEvents();
    container.innerHTML = months.map((m,idx)=>{{
        const [y, mo] = m.split('-').map(Number);
        const first = new Date(y, mo-1, 1);
        const last = new Date(y, mo, 0);
        const startDow = first.getDay(); // 0=Sun
        // 月曜始まり
        const startOffset = (startDow + 6) % 7;
        const totalDays = last.getDate();
        const today = new Date();
        const todayStr = today.toISOString().split('T')[0];

        // Group events by date
        const evByDate = {{}};
        fe.forEach(e=>{{
            if(e.date.startsWith(m)){{
                const d = parseInt(e.date.split('-')[2]);
                if(!evByDate[d]) evByDate[d]=[];
                evByDate[d].push(e);
            }}
        }});

        let html = `<div class="calendar-section${{idx===0?' active':''}}" id="month-${{m}}">`;
        html += `<div class="calendar-month-title"><div class="month-year">${{monthNames[m][0]}}</div><div class="month-ja">${{monthNames[m][1]}}</div></div>`;
        html += '<div class="calendar-grid">';
        // Headers (Mon-Sun)
        const headers = ['月','火','水','木','金','土','日'];
        const hClasses = ['mon','','','','','sat','sun'];
        headers.forEach((h,i)=>{{
            html += `<div class="day-header ${{hClasses[i]}}">${{h}}</div>`;
        }});
        // Empty cells before first day
        for(let i=0;i<startOffset;i++) html += '<div class="day-cell empty"></div>';
        // Days
        for(let d=1;d<=totalDays;d++) {{
            const dateStr = `${{y}}-${{String(mo).padStart(2,'0')}}-${{String(d).padStart(2,'0')}}`;
            const dow = new Date(y, mo-1, d).getDay();
            let cls = 'day-cell';
            if(dow===0) cls += ' sun-bg';
            if(dow===6) cls += ' sat-bg';
            if(dateStr === todayStr) cls += ' today';
            html += `<div class="${{cls}}">`;
            html += `<div class="day-number">${{d}}</div>`;
            if(evByDate[d]) {{
                evByDate[d].forEach(ev=>{{
                    const vc = venueClass(ev.venue);
                    const isSem = ev.type==='seminar';
                    const chipCls = isSem ? `ev-chip seminar ${{vc}}` : `ev-chip ${{vc}}`;
                    const shortTitle = ev.title.length > 20 ? ev.title.substring(0,20)+'…' : ev.title;
                    html += `<div class="${{chipCls}}" onclick='openModal(${{JSON.stringify(ev).replace(/'/g,"\\\\'")}})'>`;
                    if(!isSem) html += `<span class="ev-time">${{ev.time}}</span>`;
                    html += shortTitle;
                    html += '</div>';
                }});
            }}
            html += '</div>';
        }}
        // Empty cells after last day
        const endDow = (startOffset + totalDays) % 7;
        if(endDow > 0) for(let i=endDow;i<7;i++) html += '<div class="day-cell empty"></div>';
        html += '</div></div>';
        return html;
    }}).join('');
}}

// リスト生成
function buildList() {{
    const container = document.getElementById('listView');
    const fe = filteredEvents();
    container.innerHTML = months.map((m,idx)=>{{
        const monthEvents = fe.filter(e=>e.date.startsWith(m));
        if(monthEvents.length === 0) return '';
        let html = `<div class="calendar-section${{idx===0?' active':''}}" id="list-${{m}}">`;
        html += `<div class="calendar-month-title" style="margin-bottom:12px;"><div class="month-year">${{monthNames[m][0]}}</div><div class="month-ja">${{monthNames[m][1]}}</div></div>`;
        html += '<div class="event-list">';
        monthEvents.sort((a,b)=>a.date.localeCompare(b.date)||a.time.localeCompare(b.time));
        monthEvents.forEach(ev=>{{
            const d = new Date(ev.date+'T00:00:00');
            const day = d.getDate();
            const dow = dowJa[d.getDay()];
            const dowCls = d.getDay()===0?'sun':d.getDay()===6?'sat':'';
            const [tag, tagCls] = genreTag(ev.circle);
            html += `<div class="event-card" onclick='openModal(${{JSON.stringify(ev).replace(/'/g,"\\\\'")}})'>`;
            html += `<div class="event-card-date"><div class="event-card-day">${{day}}</div><div class="event-card-dow ${{dowCls}}">${{dow}}</div></div>`;
            html += '<div class="event-card-body">';
            html += `<div class="event-card-title">${{ev.title}}</div>`;
            html += '<div class="event-card-meta">';
            html += `<span style="color:${{venueColor(ev.venue)}};">● ${{ev.venue}}</span>`;
            html += `<span>${{ev.time}}～</span>`;
            html += `<span class="modal-genre-tag ${{tagCls}}" style="padding:2px 8px;font-size:10px;">${{tag}}</span>`;
            html += '</div></div></div>';
        }});
        html += '</div></div>';
        return html;
    }}).join('');
}}

function showMonth(m) {{
    const prefix = currentView==='calendar' ? 'month-' : 'list-';
    document.querySelectorAll('.calendar-section').forEach(s=>s.classList.remove('active'));
    document.querySelectorAll('.month-btn').forEach(b=>b.classList.remove('active'));
    const el = document.getElementById(prefix+m);
    if(el) el.classList.add('active');
    const idx = months.indexOf(m);
    document.querySelectorAll('.month-btn')[idx]?.classList.add('active');
}}

function setView(v) {{
    currentView = v;
    document.querySelectorAll('.view-btn').forEach(b=>b.classList.remove('active'));
    if(v==='calendar') {{
        document.getElementById('calendarView').classList.add('active');
        document.getElementById('listView').classList.remove('active');
        document.querySelectorAll('.view-btn')[0].classList.add('active');
    }} else {{
        document.getElementById('calendarView').classList.remove('active');
        document.getElementById('listView').classList.add('active');
        document.querySelectorAll('.view-btn')[1].classList.add('active');
    }}
    // Re-activate current month
    const activeBtn = document.querySelector('.month-btn.active');
    if(activeBtn) activeBtn.click();
}}

function setFilter(venue, btn) {{
    currentFilter = venue;
    document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    buildCalendars();
    buildList();
    // Re-activate current month
    const activeIdx = [...document.querySelectorAll('.month-btn')].findIndex(b=>b.classList.contains('active'));
    if(activeIdx>=0) showMonth(months[activeIdx]);
}}

function openModal(ev) {{
    const [tag, tagCls] = genreTag(ev.circle);
    document.getElementById('modalGenre').innerHTML =
        `<span class="modal-genre-tag ${{tagCls}}">${{ev.type==='seminar'?'⭐ ':''}}${{tag}}</span>`;
    document.getElementById('modalTitle').textContent = ev.title;
    document.getElementById('modalInfo').innerHTML =
        `<div><div class="info-label">開催日</div><div class="info-value">${{ev.date.replace(/-/g,'.')}}</div></div>` +
        `<div><div class="info-label">時間</div><div class="info-value">${{ev.time}}～</div></div>` +
        `<div><div class="info-label">会場</div><div class="info-value"><span class="modal-venue-badge"><span class="modal-venue-dot" style="background:${{venueColor(ev.venue)}};"></span>${{ev.venue}}</span></div></div>` +
        `<div><div class="info-label">サークル</div><div class="info-value" style="font-size:12px;">${{ev.circle}}</div></div>`;
    document.getElementById('modal').classList.add('show');
}}
function closeModal() {{
    document.getElementById('modal').classList.remove('show');
}}
document.addEventListener('keydown', e=>{{ if(e.key==='Escape') closeModal(); }});

// 初期化
buildMonthNav();
buildCalendars();
buildList();
</script>
</body>
</html>'''

# 出力
output_path = '/Users/ishiharajunichi/Desktop/北総フォルダ２/イベント/2026年度イベント/customer.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Generated: {output_path}')
