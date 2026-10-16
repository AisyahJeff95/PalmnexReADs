from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class DeleteTrialDialog(QDialog):
    """
    Delete Trial Code Modal (Screenshot 18)
    Enhanced Features:
    - Multi-trial selection checkboxes to delete multiple trials at once
    - 'Select All Trials' checkbox toggle for fast batch deletion
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("Deleting Trial Code")
        self.setFixedSize(560, 560)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(8)

        # Header Title & Subheader
        title_lbl = QLabel("Deleting Trial Code")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_lbl = QLabel("Select Codes To Be Deleted")
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
        prompt_lbl = QLabel(">> Select Codes To Be Deleted <<")
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
                background-color: #fee2e2;
                border-color: #dc2626;
                color: #dc2626;
            }
            QPushButton:pressed {
                background-color: #fca5a5;
            }
        """

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)

        yes_btn = QPushButton("✔️   Yes / Continue")
        yes_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        yes_btn.setStyleSheet(btn_qss)
        yes_btn.setFixedHeight(34)
        yes_btn.clicked.connect(self.on_delete_continue)

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
            chk_item.setCheckState(Qt.CheckState.Unchecked)

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

    def on_delete_continue(self):
        trials = self.store.get_trials() if self.store else []
        selected_codes = []

        for r in range(self.table.rowCount()):
            chk_item = self.table.item(r, 0)
            if chk_item and chk_item.checkState() == Qt.CheckState.Checked:
                code = self.table.item(r, 1).text()
                selected_codes.append(code)

        if not selected_codes:
            QMessageBox.warning(self, "No Selection", "Please check at least one trial code to delete.")
            return

        confirm_text = f"Are you sure you want to delete {len(selected_codes)} selected trial(s)?\n\nCodes: {', '.join(selected_codes)}"
        reply = QMessageBox.question(
            self, "Confirm Deletion", confirm_text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.store:
                for code in selected_codes:
                    self.store.delete_record("trials", "TRIAL_CODE", code)

            QMessageBox.information(
                self, "Trials Deleted",
                f"Successfully deleted {len(selected_codes)} trial(s) from database."
            )
            self.accept()
