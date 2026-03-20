================================================================================
  Dora SkinWeight Tools Py v4.2.0
  Python Edition - Based on DoraSkinWeightImpExp.mel by DoraYuki
================================================================================

[ English ]
------------

## Installation

1. Copy "DoraSkinWeightToolsPy.py" to your Maya scripts folder:
   - Windows: C:\Users\<username>\Documents\maya\scripts\
     (or C:\Users\<username>\Documents\maya\<version>\scripts\)
   - Mac: ~/Library/Preferences/Autodesk/maya/<version>/scripts/

2. Launch Maya.

3. Open Script Editor (Windows > General Editors > Script Editor)

4. In the Python tab, run:
   import DoraSkinWeightToolsPy
   DoraSkinWeightToolsPy.launch()

5. (Optional) To reload after updating the file:
   Maya 2022+:
     import importlib
     import DoraSkinWeightToolsPy
     importlib.reload(DoraSkinWeightToolsPy)
     DoraSkinWeightToolsPy.launch()

   Maya 2018:
     import DoraSkinWeightToolsPy
     reload(DoraSkinWeightToolsPy)
     DoraSkinWeightToolsPy.launch()

## Shelf Button (Optional)

To add a shelf button:
1. Open Script Editor
2. Type the launch command above (Python)
3. Select the text and middle-mouse-drag it to your shelf

## Compatibility

- Maya 2018 - 2025
- Python 2.7 (Maya 2018-2019) / Python 3.x (Maya 2020+)

## Features

- Import / Export skin weights (DSW format)
- Vertex Paste (apply weights to selected vertices only)
- Body Fit (BETA): Match skeleton A to skeleton B by joint names
- Data Check: Weight decimal check, influence count check,
  same-position check, skin joint set creation
- Bilingual UI (English / Japanese)


================================================================================

[ 日本語 ]
------------

## インストール方法

1. "DoraSkinWeightToolsPy.py" を Maya の scripts フォルダにコピー:
   - Windows: C:\Users\<ユーザー名>\Documents\maya\scripts\
     (または C:\Users\<ユーザー名>\Documents\maya\<バージョン>\scripts\)
   - Mac: ~/Library/Preferences/Autodesk/maya/<バージョン>/scripts/

2. Maya を起動

3. スクリプトエディタを開く (Windows > General Editors > Script Editor)

4. Python タブで以下を実行:
   import DoraSkinWeightToolsPy
   DoraSkinWeightToolsPy.launch()

5. (任意) ファイル更新後の再読み込み:
   Maya 2022+:
     import importlib
     import DoraSkinWeightToolsPy
     importlib.reload(DoraSkinWeightToolsPy)
     DoraSkinWeightToolsPy.launch()

   Maya 2018:
     import DoraSkinWeightToolsPy
     reload(DoraSkinWeightToolsPy)
     DoraSkinWeightToolsPy.launch()

## シェルフボタン（任意）

シェルフボタンを追加するには:
1. スクリプトエディタを開く
2. 上記の起動コマンドを入力 (Python)
3. テキストを選択してシェルフに中ボタンドラッグ

## 対応バージョン

- Maya 2018 - 2025
- Python 2.7 (Maya 2018-2019) / Python 3.x (Maya 2020+)

## 機能一覧

- スキンウェイトのインポート / エクスポート (DSW形式)
- 頂点ペースト（選択頂点のみにウェイト適用）
- 体型合わせ (BETA): ジョイント名マッチングでスケルトンAをBに合わせる
- データチェック: ウェイト小数点チェック、インフルエンス数チェック、
  同位置チェック、スキンジョイントセット作成
- 日英バイリンガルUI

================================================================================
