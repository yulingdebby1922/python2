from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
import shutil
import subprocess
from glob import glob

app = Flask(__name__)
input_dir = "./pdf"  # 放置 PDF 的資料夾
output_dir = "./output"
cache_dir = "/home/runner/.cache/unstructured/ingest/pipeline"

# 初始化資料夾
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(input_dir, file.filename)
        file.save(file_path)
        process_pdf(file_path)
        return redirect(url_for('download_files'))

    return redirect(url_for('index'))

def process_pdf(pdf_file):
    # 清除快取和輸出資料夾
    for folder in [cache_dir, output_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

    # 使用 unstructured-ingest 進行處理
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
        print(f"轉檔失敗：{e.stderr}")

@app.route('/download')
def download_files():
    files = os.listdir(output_dir)
    return render_template('download.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
