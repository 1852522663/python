# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QPlainTextEdit

download_records = []
max_displayed_records = 3  # 最多显示的记录数
# 函数用于检查目录权限和启动下载
def check_directory_permission(url):
    global download_records  # 使用全局变量

    cmd = "you-get -i {}".format(url)
    if sys.version_info >= (3, 5):
        # 运行外部命令并捕获输出（Python 3.5+）
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout
    else:
        # 运行外部命令并获取输出（Python 3.5以下版本）
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = process.communicate()
        output = output.decode('utf-8')

    # 使用正则表达式提取信息
    pattern = r"format:\s+(?P<format>[\w-]+)\n\s+container:\s+(?P<container>\w+)\n\s+quality:\s+(?P<quality>.+)\n\s+size:\s+(?P<size>[\d.]+ \w+)"
    print(output)  # 输出获取的视频信息
    matches = re.findall(pattern, output)

    print(matches)
    streams = []
    for match in matches:
        stream = {
            "format": match[0],
            "container": match[1],
            "quality": match[2],
            "size": match[3]
        }
        streams.append(stream)

    def compare_size(stream):
        size_str = stream["size"]
        size = float(re.search(r"([\d.]+)", size_str).group())
        return size

    # 在 streams 列表中找到 container 为 "mp4" 并且 size 最大的项
    filtered_streams = [stream for stream in streams if stream["container"] == "mp4"]
    print(filtered_streams)
    if not filtered_streams:
        print("没有找到符合条件的视频流。")
    else:
        max_size_stream = max(filtered_streams, key=compare_size)
        desktop_path = os.path.expanduser("~/Desktop")
        format_value = max_size_stream["format"]
        cmd = "you-get -o {} --format={} {}".format(desktop_path, format_value, url)
        print('下载开始:' + cmd)
        if sys.version_info >= (3, 5):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            output = result.stdout
        else:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            output = output.decode('utf-8')
        print('下载完成')

        # 将下载信息添加到下载记录列表
        download_records.append(cmd)
        update_download_records_label()  # 更新下载记录显示
        url_input.clear()  # 清空输入框

# 函数用于更新下载记录标签

def update_download_records_label():
    global download_records

    # 显示最多 max_displayed_records 条记录，每条记录都定格展示
    formatted_records = "\n-------------------------------------------------------\n".join([f"{i+1}. {record}" for i, record in enumerate(download_records[-max_displayed_records:])])
    records_textbox.setPlainText(formatted_records)



# 函数用于处理按钮点击事件
def on_button_click():
    url = url_input.text()
    check_directory_permission(url)
    # 检查记录数量，如果超过最大显示数则减少显示的记录数
    if len(download_records) > max_displayed_records:
        update_download_records_label()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("视频下载")
window.setGeometry(100, 100, 400, 200)

layout = QVBoxLayout()

url_input = QLineEdit()
url_input.setPlaceholderText("请输入视频的URL")
layout.addWidget(url_input)

button = QPushButton("开始下载")
button.clicked.connect(on_button_click)
layout.addWidget(button)

initial_window_height = 100 + max_displayed_records * 30
window.setFixedHeight(initial_window_height)


records_textbox = QPlainTextEdit()
records_textbox.setReadOnly(True)  # 设置为只读，用户可以复制文本
layout.addWidget(records_textbox)


window.setLayout(layout)
window.show()

sys.exit(app.exec_())