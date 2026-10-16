from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class YieldSelectionDialog(QDialog):
    """
    Selection Window for Yield Recording Data Entry (Matching ReaDA Pattern)
    - Left Table: Select Trial Code (Trial, Estate)
    - Right Table: Select Year (Recording Year)
    - Bottom Inputs: Enter Recording Period [ MM ] / [ YYYY ] - [ MM ] / [ YYYY ]
    - Action Buttons: '❌ Return To Main Menu' & '✔️ Start Data Entry'
    """
    def __init__(self, parent=None, store=None, mode="entry"):
        super().__init__(parent)
        self.store = store
        self.mode = mode
        self.selected_trial = None
        self.selected_year = None

        mode_title = "Yield Recording Data Entry" if mode == "entry" else "Edit Yield Recording Data"
        self.setWindowTitle(mode_title)
        self.setFixedSize(620, 520)
        self.setStyleSheet("background-color: #dcdcdc;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # Title Header
        title_lbl = QLabel(mode_title)
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_lbl)

        # Middle Grid
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(15)

        # LEFT PANEL: Select Trial Code
        left_box = QVBoxLayout()
        left_box.setSpacing(4)

        t_lbl = QLabel("Select Trial Code")
        t_lbl.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        t_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        t_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_box.addWidget(t_lbl)

        tc_container = QFrame()
        tc_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(tc_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)

        self.trial_table = QTableWidget()
        self.trial_table.setColumnCount(2)
        self.trial_table.setHorizontalHeaderLabels(["Trial", "Estate"])
        self.trial_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.trial_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.trial_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.trial_table.setAlternatingRowColors(True)

        self.trial_table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 12px; padding: 4px; }
        """)

        tc_layout.addWidget(self.trial_table)
        left_box.addWidget(tc_container, 1)
        grid_layout.addLayout(left_box, 3)

        # RIGHT PANEL: Select Year
        right_box = QVBoxLayout()
        right_box.setSpacing(4)

        y_lbl = QLabel("Select Year")
        y_lbl.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        y_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        y_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_box.addWidget(y_lbl)

        yc_container = QFrame()
        yc_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        yc_layout = QVBoxLayout(yc_container)
        yc_layout.setContentsMargins(0, 0, 0, 0)

        self.year_table = QTableWidget()
        self.year_table.setColumnCount(1)
        self.year_table.setHorizontalHeaderLabels(["Recording Year"])
        self.year_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.year_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.year_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.year_table.setAlternatingRowColors(True)

        self.year_table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 12px; padding: 4px; }
        """)

        yc_layout.addWidget(self.year_table)
        right_box.addWidget(yc_container, 1)
        grid_layout.addLayout(right_box, 2)

        main_layout.addLayout(grid_layout, 1)

        # Recording Period Inputs: [ MM ] / [ YYYY ] - [ MM ] / [ YYYY ]
        period_box = QFrame()
        period_box.setStyleSheet("background-color: #dcdcdc;")
        period_layout = QVBoxLayout(period_box)
        period_layout.setContentsMargins(0, 5, 0, 5)
        period_layout.setSpacing(4)

        period_title = QLabel("Enter Recording Period")
        period_title.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        period_title.setStyleSheet("color: #000000; border: none; background: transparent;")
        period_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        period_layout.addWidget(period_title)

        inputs_layout = QHBoxLayout()
        inputs_layout.addStretch()

        input_qss = """
            QSpinBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Segoe UI", sans-serif;
                font-size: 12px;
                font-weight: bold;
                padding: 2px;
            }
        """

        self.start_mnth = QSpinBox()
        self.start_mnth.setRange(1, 12)
        self.start_mnth.setValue(1)
        self.start_mnth.setFixedWidth(50)
        self.start_mnth.setStyleSheet(input_qss)

        slash1 = QLabel("/")
        slash1.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        slash1.setStyleSheet("color: #000000;")

        self.start_yr = QSpinBox()
        self.start_yr.setRange(1990, 2030)
        self.start_yr.setValue(2026)
        self.start_yr.setFixedWidth(70)
        self.start_yr.setStyleSheet(input_qss)

        dash = QLabel(" - ")
        dash.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
        dash.setStyleSheet("color: #000000;")

        self.end_mnth = QSpinBox()
        self.end_mnth.setRange(1, 12)
        self.end_mnth.setValue(12)
        self.end_mnth.setFixedWidth(50)
        self.end_mnth.setStyleSheet(input_qss)

        slash2 = QLabel("/")
        slash2.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        slash2.setStyleSheet("color: #000000;")

        self.end_yr = QSpinBox()
        self.end_yr.setRange(1990, 2030)
        self.end_yr.setValue(2026)
        self.end_yr.setFixedWidth(70)
        self.end_yr.setStyleSheet(input_qss)

        inputs_layout.addWidget(self.start_mnth)
        inputs_layout.addWidget(slash1)
        inputs_layout.addWidget(self.start_yr)
        inputs_layout.addWidget(dash)
        inputs_layout.addWidget(self.end_mnth)
        inputs_layout.addWidget(slash2)
        inputs_layout.addWidget(self.end_yr)
        inputs_layout.addStretch()

        period_layout.addLayout(inputs_layout)
        main_layout.addWidget(period_box)

        # Action Buttons
        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 16px;
                outline: none;
            }
            QPushButton:focus { outline: none; }
            QPushButton:hover { background-color: #f4f4f5; border-color: #800000; color: #800000; }
            QPushButton:pressed { background-color: #e4e4e7; }
        """

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        cancel_btn = QPushButton("❌   Return To Main Menu")
        cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cancel_btn.setStyleSheet(btn_qss)
        cancel_btn.setFixedHeight(34)
        cancel_btn.clicked.connect(self.reject)

        start_btn = QPushButton("✔️   Start Data Entry")
        start_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        start_btn.setStyleSheet(btn_qss)
        start_btn.setFixedHeight(34)
        start_btn.clicked.connect(self.on_start_entry)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(start_btn)

        main_layout.addLayout(btn_layout)

        self.refresh_tables()

    def refresh_tables(self):
        trials = self.store.get_trials() if self.store else []
        self.trial_table.setRowCount(len(trials))
        for row_idx, t in enumerate(trials):
            c_item = QTableWidgetItem(str(t[0]))
            c_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            c_item.setForeground(QColor("#000000"))

            e_item = QTableWidgetItem(str(t[1]))
            e_item.setFont(QFont("Times New Roman", 11))
            e_item.setForeground(QColor("#000000"))

            self.trial_table.setItem(row_idx, 0, c_item)
            self.trial_table.setItem(row_idx, 1, e_item)

        if len(trials) > 0:
            self.trial_table.selectRow(0)

        years = [1995, 1998, 2000, 2002, 2005, 2022, 2024, 2026]
        self.year_table.setRowCount(len(years))
        for row_idx, y in enumerate(years):
            y_item = QTableWidgetItem(str(y))
            y_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            y_item.setForeground(QColor("#000000"))
            y_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.year_table.setItem(row_idx, 0, y_item)

        if len(years) > 0:
            self.year_table.selectRow(len(years) - 1)

    def on_start_entry(self):
        t_row = self.trial_table.currentRow()
        y_row = self.year_table.currentRow()

        if t_row < 0:
            QMessageBox.warning(self, "No Trial Selected", "Please select a trial code from the list.")
            return

        self.selected_trial = self.trial_table.item(t_row, 0).text()
        self.selected_year = self.year_table.item(y_row, 0).text() if y_row >= 0 else "2026"
        self.accept()
