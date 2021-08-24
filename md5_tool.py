# -*- coding: utf-8 -*-

"""
File MD5 compute tool

author: Chen Zhao
last edited: 2021/8/24
"""

import sys
import os
from PyQt5.QtCore import pyqtSlot, QMetaObject
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QTextEdit,
    QPushButton, QFileDialog, QProgressBar, QMessageBox, QApplication)
import hashlib
from datetime import datetime


Algorithm = {
    "md5": {
        "obj": None,
        "digest": None,
    },
    "sha1": {
        "obj": None,
        "digest": None,
    },
    "sha256": {
        "obj": None,
        "digest": None,
    },
}


class MD5UI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.content = ""
        self.block_size = 1 * 1024 * 1024
        self.default_dir = os.path.expanduser('~')
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        self.grid = QGridLayout()
        # self.setLayout(self.grid)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.grid.addWidget(self.textEdit, 1, 0, 1, 4)

        self.filebutton = QPushButton(self.centralWidget)
        self.filebutton.setObjectName("filebutton")
        self.filebutton.setText("打开文件")
        self.grid.addWidget(self.filebutton, 2, 0)
        self.clearbutton = QPushButton(self.centralWidget)
        self.clearbutton.setObjectName("clear")
        self.clearbutton.setText("清除")
        self.grid.addWidget(self.clearbutton, 2, 1)
        self.copybutton = QPushButton(self.centralWidget)
        self.copybutton.setObjectName("copy")
        self.copybutton.setText("复制")
        self.grid.addWidget(self.copybutton, 2, 2)
        self.savebutton = QPushButton(self.centralWidget)
        self.savebutton.setObjectName("save")
        self.savebutton.setText("保存")
        self.grid.addWidget(self.savebutton, 2, 3)

        self.pbar = QProgressBar(self.centralWidget)
        self.grid.addWidget(self.pbar, 3, 0, 1, 4)
        self.pbar.setValue(0)

        self.centralWidget.setLayout(self.grid)

        self.setCentralWidget(self.centralWidget)

        QMetaObject.connectSlotsByName(self)

        self.setGeometry(100, 100, 700, 400)
        self.setWindowTitle('MD5工具')
        self.show()

    @pyqtSlot()
    def on_filebutton_clicked(self):
        fname, filetype = QFileDialog.getOpenFileName(self, 'Open file', self.default_dir)
        if not fname:
            return
        try:
            stat_result = os.stat(fname)
            size = stat_result.st_size
            mtime = Common.time2str(stat_result.st_mtime)
            for agm in Algorithm:
                Algorithm[agm]["obj"] = hashlib.__dict__[agm]()
            m = hashlib.md5()
            count = 0
            with open(fname, 'rb') as fr:
                while True:
                    data = fr.read(self.block_size)
                    if not data:
                        break
                    for agm in Algorithm:
                        Algorithm[agm]["obj"].update(data)
                    m.update(data)
                    count += self.block_size
                    self.update_pbar(count, size)
            digest = ""
            for agm in Algorithm:
                d = Algorithm[agm]["obj"].hexdigest()
                digest += f"{agm.upper()}: {d}\n"
            self.content += f"文件：{fname}\n" \
                            f"大小: {size:,} 字节\n" \
                            f"修改时间: {mtime}\n" \
                            f"{digest}\n"
            self.textEdit.setText(self.content)
            self.default_dir = os.path.split(fname)[0]
        except Exception as ex:
            QMessageBox.warning(self, '异常', f"读取文件失败：{ex}")

    @pyqtSlot()
    def on_clear_clicked(self):
        self.textEdit.clear()

    @pyqtSlot()
    def on_copy_clicked(self):
        self.textEdit.selectAll()
        self.textEdit.copy()

    @pyqtSlot()
    def on_save_clicked(self):
        fname, filetype = QFileDialog.getSaveFileName(self, 'Open file', self.default_dir, "TXT Files (*.txt)")
        if not fname:
            return
        try:
            with open(fname, "w") as fw:
                fw.write(self.content)
        except Exception as ex:
            QMessageBox.warning(self, '异常', f"写文件失败：{ex}")

    def update_pbar(self, size, total):
        rate = size / total * 100
        rate = min(100, rate)
        self.pbar.setValue(rate)


class Common():
    @staticmethod
    def time2str(timestamp, format="%Y-%m-%d %H:%M:%S"):
        return datetime.fromtimestamp(timestamp).strftime(format)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MD5UI()
    sys.exit(app.exec_())