# DoraSkinWeightToolsPy

Maya用スキンウェイト管理ツール (Python Edition)

Based on DoraSkinWeightImpExp.mel by DoraYuki

## Features

* **Import / Export** skin weights (DSW format) — Vertex Order / XYZ / UV matching
* **Vertex Paste** — apply weights to selected vertices only
* **Body Fit** — fit skeleton A to skeleton B by joint name matching
* **Cage Weight (BETA)** — auto-generate skin weights along bone chains with visual preview
* **Data Check** — weight decimal check, influence count check, same-position check
* **Bilingual UI** (English / Japanese)

## Compatibility

* Maya 2018 – 2025
* Python 2.7 (Maya 2018-2019) / Python 3.x (Maya 2020+)

## Installation

1. [Releases](https://github.com/Kiasejapan/SkinWeightToolsPy/releases) から `DoraSkinWeightToolsPy.py` をダウンロード
2. Maya の scripts フォルダにコピー:
   * Windows: `C:\Users\<username>\Documents\maya\scripts\`
     (or `C:\Users\<username>\Documents\maya\<version>\scripts\`)
   * Mac: `~/Library/Preferences/Autodesk/maya/<version>/scripts/`
3. Maya を起動
4. Script Editor (Windows > General Editors > Script Editor) の Python タブで実行:

   ```python
   import DoraSkinWeightToolsPy
   DoraSkinWeightToolsPy.launch()
   ```

5. (Optional) ファイル更新後のリロード:

   ```python
   # Maya 2022+
   import importlib
   import DoraSkinWeightToolsPy
   importlib.reload(DoraSkinWeightToolsPy)
   DoraSkinWeightToolsPy.launch()
   ```

   ```python
   # Maya 2018
   import DoraSkinWeightToolsPy
   reload(DoraSkinWeightToolsPy)
   DoraSkinWeightToolsPy.launch()
   ```

### Shelf Button (Optional)

1. Script Editor を開く
2. 上記の launch コマンドを入力 (Python)
3. テキストを選択して中ボタンドラッグでシェルフに追加

## Usage

### Export
1. スキン済みメッシュを選択
2. [Export] タブ > 名前入力 > [File] or [Object]
3. [Delete Selected DSW] で不要データを削除

### Import
1. スキン済みメッシュを選択
2. [Import] タブ > DSW選択 > モード選択 (XYZ / Vertex Order / UV)
3. [Import DSW] で適用

### Vertex Paste
選択頂点のみにウェイトをペースト:
1. ソースのウェイトをエクスポート
2. ターゲットの頂点を選択
3. DSWを選択し [Vertex Paste]

### Body Fit
1. [Body Fit] タブ
2. Body A (ソース) と Body B (ターゲット) をセット
3. [Fit Joints (A→B)]

### Cage Weight (BETA)
ボーンチェーンに沿ってスキンウェイトを自動生成:

1. ターゲットメッシュを選択 > [< Set Selected]
2. ルートジョイントを選択 > [< Set Selected]
3. [Bone edit / Cage generation] をクリック

**ボーンエディタウィンドウ:**
- ボーン名クリック: シーン内で選択
- ドロップダウン: ウェイトブレンドモードを選択
- チェックボックス: ブランチの含む/除外

**ウェイトモード:**

| 記号 | モード | 動作 |
|------|--------|------|
| ▁▃▅▇ | なめらか (Smooth) | 緩やかなS字カーブ |
| ▁▁▅▇ | くっきり (Sharp) | 中間点で急に切替 |
| ▁▁█▇ | 硬いセグメント (Rigid) | ほぼ瞬時に切替 |
| ▁▁██ | 50/50 | 中間点でハードカット |
| ── | スキップ (Skip) | ウェイト変更なし |

> 武器などの硬いパーツにはスキップを使用してください。

**生成と転写:**
1. モードを設定 → [ケージ生成] でプレビュー
2. [適用(転写)] でターゲットメッシュにウェイトを直接書き込み

### Data Check
- ウェイト精度: 閾値より細かいウェイトを検出
- 同位置チェック: 同じ位置でウェイトが異なる頂点を検出
- スキンジョイントセット作成

## Development

### Build

```
cd _build
python build.py
```

セクションファイル (`_build/src/*.txt`) を番号順に結合し、ルートの `DoraSkinWeightToolsPy.py` を生成します。

`build.bat` (リポルート) を実行すると、ビルド + git push まで一括で行います。

### Section Numbering

| Range | Category |
|-------|----------|
| 000-090 | 共通基盤 (header, i18n, progress, status, report) |
| 100-190 | ユーティリティ |
| 200-290 | データ層 (DSW, OpenMaya) |
| 300-390 | 主要機能 (Export, Import, Vertex Paste) |
| 400-490 | 拡張機能 (Body Fit, Cage Weight) |
| 500-590 | 検証・チェック |
| 600-690 | GUI |
| 900 | エントリーポイント |

## License

Based on DoraSkinWeightImpExp.mel by DoraYuki.
