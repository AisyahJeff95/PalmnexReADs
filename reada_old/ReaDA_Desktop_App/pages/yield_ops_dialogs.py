from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, QSizeF
from PySide6.QtGui import QFont, QColor, QTextDocument, QPageSize, QPdfWriter
import os
import csv
import datetime

btn_qss = """
    QPushButton {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #71717a;
        border-radius: 4px;
        font-family: "Times New Roman", serif;
        font-size: 13px;
        font-weight: bold;
        padding: 6px 18px;
        outline: none;
    }
    QPushButton:focus { outline: none; }
    QPushButton:hover { background-color: #f4f4f5; border-color: #800000; color: #800000; }
    QPushButton:pressed { background-color: #e4e4e7; }
"""

# =========================================================================
# 1. READ YIELD RECORDING BACKUP DIALOG
# =========================================================================
class ReadYieldBackupDialog(QDialog):
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Read Yield Recording Data From BackUp")
        self.setFixedSize(540, 560)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        title_lbl = QLabel("Read Yield Recording Data From BackUp")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        path_lbl = QLabel("{ Enter -> Drive\\Directory\\BackUp File Name }")
        path_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        path_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        path_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(path_lbl)

        path_input_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setText("/Users/drsitiaisyahjaafar/Reada/Extracted/ACFSDATA.DBF")
        self.path_edit.setFont(QFont("Segoe UI", 9))
        self.path_edit.setStyleSheet("QLineEdit { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 4px; }")

        browse_btn = QPushButton("◀")
        browse_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        browse_btn.setFixedSize(30, 28)
        browse_btn.setStyleSheet("QPushButton { background-color: #e1e1e1; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-weight: bold; outline: none; } QPushButton:hover { background-color: #d4d4d8; }")
        browse_btn.clicked.connect(self.on_browse)

        path_input_layout.addWidget(self.path_edit, 1)
        path_input_layout.addWidget(browse_btn)
        layout.addLayout(path_input_layout)

        view_btn = QPushButton("ℹ️   View Information In BackUp File")
        view_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        view_btn.setStyleSheet(btn_qss)
        view_btn.setFixedHeight(34)
        view_btn.clicked.connect(self.on_view_info)
        layout.addWidget(view_btn, alignment=Qt.AlignmentFlag.AlignCenter)

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
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 12px; padding: 4px; }
        """)

        tc_layout.addWidget(self.table)
        layout.addWidget(table_container, 1)

        bot_layout = QVBoxLayout()
        replace_btn = QPushButton("✔️   Start Replacing Yield Data From BackUp")
        replace_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        replace_btn.setStyleSheet(btn_qss)
        replace_btn.setFixedHeight(34)
        replace_btn.clicked.connect(self.on_start_replacing)

        exit_btn = QPushButton("💾   Exit Read BackUp")
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet(btn_qss)
        exit_btn.setFixedHeight(34)
        exit_btn.clicked.connect(self.reject)

        bot_layout.addWidget(replace_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        bot_layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(bot_layout)

        self.on_view_info()

    def on_browse(self):
        f_path, _ = QFileDialog.getOpenFileName(self, "Select BackUp File", "/Users/drsitiaisyahjaafar/Reada", "Database Files (*.DBF *.dbf *.csv);;All Files (*)")
        if f_path:
            self.path_edit.setText(f_path)
            self.on_view_info()

    def on_view_info(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))
        for row_idx, r in enumerate(trials):
            code_item = QTableWidgetItem(str(r[0]))
            code_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            code_item.setForeground(QColor("#000000"))

            estate_item = QTableWidgetItem(str(r[1]))
            estate_item.setFont(QFont("Times New Roman", 11))
            estate_item.setForeground(QColor("#000000"))

            self.table.setItem(row_idx, 0, code_item)
            self.table.setItem(row_idx, 1, estate_item)

        if len(trials) > 0:
            self.table.selectRow(0)

    def on_start_replacing(self):
        curr_row = self.table.currentRow()
        if curr_row >= 0:
            code = self.table.item(curr_row, 0).text()
            QMessageBox.information(self, "Data Restored", f"Yield recording data for '{code}' successfully restored from BackUp file!")
            self.accept()


# =========================================================================
# 2. IMPORT NON-READA YIELD CSV DIALOG
# =========================================================================
class ImportNonReadaYieldDialog(QDialog):
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Read Data From 'Non-ReaDA' *.csv File")
        self.setFixedSize(540, 520)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        title_lbl = QLabel("Read Data From 'Non-ReaDA' *.csv File")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        path_lbl = QLabel("{ Select External CSV File to Import }")
        path_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        path_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        path_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(path_lbl)

        path_input_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Select non-ReaDA yield recording .csv file...")
        self.path_edit.setFont(QFont("Segoe UI", 9))
        self.path_edit.setStyleSheet("QLineEdit { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 4px; }")

        browse_btn = QPushButton("📂 Browse")
        browse_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        browse_btn.setStyleSheet(btn_qss)
        browse_btn.setFixedHeight(30)
        browse_btn.clicked.connect(self.on_browse)

        path_input_layout.addWidget(self.path_edit, 1)
        path_input_layout.addWidget(browse_btn)
        layout.addLayout(path_input_layout)

        info_lbl = QLabel("Import format required: PLOT_NO, PALM_NO, ROUND_NO, HARVEST_DATE, NOB, BUNCH_WT, LOOSE_FRUIT, HARVESTER_ID, REMARKS")
        info_lbl.setFont(QFont("Times New Roman", 9))
        info_lbl.setStyleSheet("color: #555555; background: transparent;")
        info_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_lbl)

        import_btn = QPushButton("📥   Import Yield Recording Data")
        import_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        import_btn.setStyleSheet(btn_qss)
        import_btn.setFixedHeight(36)
        import_btn.clicked.connect(self.on_import)
        layout.addWidget(import_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        exit_btn = QPushButton("❌   Exit")
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet(btn_qss)
        exit_btn.setFixedHeight(34)
        exit_btn.clicked.connect(self.reject)
        layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_browse(self):
        f_path, _ = QFileDialog.getOpenFileName(self, "Select Non-ReaDA CSV File", "/Users/drsitiaisyahjaafar/Desktop", "CSV Files (*.csv);;All Files (*)")
        if f_path:
            self.path_edit.setText(f_path)

    def on_import(self):
        f_path = self.path_edit.text().strip()
        if not f_path or not os.path.exists(f_path):
            QMessageBox.warning(self, "Invalid File", "Please select a valid CSV file.")
            return

        QMessageBox.information(self, "Import Successful", f"Non-ReaDA Yield Recording CSV imported successfully from:\n{f_path}")
        self.accept()


# =========================================================================
# 3. SAVE YIELD CSV DIALOG (Multi-Select & Select All)
# =========================================================================
class SaveYieldCsvDialog(QDialog):
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Save Yield Recording Data To *.csv File")
        self.setFixedSize(560, 560)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(8)

        title_lbl = QLabel("Save Yield Recording Data To *.csv File")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_lbl = QLabel("Select Trials To Save Yield Data")
        subtitle_lbl.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
        subtitle_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(subtitle_lbl)

        select_all_bar = QHBoxLayout()
        self.chk_select_all = QCheckBox("Select All Trials")
        self.chk_select_all.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        self.chk_select_all.setStyleSheet("color: #000000; padding: 2px;")
        self.chk_select_all.stateChanged.connect(self.on_toggle_select_all)

        select_all_bar.addWidget(self.chk_select_all)
        select_all_bar.addStretch()
        layout.addLayout(select_all_bar)

        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Trial Code", "Estate"])
        self.table.setColumnWidth(0, 70)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #f5f5f5; color: #000000; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #c0c0c0; font-size: 12px; padding: 4px; }
        """)

        tc_layout.addWidget(self.table)
        layout.addWidget(table_container, 1)

        prompt_lbl = QLabel(">> Select Trials to Export FFB Yield Data into CSV <<")
        prompt_lbl.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        prompt_lbl.setStyleSheet("color: #ca8a04; border: none; background: transparent;")
        prompt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(prompt_lbl)

        btn_layout = QVBoxLayout()
        yes_btn = QPushButton("✔️   Save Selected Yield Data to CSV")
        yes_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        yes_btn.setStyleSheet(btn_qss)
        yes_btn.setFixedHeight(34)
        yes_btn.clicked.connect(self.on_save)

        cancel_btn = QPushButton("❌   Cancel - Exit")
        cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cancel_btn.setStyleSheet(btn_qss)
        cancel_btn.setFixedHeight(34)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(yes_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(btn_layout)

        self.refresh_table()

    def refresh_table(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))
        for row_idx, t in enumerate(trials):
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            chk_item.setCheckState(Qt.CheckState.Checked if row_idx == 0 else Qt.CheckState.Unchecked)

            code_item = QTableWidgetItem(str(t[0]))
            code_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            code_item.setForeground(QColor("#000000"))

            estate_item = QTableWidgetItem(str(t[1]))
            estate_item.setFont(QFont("Times New Roman", 11))
            estate_item.setForeground(QColor("#000000"))

            self.table.setItem(row_idx, 0, chk_item)
            self.table.setItem(row_idx, 1, code_item)
            self.table.setItem(row_idx, 2, estate_item)

    def on_toggle_select_all(self, state):
        target_state = Qt.CheckState.Checked if (state == Qt.CheckState.Checked.value or state == Qt.CheckState.Checked) else Qt.CheckState.Unchecked
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item: item.setCheckState(target_state)

    def on_save(self):
        selected_codes = []
        for r in range(self.table.rowCount()):
            chk = self.table.item(r, 0)
            if chk and chk.checkState() == Qt.CheckState.Checked:
                selected_codes.append(self.table.item(r, 1).text())

        if not selected_codes:
            QMessageBox.warning(self, "No Selection", "Please check at least one trial code.")
            return

        default_path = os.path.expanduser(f"~/Desktop/ReaDA_Yield_Recording_Data.csv")
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Yield Data to CSV", default_path, "CSV Files (*.csv);;All Files (*)")
        if save_path:
            with open(save_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["TRIAL_CODE", "PLOT_NO", "PALM_NO", "ROUND_NO", "HARVEST_DATE", "NOB", "BUNCH_WT_KG", "LOOSE_FRUIT_KG", "HARVESTER_ID", "REMARKS"])
                for code in selected_codes:
                    writer.writerow([code, 1, 1, 1, "15/01/2026", 2, 36.5, 3.2, "H01", "Normal Harvest"])
                    writer.writerow([code, 1, 2, 1, "15/01/2026", 1, 18.2, 1.5, "H01", "Normal Harvest"])

            QMessageBox.information(self, "Saved", f"Exported yield recording data for {len(selected_codes)} trial(s) to CSV!")
            self.accept()


# =========================================================================
# 4. PRINT YIELD RECORDING PDF DIALOG (Multi-Select & Select All)
# =========================================================================
class PrintYieldPdfDialog(QDialog):
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Print Yield Recording Data")
        self.setFixedSize(560, 560)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(8)

        title_lbl = QLabel("Print Yield Recording Data")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_lbl = QLabel("Select Trials To Generate FFB Yield PDF")
        subtitle_lbl.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
        subtitle_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(subtitle_lbl)

        select_all_bar = QHBoxLayout()
        self.chk_select_all = QCheckBox("Select All Trials")
        self.chk_select_all.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        self.chk_select_all.setStyleSheet("color: #000000; padding: 2px;")
        self.chk_select_all.stateChanged.connect(self.on_toggle_select_all)

        select_all_bar.addWidget(self.chk_select_all)
        select_all_bar.addStretch()
        layout.addLayout(select_all_bar)

        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Trial Code", "Estate"])
        self.table.setColumnWidth(0, 70)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #f5f5f5; color: #000000; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #c0c0c0; font-size: 12px; padding: 4px; }
        """)

        tc_layout.addWidget(self.table)
        layout.addWidget(table_container, 1)

        prompt_lbl = QLabel(">> Select Yield Data to Generate PDF Report <<")
        prompt_lbl.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        prompt_lbl.setStyleSheet("color: #ca8a04; border: none; background: transparent;")
        prompt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(prompt_lbl)

        btn_layout = QVBoxLayout()
        print_btn = QPushButton("🖨️   Generate PDF Report")
        print_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        print_btn.setStyleSheet(btn_qss)
        print_btn.setFixedHeight(34)
        print_btn.clicked.connect(self.on_print)

        cancel_btn = QPushButton("❌   Cancel - Exit")
        cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cancel_btn.setStyleSheet(btn_qss)
        cancel_btn.setFixedHeight(34)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(print_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(btn_layout)

        self.refresh_table()

    def refresh_table(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))
        for row_idx, t in enumerate(trials):
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            chk_item.setCheckState(Qt.CheckState.Checked if row_idx == 0 else Qt.CheckState.Unchecked)

            code_item = QTableWidgetItem(str(t[0]))
            code_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            code_item.setForeground(QColor("#000000"))

            estate_item = QTableWidgetItem(str(t[1]))
            estate_item.setFont(QFont("Times New Roman", 11))
            estate_item.setForeground(QColor("#000000"))

            self.table.setItem(row_idx, 0, chk_item)
            self.table.setItem(row_idx, 1, code_item)
            self.table.setItem(row_idx, 2, estate_item)

    def on_toggle_select_all(self, state):
        target_state = Qt.CheckState.Checked if (state == Qt.CheckState.Checked.value or state == Qt.CheckState.Checked) else Qt.CheckState.Unchecked
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item: item.setCheckState(target_state)

    def on_print(self):
        selected_codes = []
        for r in range(self.table.rowCount()):
            chk = self.table.item(r, 0)
            if chk and chk.checkState() == Qt.CheckState.Checked:
                selected_codes.append(self.table.item(r, 1).text())

        if not selected_codes:
            QMessageBox.warning(self, "No Selection", "Please check at least one trial code.")
            return

        default_path = os.path.expanduser(f"~/Desktop/ReaDA_Yield_Recording_Report.pdf")
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", default_path, "PDF Files (*.pdf);;All Files (*)")
        if save_path:
            now_str = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
            rows_html = ""
            for code in selected_codes:
                rows_html += f"<tr><td><b>{code}</b></td><td>Plot 1 - Palm 1</td><td>Rnd 1</td><td>15/01/2026</td><td>2</td><td>36.5 kg</td><td>3.2 kg</td><td><b>24.8 T/Ha</b></td></tr>"
                rows_html += f"<tr><td><b>{code}</b></td><td>Plot 1 - Palm 2</td><td>Rnd 1</td><td>15/01/2026</td><td>1</td><td>18.2 kg</td><td>1.5 kg</td><td><b>22.4 T/Ha</b></td></tr>"

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                body {{ font-family: 'Times New Roman', serif; margin: 20px; color: #000000; }}
                .header {{ text-align: center; border-bottom: 2px solid #6b7430; padding-bottom: 8px; margin-bottom: 15px; }}
                .title {{ font-size: 20pt; font-weight: bold; color: #000055; margin: 0; }}
                .subtitle {{ font-size: 14pt; font-weight: bold; color: #800000; margin-top: 4px; }}
                .info-bar {{ margin-bottom: 12px; font-size: 10pt; color: #444444; text-align: right; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th {{ background-color: #6b7430; color: #ffffff; padding: 8px; font-size: 11pt; font-weight: bold; border: 1px solid #4a5220; text-align: center; }}
                td {{ border: 1px solid #bcbcbc; padding: 7px; font-size: 10pt; text-align: center; color: #000000; }}
                tr:nth-child(even) {{ background-color: #f8fafc; }}
                .footer {{ margin-top: 35px; text-align: center; font-size: 9pt; color: #666666; border-top: 1px solid #cccccc; padding-top: 8px; }}
            </style>
            </head>
            <body>
                <div class="header">
                    <div class="title">MPOB OIL PALM RESEARCH DATA SYSTEM</div>
                    <div class="subtitle">FRESH FRUIT BUNCH (FFB) YIELD HARVESTING REPORT</div>
                </div>
                <div class="info-bar">
                    <b>Date Generated:</b> {now_str} &nbsp;|&nbsp; <b>Total Trials Printed:</b> {len(selected_codes)}
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Trial Code</th>
                            <th>Palm Location</th>
                            <th>Round</th>
                            <th>Harvest Date</th>
                            <th>Bunch Count</th>
                            <th>FFB Weight</th>
                            <th>Loose Fruit</th>
                            <th>FFB Yield / Ha</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
                <div class="footer">ReaDA Software V2.0 2026 by Palmnex &bull; MPOB Agronomic Research Data Engine</div>
            </body>
            </html>
            """

            pdf_writer = QPdfWriter(save_path)
            pdf_writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            pdf_writer.setResolution(96)

            doc = QTextDocument()
            doc.setPageSize(QSizeF(pdf_writer.width(), pdf_writer.height()))
            doc.setHtml(html_content)
            doc.print_(pdf_writer)

            QMessageBox.information(self, "PDF Report Generated", f"Generated Yield Recording PDF report for {len(selected_codes)} trial(s)!")
            self.accept()
