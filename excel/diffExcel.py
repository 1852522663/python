import sys
import pandas as pd
from openpyxl import Workbook
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit, QLabel

class ExcelFileComparatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.full_file_path = None
        self.partial_file_path = None
        self.output_file_path = None
        self.field_name = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Excel文件比较器')
        self.setGeometry(100, 100, 400, 200)

        self.lbl_field_name = QLabel('比较字段名:', self)
        self.txt_field_name = QLineEdit(self)
        self.txt_field_name.setPlaceholderText('输入要比较的字段名')

        self.btn_select_files = QPushButton('选择两个Excel文件', self)
        self.btn_select_files.clicked.connect(self.select_excel_files)

        self.btn_compare = QPushButton('开始比较', self)
        self.btn_compare.clicked.connect(self.compare_excel_files)
        self.btn_compare.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_field_name)
        layout.addWidget(self.txt_field_name)
        layout.addWidget(self.btn_select_files)
        layout.addWidget(self.btn_compare)

        self.setLayout(layout)

    def select_excel_files(self):
        self.full_file_path, _ = QFileDialog.getOpenFileName(self, '选择完整Excel文件')
        self.partial_file_path, _ = QFileDialog.getOpenFileName(self, '选择部分Excel文件')
        self.output_file_path, _ = QFileDialog.getSaveFileName(self, '另存为', filter="Excel文件 (*.xlsx)")

        if self.full_file_path and self.partial_file_path and self.output_file_path:
            self.btn_compare.setEnabled(True)

    def compare_excel_files(self):
        try:
            self.field_name = self.txt_field_name.text()

            if not self.field_name:
                QMessageBox.critical(self, "错误", "请输入要比较的字段名。")
                return

            # 读取Excel文件
            full_file = pd.read_excel(self.full_file_path)
            partial_file = pd.read_excel(self.partial_file_path)

            # 执行差异比较
            merged = pd.merge(full_file, partial_file, on=self.field_name, how='outer', indicator=True)

            # Map merge indicator to descriptive strings
            merged['_merge'] = merged['_merge'].replace({'left_only': 'left', 'right_only': 'right', 'both': 'both'})

            # 创建新的Excel文件并标注差异
            with pd.ExcelWriter(self.output_file_path, engine='openpyxl') as writer:
                merged.to_excel(writer, index=False, sheet_name='差异表')

            QMessageBox.information(self, "成功", f"差异比较完成，并已保存到Excel文件:\n{self.output_file_path}")

        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "未找到文件。请检查文件路径。")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"发生错误: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExcelFileComparatorApp()
    window.show()
    sys.exit(app.exec_())
