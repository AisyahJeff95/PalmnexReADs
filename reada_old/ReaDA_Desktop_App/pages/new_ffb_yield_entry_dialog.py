from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QSpinBox,
    QDoubleSpinBox, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class NewFfbYieldEntryDialog(QDialog):
    """
    Exact replica of Original ReaDA 'New Entry On F.F.B. Yield Data' Window (Screenshot 22)
    - Top Info: Trial Code, Estate Name, Recording Year (Starting Mn/Year & Ending Mn/Year)
    - Buttons: 'Set Input Variables' & 'Enter / Edit Data'
    - Left Table: Rec & Plot selection list
    - Right Table: Rec, Plot, FFB_YIELD, BUNCH_NO, BUNCH_WT, PALM_YIELD, BWT_TOTAL, BNO_TOTAL
    - Bottom Action: 'Save Data ?' with 'Yes' (Save) and 'No' (Cancel)
    - Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html)
    """
    def __init__(self, parent=None, store=None, trial_code="PR1998/1", estate_name="Banting Station", start_mn=11, start_yr=2002, end_mn=12, end_yr=2002):
        super().__init__(parent)
        self.store = store
        self.trial_code = trial_code
        self.estate_name = estate_name
        self.start_mn = start_mn
        self.start_yr = start_yr
        self.end_mn = end_mn
        self.end_yr = end_yr

        self.setWindowTitle(f"New Entry On F.F.B. Yield Data - [{self.trial_code}]")
        self.setFixedSize(980, 640)
        self.setStyleSheet("background-color: #dcdcdc;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 15, 18, 15)
        main_layout.setSpacing(10)

        # -----------------------------------------------------------------
        # 1. Header Title & QWhatsThis Help Button
        # -----------------------------------------------------------------
        top_hdr = QHBoxLayout()

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
            QPushButton:hover { background-color: #fde047; color: #713f12; }
        """)
        whatsthis_btn.setToolTip("Click here then click any input or table to view detailed feature explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        title_lbl = QLabel("New Entry On F.F.B. Yield Data")
        title_lbl.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #008080; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_hdr.addWidget(whatsthis_btn)
        top_hdr.addStretch()
        top_hdr.addWidget(title_lbl)
        top_hdr.addStretch()
        top_hdr.addSpacing(90)

        main_layout.addLayout(top_hdr)

        # -----------------------------------------------------------------
        # 2. Top Info Box (Trial Code, Estate Name, Starting & Ending Period)
        # -----------------------------------------------------------------
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 10, 15, 10)
        info_layout.setSpacing(20)

        # Left Info: Trial Code & Estate Name
        left_info = QVBoxLayout()
        left_info.setSpacing(6)

        t_row = QHBoxLayout()
        t_lbl = QLabel("Trial Code :")
        t_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        t_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        t_lbl.setFixedWidth(95)

        self.t_code_edit = QLineEdit(self.trial_code)
        self.t_code_edit.setFixedWidth(140)
        self.t_code_edit.setStyleSheet("background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-family: 'Times New Roman'; font-size: 12px; font-weight: bold; padding: 3px;")
        t_row.addWidget(t_lbl)
        t_row.addWidget(self.t_code_edit)
        t_row.addStretch()
        left_info.addLayout(t_row)

        e_row = QHBoxLayout()
        e_lbl = QLabel("Estate Name :")
        e_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        e_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        e_lbl.setFixedWidth(95)

        self.estate_edit = QLineEdit(self.estate_name)
        self.estate_edit.setFixedWidth(240)
        self.estate_edit.setStyleSheet("background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-family: 'Times New Roman'; font-size: 12px; font-weight: bold; padding: 3px;")
        e_row.addWidget(e_lbl)
        e_row.addWidget(self.estate_edit)
        e_row.addStretch()
        left_info.addLayout(e_row)

        info_layout.addLayout(left_info, 1)

        # Right Info: Recording Year & Starting/Ending Period
        right_info = QHBoxLayout()
        right_info.setSpacing(15)

        rec_lbl = QLabel("Recording Year :")
        rec_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        rec_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        right_info.addWidget(rec_lbl, alignment=Qt.AlignmentFlag.AlignVCenter)

        spin_qss = """
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

        # Starting Period
        sp_vbox = QVBoxLayout()
        sp_vbox.setSpacing(2)
        sp_sub = QLabel("Mn / Year")
        sp_sub.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
        sp_sub.setStyleSheet("color: #000000; border: none; background: transparent;")
        sp_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sp_hbox = QHBoxLayout()
        sp_hbox.setSpacing(3)
        self.sp_mn = QSpinBox()
        self.sp_mn.setRange(1, 12)
        self.sp_mn.setValue(self.start_mn)
        self.sp_mn.setFixedWidth(44)
        self.sp_mn.setStyleSheet(spin_qss)

        slash1 = QLabel("/")
        slash1.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        slash1.setStyleSheet("color: #000000; border: none; background: transparent;")

        self.sp_yr = QSpinBox()
        self.sp_yr.setRange(1990, 2030)
        self.sp_yr.setValue(self.start_yr)
        self.sp_yr.setFixedWidth(60)
        self.sp_yr.setStyleSheet(spin_qss)

        sp_hbox.addWidget(self.sp_mn)
        sp_hbox.addWidget(slash1)
        sp_hbox.addWidget(self.sp_yr)

        sp_lbl = QLabel("Starting Period")
        sp_lbl.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
        sp_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        sp_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sp_vbox.addWidget(sp_sub)
        sp_vbox.addLayout(sp_hbox)
        sp_vbox.addWidget(sp_lbl)
        right_info.addLayout(sp_vbox)

        # Ending Period
        ep_vbox = QVBoxLayout()
        ep_vbox.setSpacing(2)
        ep_sub = QLabel("Mn / Year")
        ep_sub.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
        ep_sub.setStyleSheet("color: #000000; border: none; background: transparent;")
        ep_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ep_hbox = QHBoxLayout()
        ep_hbox.setSpacing(3)
        self.ep_mn = QSpinBox()
        self.ep_mn.setRange(1, 12)
        self.ep_mn.setValue(self.end_mn)
        self.ep_mn.setFixedWidth(44)
        self.ep_mn.setStyleSheet(spin_qss)

        slash2 = QLabel("/")
        slash2.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        slash2.setStyleSheet("color: #000000; border: none; background: transparent;")

        self.ep_yr = QSpinBox()
        self.ep_yr.setRange(1990, 2030)
        self.ep_yr.setValue(self.end_yr)
        self.ep_yr.setFixedWidth(60)
        self.ep_yr.setStyleSheet(spin_qss)

        ep_hbox.addWidget(self.ep_mn)
        ep_hbox.addWidget(slash2)
        ep_hbox.addWidget(self.ep_yr)

        ep_lbl = QLabel("Ending Period")
        ep_lbl.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
        ep_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        ep_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ep_vbox.addWidget(ep_sub)
        ep_vbox.addLayout(ep_hbox)
        ep_vbox.addWidget(ep_lbl)
        right_info.addLayout(ep_vbox)
        ep_lbl.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
        ep_lbl.setStyleSheet("color: #000000;")
        ep_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ep_vbox.addWidget(ep_sub)
        ep_vbox.addLayout(ep_hbox)
        ep_vbox.addWidget(ep_lbl)
        right_info.addLayout(ep_vbox)

        info_layout.addLayout(right_info, 1)

        main_layout.addWidget(info_frame)

        # -----------------------------------------------------------------
        # 3. Action Buttons Above Tables: 'Set Input Variables' & 'Enter / Edit Data'
        # -----------------------------------------------------------------
        ctrl_bar = QHBoxLayout()

        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 5px 14px;
                outline: none;
            }
            QPushButton:hover { background-color: #f4f4f5; border-color: #800000; color: #800000; }
        """

        set_var_btn = QPushButton("Set Input Variables")
        set_var_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        set_var_btn.setStyleSheet(btn_qss)
        set_var_btn.setWhatsThis("<b>Set Input Variables:</b> Configure trial parameters, plot factors, and harvesting recording intervals.")
        set_var_btn.setToolTip("Configure trial parameters, plot factors, and harvesting recording intervals.")
        set_var_btn.clicked.connect(self.on_set_variables)

        edit_data_btn = QPushButton("Enter / Edit Data")
        edit_data_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        edit_data_btn.setStyleSheet(btn_qss)
        edit_data_btn.setWhatsThis("<b>Enter / Edit Data:</b> Open interactive FFB harvesting grid editor for plots and palms.")
        edit_data_btn.setToolTip("Open interactive FFB harvesting grid editor for plots and palms.")
        edit_data_btn.clicked.connect(self.on_enter_edit_data)

        ctrl_bar.addSpacing(20)
        ctrl_bar.addWidget(set_var_btn)
        ctrl_bar.addStretch()
        ctrl_bar.addWidget(edit_data_btn)
        ctrl_bar.addStretch()

        main_layout.addLayout(ctrl_bar)

        # -----------------------------------------------------------------
        # 4. Split Tables View (Left Plot List Table & Right Main Summary Grid)
        # -----------------------------------------------------------------
        tables_layout = QHBoxLayout()
        tables_layout.setSpacing(12)

        # Left Table Container (Rec & Plot)
        left_table_box = QFrame()
        left_table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        left_table_box.setFixedWidth(160)
        lt_layout = QVBoxLayout(left_table_box)
        lt_layout.setContentsMargins(0, 0, 0, 0)

        self.left_table = QTableWidget()
        self.left_table.setColumnCount(2)
        self.left_table.setHorizontalHeaderLabels(["Rec", "Plot"])
        self.left_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.left_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.left_table.setAlternatingRowColors(True)

        self.left_table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        lt_layout.addWidget(self.left_table)
        tables_layout.addWidget(left_table_box)

        # Right Main Table Container
        right_table_box = QFrame()
        right_table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        rt_layout = QVBoxLayout(right_table_box)
        rt_layout.setContentsMargins(0, 0, 0, 0)

        self.right_table = QTableWidget()
        self.right_table.setColumnCount(8)

        right_headers = [
            "Rec", "Plot", "FFB_YIELD", "BUNCH_NO", "BUNCH_WT", "PALM_YIELD", "BWT_TOTAL", "BNO_TOTAL"
        ]

        # QWhatsThis Explanations for Right Table Headers (doc.qt.io/qt-6/qwhatsthis.html)
        self.whats_this_dict = {
            0: "<b>Rec:</b> Record sequence index for the trial plot.",
            1: "<b>Plot:</b> Plot Number within the agronomy trial layout.",
            2: "<b>FFB_YIELD:</b> Total Fresh Fruit Bunch Yield (Tons / Ha / Year).",
            3: "<b>BUNCH_NO:</b> Average Number of Bunches harvested per palm (NOB/palm).",
            4: "<b>BUNCH_WT:</b> Mean Bunch Weight (MBW kg / bunch).",
            5: "<b>PALM_YIELD:</b> Annual FFB Yield per single palm (kg / palm / year).",
            6: "<b>BWT_TOTAL:</b> Cumulative total bunch weight harvested across all monitored palms in plot (kg).",
            7: "<b>BNO_TOTAL:</b> Cumulative total bunch count harvested across all monitored palms in plot."
        }

        self.right_table.setRowCount(0)
        self.right_table.setColumnCount(len(right_headers))

        for col_idx, h_text in enumerate(right_headers):
            header_item = QTableWidgetItem(h_text)
            header_desc = self.whats_this_dict.get(col_idx, h_text)
            header_item.setWhatsThis(header_desc)
            header_item.setToolTip(header_desc)
            self.right_table.setHorizontalHeaderItem(col_idx, header_item)

        self.right_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.right_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.right_table.setAlternatingRowColors(True)

        self.right_table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
            QHeaderView::section:hover { background-color: #4a5220; }
        """)

        rt_layout.addWidget(self.right_table)
        tables_layout.addWidget(right_table_box, 1)

        main_layout.addLayout(tables_layout, 1)

        # -----------------------------------------------------------------
        # 5. Bottom Action Bar: 'Save Data ?' with 'Yes' and 'No' Buttons
        # -----------------------------------------------------------------
        bot_frame = QFrame()
        bot_frame.setStyleSheet("background: transparent;")
        bot_layout = QHBoxLayout(bot_frame)
        bot_layout.setContentsMargins(0, 0, 0, 0)
        bot_layout.setSpacing(15)

        bot_layout.addStretch()

        prompt_save = QLabel("Save Data ?")
        prompt_save.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        prompt_save.setStyleSheet("color: #800000; border: none; background: transparent;")

        yes_btn = QPushButton("✔️   Yes")
        yes_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        yes_btn.setFixedWidth(100)
        yes_btn.setFixedHeight(34)
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover { background-color: #047857; color: #ffffff; }
        """)
        yes_btn.setWhatsThis("<b>Yes (Save Data):</b> Save newly entered FFB Yield records into SQLite database.")
        yes_btn.setToolTip("Save newly entered FFB Yield records into SQLite database.")
        yes_btn.clicked.connect(self.on_save_data)

        no_btn = QPushButton("🚫   No")
        no_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        no_btn.setFixedWidth(100)
        no_btn.setFixedHeight(34)
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover { background-color: #fee2e2; color: #dc2626; border-color: #dc2626; }
        """)
        no_btn.setWhatsThis("<b>No (Cancel):</b> Exit without saving FFB Yield data.")
        no_btn.setToolTip("Exit without saving FFB Yield data.")
        no_btn.clicked.connect(self.reject)

        bot_layout.addWidget(prompt_save)
        bot_layout.addWidget(yes_btn)
        bot_layout.addWidget(no_btn)

        main_layout.addLayout(bot_layout)

        self.load_sample_data()

    def load_sample_data(self):
        sample_plots = [
            (1, 1, 24.5, 14.2, 19.8, 142.5, 1425.0, 72),
            (2, 2, 22.8, 13.5, 18.5, 131.0, 1310.0, 68),
            (3, 3, 26.2, 15.0, 21.2, 158.0, 1580.0, 78),
            (4, 4, 21.0, 12.8, 17.5, 120.0, 1200.0, 64)
        ]

        self.left_table.setRowCount(len(sample_plots))
        self.right_table.setRowCount(len(sample_plots))

        for r_idx, p in enumerate(sample_plots):
            # Left Table
            self.left_table.setItem(r_idx, 0, self.create_item(p[0]))
            self.left_table.setItem(r_idx, 1, self.create_item(p[1]))

            # Right Table
            self.right_table.setItem(r_idx, 0, self.create_item(p[0]))
            self.right_table.setItem(r_idx, 1, self.create_item(p[1]))
            self.right_table.setItem(r_idx, 2, self.create_item(p[2]))
            self.right_table.setItem(r_idx, 3, self.create_item(p[3]))
            self.right_table.setItem(r_idx, 4, self.create_item(p[4]))
            self.right_table.setItem(r_idx, 5, self.create_item(p[5]))
            self.right_table.setItem(r_idx, 6, self.create_item(p[6]))
            self.right_table.setItem(r_idx, 7, self.create_item(p[7]))

    def create_item(self, val):
        item = QTableWidgetItem(str(val))
        item.setFont(QFont("Times New Roman", 11))
        item.setForeground(QColor("#000000"))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        return item

    def on_set_variables(self):
        QMessageBox.information(self, "Input Variables Set", f"Input variables and recording periods set for Trial '{self.t_code_edit.text()}'!")

    def on_enter_edit_data(self):
        QMessageBox.information(self, "Grid Editor Active", f"Entering interactive grid editor for Trial '{self.t_code_edit.text()}'!")

    def on_save_data(self):
        QMessageBox.information(self, "Data Saved", f"New FFB Yield Data for Trial '{self.t_code_edit.text()}' saved successfully!")
        self.accept()
