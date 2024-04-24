import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLineEdit, QTableView, QFileDialog, QFontDialog,
                               QStyledItemDelegate, QMenu, QHeaderView, QStyleOptionViewItem)
from PySide6.QtGui import QFont, QAction
from PySide6.QtCore import Qt, QPoint
from log_reader import LogReader
from log_filter import LogFilter
from log_table_model import LogTableModel


class MessageDelegate(QStyledItemDelegate):
    def __init__(self, message_column_index):
        super().__init__()
        self.message_column_index = message_column_index

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.column() == self.message_column_index:
            option.wrapText = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_button = None
        self.change_font_button = None
        self.filter_level = None
        self.filter_name = None
        self.filter_button = None
        self.table = None
        self.data_frame = None
        self.model = None
        self.column_menu_button = None
        self.message_column_index = None
        self.setWindowTitle("Log Viewer")
        self.setup_ui()
        self.custom_font = QFont("Sarasa Mono SC", 10)  # Default monospace font
        self.resize(1440, 900)

    def setup_ui(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        self.load_button = QPushButton("载入日志")
        self.load_button.clicked.connect(self.load_log)

        self.change_font_button = QPushButton("更改字体")
        self.change_font_button.clicked.connect(self.change_font)

        self.filter_level = QLineEdit()
        self.filter_level.setPlaceholderText("根据级别过滤")

        self.filter_name = QLineEdit()
        self.filter_name.setPlaceholderText("根据名称过滤")

        self.filter_button = QPushButton("应用过滤")
        self.filter_button.clicked.connect(self.filter_log)

        self.column_menu_button = QPushButton("选择列")
        self.column_menu_button.clicked.connect(self.show_column_menu)

        btn_layout.addWidget(self.load_button)
        btn_layout.addWidget(self.change_font_button)
        btn_layout.addWidget(self.filter_level)
        btn_layout.addWidget(self.filter_name)
        btn_layout.addWidget(self.filter_button)
        btn_layout.addWidget(self.column_menu_button)

        layout.addLayout(btn_layout)

        self.table = QTableView()
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # 行高根据内容自动调整
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # 列宽自适应
        layout.addWidget(self.table)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_log(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "打开日志文件", "", "JSON Lines (*.jsonl);;所有文件 (*)")
        if filepath:
            reader = LogReader(filepath)
            self.data_frame = reader.read_logs()
            self.model = LogTableModel(self.data_frame)
            self.table.setModel(self.model)
            self.update_table_font()

            try:
                message_index = self.model.column_names().index('message')
                self.table.setItemDelegateForColumn(message_index, MessageDelegate(message_index))
                self.table.setColumnWidth(message_index, 960)  # 为 "message" 列设置宽度
            except ValueError:
                print("No 'message' column found in the data")

    def change_font(self):
        # QFontDialog.getFont 需要一个有效的 QFont 对象作为参数
        ok, font = QFontDialog.getFont(self.custom_font, self)
        if ok:
            self.custom_font = font
            self.update_table_font()

    def update_table_font(self):
        if self.table.model():  # 只有当表格有模型时才设置字体
            self.table.setFont(self.custom_font)

    def filter_log(self):
        level = self.filter_level.text()
        name = self.filter_name.text()
        filtered_data = LogFilter.filter_logs(self.data_frame, level, name)
        self.table.setModel(LogTableModel(filtered_data))
        self.table.setFont(self.custom_font)

    def show_column_menu(self):
        menu = QMenu()

        for i in range(self.table.model().columnCount()):
            action = QAction(self.table.model().headerData(i, Qt.Orientation.Horizontal), self)
            action.setCheckable(True)
            action.setChecked(not self.table.isColumnHidden(i))
            action.toggled.connect(lambda visible, col=i: self.table.setColumnHidden(col, not visible))
            menu.addAction(action)
        menu.exec(self.column_menu_button.mapToGlobal(QPoint(0, self.column_menu_button.height())))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
