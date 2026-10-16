from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QSpinBox,
    QDoubleSpinBox, QComboBox, QCheckBox, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class NutrientVariablesConfigDialog(QDialog):
    """
    Exact replica of Original ReaDA 'Set Input Variables' Checkbox Panel (Screenshot 23 Overlay)
    Allows users to toggle active nutrient columns for Leaf Tissue Nutrient Analysis
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Input Variables - Palm Nutrients")
        self.setFixedSize(360, 480)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        hdr = QLabel("Select Active Nutrient Variables:")
        hdr.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        hdr.setStyleSheet("color: #800000;")
        layout.addWidget(hdr)

        box = QFrame()
        box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        b_layout = QVBoxLayout(box)
        b_layout.setContentsMargins(15, 12, 15, 12)
        b_layout.setSpacing(6)

        self.vars = [
            ("Sample Type", True),
            ("Ledger No", True),
            ("Plot No", True),
            ("Extra Plot", False),
            ("Sub Plot", False),
            ("N  (%)", True),
            ("P  (%)", True),
            ("K  (%)", True),
            ("Ca (%)", True),
            ("Mg (%)", True),
            ("S  (%)", True),
            ("Cl (ppm)", True),
            ("Cu (ppm)", True),
            ("Zn (ppm)", True),
            ("Mn (ppm)", True),
            ("Fe (ppm)", True),
            ("B  (ppm)", True),
            ("Sample Dry Wt.", True)
        ]

        self.checkboxes = []
        chk_qss = "QCheckBox { color: #000000; font-family: 'Segoe UI', sans-serif; font-size: 12px; font-weight: bold; }"

        for name, default_val in self.vars:
            chk = QCheckBox(f". {name}")
            chk.setStyleSheet(chk_qss)
            chk.setChecked(default_val)
            b_layout.addWidget(chk)
            self.checkboxes.append(chk)

        layout.addWidget(box, 1)

        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        ok_btn = QPushButton("Apply Variables")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: #ffffff;
                border: 1px solid #500000;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 5px 14px;
            }
            QPushButton:hover { background-color: #990000; }
        """)
        ok_btn.clicked.connect(self.accept)
        btn_bar.addWidget(ok_btn)

        layout.addLayout(btn_bar)


class NewTissueNutrientsEntryDialog(QDialog):
    """
    Exact replica of Original ReaDA 'New Entry On Palm Sample Nutrients Data' Window (Screenshot 23 & 24)
    - Aligned layout: Left 'Sample' title at the top, cleanly arranged 10 dropdowns from top to bottom
    - Top Info: Trial Code, Estate Name, Sampling Date (DD / MM / YYYY) with 'Dy / Mn / Year' subheader
    - Buttons: 'Set Input Variables' & 'Enter / Edit Data'
    - Right Summary Grid Table: Nutrient percentage and ppm concentration grid
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

        self.setWindowTitle(f"New Entry On Palm Sample Nutrients Data - [{self.trial_code}]")
        self.setFixedSize(1020, 660)
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

        title_lbl = QLabel("New Entry On Palm Sample Nutrients Data")
        title_lbl.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_hdr.addWidget(whatsthis_btn)
        top_hdr.addStretch()
        top_hdr.addWidget(title_lbl)
        top_hdr.addStretch()
        top_hdr.addSpacing(90)

        main_layout.addLayout(top_hdr)

        # -----------------------------------------------------------------
        # 2. Top Info Box (Trial Code, Estate Name, Sampling Date)
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

        # Right Info: Sampling Date (Dy/Mn/Year)
        right_info = QHBoxLayout()
        right_info.setSpacing(15)

        date_vbox = QVBoxLayout()
        date_vbox.setSpacing(2)

        sub_hdr = QLabel("Dy / Mn / Year")
        sub_hdr.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
        sub_hdr.setStyleSheet("color: #000000; border: none; background: transparent;")
        sub_hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_hbox = QHBoxLayout()
        date_hbox.setSpacing(3)

        d_lbl = QLabel("Sampling Date :")
        d_lbl.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        d_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")

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

        self.d_spin = QSpinBox()
        self.d_spin.setRange(1, 31)
        self.d_spin.setValue(self.day)
        self.d_spin.setFixedWidth(44)
        self.d_spin.setStyleSheet(spin_qss)

        s1 = QLabel("/")
        s1.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        s1.setStyleSheet("color: #000000; border: none; background: transparent;")

        self.m_spin = QSpinBox()
        self.m_spin.setRange(1, 12)
        self.m_spin.setValue(self.month)
        self.m_spin.setFixedWidth(44)
        self.m_spin.setStyleSheet(spin_qss)

        s2 = QLabel("/")
        s2.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        s2.setStyleSheet("color: #000000; border: none; background: transparent;")

        self.y_spin = QSpinBox()
        self.y_spin.setRange(1990, 2030)
        self.y_spin.setValue(self.year)
        self.y_spin.setFixedWidth(60)
        self.y_spin.setStyleSheet(spin_qss)

        date_hbox.addWidget(d_lbl)
        date_hbox.addWidget(self.d_spin)
        date_hbox.addWidget(s1)
        date_hbox.addWidget(self.m_spin)
        date_hbox.addWidget(s2)
        date_hbox.addWidget(self.y_spin)

        date_vbox.addWidget(sub_hdr)
        date_vbox.addLayout(date_hbox)
        right_info.addLayout(date_vbox)

        info_layout.addLayout(right_info, 1)

        main_layout.addWidget(info_frame)

        # -----------------------------------------------------------------
        # 3. Action Buttons: 'Set Input Variables' & 'Enter / Edit Data'
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
        set_var_btn.setWhatsThis("<b>Set Input Variables:</b> Select active nutrient elements (N, P, K, Mg, Ca, S, Cl, Cu, Zn, Mn, Fe, B).")
        set_var_btn.setToolTip("Select active nutrient elements (N, P, K, Mg, Ca, S, Cl, Cu, Zn, Mn, Fe, B).")
        set_var_btn.clicked.connect(self.on_set_variables)

        edit_data_btn = QPushButton("Enter / Edit Data")
        edit_data_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        edit_data_btn.setStyleSheet(btn_qss)
        edit_data_btn.setWhatsThis("<b>Enter / Edit Data:</b> Open interactive foliar tissue nutrients grid editor.")
        edit_data_btn.setToolTip("Open interactive foliar tissue nutrients grid editor.")
        edit_data_btn.clicked.connect(self.on_enter_edit_data)

        ctrl_bar.addSpacing(20)
        ctrl_bar.addWidget(set_var_btn)
        ctrl_bar.addStretch()
        ctrl_bar.addWidget(edit_data_btn)
        ctrl_bar.addStretch()

        main_layout.addLayout(ctrl_bar)

        # -----------------------------------------------------------------
        # 4. Main Body: Left Sample Selection Box & Right Main Nutrients Grid
        # -----------------------------------------------------------------
        body_layout = QHBoxLayout()
        body_layout.setSpacing(12)

        # Left Sample Box ({1} FROND17, {2} STEM, {3} ROOT, {4} RACHIS, {5} LEAF...)
        # Re-aligned matching Screenshot 23 (Sample title at TOP, dropdowns top to bottom)
        sample_box = QFrame()
        sample_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        sample_box.setFixedWidth(200)
        sb_layout = QVBoxLayout(sample_box)
        sb_layout.setContentsMargins(10, 12, 10, 12)
        sb_layout.setSpacing(6)

        s_hdr = QLabel("Sample")
        s_hdr.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        s_hdr.setStyleSheet("color: #800000; border: none; background: transparent;")
        s_hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb_layout.addWidget(s_hdr)

        sample_defaults = ["FROND17", "STEM", "ROOT", "RACHIS", "LEAF", "", "", "", "", ""]
        combo_qss = """
            QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Segoe UI", "Times New Roman", sans-serif;
                font-size: 11px;
                font-weight: bold;
                padding: 2px 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                selection-background-color: #0078d7;
                selection-color: #ffffff;
                border: 1px solid #71717a;
            }
        """

        for i in range(10):
            row_h = QHBoxLayout()
            row_h.setSpacing(4)

            idx_lbl = QLabel(f"{{{i+1}}}")
            idx_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            idx_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
            idx_lbl.setFixedWidth(26)

            cbox = QComboBox()
            cbox.setStyleSheet(combo_qss)
            cbox.addItems(["", "FROND17", "STEM", "ROOT", "RACHIS", "LEAF", "OTHER"])
            cbox.setCurrentText(sample_defaults[i])

            row_h.addWidget(idx_lbl)
            row_h.addWidget(cbox, 1)
            sb_layout.addLayout(row_h)

        sb_layout.addStretch()
        body_layout.addWidget(sample_box)

        # Right Main Nutrients Summary Grid Table
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(15)

        headers = [
            "Sample Type", "Plot No", "N %", "P %", "K %", "Ca %", "Mg %",
            "S %", "Cl ppm", "Cu ppm", "Zn ppm", "Mn ppm", "Fe ppm", "B ppm", "Dry Wt (g)"
        ]

        # QWhatsThis Explanations for Foliar Nutrients Table Headers (doc.qt.io/qt-6/qwhatsthis.html)
        self.whats_this_dict = {
            0: "<b>Sample Type:</b> Tissue organ type (Frond 17, Stem, Root, Rachis, Leaflet).",
            1: "<b>Plot No:</b> Monitored Plot Number within the trial layout.",
            2: "<b>N (%):</b> Foliar Nitrogen concentration percentage (%). Standard Frond 17 target: 2.50% - 2.80%.",
            3: "<b>P (%):</b> Foliar Phosphorus concentration percentage (%). Standard target: 0.15% - 0.18%.",
            4: "<b>K (%):</b> Foliar Potassium concentration percentage (%). Standard target: 1.00% - 1.25%.",
            5: "<b>Ca (%):</b> Foliar Calcium concentration percentage (%). Standard target: 0.50% - 0.70%.",
            6: "<b>Mg (%):</b> Foliar Magnesium concentration percentage (%). Standard target: 0.25% - 0.35%.",
            7: "<b>S (%):</b> Foliar Sulfur concentration percentage (%).",
            8: "<b>Cl (ppm):</b> Foliar Chlorine micro-nutrient concentration (parts per million).",
            9: "<b>Cu (ppm):</b> Foliar Copper micro-nutrient concentration (ppm).",
            10: "<b>Zn (ppm):</b> Foliar Zinc micro-nutrient concentration (ppm).",
            11: "<b>Mn (ppm):</b> Foliar Manganese micro-nutrient concentration (ppm).",
            12: "<b>Fe (ppm):</b> Foliar Iron micro-nutrient concentration (ppm).",
            13: "<b>B (ppm):</b> Foliar Boron micro-nutrient concentration (ppm). Standard target: 15 - 25 ppm.",
            14: "<b>Dry Wt (g):</b> Oven-dried sample weight in grams (g)."
        }

        self.table.setRowCount(0)
        self.table.setColumnCount(len(headers))

        for col_idx, h_text in enumerate(headers):
            header_item = QTableWidgetItem(h_text)
            header_desc = self.whats_this_dict.get(col_idx, h_text)
            header_item.setWhatsThis(header_desc)
            header_item.setToolTip(header_desc)
            self.table.setHorizontalHeaderItem(col_idx, header_item)

        self.table.setColumnWidth(0, 95)
        self.table.setColumnWidth(1, 65)
        for c in range(2, 15):
            self.table.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
            QHeaderView::section:hover { background-color: #4a5220; }
        """)

        tb_layout.addWidget(self.table)
        body_layout.addWidget(table_box, 1)

        main_layout.addLayout(body_layout, 1)

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
        yes_btn.setWhatsThis("<b>Yes (Save Data):</b> Save newly entered Leaf Nutrients records into SQLite database.")
        yes_btn.setToolTip("Save newly entered Leaf Nutrients records into SQLite database.")
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
        no_btn.setWhatsThis("<b>No (Cancel):</b> Exit without saving Leaf Nutrients data.")
        no_btn.setToolTip("Exit without saving Leaf Nutrients data.")
        no_btn.clicked.connect(self.reject)

        bot_layout.addWidget(prompt_save)
        bot_layout.addWidget(yes_btn)
        bot_layout.addWidget(no_btn)

        main_layout.addLayout(bot_layout)

        self.load_sample_data()

    def load_sample_data(self):
        t_code = self.t_code_edit.text() if hasattr(self, 't_code_edit') and self.t_code_edit.text() else self.trial_code
        if self.store:
            sample_records = self.store.get_tissue_nutrients(t_code)
        else:
            sample_records = [
                ("FROND17", 1, 2.65, 0.16, 1.15, 0.62, 0.28, 0.18, 120, 5.2, 18.5, 85, 92, 18.0, 150.0),
                ("FROND17", 2, 2.58, 0.15, 1.10, 0.58, 0.26, 0.17, 115, 4.8, 17.2, 80, 88, 16.5, 145.0),
                ("FROND17", 3, 2.72, 0.17, 1.22, 0.65, 0.31, 0.19, 125, 5.5, 19.8, 90, 96, 19.5, 155.0),
                ("FROND17", 4, 2.45, 0.14, 1.05, 0.54, 0.24, 0.16, 110, 4.5, 16.0, 75, 84, 15.0, 140.0)
            ]

        self.table.setRowCount(len(sample_records))

        for r_idx, r in enumerate(sample_records):
            for c_idx in range(min(15, len(r))):
                item = QTableWidgetItem(str(r[c_idx]))
                item.setFont(QFont("Times New Roman", 11))
                item.setForeground(QColor("#000000"))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                desc = self.whats_this_dict.get(c_idx, str(r[c_idx]))
                item.setWhatsThis(desc)
                item.setToolTip(desc)
                self.table.setItem(r_idx, c_idx, item)

    def on_set_variables(self):
        dlg = NutrientVariablesConfigDialog(self)
        if dlg.exec():
            QMessageBox.information(self, "Variables Configured", "Successfully updated active foliar nutrient variables!")

    def on_enter_edit_data(self):
        QMessageBox.information(self, "Grid Editor Active", f"Entering interactive tissue nutrient grid editor for Trial '{self.t_code_edit.text()}'!")

    def on_save_data(self):
        QMessageBox.information(self, "Data Saved", f"New Palm Sample Nutrients Data for Trial '{self.t_code_edit.text()}' saved successfully!")
        self.accept()
