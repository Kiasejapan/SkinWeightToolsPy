# DoraSkinWeightToolsPy

Skin weight management tool for Maya (Python Edition).
Provides DSW format weight import/export, cage weight auto-generation, same-position check, and more in a single file.

---

## Installation

### 1. Download DoraSkinWeightToolsPy

Right-click the link below and select **"Save link as..."** to download.

> **[DoraSkinWeightToolsPy.py](https://github.com/Kiasejapan/SkinWeightToolsPy/raw/refs/heads/main/DoraSkinWeightToolsPy.py)**

### 2. Place the file

Copy `DoraSkinWeightToolsPy.py` to your Maya scripts folder:

```
C:\Users\<username>\Documents\maya\scripts\
```

> Mac: `~/Library/Preferences/Autodesk/maya/<version>/scripts/`

### 3. Launch in Maya

Open Script Editor (Windows > General Editors > Script Editor).
Switch to the Python tab and run:

```python
import DoraSkinWeightToolsPy
DoraSkinWeightToolsPy.launch()
```

### 4. Reload after update (optional)

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

### Shelf Button (optional)

1. Open Script Editor
2. Type the launch command above (Python)
3. Select the text and middle-mouse-drag it to your shelf

---

## Compatibility

* Maya 2018 – 2025
* Python 2.7 (Maya 2018-2019) / Python 3.x (Maya 2020+)

---

## Features

* **Import / Export** — DSW format skin weights (Vertex Order / XYZ / UV matching)
* **Vertex Paste** — Apply weights to selected vertices only
* **Body Fit** — Match skeleton A to skeleton B by joint name
* **Cage Weight (BETA)** — Auto-generate skin weights along bone chains
* **Data Check** — Weight decimal check/clean, influence count check, same-position weight check
* **Update** — One-click update from GitHub via the in-tool Update button
* **Bilingual UI** — English / Japanese toggle

---

## In-Tool Update

Click the **Update** button in the tool window to check for new versions on GitHub.
If a newer version is found, it will be downloaded, installed, and reloaded automatically.

---

## License

Based on DoraSkinWeightImpExp.mel by DoraYuki.

---
---

# DoraSkinWeightToolsPy（日本語）

Maya 用スキンウェイト管理ツール（Python Edition）です。
DSW 形式でのウェイト入出力、ケージウェイト自動生成、同位置チェックなどを 1 ファイルで提供します。

---

## 導入手順

### 1. DoraSkinWeightToolsPy をダウンロード

以下のリンクを **右クリック → 名前を付けてリンク先を保存** でダウンロードしてください。

> **[DoraSkinWeightToolsPy.py](https://github.com/Kiasejapan/SkinWeightToolsPy/raw/refs/heads/main/DoraSkinWeightToolsPy.py)**

### 2. 所定の場所に配置

以下のパスに `DoraSkinWeightToolsPy.py` を配置してください。

```
C:\Users\ユーザー名\Documents\maya\scripts\
```

> Mac の場合: `~/Library/Preferences/Autodesk/maya/<version>/scripts/`

### 3. Maya で実行

Maya を起動し、Script Editor（スクリプトエディター）を開きます。
言語を Python に切り替えて以下を実行してください。

```python
import DoraSkinWeightToolsPy
DoraSkinWeightToolsPy.launch()
```

### 4. ファイル更新後のリロード（任意）

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

### シェルフボタン（任意）

1. Script Editor を開く
2. 上記の起動コマンドを入力（Python）
3. テキストを選択して中ボタンドラッグでシェルフに追加

---

## 対応バージョン

* Maya 2018 – 2025
* Python 2.7 (Maya 2018-2019) / Python 3.x (Maya 2020+)

---

## 機能一覧

* **Import / Export** — DSW 形式でスキンウェイトを入出力（頂点番号順 / XYZ 座標 / UV 座標）
* **Vertex Paste** — 選択した頂点のみにウェイトをペースト
* **Body Fit** — ジョイント名マッチングでスケルトン A を B に合わせる
* **Cage Weight (BETA)** — ボーンチェーンに沿ってスキンウェイトを自動生成
* **Data Check** — ウェイト小数点チェック / クリーン、インフルエンス数チェック、同位置ウェイトチェック
* **Update** — ツール内ボタンから GitHub 最新版を取得・自動リロード
* **Bilingual UI** — 日本語 / 英語 切替

---

## ツール内アップデート

ツールウィンドウの **Update** ボタンをクリックすると、GitHub の最新版と比較し、
新しいバージョンがあればワンクリックでダウンロード・インストール・リロードできます。

---

## License

Based on DoraSkinWeightImpExp.mel by DoraYuki.
