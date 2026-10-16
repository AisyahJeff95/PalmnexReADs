from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QWhatsThis
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class TrialAnnualDataWindow(QFrame):
    """
    Original ReaDA 'Trial Annual Data' View (Screenshot 9)
    Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html):
    - Features '❓ What's This?' button in the header bar
    - Each table header and data cell contains explicit QWhatsThis explanations
    - Clicking any column in What's This mode displays an explanatory popup
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.parent_window = parent
        self.store = store
        self.setStyleSheet("QFrame { background-color: #f0f0f0; border: 1px solid #bcbcbc; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(10)

        # -----------------------------------------------------------------
        # Header Bar (Title, QWhatsThis Button & Close Button)
        # -----------------------------------------------------------------
        header_bar = QHBoxLayout()

        title_lbl = QLabel("Trial Annual Data")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # QWhatsThis Button (qt.io/qt-6/qwhatsthis.html)
        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("""
            QPushButton {
                background-color: #fef08a;
                color: #854d0e;
                border: 1px solid #ca8a04;
                border-radius: 3px;
                padding: 4px 10px;
                font-family: "Segoe UI", sans-serif;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #fde047;
                color: #713f12;
            }
        """)
        whatsthis_btn.setToolTip("Click here then click any table column to view detailed field explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(self.on_whatsthis_clicked)

        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e1e1e1;
                color: #000000;
                border: 1px solid #adadad;
                border-radius: 2px;
                padding: 4px 14px;
                font-family: "Segoe UI", sans-serif;
            }
            QPushButton:hover {
                background-color: #fee2e2;
                color: #dc2626;
                border-color: #dc2626;
            }
        """)
        close_btn.clicked.connect(self.on_close_clicked)

        header_bar.addWidget(whatsthis_btn)
        header_bar.addStretch()
        header_bar.addWidget(title_lbl)
        header_bar.addStretch()
        header_bar.addWidget(close_btn)

        layout.addLayout(header_bar)

        # -----------------------------------------------------------------
        # Standard Qt QTableWidget Template (Matching Qt SQL QTableView doc)
        # -----------------------------------------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(17)

        headers = [
            "Code", "Estate",
            "Rec Mn", "Rec Yr", "Rec Mn", "Rec Yr",
            "FFB Mn Yr", "FFB Mn Yr", "FFB B",
            "Nutr Dy", "Nutr Mn", "Nutr Yr",
            "Veg Dy", "Veg Mn", "Veg Yr",
            "Soil Dy", "Soil Mn"
        ]

        # QWhatsThis Explanations Dictionary for Table Columns
        self.whats_this_dict = {
            0: "<b>Code (Trial Code):</b> Unique Agronomy Trial Identification Code assigned by MPOB (e.g., PR1998/1, PR2002/4).",
            1: "<b>Estate:</b> Oil Palm Plantation Estate or Research Station Name (e.g., Banting Station).",
            2: "<b>Rec Mn (Start Month):</b> Starting Month of the Trial Data Recording Period (01-12).",
            3: "<b>Rec Yr (Start Year):</b> Starting Year of the Trial Data Recording Period (YYYY).",
            4: "<b>Rec Mn (End Month):</b> Ending Month of the Trial Data Recording Period (01-12).",
            5: "<b>Rec Yr (End Year):</b> Ending Year of the Trial Data Recording Period (YYYY).",
            6: "<b>FFB Mn Yr (Start Period):</b> Fresh Fruit Bunch Yield Harvesting Start Period (Month Year).",
            7: "<b>FFB Mn Yr (End Period):</b> Fresh Fruit Bunch Yield Harvesting End Period (Month Year).",
            8: "<b>FFB B (Backup Status):</b> Indicates whether FFB Yield Data has been Backed Up ('B' = Backed Up).",
            9: "<b>Nutr Dy (Nutrient Sampling Day):</b> Day of the month when Leaf Foliar Sampling was conducted (01-31).",
            10: "<b>Nutr Mn (Nutrient Sampling Month):</b> Month when Leaf Foliar Sampling was conducted (01-12).",
            11: "<b>Nutr Yr (Nutrient Sampling Year):</b> Year when Leaf Foliar Sampling was conducted (YYYY).",
            12: "<b>Veg Dy (Vegetative Sampling Day):</b> Day of the month when Frond 17 Vegetative Field Sampling was conducted (01-31).",
            13: "<b>Veg Mn (Vegetative Sampling Month):</b> Month when Frond 17 Vegetative Field Sampling was conducted (01-12).",
            14: "<b>Veg Yr (Vegetative Sampling Year):</b> Year when Frond 17 Vegetative Field Sampling was conducted (YYYY).",
            15: "<b>Soil Dy (Soil Sampling Day):</b> Day of the month when Soil Nutrient Chemical Analysis was sampled (01-31).",
            16: "<b>Soil Mn (Soil Sampling Month):</b> Month when Soil Nutrient Chemical Analysis was sampled (01-12)."
        }

        self.table.setRowCount(0)
        self.table.setColumnCount(len(headers))

        for col_idx, h_text in enumerate(headers):
            header_item = QTableWidgetItem(h_text)
            header_desc = self.whats_this_dict.get(col_idx, h_text)
            header_item.setWhatsThis(header_desc)
            header_item.setToolTip(header_desc)
            self.table.setHorizontalHeaderItem(col_idx, header_item)

        self.table.setAlternatingRowColors(True)

        # Set clean column widths for perfect alignment
        col_widths = [
            85, 120,    # Trial Info
            55, 55, 55, 55, # Recording Yield
            75, 75, 55, # FFB Yield
            55, 55, 55, # Palms Nutrients
            55, 55, 55, # Vegetative Measurements
            55, 55      # Soil Nutrients
        ]

        for col_idx, w in enumerate(col_widths):
            self.table.setColumnWidth(col_idx, w)

        # Standardized Qt QTableView QSS Template
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                gridline-color: #c0c0c0;
                border: 1px solid #adadad;
                font-family: "Segoe UI", "Tahoma", sans-serif;
                font-size: 11px;
                selection-background-color: #0078d7;
                selection-color: #ffffff;
            }
            QTableWidget::item {
                color: #000000;
                background-color: #ffffff;
                padding: 4px;
                border: none;
            }
            QTableWidget::item:alternate {
                background-color: #f8fafc;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #e1e1e1;
                color: #000000;
                font-family: "Segoe UI", "Tahoma", sans-serif;
                font-weight: bold;
                border: 1px solid #adadad;
                font-size: 11px;
                padding: 5px;
                text-align: center;
            }
            QHeaderView::section:hover {
                background-color: #e5f1fb;
            }
        """)

        layout.addWidget(self.table)
        self.refresh_table()

    def on_whatsthis_clicked(self):
        """
        Enters QWhatsThis mode (https://doc.qt.io/qt-6/qwhatsthis.html)
        Changes cursor to '?' and allows clicking any element to view help description
        """
        QWhatsThis.enterWhatsThisMode()

    def on_close_clicked(self):
        if self.parent_window and hasattr(self.parent_window, 'show_home_branding'):
            self.parent_window.show_home_branding()
        elif self.parent_window and hasattr(self.parent_window, 'close_annual_data_window'):
            self.parent_window.close_annual_data_window()
        else:
            self.hide()

    def create_table_item(self, text, col_idx=0, is_bold=False, align_center=True):
        item = QTableWidgetItem(str(text))
        item.setForeground(QColor("#000000"))
        desc = self.whats_this_dict.get(col_idx, str(text))
        item.setWhatsThis(desc)
        item.setToolTip(desc)

        if is_bold:
            item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        else:
            item.setFont(QFont("Segoe UI", 9))

        if align_center:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        return item

    def refresh_table(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(max(len(trials), 10))

        for r_idx in range(10):
            if r_idx < len(trials):
                t = trials[r_idx]
                self.table.setItem(r_idx, 0, self.create_table_item(t[0], col_idx=0, is_bold=True, align_center=False))
                self.table.setItem(r_idx, 1, self.create_table_item(t[1], col_idx=1, align_center=False))

                # Demo historical data entries matching screenshot columns
                self.table.setItem(r_idx, 2, self.create_table_item("01", col_idx=2))
                self.table.setItem(r_idx, 3, self.create_table_item("1995", col_idx=3))
                self.table.setItem(r_idx, 4, self.create_table_item("02", col_idx=4))
                self.table.setItem(r_idx, 5, self.create_table_item("1995", col_idx=5))

                self.table.setItem(r_idx, 6, self.create_table_item("01 1995", col_idx=6))
                self.table.setItem(r_idx, 7, self.create_table_item("02 1995", col_idx=7))
                self.table.setItem(r_idx, 8, self.create_table_item("B", col_idx=8))

                self.table.setItem(r_idx, 9, self.create_table_item("15", col_idx=9))
                self.table.setItem(r_idx, 10, self.create_table_item("06", col_idx=10))
                self.table.setItem(r_idx, 11, self.create_table_item("1998", col_idx=11))

                self.table.setItem(r_idx, 12, self.create_table_item("20", col_idx=12))
                self.table.setItem(r_idx, 13, self.create_table_item("08", col_idx=13))
                self.table.setItem(r_idx, 14, self.create_table_item("1998", col_idx=14))

                self.table.setItem(r_idx, 15, self.create_table_item("10", col_idx=15))
                self.table.setItem(r_idx, 16, self.create_table_item("05", col_idx=16))
            else:
                for c_idx in range(17):
                    self.table.setItem(r_idx, c_idx, self.create_table_item("", col_idx=c_idx))
