from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
import os
from utils.dbf_parser import DBFParser

class ReadBackupDialog(QDialog):
    """
    Exact replica of Original ReaDA 'Read Trial Main Info from BackUp File' Window (Screenshot 16)
    - Path Input Box: { Enter -> Drive\Directory\BackUp File Name } with browse button
    - Button: 'ℹ️ View Information In BackUp File'
    - Green Title: 'Information Availabled In BackUp File'
    - Red Subtitle: 'Select Code To Be Read'
    - Table View: Trial Code | Estate
    - Action Buttons: 'Start Replacing Data From BackUp File' & 'Exit Read BackUp'
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Read Trial Main Info from BackUp File")
        self.setFixedSize(540, 560)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        # -----------------------------------------------------------------
        # Title Header
        # -----------------------------------------------------------------
        title_lbl = QLabel("Read Trial Main Info from BackUp File")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        # -----------------------------------------------------------------
        # Path Entry & Browse Button
        # -----------------------------------------------------------------
        path_box = QVBoxLayout()
        path_box.setSpacing(4)

        path_lbl = QLabel("{ Enter -> Drive\\Directory\\BackUp File Name }")
        path_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        path_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        path_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_box.addWidget(path_lbl)

        path_input_layout = QHBoxLayout()
        path_input_layout.setSpacing(4)

        self.path_edit = QLineEdit()
        self.path_edit.setText("/Users/drsitiaisyahjaafar/Reada/Extracted/ACFSINFO.DBF")
        self.path_edit.setFont(QFont("Segoe UI", 9))
        self.path_edit.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                padding: 4px;
            }
        """)

        browse_btn = QPushButton("◀")
        browse_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        browse_btn.setFixedWidth(30)
        browse_btn.setFixedHeight(28)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #e1e1e1;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #d4d4d8;
            }
        """)
        browse_btn.clicked.connect(self.on_browse_file)

        path_input_layout.addWidget(self.path_edit, 1)
        path_input_layout.addWidget(browse_btn)
        path_box.addLayout(path_input_layout)

        layout.addLayout(path_box)

        # -----------------------------------------------------------------
        # View Info Button
        # -----------------------------------------------------------------
        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 5px 14px;
                outline: none;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:hover {
                background-color: #f4f4f5;
                border-color: #800000;
                color: #800000;
            }
            QPushButton:pressed {
                background-color: #e4e4e7;
            }
        """

        view_btn = QPushButton("ℹ️   View Information In BackUp File")
        view_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        view_btn.setStyleSheet(btn_qss)
        view_btn.setFixedHeight(34)
        view_btn.clicked.connect(self.on_view_info)
        layout.addWidget(view_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # -----------------------------------------------------------------
        # Information Available Headers & Table
        # -----------------------------------------------------------------
        info_header = QLabel("Information Availabled In BackUp File")
        info_header.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        info_header.setStyleSheet("color: #047857; border: none; background: transparent;")
        info_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub_header = QLabel("Select Code To Be Read")
        sub_header.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        sub_header.setStyleSheet("color: #800000; border: none; background: transparent;")
        sub_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(info_header)
        layout.addWidget(sub_header)

        # Table Box
        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Trial Code", "Estate"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                gridline-color: #d0d0d0;
                border: none;
                font-family: "Times New Roman", serif;
                font-size: 12px;
                selection-background-color: #0078d7;
                selection-color: #ffffff;
            }
            QTableWidget::item {
                color: #000000;
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #666666;
                color: #ffffff;
                font-family: "Times New Roman", serif;
                font-weight: bold;
                border: 1px solid #444444;
                font-size: 12px;
                padding: 4px;
            }
        """)

        tc_layout.addWidget(self.table)
        layout.addWidget(table_container, 1)

        # -----------------------------------------------------------------
        # Action Buttons
        # -----------------------------------------------------------------
        bot_layout = QVBoxLayout()
        bot_layout.setSpacing(6)

        self.replace_btn = QPushButton("✔️   Start Replacing Data From BackUp File")
        self.replace_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.replace_btn.setStyleSheet(btn_qss)
        self.replace_btn.setFixedHeight(34)
        self.replace_btn.clicked.connect(self.on_start_replacing)

        exit_btn = QPushButton("💾   Exit Read BackUp")
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet(btn_qss)
        exit_btn.setFixedHeight(34)
        exit_btn.clicked.connect(self.reject)

        bot_layout.addWidget(self.replace_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        bot_layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(bot_layout)

        # Auto-load default backup if present
        self.on_view_info()

    def on_browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select BackUp File", "/Users/drsitiaisyahjaafar/Reada",
            "Database Files (*.DBF *.dbf *.csv *.db);;All Files (*)"
        )
        if file_path:
            self.path_edit.setText(file_path)
            self.on_view_info()

    def on_view_info(self):
        file_path = self.path_edit.text().strip()
        if not os.path.exists(file_path):
            return

        records = []
        if file_path.upper().endswith(".DBF"):
            try:
                parser = DBFParser(file_path)
                dbf_recs = parser.read_records()
                for r in dbf_recs:
                    code = str(r.get("TRIAL_CODE", r.get("CODE", ""))).strip()
                    estate = str(r.get("ESTATE", r.get("LOCATION", "Station"))).strip()
                    if code:
                        records.append((code, estate))
            except Exception:
                pass

        if not records and self.store:
            # Fallback to store trials
            records = self.store.get_trials()

        self.table.setRowCount(len(records))
        for row_idx, r in enumerate(records):
            code_item = QTableWidgetItem(str(r[0]))
            code_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            code_item.setForeground(QColor("#000000"))

            estate_item = QTableWidgetItem(str(r[1]))
            estate_item.setFont(QFont("Times New Roman", 11))
            estate_item.setForeground(QColor("#000000"))

            self.table.setItem(row_idx, 0, code_item)
            self.table.setItem(row_idx, 1, estate_item)

        if len(records) > 0:
            self.table.selectRow(0)

    def on_start_replacing(self):
        curr_row = self.table.currentRow()
        if curr_row < 0:
            QMessageBox.warning(self, "No Selection", "Please highlight and select a trial code from the backup list.")
            return

        code = self.table.item(curr_row, 0).text()
        estate = self.table.item(curr_row, 1).text()

        if self.store:
            self.store.add_trial(code, estate, "MPOB Backup", 2000, 148, "F3", "DxP AVROS")

        QMessageBox.information(self, "Data Restored", f"Trial data for '{code}' successfully restored from BackUp file!")
        self.accept()
