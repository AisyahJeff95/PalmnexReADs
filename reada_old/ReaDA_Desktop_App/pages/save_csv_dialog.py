from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
import os
import csv

class SaveCsvDialog(QDialog):
    """
    Export Trial Information to CSV File readable by Excel (Screenshot 17)
    Enhanced Features:
    - Multi-trial selection with checkboxes to export all selected trials into ONE consolidated CSV table
    - 'Select All Trials' checkbox toggle for fast batch exporting
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("Save Trial Info As *.csv File (Excel)")
        self.setFixedSize(560, 560)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(8)

        # Header Title & Subheader
        title_lbl = QLabel("Save Trial Info As *.csv File (Excel)")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_lbl = QLabel("Select Trials To Be Saved Into Consolidated Table")
        subtitle_lbl.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
        subtitle_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(subtitle_lbl)

        # Select All Control Bar
        select_all_bar = QHBoxLayout()
        self.chk_select_all = QCheckBox("Select All Trials")
        self.chk_select_all.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        self.chk_select_all.setStyleSheet("color: #000000; padding: 2px;")
        self.chk_select_all.stateChanged.connect(self.on_toggle_select_all)

        select_all_bar.addWidget(self.chk_select_all)
        select_all_bar.addStretch()
        layout.addLayout(select_all_bar)

        # Table View: AGRONOMY TRIAL CODE with Checkbox column
        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)
        tc_layout.setSpacing(0)

        banner_lbl = QLabel("AGRONOMY TRIAL CODE LIST")
        banner_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        banner_lbl.setStyleSheet("background-color: #f0f0f0; color: #000000; border-bottom: 1px solid #71717a; padding: 4px;")
        banner_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tc_layout.addWidget(banner_lbl)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Trial Code", "Estate"])
        self.table.setColumnWidth(0, 70)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
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
                background-color: #f5f5f5;
                color: #000000;
                font-family: "Times New Roman", serif;
                font-weight: bold;
                border: 1px solid #c0c0c0;
                font-size: 12px;
                padding: 4px;
            }
        """)

        tc_layout.addWidget(self.table)
        layout.addWidget(table_container, 1)

        # Prompt & Action Buttons
        prompt_lbl = QLabel(">> Select Trials to Export into One Table <<")
        prompt_lbl.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        prompt_lbl.setStyleSheet("color: #ca8a04; border: none; background: transparent;")
        prompt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(prompt_lbl)

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

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)

        yes_btn = QPushButton("✔️   Save Selected Trials to CSV Table")
        yes_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        yes_btn.setStyleSheet(btn_qss)
        yes_btn.setFixedHeight(34)
        yes_btn.clicked.connect(self.on_save_continue)

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
            # Column 0: Checkbox Item
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
        is_checked = (state == Qt.CheckState.Checked.value or state == Qt.CheckState.Checked)
        target_state = Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item:
                item.setCheckState(target_state)

    def on_save_continue(self):
        trials = self.store.get_trials() if self.store else []
        selected_trials = []

        for r in range(self.table.rowCount()):
            chk_item = self.table.item(r, 0)
            if chk_item and chk_item.checkState() == Qt.CheckState.Checked:
                if r < len(trials):
                    selected_trials.append(trials[r])

        if not selected_trials:
            QMessageBox.warning(self, "No Selection", "Please check at least one trial to export.")
            return

        default_path = os.path.expanduser(f"~/Desktop/ReaDA_Consolidated_Trial_Data.csv")

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Selected Trials as Consolidated CSV Table (Excel)", default_path,
            "Excel CSV Files (*.csv);;All Files (*)"
        )

        if save_path:
            try:
                with open(save_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    # Write Header Row
                    writer.writerow(["TRIAL_CODE", "ESTATE", "GROUP_NAME", "PL_YEAR", "PL_DENSITY", "FACTOR_INFO", "PROGENY"])

                    # Write all selected trial rows into ONE table!
                    for t_data in selected_trials:
                        writer.writerow([t_data[0], t_data[1], t_data[2], t_data[3], t_data[4], t_data[5], t_data[6]])

                QMessageBox.information(
                    self, "Consolidated CSV Exported",
                    f"Successfully exported {len(selected_trials)} selected trials into ONE consolidated CSV table!\n\nFile Location:\n{save_path}"
                )
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Could not write CSV file:\n{str(e)}")
