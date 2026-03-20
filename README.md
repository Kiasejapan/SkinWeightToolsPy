# DoraSkinWeightToolsPy

Maya用スキンウェイト管理ツール (Python Edition)

Based on DoraSkinWeightImpExp.mel by DoraYuki

## Features

- **Import / Export** skin weights (DSW format) — Vertex Order / XYZ / UV matching
- **Vertex Paste** — apply weights to selected vertices only
- **Body Fit (BETA)** — fit skeleton A to skeleton B by joint name matching
- **Data Check** — weight decimal check, influence count check, same-position check
- **Bilingual UI** (English / Japanese)

## Compatibility

- Maya 2018 – 2025
- Python 2.7 (Maya 2018-2019) / Python 3.x (Maya 2020+)

## Installation

1. [Releases](../../releases) から `DoraSkinWeightToolsPy.py` をダウンロード
2. Maya の scripts フォルダにコピー:
   - Windows: `C:\Users\<user>\Documents\maya\scripts\`
3. Maya で実行:
   ```python
   import DoraSkinWeightToolsPy
   DoraSkinWeightToolsPy.launch()
   ```

## Development

### フォルダ構成

```
DoraSkinWeightToolsPy/
├── _build/
│   ├── src/            ← セクション別ソースファイル
│   │   ├── 000_header.txt
│   │   ├── 010_i18n.txt
│   │   ├── ...
│   │   └── 900_entry.txt
│   ├── backup/         ← ビルド前バックアップ
│   ├── build.py        ← ビルドスクリプト (Python)
│   └── build.bat       ← Windows用ラッパー
├── SECTION_MAP.md      ← セクション対応表・依存関係
├── .gitignore
├── README.md
└── DoraSkinWeightToolsPy.py  ← ★ビルド成果物 (配布ファイル)
```

### ビルド

```bash
cd _build
python build.py
```

セクションファイル (`_build/src/*.txt`) を番号順に結合し、ルートの `DoraSkinWeightToolsPy.py` を生成します。

### 採番ルール

- `000-090`: 共通基盤 (header, i18n, progress, status, report)
- `100-190`: ユーティリティ
- `200-290`: データ層 (DSW, OpenMaya)
- `300-390`: 主要機能 (Export, Import, Vertex Paste)
- `400-490`: 拡張機能 (Body Fit)
- `500-590`: 検証・チェック
- `600-690`: GUI
- `900`: エントリーポイント

詳細は [SECTION_MAP.md](SECTION_MAP.md) を参照。

## License

Based on DoraSkinWeightImpExp.mel by DoraYuki.
