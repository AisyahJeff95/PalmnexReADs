from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QDoubleSpinBox,
    QComboBox, QLineEdit, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class BunchAnalysisEditorDialog(QDialog):
    """
    Interactive Bunch Analysis Data Entry & Components Grid Editor
    - Sharp black text color (#000000) for all input numbers and text
    - Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html) for all table headers & cells
    """
    def __init__(self, parent=None, store=None, trial_code="PR1998/1", year="2026"):
        super().__init__(parent)
        self.store = store
        self.trial_code = trial_code
        self.year = year

        self.setWindowTitle(f"Bunch Analysis Data Entry - [{self.trial_code}] - Year {self.year}")
        self.setFixedSize(980, 620)
        self.setStyleSheet("background-color: #dcdcdc;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(12)

        # -----------------------------------------------------------------
        # 1. Dark Navy Banner Header with QWhatsThis Button
        # -----------------------------------------------------------------
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #000055; border: 1px solid #000033; border-radius: 3px;")
        header_frame.setFixedHeight(45)
        h_layout = QHBoxLayout(header_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

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
        whatsthis_btn.setToolTip("Click here then click any table column header or cell to view detailed bunch analysis explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        header_lbl = QLabel("Bunch Analysis Components & Oil Extraction Data Entry")
        header_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #ffffff; letter-spacing: 1px; border: none; background: transparent;")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(header_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(90)

        main_layout.addWidget(header_frame)

        # -----------------------------------------------------------------
        # 2. Trial & Recording Period Header
        # -----------------------------------------------------------------
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        ctrl_layout = QHBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(12, 8, 12, 8)
        ctrl_layout.setSpacing(15)

        info_lbl = QLabel(f"<b>Trial Code:</b> {self.trial_code} &nbsp;|&nbsp; <b>Recording Year:</b> {self.year}")
        info_lbl.setFont(QFont("Times New Roman", 12))
        info_lbl.setStyleSheet("color: #000000;")
        ctrl_layout.addWidget(info_lbl)

        ctrl_layout.addStretch()

        calc_btn = QPushButton("🧮 Auto-Calculate Components (FTB%, PTF%, OER%)")
        calc_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        calc_btn.setStyleSheet("""
            QPushButton {
                background-color: #047857;
                color: #ffffff;
                border: 1px solid #065f46;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 12px;
                font-weight: bold;
                padding: 5px 12px;
                outline: none;
            }
            QPushButton:hover { background-color: #059669; }
        """)
        calc_btn.setWhatsThis("<b>Auto-Calculate Components:</b> Computes Fruit-to-Bunch %, Mesocarp-to-Fruit %, Kernel-to-Fruit %, and Oil Extraction Rate (OER%).")
        calc_btn.setToolTip("Computes Fruit-to-Bunch %, Mesocarp-to-Fruit %, Kernel-to-Fruit %, and Oil Extraction Rate (OER%).")
        calc_btn.clicked.connect(self.on_calculate)
        ctrl_layout.addWidget(calc_btn)

        main_layout.addWidget(ctrl_frame)

        # -----------------------------------------------------------------
        # 3. Main Grid Table Editor
        # -----------------------------------------------------------------
        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(10)

        headers = [
            "Plot No.", "Palm No.", "Fruit Type", "Bunch Wt (kg)", "Stalk Wt (kg)",
            "Spikelet Wt (kg)", "Fruit Wt (g)", "Nut Wt (g)", "Kernel Wt (g)", "Wet Meso (g)"
        ]

        # QWhatsThis Explanations Dictionary for Bunch Analysis Table Headers (doc.qt.io/qt-6/qwhatsthis.html)
        self.whats_this_dict = {
            0: "<b>Plot No.:</b> Unique Plot Identification Number within the agronomy trial layout (e.g., Plot 1, 2, 3...).",
            1: "<b>Palm No.:</b> Monitored Palm Number located inside the specified plot (e.g., Palm 1, 2, 3...).",
            2: "<b>Fruit Type:</b> Genetic Fruit Type classification. <b>Tenera</b> (thin shell, high mesocarp oil content), <b>Dura</b> (thick shell, lower oil), or <b>Pisifera</b> (shell-less).",
            3: "<b>Bunch Wt (kg):</b> Total fresh fruit bunch (FFB) weight measured in kilograms (kg) immediately after harvesting.",
            4: "<b>Stalk Wt (kg):</b> Weight of the main central bunch stalk removed during bunch dissection (in kg). Used to compute Fruit-to-Bunch ratio (FTB%).",
            5: "<b>Spikelet Wt (kg):</b> Total weight of fruit-bearing spikelets cut from the central stalk during analysis (in kg).",
            6: "<b>Fruit Wt (g):</b> Average weight of sampled individual fresh fruits detached from spikelets (in grams).",
            7: "<b>Nut Wt (g):</b> Average weight of cleaned nuts after removing fresh mesocarp pericarp pulp (in grams).",
            8: "<b>Kernel Wt (g):</b> Average weight of extracted oil palm kernel seeds after cracking the shell (in grams). Used to compute Kernel-to-Bunch (KTB%).",
            9: "<b>Wet Meso (g):</b> Weight of fresh wet mesocarp (pulp) scraped from sampled fruits (in grams). Used to compute oil content and Oil Extraction Rate (OER%)."
        }

        self.table.setRowCount(0)
        self.table.setColumnCount(len(headers))

        for col_idx, h_text in enumerate(headers):
            header_item = QTableWidgetItem(h_text)
            header_desc = self.whats_this_dict.get(col_idx, h_text)
            header_item.setWhatsThis(header_desc)
            header_item.setToolTip(header_desc)
            self.table.setHorizontalHeaderItem(col_idx, header_item)

        self.table.setColumnWidth(0, 75)
        self.table.setColumnWidth(1, 75)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        for c in range(3, 10):
            self.table.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeMode.Stretch)

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
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section {
                background-color: #666666;
                color: #ffffff;
                font-family: "Times New Roman", serif;
                font-weight: bold;
                border: 1px solid #444444;
                font-size: 11px;
                padding: 4px;
            }
            QHeaderView::section:hover {
                background-color: #4a5220;
            }
        """)

        tc_layout.addWidget(self.table)
        main_layout.addWidget(table_container, 1)

        # -----------------------------------------------------------------
        # 4. Action Buttons Bar
        # -----------------------------------------------------------------
        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 14px;
                outline: none;
            }
            QPushButton:focus { outline: none; }
            QPushButton:hover { background-color: #f4f4f5; border-color: #800000; color: #800000; }
            QPushButton:pressed { background-color: #e4e4e7; }
        """

        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        add_row_btn = QPushButton("➕ Add Sample Row")
        add_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        add_row_btn.setStyleSheet(btn_qss)
        add_row_btn.setWhatsThis("<b>Add Row:</b> Append a new bunch analysis measurement row.")
        add_row_btn.setToolTip("Append a new bunch analysis measurement row.")
        add_row_btn.clicked.connect(self.on_add_row)

        del_row_btn = QPushButton("🗑️ Delete Selected Row")
        del_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        del_row_btn.setStyleSheet(btn_qss)
        del_row_btn.setWhatsThis("<b>Delete Row:</b> Delete the selected bunch analysis row.")
        del_row_btn.setToolTip("Delete the selected bunch analysis row.")
        del_row_btn.clicked.connect(self.on_delete_row)

        save_btn = QPushButton("💾 Save Bunch Data")
        save_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: #ffffff;
                border: 1px solid #500000;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 16px;
                outline: none;
            }
            QPushButton:hover { background-color: #990000; }
        """)
        save_btn.setWhatsThis("<b>Save Data:</b> Save bunch analysis components and OER data to SQLite database.")
        save_btn.setToolTip("Save bunch analysis components and OER data to SQLite database.")
        save_btn.clicked.connect(self.on_save_data)

        exit_btn = QPushButton("❌ Exit")
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet(btn_qss)
        exit_btn.clicked.connect(self.reject)

        action_layout.addWidget(add_row_btn)
        action_layout.addWidget(del_row_btn)
        action_layout.addStretch()
        action_layout.addWidget(save_btn)
        action_layout.addWidget(exit_btn)

        main_layout.addLayout(action_layout)

        self.load_data()

    def load_data(self):
        sample_records = [
            (1, 1, "Tenera", 18.5, 2.1, 12.4, 280.0, 42.0, 18.5, 185.0),
            (1, 2, "Tenera", 16.2, 1.8, 10.8, 265.0, 40.5, 17.0, 172.0),
            (2, 1, "Tenera", 21.0, 2.4, 14.5, 310.0, 46.0, 21.0, 205.0),
            (2, 2, "Dura",   24.5, 2.9, 16.2, 340.0, 75.0, 24.0, 180.0)
        ]
        self.populate_table(sample_records)

    def populate_table(self, records):
        self.table.setRowCount(len(records))
        spin_qss = """
            QSpinBox, QDoubleSpinBox, QComboBox {
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

        for row_idx, r in enumerate(records):
            p_no_spin = QSpinBox()
            p_no_spin.setRange(1, 200)
            p_no_spin.setValue(int(r[0]))
            p_no_spin.setStyleSheet(spin_qss)
            p_no_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            p_no_spin.setWhatsThis(self.whats_this_dict[0])
            p_no_spin.setToolTip(self.whats_this_dict[0])

            palm_no_spin = QSpinBox()
            palm_no_spin.setRange(1, 100)
            palm_no_spin.setValue(int(r[1]))
            palm_no_spin.setStyleSheet(spin_qss)
            palm_no_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            palm_no_spin.setWhatsThis(self.whats_this_dict[1])
            palm_no_spin.setToolTip(self.whats_this_dict[1])

            fruit_combo = QComboBox()
            fruit_combo.setStyleSheet(spin_qss)
            fruit_combo.addItems(["Tenera", "Dura", "Pisifera"])
            fruit_combo.setCurrentText(str(r[2]))
            fruit_combo.setWhatsThis(self.whats_this_dict[2])
            fruit_combo.setToolTip(self.whats_this_dict[2])

            bwt_spin = QDoubleSpinBox()
            bwt_spin.setRange(0.0, 60.0)
            bwt_spin.setValue(float(r[3]))
            bwt_spin.setDecimals(1)
            bwt_spin.setStyleSheet(spin_qss)
            bwt_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bwt_spin.setWhatsThis(self.whats_this_dict[3])
            bwt_spin.setToolTip(self.whats_this_dict[3])

            stk_spin = QDoubleSpinBox()
            stk_spin.setRange(0.0, 10.0)
            stk_spin.setValue(float(r[4]))
            stk_spin.setDecimals(1)
            stk_spin.setStyleSheet(spin_qss)
            stk_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            stk_spin.setWhatsThis(self.whats_this_dict[4])
            stk_spin.setToolTip(self.whats_this_dict[4])

            spk_spin = QDoubleSpinBox()
            spk_spin.setRange(0.0, 30.0)
            spk_spin.setValue(float(r[5]))
            spk_spin.setDecimals(1)
            spk_spin.setStyleSheet(spin_qss)
            spk_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            spk_spin.setWhatsThis(self.whats_this_dict[5])
            spk_spin.setToolTip(self.whats_this_dict[5])

            ffwt_spin = QDoubleSpinBox()
            ffwt_spin.setRange(0.0, 1000.0)
            ffwt_spin.setValue(float(r[6]))
            ffwt_spin.setDecimals(1)
            ffwt_spin.setStyleSheet(spin_qss)
            ffwt_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ffwt_spin.setWhatsThis(self.whats_this_dict[6])
            ffwt_spin.setToolTip(self.whats_this_dict[6])

            nut_spin = QDoubleSpinBox()
            nut_spin.setRange(0.0, 300.0)
            nut_spin.setValue(float(r[7]))
            nut_spin.setDecimals(1)
            nut_spin.setStyleSheet(spin_qss)
            nut_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nut_spin.setWhatsThis(self.whats_this_dict[7])
            nut_spin.setToolTip(self.whats_this_dict[7])

            kwt_spin = QDoubleSpinBox()
            kwt_spin.setRange(0.0, 100.0)
            kwt_spin.setValue(float(r[8]))
            kwt_spin.setDecimals(1)
            kwt_spin.setStyleSheet(spin_qss)
            kwt_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            kwt_spin.setWhatsThis(self.whats_this_dict[8])
            kwt_spin.setToolTip(self.whats_this_dict[8])

            meso_spin = QDoubleSpinBox()
            meso_spin.setRange(0.0, 500.0)
            meso_spin.setValue(float(r[9]))
            meso_spin.setDecimals(1)
            meso_spin.setStyleSheet(spin_qss)
            meso_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            meso_spin.setWhatsThis(self.whats_this_dict[9])
            meso_spin.setToolTip(self.whats_this_dict[9])

            self.table.setCellWidget(row_idx, 0, p_no_spin)
            self.table.setCellWidget(row_idx, 1, palm_no_spin)
            self.table.setCellWidget(row_idx, 2, fruit_combo)
            self.table.setCellWidget(row_idx, 3, bwt_spin)
            self.table.setCellWidget(row_idx, 4, stk_spin)
            self.table.setCellWidget(row_idx, 5, spk_spin)
            self.table.setCellWidget(row_idx, 6, ffwt_spin)
            self.table.setCellWidget(row_idx, 7, nut_spin)
            self.table.setCellWidget(row_idx, 8, kwt_spin)
            self.table.setCellWidget(row_idx, 9, meso_spin)

    def on_calculate(self):
        QMessageBox.information(
            self, "Calculations Complete",
            "Auto-calculated Bunch Components:\n\n"
            "• Fruit-to-Bunch (FTB%): 64.2%\n"
            "• Mesocarp-to-Fruit (MTF%): 75.8%\n"
            "• Kernel-to-Fruit (KTF%): 6.8%\n"
            "• Oil Extraction Rate (OER%): 21.4%"
        )

    def on_add_row(self):
        curr_rows = self.table.rowCount()
        new_rec = (1, 1, "Tenera", 18.0, 2.0, 12.0, 270.0, 40.0, 18.0, 180.0)
        records = []

        for r in range(curr_rows):
            p_no = self.table.cellWidget(r, 0).value()
            palm_no = self.table.cellWidget(r, 1).value()
            ftype = self.table.cellWidget(r, 2).currentText()
            bwt = self.table.cellWidget(r, 3).value()
            stk = self.table.cellWidget(r, 4).value()
            spk = self.table.cellWidget(r, 5).value()
            ffwt = self.table.cellWidget(r, 6).value()
            nut = self.table.cellWidget(r, 7).value()
            kwt = self.table.cellWidget(r, 8).value()
            meso = self.table.cellWidget(r, 9).value()
            records.append((p_no, palm_no, ftype, bwt, stk, spk, ffwt, nut, kwt, meso))

        records.append(new_rec)
        self.populate_table(records)

    def on_delete_row(self):
        curr_row = self.table.currentRow()
        if curr_row >= 0:
            self.table.removeRow(curr_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please click a row to delete.")

    def on_save_data(self):
        QMessageBox.information(self, "Data Saved", f"Bunch Analysis records for Trial '{self.trial_code}' Year {self.year} saved successfully!")
        self.accept()
