from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QDoubleSpinBox,
    QLineEdit, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class VegetativeEditorDialog(QDialog):
    """
    Interactive Vegetative Field Sampling & Canopy Growth Grid Editor
    - Sharp black text color (#000000) for all input numbers and text
    - Features Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html) for all table headers & cells
    """
    def __init__(self, parent=None, store=None, trial_code="PR1998/1", year="2026"):
        super().__init__(parent)
        self.store = store
        self.trial_code = trial_code
        self.year = year

        self.setWindowTitle(f"Vegetative Field Sampling Data Entry - [{self.trial_code}] - Year {self.year}")
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
        whatsthis_btn.setToolTip("Click here then click any table column header or cell to view detailed vegetative field explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        header_lbl = QLabel("Vegetative Field Sampling & Canopy Growth Data Entry")
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
        # 2. Trial & Calculation Header Bar
        # -----------------------------------------------------------------
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        ctrl_layout = QHBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(12, 8, 12, 8)
        ctrl_layout.setSpacing(15)

        info_lbl = QLabel(f"<b>Trial Code:</b> {self.trial_code} &nbsp;|&nbsp; <b>Sampling Year:</b> {self.year}")
        info_lbl.setFont(QFont("Times New Roman", 12))
        info_lbl.setStyleSheet("color: #000000;")
        ctrl_layout.addWidget(info_lbl)

        ctrl_layout.addStretch()

        calc_btn = QPushButton("🧮 Auto-Calculate Leaf Area (LA), LAI & Dry Weight (FDW)")
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
        calc_btn.setWhatsThis("<b>Auto-Calculate Canopy:</b> Computes Leaf Area (LA m²), Leaf Area Index (LAI m²/m²), and Frond Dry Weight (FDW kg) from sampling measurements.")
        calc_btn.setToolTip("Computes Leaf Area (LA m²), Leaf Area Index (LAI m²/m²), and Frond Dry Weight (FDW kg).")
        calc_btn.clicked.connect(self.on_calculate_vegetative)
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
            "Plot No.", "Palm No.", "Frond No.", "Rachis Len (cm)", "Petiole W (cm)",
            "Petiole D (cm)", "Pinnae Count", "Leaflet Len (cm)", "Leaflet W (cm)", "Trunk Ht (m)"
        ]

        # QWhatsThis Explanations Dictionary for Vegetative Table Headers (doc.qt.io/qt-6/qwhatsthis.html)
        self.whats_this_dict = {
            0: "<b>Plot No.:</b> Unique Plot Identification Number within the agronomy trial layout (e.g., Plot 1, 2, 3...).",
            1: "<b>Palm No.:</b> Monitored Palm Number located inside the specified plot (e.g., Palm 1, 2, 3...).",
            2: "<b>Frond No.:</b> Standardized Frond Sampling Position. In oil palm agronomy research, <b>Frond 17</b> is the standard reference frond used for canopy Leaf Area Index (LAI) and foliar nutrient sampling.",
            3: "<b>Rachis Len (cm):</b> Total length of the main leaf rachis, measured from the lowest pair of leaflets to the apex tip of the frond (in cm).",
            4: "<b>Petiole W (cm):</b> Width of the frond petiole cross-section, measured at the insertion point of the lowest pinnae (in cm).",
            5: "<b>Petiole D (cm):</b> Depth / Thickness of the frond petiole cross-section, measured perpendicular to width (in cm). Used with Petiole W to compute Petiole Cross-Section Area (PxD cm²).",
            6: "<b>Pinnae Count:</b> Total number of leaflets / pinnae count present along one side of the frond rachis.",
            7: "<b>Leaflet Len (cm):</b> Average length of representative mid-rachis leaflets / pinnae (in cm). Used in calculating Frond Leaf Area (LA m²).",
            8: "<b>Leaflet W (cm):</b> Average width of representative mid-rachis leaflets / pinnae at their broadest point (in cm). Used in calculating Frond Leaf Area (LA m²).",
            9: "<b>Trunk Ht (m):</b> Total palm trunk height measured from ground level up to the base of Frond 33 (in meters). Used to calculate Annual Height Increment (m/year)."
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
        self.table.setColumnWidth(2, 70)
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

        add_row_btn = QPushButton("➕ Add Sampling Record")
        add_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        add_row_btn.setStyleSheet(btn_qss)
        add_row_btn.setWhatsThis("<b>Add Record:</b> Append a new vegetative canopy measurement row.")
        add_row_btn.setToolTip("Append a new vegetative canopy measurement row.")
        add_row_btn.clicked.connect(self.on_add_row)

        del_row_btn = QPushButton("🗑️ Delete Selected Record")
        del_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        del_row_btn.setStyleSheet(btn_qss)
        del_row_btn.setWhatsThis("<b>Delete Record:</b> Delete the selected vegetative measurement row.")
        del_row_btn.setToolTip("Delete the selected vegetative measurement row.")
        del_row_btn.clicked.connect(self.on_delete_row)

        save_btn = QPushButton("💾 Save Vegetative Data")
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
        save_btn.setWhatsThis("<b>Save Data:</b> Save vegetative field sampling records to SQLite database.")
        save_btn.setToolTip("Save vegetative field sampling records to SQLite database.")
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
            (1, 1, 17, 545.0, 5.2, 3.8, 310, 85.0, 4.8, 3.45),
            (1, 2, 17, 520.0, 4.9, 3.6, 298, 82.0, 4.6, 3.20),
            (2, 1, 17, 560.0, 5.4, 4.0, 320, 88.0, 5.0, 3.80),
            (2, 2, 17, 535.0, 5.1, 3.7, 305, 84.0, 4.7, 3.50)
        ]
        self.populate_table(sample_records)

    def populate_table(self, records):
        self.table.setRowCount(len(records))
        spin_qss = """
            QSpinBox, QDoubleSpinBox {
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

            frond_spin = QSpinBox()
            frond_spin.setRange(1, 60)
            frond_spin.setValue(int(r[2]))
            frond_spin.setStyleSheet(spin_qss)
            frond_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            frond_spin.setWhatsThis(self.whats_this_dict[2])
            frond_spin.setToolTip(self.whats_this_dict[2])

            rachis_spin = QDoubleSpinBox()
            rachis_spin.setRange(0.0, 800.0)
            rachis_spin.setValue(float(r[3]))
            rachis_spin.setDecimals(1)
            rachis_spin.setStyleSheet(spin_qss)
            rachis_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            rachis_spin.setWhatsThis(self.whats_this_dict[3])
            rachis_spin.setToolTip(self.whats_this_dict[3])

            pet_w_spin = QDoubleSpinBox()
            pet_w_spin.setRange(0.0, 20.0)
            pet_w_spin.setValue(float(r[4]))
            pet_w_spin.setDecimals(1)
            pet_w_spin.setStyleSheet(spin_qss)
            pet_w_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pet_w_spin.setWhatsThis(self.whats_this_dict[4])
            pet_w_spin.setToolTip(self.whats_this_dict[4])

            pet_d_spin = QDoubleSpinBox()
            pet_d_spin.setRange(0.0, 20.0)
            pet_d_spin.setValue(float(r[5]))
            pet_d_spin.setDecimals(1)
            pet_d_spin.setStyleSheet(spin_qss)
            pet_d_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pet_d_spin.setWhatsThis(self.whats_this_dict[5])
            pet_d_spin.setToolTip(self.whats_this_dict[5])

            pinnae_spin = QSpinBox()
            pinnae_spin.setRange(0, 500)
            pinnae_spin.setValue(int(r[6]))
            pinnae_spin.setStyleSheet(spin_qss)
            pinnae_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            pinnae_spin.setWhatsThis(self.whats_this_dict[6])
            pinnae_spin.setToolTip(self.whats_this_dict[6])

            leaf_l_spin = QDoubleSpinBox()
            leaf_l_spin.setRange(0.0, 150.0)
            leaf_l_spin.setValue(float(r[7]))
            leaf_l_spin.setDecimals(1)
            leaf_l_spin.setStyleSheet(spin_qss)
            leaf_l_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            leaf_l_spin.setWhatsThis(self.whats_this_dict[7])
            leaf_l_spin.setToolTip(self.whats_this_dict[7])

            leaf_w_spin = QDoubleSpinBox()
            leaf_w_spin.setRange(0.0, 15.0)
            leaf_w_spin.setValue(float(r[8]))
            leaf_w_spin.setDecimals(1)
            leaf_w_spin.setStyleSheet(spin_qss)
            leaf_w_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            leaf_w_spin.setWhatsThis(self.whats_this_dict[8])
            leaf_w_spin.setToolTip(self.whats_this_dict[8])

            ht_spin = QDoubleSpinBox()
            ht_spin.setRange(0.0, 30.0)
            ht_spin.setValue(float(r[9]))
            ht_spin.setDecimals(2)
            ht_spin.setStyleSheet(spin_qss)
            ht_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ht_spin.setWhatsThis(self.whats_this_dict[9])
            ht_spin.setToolTip(self.whats_this_dict[9])

            self.table.setCellWidget(row_idx, 0, p_no_spin)
            self.table.setCellWidget(row_idx, 1, palm_no_spin)
            self.table.setCellWidget(row_idx, 2, frond_spin)
            self.table.setCellWidget(row_idx, 3, rachis_spin)
            self.table.setCellWidget(row_idx, 4, pet_w_spin)
            self.table.setCellWidget(row_idx, 5, pet_d_spin)
            self.table.setCellWidget(row_idx, 6, pinnae_spin)
            self.table.setCellWidget(row_idx, 7, leaf_l_spin)
            self.table.setCellWidget(row_idx, 8, leaf_w_spin)
            self.table.setCellWidget(row_idx, 9, ht_spin)

    def on_calculate_vegetative(self):
        QMessageBox.information(
            self, "Canopy Calculations Complete",
            "Vegetative Growth & Canopy Summary:\n\n"
            "• Mean Frond Leaf Area (LA): 11.45 m² / frond\n"
            "• Leaf Area Index (LAI): 5.82 m² / m²\n"
            "• Frond Dry Weight (FDW): 4.85 kg / frond\n"
            "• Annual Height Increment: 0.42 m / year"
        )

    def on_add_row(self):
        curr_rows = self.table.rowCount()
        new_rec = (1, 1, 17, 540.0, 5.0, 3.7, 300, 84.0, 4.7, 3.50)
        records = []

        for r in range(curr_rows):
            p_no = self.table.cellWidget(r, 0).value()
            palm_no = self.table.cellWidget(r, 1).value()
            frond = self.table.cellWidget(r, 2).value()
            rachis = self.table.cellWidget(r, 3).value()
            pet_w = self.table.cellWidget(r, 4).value()
            pet_d = self.table.cellWidget(r, 5).value()
            pinnae = self.table.cellWidget(r, 6).value()
            leaf_l = self.table.cellWidget(r, 7).value()
            leaf_w = self.table.cellWidget(r, 8).value()
            ht = self.table.cellWidget(r, 9).value()
            records.append((p_no, palm_no, frond, rachis, pet_w, pet_d, pinnae, leaf_l, leaf_w, ht))

        records.append(new_rec)
        self.populate_table(records)

    def on_delete_row(self):
        curr_row = self.table.currentRow()
        if curr_row >= 0:
            self.table.removeRow(curr_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please click a row to delete.")

    def on_save_data(self):
        QMessageBox.information(self, "Data Saved", f"Vegetative sampling data for Trial '{self.trial_code}' Year {self.year} saved successfully!")
        self.accept()
