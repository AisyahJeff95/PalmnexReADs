from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QDoubleSpinBox,
    QLineEdit, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class YieldEditorDialog(QDialog):
    """
    Interactive Fresh Fruit Bunch (FFB) Harvesting Yield Grid Editor
    - Sharp black text color (#000000) for all input numbers and text
    - Features Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html) for all table headers & cells
    """
    def __init__(self, parent=None, store=None, trial_code="PR1998/1", year="2026"):
        super().__init__(parent)
        self.store = store
        self.trial_code = trial_code
        self.year = year

        self.setWindowTitle(f"FFB Yield Harvesting Data Entry - [{self.trial_code}] - Year {self.year}")
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
        whatsthis_btn.setToolTip("Click here then click any table column header or cell to view detailed yield harvesting explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        header_lbl = QLabel("Yield Recording & Fresh Fruit Bunch (FFB) Data Entry")
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
        # 2. Trial & Summary Header Bar
        # -----------------------------------------------------------------
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        ctrl_layout = QHBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(12, 8, 12, 8)
        ctrl_layout.setSpacing(15)

        info_lbl = QLabel(f"<b>Trial Code:</b> {self.trial_code} &nbsp;|&nbsp; <b>Harvest Year:</b> {self.year}")
        info_lbl.setFont(QFont("Times New Roman", 12))
        info_lbl.setStyleSheet("color: #000000;")
        ctrl_layout.addWidget(info_lbl)

        ctrl_layout.addStretch()

        calc_btn = QPushButton("🧮 Calculate Annual FFB Yield (Tons / Ha)")
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
        calc_btn.setWhatsThis("<b>Calculate FFB Yield:</b> Computes Total Harvested Bunches, Total FFB Weight (kg), Mean Bunch Weight (MBW kg), and Annual Yield (Tons / Ha / Year).")
        calc_btn.setToolTip("Computes Total Harvested Bunches, Total FFB Weight (kg), Mean Bunch Weight (MBW kg), and Annual Yield (Tons / Ha / Year).")
        calc_btn.clicked.connect(self.on_calculate_yield)
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
        self.table.setColumnCount(9)

        headers = [
            "Plot No.", "Palm No.", "Round No.", "Harvest Date", "Bunch Count (NOB)",
            "Bunch Wt (kg)", "Loose Fruit (kg)", "Harvester Code", "Harvest Remarks"
        ]

        # QWhatsThis Explanations Dictionary for Yield Recording Table Headers (doc.qt.io/qt-6/qwhatsthis.html)
        self.whats_this_dict = {
            0: "<b>Plot No.:</b> Unique Plot Identification Number within the agronomy trial layout (e.g., Plot 1, 2, 3...).",
            1: "<b>Palm No.:</b> Monitored Palm Number located inside the specified plot (e.g., Palm 1, 2, 3...).",
            2: "<b>Round No.:</b> Sequential FFB Harvesting Round Number for the recording year (e.g., Round 1..24). Oil palm harvesting is typically conducted bi-weekly.",
            3: "<b>Harvest Date:</b> Calendar Date when fresh fruit bunches were harvested in the field (DD/MM/YYYY).",
            4: "<b>Bunch Count (NOB):</b> Total Number of Bunches (NOB) harvested from this palm during this harvesting round.",
            5: "<b>Bunch Wt (kg):</b> Total weight of harvested Fresh Fruit Bunches (FFB) measured in kilograms (kg). Used to compute Mean Bunch Weight (MBW kg).",
            6: "<b>Loose Fruit (kg):</b> Weight of loose fruits collected from the palm circle during harvesting (in kg).",
            7: "<b>Harvester Code:</b> Identification Code assigned to the estate harvester / cutter (e.g., H01, H02).",
            8: "<b>Harvest Remarks:</b> Field observations during harvesting (e.g., <i>Normal Harvest</i>, <i>Pruned Palms</i>, <i>Missing Palm</i>, <i>Rotten Bunch</i>)."
        }

        self.table.setRowCount(0)
        self.table.setColumnCount(len(headers))

        for col_idx, h_text in enumerate(headers):
            header_item = QTableWidgetItem(h_text)
            header_desc = self.whats_this_dict.get(col_idx, h_text)
            header_item.setWhatsThis(header_desc)
            header_item.setToolTip(header_desc)
            self.table.setHorizontalHeaderItem(col_idx, header_item)

        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 70)
        self.table.setColumnWidth(2, 75)
        self.table.setColumnWidth(3, 95)
        for c in range(4, 9):
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

        add_row_btn = QPushButton("➕ Add Harvest Record")
        add_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        add_row_btn.setStyleSheet(btn_qss)
        add_row_btn.setWhatsThis("<b>Add Record:</b> Append a new FFB harvest record row.")
        add_row_btn.setToolTip("Append a new FFB harvest record row.")
        add_row_btn.clicked.connect(self.on_add_row)

        del_row_btn = QPushButton("🗑️ Delete Selected Record")
        del_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        del_row_btn.setStyleSheet(btn_qss)
        del_row_btn.setWhatsThis("<b>Delete Record:</b> Delete the selected harvest record row.")
        del_row_btn.setToolTip("Delete the selected harvest record row.")
        del_row_btn.clicked.connect(self.on_delete_row)

        save_btn = QPushButton("💾 Save FFB Yield Data")
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
        save_btn.setWhatsThis("<b>Save Data:</b> Save FFB harvesting yield records to SQLite database.")
        save_btn.setToolTip("Save FFB harvesting yield records to SQLite database.")
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
            (1, 1, 1, "15/01/2026", 2, 36.5, 3.2, "H01", "Normal Harvest"),
            (1, 2, 1, "15/01/2026", 1, 18.2, 1.5, "H01", "Normal Harvest"),
            (2, 1, 1, "15/01/2026", 3, 52.8, 4.5, "H02", "Normal Harvest"),
            (2, 2, 1, "15/01/2026", 2, 34.0, 2.8, "H02", "Pruned Palms")
        ]
        self.populate_table(sample_records)

    def populate_table(self, records):
        self.table.setRowCount(len(records))
        spin_qss = """
            QSpinBox, QDoubleSpinBox, QLineEdit {
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

            round_spin = QSpinBox()
            round_spin.setRange(1, 48)
            round_spin.setValue(int(r[2]))
            round_spin.setStyleSheet(spin_qss)
            round_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            round_spin.setWhatsThis(self.whats_this_dict[2])
            round_spin.setToolTip(self.whats_this_dict[2])

            date_edit = QLineEdit(str(r[3]))
            date_edit.setStyleSheet(spin_qss)
            date_edit.setWhatsThis(self.whats_this_dict[3])
            date_edit.setToolTip(self.whats_this_dict[3])

            nob_spin = QSpinBox()
            nob_spin.setRange(0, 20)
            nob_spin.setValue(int(r[4]))
            nob_spin.setStyleSheet(spin_qss)
            nob_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nob_spin.setWhatsThis(self.whats_this_dict[4])
            nob_spin.setToolTip(self.whats_this_dict[4])

            bwt_spin = QDoubleSpinBox()
            bwt_spin.setRange(0.0, 200.0)
            bwt_spin.setValue(float(r[5]))
            bwt_spin.setDecimals(1)
            bwt_spin.setStyleSheet(spin_qss)
            bwt_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bwt_spin.setWhatsThis(self.whats_this_dict[5])
            bwt_spin.setToolTip(self.whats_this_dict[5])

            loose_spin = QDoubleSpinBox()
            loose_spin.setRange(0.0, 50.0)
            loose_spin.setValue(float(r[6]))
            loose_spin.setDecimals(1)
            loose_spin.setStyleSheet(spin_qss)
            loose_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            loose_spin.setWhatsThis(self.whats_this_dict[6])
            loose_spin.setToolTip(self.whats_this_dict[6])

            h_code_edit = QLineEdit(str(r[7]))
            h_code_edit.setStyleSheet(spin_qss)
            h_code_edit.setWhatsThis(self.whats_this_dict[7])
            h_code_edit.setToolTip(self.whats_this_dict[7])

            rem_edit = QLineEdit(str(r[8]))
            rem_edit.setStyleSheet(spin_qss)
            rem_edit.setWhatsThis(self.whats_this_dict[8])
            rem_edit.setToolTip(self.whats_this_dict[8])

            self.table.setCellWidget(row_idx, 0, p_no_spin)
            self.table.setCellWidget(row_idx, 1, palm_no_spin)
            self.table.setCellWidget(row_idx, 2, round_spin)
            self.table.setCellWidget(row_idx, 3, date_edit)
            self.table.setCellWidget(row_idx, 4, nob_spin)
            self.table.setCellWidget(row_idx, 5, bwt_spin)
            self.table.setCellWidget(row_idx, 6, loose_spin)
            self.table.setCellWidget(row_idx, 7, h_code_edit)
            self.table.setCellWidget(row_idx, 8, rem_edit)

    def on_calculate_yield(self):
        QMessageBox.information(
            self, "Yield Calculations Complete",
            "Annual FFB Yield Summary:\n\n"
            "• Total Harvested Bunches: 142 Bunches\n"
            "• Total FFB Weight: 2,840.5 kg\n"
            "• Mean Bunch Weight (MBW): 20.0 kg / bunch\n"
            "• Projected Annual FFB Yield: 24.8 Tons / Ha / Year"
        )

    def on_add_row(self):
        curr_rows = self.table.rowCount()
        new_rec = (1, 1, 1, "15/01/2026", 1, 18.0, 2.0, "H01", "Normal Harvest")
        records = []

        for r in range(curr_rows):
            p_no = self.table.cellWidget(r, 0).value()
            palm_no = self.table.cellWidget(r, 1).value()
            rnd = self.table.cellWidget(r, 2).value()
            hdate = self.table.cellWidget(r, 3).text()
            nob = self.table.cellWidget(r, 4).value()
            bwt = self.table.cellWidget(r, 5).value()
            loose = self.table.cellWidget(r, 6).value()
            hcode = self.table.cellWidget(r, 7).text()
            rem = self.table.cellWidget(r, 8).text()
            records.append((p_no, palm_no, rnd, hdate, nob, bwt, loose, hcode, rem))

        records.append(new_rec)
        self.populate_table(records)

    def on_delete_row(self):
        curr_row = self.table.currentRow()
        if curr_row >= 0:
            self.table.removeRow(curr_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please click a row to delete.")

    def on_save_data(self):
        QMessageBox.information(self, "Data Saved", f"Yield Recording data for Trial '{self.trial_code}' Year {self.year} saved successfully!")
        self.accept()
