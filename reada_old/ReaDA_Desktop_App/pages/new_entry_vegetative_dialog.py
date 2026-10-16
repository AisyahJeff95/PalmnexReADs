from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QSpinBox,
    QDoubleSpinBox, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class NewEntryVegetativeDialog(QDialog):
    """
    Exact replica of Original ReaDA 'New Entry On Vegetative Field Measurement Data' Window
    - Top Info: Trial Code, Estate Name, Sampling Date (DD / MM / YYYY)
    - Buttons: 'Set Input Variables' & 'Enter / Edit Data'
    - Main Grid Table: Plot No, Frond No (17), Rachis Len (cm), Petiole W (cm), Petiole D (cm), Pinnae Count, Leaflet Len (cm), Leaflet W (cm), Trunk Ht (m)
    - Bottom Action: 'Save Data ?' with 'Yes' (Save) and 'No' (Cancel)
    - Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html)
    """
    def __init__(self, parent=None, store=None, trial_code="PR1998/1", estate_name="Banting Station", day=1, month=1, year=2022):
        super().__init__(parent)
        self.store = store
        self.trial_code = trial_code
        self.estate_name = estate_name
        self.day = day
        self.month = month
        self.year = year

        self.setWindowTitle(f"New Entry On Vegetative Field Measurement Data - [{self.trial_code}]")
        self.setFixedSize(980, 640)
        self.setStyleSheet("background-color: #dcdcdc;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 15, 18, 15)
        main_layout.setSpacing(10)

        # 1. Header Banner
        top_hdr = QHBoxLayout()
        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("""
            QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 10px; font-family: "Segoe UI", sans-serif; font-weight: bold; outline: none; }
            QPushButton:hover { background-color: #fde047; color: #713f12; }
        """)
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        title_lbl = QLabel("New Entry On Vegetative Field Measurement Data")
        title_lbl.setFont(QFont("Times New Roman", 19, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000055; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_hdr.addWidget(whatsthis_btn)
        top_hdr.addStretch()
        top_hdr.addWidget(title_lbl)
        top_hdr.addStretch()
        top_hdr.addSpacing(90)
        main_layout.addLayout(top_hdr)

        # 2. Top Info Box
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 10, 15, 10)
        info_layout.setSpacing(20)

        left_info = QVBoxLayout()
        left_info.setSpacing(6)

        t_row = QHBoxLayout()
        t_lbl = QLabel("Trial Code :")
        t_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        t_lbl.setFixedWidth(95)
        self.t_code_edit = QLineEdit(self.trial_code)
        self.t_code_edit.setFixedWidth(140)
        self.t_code_edit.setStyleSheet("background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-weight: bold; padding: 3px;")
        t_row.addWidget(t_lbl)
        t_row.addWidget(self.t_code_edit)
        t_row.addStretch()
        left_info.addLayout(t_row)

        e_row = QHBoxLayout()
        e_lbl = QLabel("Estate Name :")
        e_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        e_lbl.setFixedWidth(95)
        self.estate_edit = QLineEdit(self.estate_name)
        self.estate_edit.setFixedWidth(240)
        self.estate_edit.setStyleSheet("background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-weight: bold; padding: 3px;")
        e_row.addWidget(e_lbl)
        e_row.addWidget(self.estate_edit)
        e_row.addStretch()
        left_info.addLayout(e_row)

        info_layout.addLayout(left_info, 1)

        right_info = QHBoxLayout()
        date_vbox = QVBoxLayout()
        date_vbox.setSpacing(2)
        sub_hdr = QLabel("Dy / Mn / Year")
        sub_hdr.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))

        date_hbox = QHBoxLayout()
        d_lbl = QLabel("Sampling Date :")
        d_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        spin_qss = "QSpinBox { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-weight: bold; padding: 2px; }"

        d_sp = QSpinBox()
        d_sp.setRange(1, 31)
        d_sp.setValue(self.day)
        d_sp.setFixedWidth(44)
        d_sp.setStyleSheet(spin_qss)

        m_sp = QSpinBox()
        m_sp.setRange(1, 12)
        m_sp.setValue(self.month)
        m_sp.setFixedWidth(44)
        m_sp.setStyleSheet(spin_qss)

        y_sp = QSpinBox()
        y_sp.setRange(1990, 2030)
        y_sp.setValue(self.year)
        y_sp.setFixedWidth(60)
        y_sp.setStyleSheet(spin_qss)

        date_hbox.addWidget(d_lbl)
        date_hbox.addWidget(d_sp)
        date_hbox.addWidget(QLabel("/"))
        date_hbox.addWidget(m_sp)
        date_hbox.addWidget(QLabel("/"))
        date_hbox.addWidget(y_sp)

        date_vbox.addWidget(sub_hdr, alignment=Qt.AlignmentFlag.AlignCenter)
        date_vbox.addLayout(date_hbox)
        right_info.addLayout(date_vbox)

        info_layout.addLayout(right_info, 1)
        main_layout.addWidget(info_frame)

        # 3. Action Buttons Bar
        ctrl_bar = QHBoxLayout()
        btn_qss = "QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-family: 'Times New Roman', serif; font-size: 13px; font-weight: bold; padding: 5px 14px; outline: none; } QPushButton:hover { background-color: #f4f4f5; border-color: #800000; color: #800000; }"

        set_var_btn = QPushButton("Set Input Variables")
        set_var_btn.setStyleSheet(btn_qss)
        set_var_btn.clicked.connect(lambda: QMessageBox.information(self, "Variables Set", "Vegetative variables configured."))

        edit_data_btn = QPushButton("Enter / Edit Data")
        edit_data_btn.setStyleSheet(btn_qss)
        edit_data_btn.clicked.connect(lambda: QMessageBox.information(self, "Grid Active", "Vegetative Canopy Editor Active."))

        ctrl_bar.addSpacing(20)
        ctrl_bar.addWidget(set_var_btn)
        ctrl_bar.addStretch()
        ctrl_bar.addWidget(edit_data_btn)
        ctrl_bar.addStretch()

        main_layout.addLayout(ctrl_bar)

        # 4. Main Table Grid
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        headers = [
            "Plot No.", "Palm No.", "Frond No.", "Rachis Len (cm)", "Petiole W (cm)",
            "Petiole D (cm)", "Pinnae Count", "Leaflet Len (cm)", "Leaflet W (cm)", "Trunk Ht (m)"
        ]

        self.whats_this_dict = {
            0: "<b>Plot No.:</b> Unique Plot Identification Number.",
            1: "<b>Palm No.:</b> Monitored Palm Number.",
            2: "<b>Frond No.:</b> Standardized Frond Sampling Position (Frond 17).",
            3: "<b>Rachis Len (cm):</b> Length of the main leaf rachis (cm).",
            4: "<b>Petiole W (cm):</b> Width of the frond petiole cross-section (cm).",
            5: "<b>Petiole D (cm):</b> Depth of the frond petiole cross-section (cm).",
            6: "<b>Pinnae Count:</b> Leaflets count on one side of frond.",
            7: "<b>Leaflet Len (cm):</b> Average length of mid-rachis leaflets (cm).",
            8: "<b>Leaflet W (cm):</b> Average width of mid-rachis leaflets (cm).",
            9: "<b>Trunk Ht (m):</b> Total palm trunk height to Frond 33 base (m)."
        }

        self.table.setRowCount(0)
        self.table.setColumnCount(len(headers))

        for col_idx, h_text in enumerate(headers):
            header_item = QTableWidgetItem(h_text)
            header_desc = self.whats_this_dict.get(col_idx, h_text)
            header_item.setWhatsThis(header_desc)
            header_item.setToolTip(header_desc)
            self.table.setHorizontalHeaderItem(col_idx, header_item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        tb_layout.addWidget(self.table)
        main_layout.addWidget(table_box, 1)

        # 5. Bottom Save Action Bar
        bot_layout = QHBoxLayout()
        bot_layout.addStretch()

        prompt_save = QLabel("Save Data ?")
        prompt_save.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        prompt_save.setStyleSheet("color: #800000;")

        yes_btn = QPushButton("✔️   Yes")
        yes_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-weight: bold; padding: 6px 16px; } QPushButton:hover { background-color: #047857; color: #ffffff; }")
        yes_btn.clicked.connect(self.accept)

        no_btn = QPushButton("🚫   No")
        no_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-weight: bold; padding: 6px 16px; } QPushButton:hover { background-color: #fee2e2; color: #dc2626; }")
        no_btn.clicked.connect(self.reject)

        bot_layout.addWidget(prompt_save)
        bot_layout.addWidget(yes_btn)
        bot_layout.addWidget(no_btn)

        main_layout.addLayout(bot_layout)

        self.load_sample_data()

    def load_sample_data(self):
        sample_records = [
            (1, 1, 17, 545.0, 5.2, 3.8, 310, 85.0, 4.8, 3.45),
            (1, 2, 17, 520.0, 4.9, 3.6, 298, 82.0, 4.6, 3.20),
            (2, 1, 17, 560.0, 5.4, 4.0, 320, 88.0, 5.0, 3.80),
            (2, 2, 17, 535.0, 5.1, 3.7, 305, 84.0, 4.7, 3.50)
        ]
        self.table.setRowCount(len(sample_records))

        for r_idx, r in enumerate(sample_records):
            for c_idx in range(10):
                item = QTableWidgetItem(str(r[c_idx]))
                item.setFont(QFont("Times New Roman", 11))
                item.setForeground(QColor("#000000"))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(r_idx, c_idx, item)
