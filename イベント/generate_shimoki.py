#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下期（2026-10〜2027-03）のイベントフォルダ・レポート・プレゼンPDFを生成する。

generate_all.py の生成ロジックを流用するが、main() は index.html を
上書きしてしまうため呼ばない。フォルダ名はカレンダー(index.html)の
events配列からそのまま取得し、リンク先と確実に一致させる。
"""
import os, sys, json

BASE_DIR = '/Users/ishiharajunichi/Desktop/北総フォルダ２/イベント'
OUT_DIR  = os.path.join(BASE_DIR, '2026年度イベント')
CAL      = os.path.join(OUT_DIR, 'index.html')

sys.path.insert(0, BASE_DIR)
import generate_all as G


def load_from_calendar(since='2026-10-01'):
    s = open(CAL, encoding='utf-8').read()
    T = 'const events = '
    i = s.index(T); j = s.index('];', i)
    events = json.loads(s[i+len(T):j+1])
    out = []
    for idx, e in enumerate(sorted([x for x in events if x['date'] >= since],
                                   key=lambda x: (x['date'], x['venue'], x['time'])), 1):
        out.append({
            'idx': idx,
            'date': e['date'],
            'time': e.get('time', ''),
            'venue': e.get('venue', ''),
            'circle': e.get('circle', ''),
            'title': e.get('title', ''),
            'member': e.get('member', ''),
            'folder_name': e['folder'],
        })
    return out


def main():
    dry = '--dry-run' in sys.argv
    events = load_from_calendar()
    print(f"対象: {len(events)}件")

    # 既存フォルダとの衝突確認
    exists = [e for e in events if os.path.isdir(os.path.join(OUT_DIR, e['folder_name']))]
    if exists:
        print(f"⚠ 既に存在するフォルダ: {len(exists)}件")
        for e in exists[:5]:
            print("   ", e['folder_name'])
    if dry:
        print("--dry-run のため生成しません")
        for e in events[:3]:
            print("  例:", e['folder_name'])
        return

    made = skipped = pdf_err = 0
    for i, ev in enumerate(events, 1):
        folder = os.path.join(OUT_DIR, ev['folder_name'])
        os.makedirs(folder, exist_ok=True)

        rpt_path = os.path.join(folder, 'report.html')
        pdf_path = os.path.join(folder, 'presentation.pdf')

        # 既存ファイルは上書きしない（上期の成果物を守るため）
        if os.path.exists(rpt_path) and os.path.exists(pdf_path):
            skipped += 1
            continue

        report = G.generate_report_content(ev)
        if not os.path.exists(rpt_path):
            with open(rpt_path, 'w', encoding='utf-8') as f:
                f.write(G.generate_report_html(ev, report))
        if not os.path.exists(pdf_path):
            try:
                G.generate_presentation_pdf(ev, report, pdf_path)
            except Exception as ex:
                pdf_err += 1
                print(f"  ⚠ PDF生成エラー [{ev['title'][:28]}]: {ex}")
        made += 1
        if i % 40 == 0:
            print(f"  ...{i}/{len(events)}")

    print(f"\n完了: 生成 {made}件 / スキップ {skipped}件 / PDFエラー {pdf_err}件")


if __name__ == '__main__':
    main()
