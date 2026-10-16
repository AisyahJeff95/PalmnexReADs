from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton, QButtonGroup,
    QSpinBox, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class NewAnnualDataEntryDialog(QDialog):
    """
    Exact replica of Original ReaDA 'New Annual Data Entry' Window (Screenshots 20 & 21)
    - Dynamic date entry inputs apper under selected radio button option
    - Only the Continue button under the ACTIVE radio option is ENABLED; others are greyed out!
    - Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html)
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.selected_trial = None

        self.setWindowTitle("New Annual Data Entry")
        self.setFixedSize(780, 600)
        self.setStyleSheet("background-color: #e8e8e8;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 18, 20, 18)
        main_layout.setSpacing(10)

        # -----------------------------------------------------------------
        # 1. Header Bar: Title, QWhatsThis & Exit Procedure Button
        # -----------------------------------------------------------------
        top_bar = QHBoxLayout()

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
        whatsthis_btn.setToolTip("Click here then click any section or option to view detailed feature explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        title_lbl = QLabel("New Annual Data Entry")
        title_lbl.setFont(QFont("Times New Roman", 18, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #008080; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        exit_btn = QPushButton("❌   Exit\nProcedure")
        exit_btn.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                padding: 6px 12px;
                outline: none;
            }
            QPushButton:hover { background-color: #fee2e2; color: #dc2626; border-color: #dc2626; }
        """)
        exit_btn.clicked.connect(self.reject)

        top_bar.addWidget(whatsthis_btn)
        top_bar.addStretch()
        top_bar.addWidget(title_lbl)
        top_bar.addStretch()
        top_bar.addWidget(exit_btn)

        main_layout.addLayout(top_bar)

        # -----------------------------------------------------------------
        # 2. AGRONOMY TRIAL CODE Table (Center)
        # -----------------------------------------------------------------
        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        table_container.setFixedWidth(280)
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)

        self.trial_table = QTableWidget()
        self.trial_table.setColumnCount(2)
        self.trial_table.setHorizontalHeaderLabels(["AGRONOMY TRIAL CODE", "Estate"])
        self.trial_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.trial_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.trial_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.trial_table.setAlternatingRowColors(True)

        self.trial_table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        tc_layout.addWidget(self.trial_table)
        main_layout.addWidget(table_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # -----------------------------------------------------------------
        # 3. Middle 4 Data Type Header Boxes (Matching Screenshot 20 & 21)
        # -----------------------------------------------------------------
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        card_headers = [
            ("F.F.B. Yield\nRecording Period", "<b>F.F.B. Yield Recording Period:</b> Configure annual Fresh Fruit Bunch harvesting start/end recording months and years."),
            ("Palms Tissue\nSampling Date", "<b>Palms Tissue Sampling Date:</b> Configure annual Leaf Foliar Tissue Nutrient sampling dates (N, P, K, Mg, Ca)."),
            ("Vegetative Meas.\nSampling Date", "<b>Vegetative Meas. Sampling Date:</b> Configure annual Frond 17 Vegetative Field Canopy sampling dates (Rachis, Petiole WxD, Leaf Area)."),
            ("Soil\nSampling Date", "<b>Soil Sampling Date:</b> Configure annual Soil Chemical & pH Sampling dates.")
        ]

        card_box_qss = """
            QLabel {
                background-color: #808080;
                color: #ffffff;
                font-family: "Times New Roman", serif;
                font-size: 11px;
                font-weight: bold;
                border: 1px solid #555555;
                padding: 6px 2px;
            }
        """

        for text, desc in card_headers:
            lbl = QLabel(text)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(card_box_qss)
            lbl.setFixedHeight(40)
            lbl.setWhatsThis(desc)
            lbl.setToolTip(desc)
            cards_layout.addWidget(lbl, 1)

        main_layout.addSpacing(6)
        main_layout.addLayout(cards_layout)

        # -----------------------------------------------------------------
        # 4. Bottom Selection Controls & Dynamic Input Columns
        # -----------------------------------------------------------------
        prompt_lbl1 = QLabel(">> Mark Data Type Button For New Date Entry <<")
        prompt_lbl1.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        prompt_lbl1.setStyleSheet("color: #000000; border: none; background: transparent;")
        prompt_lbl1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(prompt_lbl1)

        # 4 Columns Container for Radio + Dynamic Date Inputs + Continue Button
        cols_layout = QHBoxLayout()
        cols_layout.setSpacing(12)

        self.button_group = QButtonGroup(self)

        radio_options = [
            ("Yield Parameters", 0, "Select Yield Parameters to enter new FFB harvesting recording date periods."),
            ("Tissue Sampl", 1, "Select Tissue Sampl to enter new Leaf Foliar Nutrient sampling dates."),
            ("Veg. Meas.", 2, "Select Veg. Meas. to enter new Vegetative Canopy measurement dates."),
            ("Soil Sample", 3, "Select Soil Sample to enter new Soil Chemical sampling dates.")
        ]

        self.radios = []
        self.date_widgets = []
        self.cont_btns = []

        spin_qss = """
            QSpinBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
                font-weight: bold;
                padding: 1px;
            }
        """

        enabled_btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 4px;
                outline: none;
            }
            QPushButton:hover { background-color: #fff8f8; border-color: #800000; color: #800000; }
        """

        disabled_btn_qss = """
            QPushButton {
                background-color: #d4d4d8;
                color: #71717a;
                border: 1px solid #a1a1aa;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 4px;
                outline: none;
            }
        """

        for text, r_id, desc in radio_options:
            col_frame = QFrame()
            col_frame.setStyleSheet("background: transparent;")
            col_vlayout = QVBoxLayout(col_frame)
            col_vlayout.setContentsMargins(0, 0, 0, 0)
            col_vlayout.setSpacing(4)

            # Radio Button
            r_btn = QRadioButton(text)
            r_btn.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            r_btn.setStyleSheet("QRadioButton { color: #000000; background: transparent; }")
            r_btn.setWhatsThis(desc)
            r_btn.setToolTip(desc)
            self.button_group.addButton(r_btn, r_id)
            self.radios.append(r_btn)
            col_vlayout.addWidget(r_btn, alignment=Qt.AlignmentFlag.AlignCenter)

            # Dynamic Date Inputs Box
            date_box = QFrame()
            date_box.setStyleSheet("background: transparent;")
            db_layout = QVBoxLayout(date_box)
            db_layout.setContentsMargins(0, 2, 0, 2)
            db_layout.setSpacing(2)

            sub_hdr = QLabel("Recording Period" if r_id == 0 else "Sampling Date")
            sub_hdr.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
            sub_hdr.setStyleSheet("color: #000000;")
            sub_hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
            db_layout.addWidget(sub_hdr)

            inputs_hlayout = QHBoxLayout()
            inputs_hlayout.setSpacing(2)
            inputs_hlayout.addStretch()

            if r_id == 0:  # Yield Recording Period: [ MM ] / [ YYYY ] - [ MM ] / [ YYYY ]
                m1 = QSpinBox()
                m1.setRange(1, 12)
                m1.setValue(1)
                m1.setFixedWidth(42)
                m1.setStyleSheet(spin_qss)

                s1 = QLabel("/")
                s1.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))

                y1 = QSpinBox()
                y1.setRange(1990, 2030)
                y1.setValue(2026)
                y1.setFixedWidth(58)
                y1.setStyleSheet(spin_qss)

                dash = QLabel("-")
                dash.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))

                m2 = QSpinBox()
                m2.setRange(1, 12)
                m2.setValue(12)
                m2.setFixedWidth(42)
                m2.setStyleSheet(spin_qss)

                s2 = QLabel("/")
                s2.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))

                y2 = QSpinBox()
                y2.setRange(1990, 2030)
                y2.setValue(2026)
                y2.setFixedWidth(58)
                y2.setStyleSheet(spin_qss)

                inputs_hlayout.addWidget(m1)
                inputs_hlayout.addWidget(s1)
                inputs_hlayout.addWidget(y1)
                inputs_hlayout.addWidget(dash)
                inputs_hlayout.addWidget(m2)
                inputs_hlayout.addWidget(s2)
                inputs_hlayout.addWidget(y2)
            else:  # Sampling Date: [ DD ] / [ MM ] / [ YYYY ]
                d = QSpinBox()
                d.setRange(1, 31)
                d.setValue(15)
                d.setFixedWidth(42)
                d.setStyleSheet(spin_qss)

                s1 = QLabel("/")
                s1.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))

                m = QSpinBox()
                m.setRange(1, 12)
                m.setValue(6)
                m.setFixedWidth(42)
                m.setStyleSheet(spin_qss)

                s2 = QLabel("/")
                s2.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))

                y = QSpinBox()
                y.setRange(1990, 2030)
                y.setValue(2026)
                y.setFixedWidth(58)
                y.setStyleSheet(spin_qss)

                inputs_hlayout.addWidget(d)
                inputs_hlayout.addWidget(s1)
                inputs_hlayout.addWidget(m)
                inputs_hlayout.addWidget(s2)
                inputs_hlayout.addWidget(y)

            inputs_hlayout.addStretch()
            db_layout.addLayout(inputs_hlayout)
            col_vlayout.addWidget(date_box)
            self.date_widgets.append(date_box)

            # Continue Button
            c_btn = QPushButton("✔️   Continue")
            c_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            c_btn.setFixedHeight(32)
            c_btn.clicked.connect(lambda _, i=r_id: self.on_continue_clicked(i))
            col_vlayout.addWidget(c_btn)
            self.cont_btns.append(c_btn)

            cols_layout.addWidget(col_frame, 1)

        main_layout.addLayout(cols_layout)

        prompt_lbl2 = QLabel("{ Click Yes Button To Confirm Selection/Continue }")
        prompt_lbl2.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        prompt_lbl2.setStyleSheet("color: #800000; border: none; background: transparent;")
        prompt_lbl2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(prompt_lbl2)

        self.button_group.idToggled.connect(self.on_radio_changed)
        self.radios[0].setChecked(True)
        self.update_active_option(0)

        self.refresh_trials()

    def on_radio_changed(self, id_val, is_checked):
        if is_checked:
            self.update_active_option(id_val)

    def update_active_option(self, active_idx):
        enabled_btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #800000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 4px;
                outline: none;
            }
            QPushButton:hover { background-color: #fff8f8; border-color: #800000; }
        """

        disabled_btn_qss = """
            QPushButton {
                background-color: #d4d4d8;
                color: #a1a1aa;
                border: 1px solid #a1a1aa;
                border-radius: 3px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 4px;
                outline: none;
            }
        """

        for idx in range(4):
            if idx == active_idx:
                self.date_widgets[idx].setVisible(True)
                self.cont_btns[idx].setEnabled(True)
                self.cont_btns[idx].setStyleSheet(enabled_btn_qss)
            else:
                self.date_widgets[idx].setVisible(False)
                self.cont_btns[idx].setEnabled(False)
                self.cont_btns[idx].setStyleSheet(disabled_btn_qss)

    def refresh_trials(self):
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

    def on_continue_clicked(self, option_index):
        row = self.trial_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Trial Selected", "Please select an Agronomy Trial Code from the top table.")
            return

        trial_code = self.trial_table.item(row, 0).text()
        estate_name = self.trial_table.item(row, 1).text() if self.trial_table.item(row, 1) else "Banting Station"

        if option_index == 0:  # FFB Yield Parameters -> Launch Screenshot 22 Window!
            from pages.new_ffb_yield_entry_dialog import NewFfbYieldEntryDialog
            dlg = NewFfbYieldEntryDialog(
                self, self.store,
                trial_code=trial_code, estate_name=estate_name,
                start_mn=11, start_yr=2002, end_mn=12, end_yr=2002
            )
            dlg.exec()
            self.accept()
        elif option_index == 1:  # Palms Tissue Sampling -> Launch Screenshot 23 Window!
            from pages.new_tissue_nutrients_entry_dialog import NewTissueNutrientsEntryDialog
            dlg = NewTissueNutrientsEntryDialog(
                self, self.store,
                trial_code=trial_code, estate_name=estate_name,
                day=1, month=1, year=2022
            )
            dlg.exec()
            self.accept()
        elif option_index == 2:  # Vegetative Measurements -> Launch NewEntryVegetativeDialog!
            from pages.new_entry_vegetative_dialog import NewEntryVegetativeDialog
            dlg = NewEntryVegetativeDialog(
                self, self.store,
                trial_code=trial_code, estate_name=estate_name,
                day=1, month=1, year=2022
            )
            dlg.exec()
            self.accept()
        elif option_index == 3:  # Soil Sampling -> Launch NewEntrySoilDialog!
            from pages.new_entry_soil_dialog import NewEntrySoilDialog
            dlg = NewEntrySoilDialog(
                self, self.store,
                trial_code=trial_code, estate_name=estate_name,
                day=1, month=1, year=2022
            )
            dlg.exec()
            self.accept()
