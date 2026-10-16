from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from pages.palm_numbering_editor_dialog import PalmNumberingEditorDialog

class EditPalmSelectionDialog(QDialog):
    """
    Exact replica of Original ReaDA 'Entry/Editing Palm Numbering' Selection Window (Screenshot 2)
    - Header: 'Entry/Editing Palm Numbering'
    - Subheader: 'Select Code To Be Edited'
    - Table displaying AGRONOMY TRIAL CODE list (Trial Code, Estate)
    - Prompt: '>> HighLight Selection <<'
    - Buttons: '✔️ Yes / Continue' and '❌ Cancel - Exit'
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.selected_trial_data = None

        self.setWindowTitle("Entry/Editing Palm Numbering")
        self.setFixedSize(520, 520)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)

        # Header & Subheader Labels
        title_lbl = QLabel("Entry/Editing Palm Numbering")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_lbl = QLabel("Select Code To Be Edited")
        subtitle_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        subtitle_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(subtitle_lbl)

        # Table View: AGRONOMY TRIAL CODE
        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)
        tc_layout.setSpacing(0)

        banner_lbl = QLabel("AGRONOMY TRIAL CODE")
        banner_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        banner_lbl.setStyleSheet("background-color: #f0f0f0; color: #000000; border-bottom: 1px solid #71717a; padding: 4px;")
        banner_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tc_layout.addWidget(banner_lbl)

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
                background-color: #f5f5f5;
                color: #000000;
                font-family: "Times New Roman", serif;
                font-weight: bold;
                border: 1px solid #c0c0c0;
                font-size: 12px;
                padding: 4px;
            }
        """)

        self.table.itemDoubleClicked.connect(self.on_yes_continue)
        tc_layout.addWidget(self.table)
        layout.addWidget(table_container, 1)

        # Prompt & Action Buttons
        prompt_lbl = QLabel(">> HighLight Selection <<")
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

        yes_btn = QPushButton("✔️   Yes / Continue")
        yes_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        yes_btn.setStyleSheet(btn_qss)
        yes_btn.setFixedHeight(34)
        yes_btn.clicked.connect(self.on_yes_continue)

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
            code_item = QTableWidgetItem(str(t[0]))
            code_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            code_item.setForeground(QColor("#000000"))

            estate_item = QTableWidgetItem(str(t[1]))
            estate_item.setFont(QFont("Times New Roman", 11))
            estate_item.setForeground(QColor("#000000"))

            self.table.setItem(row_idx, 0, code_item)
            self.table.setItem(row_idx, 1, estate_item)

        if len(trials) > 0:
            self.table.selectRow(0)

    def on_yes_continue(self):
        curr_row = self.table.currentRow()
        trials = self.store.get_trials() if self.store else []

        if curr_row >= 0 and curr_row < len(trials):
            self.selected_trial_data = trials[curr_row]
            trial_code = self.selected_trial_data[0]
            estate = self.selected_trial_data[1]

            # Open Palm Numbering Editor Dialog!
            dlg = PalmNumberingEditorDialog(self, self.store, trial_code=trial_code, estate=estate)
            if dlg.exec():
                self.accept()
        else:
            QMessageBox.warning(self, "No Selection", "Please highlight and select a trial code from the list.")
