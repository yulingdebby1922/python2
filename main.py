import os
import shutil
import subprocess
from glob import glob

# 指定目錄並尋找所有 PDF 檔案
input_dir = "./pdf"  # 放置 PDF 的資料夾
output_dir = "./output"
cache_dir = "/home/runner/.cache/unstructured/ingest/pipeline"

# 清除快取和輸出資料夾
for folder in [cache_dir, output_dir]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"{folder} 已清除。")
    os.makedirs(folder, exist_ok=True)

# 顯示 pdfs 資料夾中的檔案
print(f"檢查 {input_dir} 資料夾中的檔案...")
all_files = os.listdir(input_dir)
print(f"找到以下檔案：{all_files}")

# 尋找 PDF 檔案
pdf_files = glob(os.path.join(input_dir, "*.pdf"))

if not pdf_files:
    print("沒有找到任何 PDF 檔案。請確認檔案已上傳至正確的資料夾。")
    exit(1)

# 處理每一個 PDF 檔案
for pdf_file in pdf_files:
    print(f"正在處理檔案：{pdf_file}")

    command = [
        "unstructured-ingest", "local",
        "--input-path", pdf_file,
        "--output-dir", output_dir,
        "--reprocess",
        "--skip-infer-table-types", "true"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("成功轉檔！")
        print(f"CLI 工具輸出內容（stdout）：\n{result.stdout}")
        print(f"CLI 工具錯誤內容（stderr）：\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print("轉檔失敗。")
        print(f"錯誤訊息：\n{e.stderr}")

# 列出輸出資料夾的內容
files = os.listdir(output_dir)
if files:
    print("輸出資料夾的檔案：")
    for f in files:
        print(f"- {f}")
else:
    print("輸出資料夾中沒有任何檔案。")
