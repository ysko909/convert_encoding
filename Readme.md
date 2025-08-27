# テキストファイルエンコード変換スクリプト

テキストファイルのエンコーディングを変換するPythonスクリプトです。SJIS（Shift-JIS）とUTF-8の相互変換に対応しています。

## 機能

- **ファイル/フォルダ単位での一括変換**: 単一ファイルまたはフォルダ内の全`.txt`・`.md`ファイルを一括変換
- **双方向変換**: SJIS→UTF-8（デフォルト）、UTF-8→SJIS
- **柔軟なファイル処理**: 新規ファイル作成または元ファイル上書き
- **エンコーディング自動検出**: 変換前のファイルエンコーディングを自動検出・表示
- **静寂モード**: エラーメッセージや警告を非表示にするオプション
- **対象ファイルフィルタリング**: `.txt`および`.md`ファイル以外は自動スキップ（警告表示）

## 必要な環境

- Python 3.6以降
- 標準ライブラリのみ使用（追加パッケージのインストール不要）

## インストール

1. スクリプトファイル `convert_encoding.py` をダウンロード
2. 実行権限を付与（Unix系OSの場合）

```bash
chmod +x convert_encoding.py
```

## 使用方法

### 基本構文

```bash
python convert_encoding.py <ファイル/フォルダパス> [オプション]
```

### オプション

| オプション | 短縮形 | 説明 |
|------------|--------|------|
| `--reverse` | `-r` | UTF-8→SJIS変換（省略時はSJIS→UTF-8） |
| `--overwrite` | `-o` | 元ファイルを上書き（省略時は新規ファイル作成） |
| `--quiet` | `-q` | エラーメッセージと警告メッセージを非表示 |
| `--help` | `-h` | ヘルプメッセージを表示 |

## 使用例

### 基本的な使用例

```bash
# 単一ファイル（.txt/.md）をSJIS→UTF-8に変換（新規ファイル作成）
python convert_encoding.py sample.txt
python convert_encoding.py note.md

# フォルダ内の全txt/mdファイルを変換
python convert_encoding.py ./text_files/

# UTF-8→SJIS変換
python convert_encoding.py sample.txt -r
python convert_encoding.py note.md --reverse
```

### 高度な使用例

```bash
# 元ファイルを上書き
python convert_encoding.py sample.txt -o
python convert_encoding.py note.md --overwrite

# UTF-8→SJIS変換 + 上書き
python convert_encoding.py sample.txt -r -o

# 静寂モード（エラーメッセージ非表示）
python convert_encoding.py ./mixed_files/ -q

# 全オプション組み合わせ
python convert_encoding.py ./text_files/ -r -o -q
```

## ファイル命名規則

新規ファイル作成モード（デフォルト）では、以下の規則でファイル名が決定されます：

- **SJIS→UTF-8変換**: `元ファイル名_utf-8.拡張子`
- **UTF-8→SJIS変換**: `元ファイル名_sjis.拡張子`

### 例

```
sample.txt → sample_utf-8.txt  （SJIS→UTF-8）
note.md    → note_utf-8.md
report.txt → report_sjis.txt   （UTF-8→SJIS）
memo.md    → memo_sjis.md
```

## 動作仕様

### 対象ファイル

- **対象拡張子**: `.txt`, `.md`
- **除外ファイル**: `.csv`、`.doc`、`.xlsx`など`.txt`または`.md`以外の拡張子は自動的に除外（スキップ時に警告表示、quietモードでは非表示）

### エンコーディング検出

スクリプトは以下の順序でエンコーディングを自動検出します：

1. UTF-8
2. Shift-JIS (shift_jis)
3. CP932
4. EUC-JP
5. ISO-2022-JP

### エラーハンドリング

- **存在しないパス**: エラーメッセージを表示して終了
- **権限エラー**: ファイルアクセス権限がない場合はスキップ
- **エンコーディングエラー**: 変換に失敗したファイルは個別にエラー表示
- **継続処理**: 一部のファイルでエラーが発生しても、他のファイルの処理は継続
- **対象外ファイル**: `.txt`, `.md`以外はスキップし、警告（quiet時は非表示）

## 出力例

### 通常モード

```
変換モード: SJIS → UTF-8
ファイル処理: 新規ファイルを作成
--------------------------------------------------

警告: 2個の非.txt/.mdファイルをスキップしました。
  スキップ: ./text_files/sample.csv
  スキップ: ./text_files/image.png

処理中: ./text_files/sample.txt
  検出されたエンコーディング: shift_jis
変換完了: ./text_files/sample.txt -> ./text_files/sample_utf-8.txt
  shift_jis -> utf-8

処理中: ./text_files/note.md
  検出されたエンコーディング: shift_jis
変換完了: ./text_files/note.md -> ./text_files/note_utf-8.md
  shift_jis -> utf-8

==================================================
変換結果: 成功 2件, エラー 0件
処理が完了しました。
```

### 静寂モード（-qオプション）

```bash
python convert_encoding.py ./text_files/ -q
# エラーメッセージや警告、スキップ表示はなく、静かに処理されます
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. 「ファイルが見つからない」エラー

**原因**: 指定されたパスが存在しない

**解決方法**: 
```bash
# パスを確認
ls -la /path/to/your/files/
# 正しいパスを指定
python convert_encoding.py /correct/path/to/files/
```

#### 2. 権限エラー

**原因**: ファイルの読み取り/書き込み権限がない

**解決方法**:
```bash
# 権限を確認
ls -la target_file.txt
# 権限を変更
chmod 644 target_file.txt
```

#### 3. エンコーディング変換エラー

**原因**: ファイルが破損している、または想定外のエンコーディング

**解決方法**:
- ファイルの内容を確認
- 別のテキストエディタでファイルを開いて確認
- 必要に応じて手動でエンコーディングを修正

#### 4. 大量の警告メッセージ

**原因**: `.txt`や`.md`以外のファイルが多数含まれるフォルダを指定

**解決方法**:
```bash
# 静寂モードを使用
python convert_encoding.py ./mixed_folder/ -q
```

## 注意事項

### ファイル処理について

- **バックアップ推奨**: 重要なファイルは事前にバックアップを取ってから実行
- **上書きモード**: `-o`オプション使用時は元ファイルが完全に置き換えられます
- **ファイル名重複**: 新規ファイル作成時に同名ファイルが存在する場合は上書きされます

### エンコーディングについて

- **自動検出の限界**: 短いテキストや特殊な文字を含まない場合、検出が困難な場合があります
- **文字化け**: 間違ったエンコーディングで変換すると文字化けが発生する可能性があります
- **Shift-JIS対応**: CP932（Windows-31J）も基本的にShift-JISとして処理されます

## ライセンス

このスクリプトはMITライセンスの下で公開されています。

---

**注意**: このツールは教育目的および個人利用を想定しています。重要なデータを扱う場合は、必ず事前にバックアップを取ってから使用してください。
