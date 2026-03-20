# DoraSkinWeightToolsPy - Section Map
# Claude がコードを参照・修正する際のガイド

## リポジトリ情報
- **ツール名**: DoraSkinWeightToolsPy
- **成果物**: `DoraSkinWeightToolsPy.py` (単一ファイル)
- **対応Maya**: 2018-2025 (Python 2.7 / 3.x)

## セクション一覧

| # | ファイル | 行数 | 内容 | 依存先 |
|---|---------|------|------|--------|
| 000 | `000_header.txt` | 24 | エンコーディング宣言, imports, VERSION, PY2互換 | — |
| 010 | `010_i18n.txt` | 144 | `_LANG`, `_S` 辞書, `tr()`, `set_language()` | 000 |
| 020 | `020_progress.txt` | 26 | `progress_start/update/end()` | 000 |
| 030 | `030_status_line.txt` | 30 | `show_status()`, `show_check_result()` | 010 |
| 040 | `040_report_logger.txt` | 52 | `Report` クラス | 010 |
| 100 | `100_utility.txt` | 62 | `vtx_to_uv`, `get_shape`, `get_skin_cluster` 等 | 000 |
| 110 | `110_spatial_index.txt` | 62 | `SpatialIndex` クラス (XYZ/UV空間検索) | 000 |
| 200 | `200_dsw_readwrite.txt` | 44 | `read_dsw`, `write_dsw_file`, `delete_dsw` | 100 |
| 210 | `210_openmaya_helpers.txt` | 89 | `_bulk_get_weights/positions/uvs` (OpenMaya API) | 000 |
| 300 | `300_export.txt` | 95 | `dsw_export()` | 100, 200, 210 |
| 310 | `310_import.txt` | 205 | `dsw_import()`, `_build_wp`, `_wt_copy`, `_bind_dsw` | 100, 110, 200, 210 |
| 320 | `320_vertex_paste.txt` | 71 | `vertex_paste_weights()` | 100, 110, 200, 210, 310 |
| 400 | `400_body_fit.txt` | 214 | `body_fit_joints()`, `body_fit_reset()` | 100 |
| 500 | `500_data_check.txt` | 193 | `check_weight_digit`, `check_influence_count` 等 | 100, 210 |
| 510 | `510_dsw_list.txt` | 14 | `get_dsw_list()` | 200 |
| 600 | `600_gui.txt` | 348 | `DoraSkinWeightUI` クラス (全UI) | 全セクション |
| 900 | `900_entry.txt` | 8 | `launch()`, `DoraSkinWeightToolsPy()` | 600 |

## 採番ルール (ビルド・コード管理ガイド準拠)

| レンジ | カテゴリ |
|--------|----------|
| 000-090 | 共通基盤 (header, i18n, progress, status, report) |
| 100-190 | ユーティリティ (汎用関数, 空間インデックス) |
| 200-290 | データ層 (DSWファイル操作, OpenMaya) |
| 300-390 | 主要機能 (Export, Import, Vertex Paste) |
| 400-490 | 拡張機能 (Body Fit) |
| 500-590 | 検証・チェック機能 |
| 600-690 | GUI |
| 900 | エントリーポイント |

## Claude用ワークフロー

### コード参照 (public リポの場合)
```
raw URL テンプレート:
https://raw.githubusercontent.com/{OWNER}/{REPO}/main/_build/src/{SECTION_FILE}

例: i18n を取得
https://raw.githubusercontent.com/{OWNER}/{REPO}/main/_build/src/010_i18n.txt
```

### 修正の流れ
1. SECTION_MAP.md を確認して対象セクションを特定
2. 該当セクションファイルの raw URL を web_fetch で取得
3. コードを修正
4. 修正後のセクションファイルを出力
5. ユーザーが git commit → push → build
