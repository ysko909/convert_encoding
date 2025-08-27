import os
import sys
import glob
import argparse
from pathlib import Path


def detect_encoding(file_path):
    """ファイルのエンコーディングを検出する"""
    encodings = ['utf-8', 'shift_jis', 'cp932', 'euc-jp', 'iso-2022-jp']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    
    return None


def convert_file_encoding(input_file, from_encoding, to_encoding, overwrite=False, quiet=False):
    """ファイルのエンコーディングを変換する"""
    try:
        # ファイルを読み込み
        with open(input_file, 'r', encoding=from_encoding) as f:
            content = f.read()
        
        if overwrite:
            # 元ファイルを上書き
            output_file = input_file
        else:
            # 新規ファイルを作成
            input_path = Path(input_file)
            if to_encoding.lower() == 'utf-8':
                suffix = '_utf-8'
            elif to_encoding.lower() in ['shift_jis', 'sjis', 'cp932']:
                suffix = '_sjis'
            else:
                suffix = f'_{to_encoding.lower()}'
            
            output_file = input_path.parent / f"{input_path.stem}{suffix}{input_path.suffix}"
        
        # ファイルを書き込み
        with open(output_file, 'w', encoding=to_encoding) as f:
            f.write(content)
        
        if not quiet:
            print(f"変換完了: {input_file} -> {output_file}")
            print(f"  {from_encoding} -> {to_encoding}")
        return True
        
    except Exception as e:
        if not quiet:
            print(f"エラー: {input_file} の変換に失敗しました - {str(e)}")
        return False


def get_target_files(path, quiet=False):
    """指定されたパスからtxtファイルとmdファイルのリストを取得する"""
    target_files = []
    non_target_files = []
    valid_exts = ['.txt', '.md']
    
    if os.path.isfile(path):
        # ファイルが指定された場合
        if Path(path).suffix.lower() in valid_exts:
            target_files.append(path)
        else:
            non_target_files.append(path)
            if not quiet:
                print(f"警告: {path} は.txtまたは.mdファイルではありません。スキップします。")
    elif os.path.isdir(path):
        # フォルダが指定された場合
        all_files = glob.glob(os.path.join(path, '*'))
        for file in all_files:
            if os.path.isfile(file):
                if Path(file).suffix.lower() in valid_exts:
                    target_files.append(file)
                else:
                    non_target_files.append(file)
        
        # 非対象ファイルの警告（quietモードでない場合のみ）
        if not quiet and non_target_files:
            print(f"警告: {len(non_target_files)}個の非.txt/.mdファイルをスキップしました。")
            # ファイル数が多い場合は個別表示を制限
            if len(non_target_files) <= 5:
                for file in non_target_files:
                    print(f"  スキップ: {file}")
            else:
                for file in non_target_files[:3]:
                    print(f"  スキップ: {file}")
                print(f"  ... その他 {len(non_target_files) - 3} ファイル")
        
        if not target_files:
            if not quiet:
                print(f"警告: {path} に.txtまたは.mdファイルが見つかりませんでした。")
    else:
        if not quiet:
            print(f"エラー: {path} は存在しないパスです。")
    
    return target_files


def main():
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(
        description='テキストファイルのエンコード変換スクリプト',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python convert_encoding.py sample.txt                 # SJIS→UTF-8、新規ファイル作成
  python convert_encoding.py ./text_files/              # フォルダ内の全txtファイルとmdファイルを変換
  python convert_encoding.py sample.txt -r              # UTF-8→SJIS変換
  python convert_encoding.py sample.txt -o              # 元ファイルを上書き
  python convert_encoding.py sample.txt -r -o           # UTF-8→SJIS、上書き
  python convert_encoding.py ./mixed_files/ -q          # 静寂モード（エラーメッセージ非表示）
        """
    )
    
    parser.add_argument(
        'path',
        help='変換対象のファイルまたはフォルダパス'
    )
    
    parser.add_argument(
        '-r', '--reverse',
        action='store_true',
        help='UTF-8→SJIS変換（省略時はSJIS→UTF-8）'
    )
    
    parser.add_argument(
        '-o', '--overwrite',
        action='store_true',
        help='元ファイルを上書き（省略時は新規ファイル作成）'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='エラーメッセージと警告メッセージを非表示にする'
    )
    
    # 引数の解析
    args = parser.parse_args()
    
    target_path = args.path
    reverse_mode = args.reverse
    overwrite_mode = args.overwrite
    quiet_mode = args.quiet
    
    # エンコーディングの設定
    if reverse_mode:
        from_encoding = 'utf-8'
        to_encoding = 'shift_jis'
        if not quiet_mode:
            print("変換モード: UTF-8 → SJIS")
    else:
        from_encoding = 'shift_jis'
        to_encoding = 'utf-8'
        if not quiet_mode:
            print("変換モード: SJIS → UTF-8")
    
    # ファイル処理モードの表示
    if not quiet_mode:
        if overwrite_mode:
            print("ファイル処理: 元ファイルを上書き")
        else:
            print("ファイル処理: 新規ファイルを作成")
        
        if quiet_mode:
            print("出力モード: 静寂モード（エラーメッセージ非表示）")
        
        print("-" * 50)
    
    # 対象ファイルの取得
    target_files = get_target_files(target_path, quiet_mode)
    if not target_files:
        if not quiet_mode:
            print("変換対象のファイルがありません。")
        sys.exit(1)
    
    # ファイルの変換処理
    success_count = 0
    error_count = 0
    
    for target_file in target_files:
        if not quiet_mode:
            print(f"\n処理中: {target_file}")
        
        # エンコーディング自動検出（参考情報として表示）
        if not quiet_mode:
            detected_encoding = detect_encoding(target_file)
            if detected_encoding:
                print(f"  検出されたエンコーディング: {detected_encoding}")
                
                # 検出されたエンコーディングが変換元と異なる場合は警告
                if detected_encoding.lower() not in [from_encoding.lower(), 'cp932'] and from_encoding.lower() == 'shift_jis':
                    print(f"  警告: 検出されたエンコーディング({detected_encoding})が想定と異なります")
                elif detected_encoding.lower() != from_encoding.lower() and from_encoding.lower() == 'utf-8':
                    print(f"  警告: 検出されたエンコーディング({detected_encoding})が想定と異なります")
        
        # ファイル変換の実行
        if convert_file_encoding(target_file, from_encoding, to_encoding, overwrite_mode, quiet_mode):
            success_count += 1
        else:
            error_count += 1
    
    # 結果の表示
    if not quiet_mode:
        print("\n" + "=" * 50)
        print(f"変換結果: 成功 {success_count}件, エラー {error_count}件")
        print("処理が完了しました。")


if __name__ == "__main__":
    main()
  
