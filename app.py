from flask import Flask, render_template, send_from_directory, url_for
import os
from datetime import datetime
import math

app = Flask(__name__)

# 文件存储的根目录，这里设置为当前目录下的 files 文件夹
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 将字节大小转换为可读的字符串
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

# 获取文件或目录的类型
def get_item_type(path):
    if os.path.isfile(path):
        return 'file'
    elif os.path.isdir(path):
        return 'directory'
    else:
        return 'unknown'

# 获取文件或目录的大小
def get_item_size(path):
    if os.path.isfile(path):
        return convert_size(os.path.getsize(path))
    else:
        return '-'

# 获取文件或目录的修改日期
def get_item_modified(path):
    modified_timestamp = os.path.getmtime(path)
    return datetime.fromtimestamp(modified_timestamp).strftime('%Y-%m-%d %H:%M:%S')

# 显示文件列表和基本信息
@app.route('/')
def file_list():
    return browse('')

# 进入子目录
@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse(subpath=''):
    # 处理根路径的情况
    if not subpath:
        directory = UPLOAD_FOLDER
        current_path = '/'
    else:
        # 处理子目录的情况
        directory = os.path.join(UPLOAD_FOLDER, subpath)
        current_path = '/' + subpath
    
    items = []
    
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        item_type = get_item_type(full_path)
        if item_type == 'file':
            items.append({
                'name': item,
                'type': 'file',
                'size': get_item_size(full_path),
                'modified': get_item_modified(full_path),
                'url': url_for('download', filename=item)
            })
        elif item_type == 'directory':
            items.append({
                'name': item,
                'type': 'directory'
            })
    
    return render_template('index.html', items=items, current_path=current_path)

# 下载文件
@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

