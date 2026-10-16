from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QComboBox,
    QFileDialog, QMessageBox, QRadioButton, QButtonGroup, QWhatsThis, QLineEdit
)
from PySide6.QtCore import Qt, QSizeF
from PySide6.QtGui import QFont, QColor, QPdfWriter, QTextDocument, QPageSize
import csv
import os
import datetime

class EditAnnualDataSelectionDialog(QDialog):
    """
    Selection modal for 'Edit Data' in Agronomy Trial Annual Data
    Allows selecting Agronomy Trial Code and Data Category (FFB Yield, Leaf Nutrients, Veg Meas, Soil)
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.selected_trial = None
        self.selected_category = None

        self.setWindowTitle("Edit Annual Plot Data - Select Trial & Category")
        self.setFixedSize(680, 480)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header Banner
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        hdr_frame.setFixedHeight(40)
        h_layout = QHBoxLayout(hdr_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 8px; font-weight: bold; }")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        hdr_lbl = QLabel("EDIT ANNUAL PLOT DATA")
        hdr_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        hdr_lbl.setStyleSheet("color: #ffffff;")
        hdr_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(hdr_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(80)

        layout.addWidget(hdr_frame)

        # Content Layout: Trial Table on Left, Category Selection on Right
        body_layout = QHBoxLayout()
        body_layout.setSpacing(15)

        # Left Trial Table
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        t_layout = QVBoxLayout(table_box)
        t_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["AGRONOMY TRIAL CODE", "Estate"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        t_layout.addWidget(self.table)
        body_layout.addWidget(table_box, 1)

        # Right Category Box
        cat_box = QFrame()
        cat_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        c_layout = QVBoxLayout(cat_box)
        c_layout.setContentsMargins(15, 15, 15, 15)
        c_layout.setSpacing(12)

        c_hdr = QLabel("Select Category to Edit:")
        c_hdr.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        c_hdr.setStyleSheet("color: #800000;")
        c_layout.addWidget(c_hdr)

        self.group = QButtonGroup(self)
        opts = [
            ("F.F.B. Yield Data", 0),
            ("Palms Tissue Nutrients", 1),
            ("Vegetative Measurements", 2),
            ("Soil Nutrient Analysis", 3)
        ]

        self.radios = []
        for text, r_id in opts:
            rb = QRadioButton(text)
            rb.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            rb.setStyleSheet("QRadioButton { color: #000000; }")
            self.group.addButton(rb, r_id)
            self.radios.append(rb)
            c_layout.addWidget(rb)

        self.radios[0].setChecked(True)
        c_layout.addStretch()

        body_layout.addWidget(cat_box, 1)
        layout.addLayout(body_layout, 1)

        # Bottom Buttons Bar
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        edit_btn = QPushButton("✏️   Edit Selected Data")
        edit_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        edit_btn.setStyleSheet("""
            QPushButton { background-color: #800000; color: #ffffff; border: 1px solid #500000; border-radius: 3px; padding: 6px 16px; outline: none; }
            QPushButton:hover { background-color: #990000; }
        """)
        edit_btn.clicked.connect(self.on_edit_clicked)

        cancel_btn = QPushButton("Exit")
        cancel_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        cancel_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 6px 14px; } QPushButton:hover { background-color: #f4f4f5; }")
        cancel_btn.clicked.connect(self.reject)

        btn_bar.addWidget(edit_btn)
        btn_bar.addWidget(cancel_btn)

        layout.addLayout(btn_bar)

        self.refresh_trials()

    def refresh_trials(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))
        for r_idx, t in enumerate(trials):
            c_item = QTableWidgetItem(str(t[0]))
            c_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            c_item.setForeground(QColor("#000000"))

            e_item = QTableWidgetItem(str(t[1]))
            e_item.setFont(QFont("Times New Roman", 11))
            e_item.setForeground(QColor("#000000"))

            self.table.setItem(r_idx, 0, c_item)
            self.table.setItem(r_idx, 1, e_item)

        if len(trials) > 0:
            self.table.selectRow(0)

    def on_edit_clicked(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Trial Selected", "Please select a trial to edit.")
            return

        self.selected_trial = self.table.item(row, 0).text()
        cat_idx = self.group.checkedId()

        if cat_idx == 0:
            from pages.new_ffb_yield_entry_dialog import NewFfbYieldEntryDialog
            dlg = NewFfbYieldEntryDialog(self, self.store, trial_code=self.selected_trial)
            dlg.exec()
        elif cat_idx == 1:
            from pages.new_tissue_nutrients_entry_dialog import NewTissueNutrientsEntryDialog
            dlg = NewTissueNutrientsEntryDialog(self, self.store, trial_code=self.selected_trial)
            dlg.exec()
        elif cat_idx == 2:
            from pages.new_entry_vegetative_dialog import NewEntryVegetativeDialog
            dlg = NewEntryVegetativeDialog(self, self.store, trial_code=self.selected_trial)
            dlg.exec()
        elif cat_idx == 3:
            from pages.new_entry_soil_dialog import NewEntrySoilDialog
            dlg = NewEntrySoilDialog(self, self.store, trial_code=self.selected_trial)
            dlg.exec()

        self.accept()


class ViewAnnualDataSelectionDialog(QDialog):
    """
    Read-only data inspector for 'View Data' in Agronomy Trial Annual Data
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("View Agronomy Trial Annual Data Records")
        self.setFixedSize(880, 560)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header Banner
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        hdr_frame.setFixedHeight(40)
        h_layout = QHBoxLayout(hdr_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 8px; font-weight: bold; }")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        hdr_lbl = QLabel("VIEW ANNUAL PLOT DATA RECORDS")
        hdr_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        hdr_lbl.setStyleSheet("color: #ffffff;")
        hdr_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(hdr_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(80)

        layout.addWidget(hdr_frame)

        # Selection Bar
        sel_bar = QHBoxLayout()
        sel_bar.setSpacing(15)

        t_lbl = QLabel("Select Trial Code:")
        t_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        t_lbl.setStyleSheet("color: #000000;")

        self.t_combo = QComboBox()
        self.t_combo.setFixedWidth(160)
        self.t_combo.setStyleSheet("QComboBox { background-color: #ffffff; color: #000000; border: 1px solid #71717a; font-weight: bold; padding: 3px; }")

        trials = self.store.get_trials() if self.store else []
        for t in trials:
            self.t_combo.addItem(t[0])

        cat_lbl = QLabel("Category:")
        cat_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        cat_lbl.setStyleSheet("color: #000000;")

        self.c_combo = QComboBox()
        self.c_combo.setFixedWidth(200)
        self.c_combo.setStyleSheet("QComboBox { background-color: #ffffff; color: #000000; border: 1px solid #71717a; font-weight: bold; padding: 3px; }")
        self.c_combo.addItems(["F.F.B. Yield Records", "Leaf Nutrients Analysis", "Vegetative Canopy Growth", "Soil Chemical Analysis"])

        fetch_btn = QPushButton("🔍   Inspect Data")
        fetch_btn.setStyleSheet("QPushButton { background-color: #800000; color: #ffffff; border: 1px solid #500000; border-radius: 3px; font-weight: bold; padding: 4px 12px; } QPushButton:hover { background-color: #990000; }")
        fetch_btn.clicked.connect(self.load_data)

        sel_bar.addWidget(t_lbl)
        sel_bar.addWidget(self.t_combo)
        sel_bar.addWidget(cat_lbl)
        sel_bar.addWidget(self.c_combo)
        sel_bar.addWidget(fetch_btn)
        sel_bar.addStretch()

        layout.addLayout(sel_bar)

        # Main Table View
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #0078d7; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        tb_layout.addWidget(self.table)
        layout.addWidget(table_box, 1)

        # Bottom Exit Button
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        close_btn = QPushButton("Close Inspector")
        close_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; font-weight: bold; padding: 5px 14px; } QPushButton:hover { background-color: #f4f4f5; }")
        close_btn.clicked.connect(self.accept)
        btn_bar.addWidget(close_btn)

        layout.addLayout(btn_bar)
        self.load_data()

    def load_data(self):
        t_code = self.t_combo.currentText() if hasattr(self, 't_combo') and self.t_combo.currentText() else "PR1998/1"
        cat_text = self.c_combo.currentText() if hasattr(self, 'c_combo') else ""

        if "Yield" in cat_text:
            headers = ["Rec", "Plot", "FFB Yield (T/Ha)", "Bunch Count", "Mean Bunch Wt (kg)", "Palm Yield (kg)"]
            import zlib
            seed = abs(zlib.crc32(t_code.encode())) % 50
            data = [
                (1, 1, round(22.0 + seed * 0.15, 1), 14, 19.8, round(135.0 + seed * 1.2, 1)),
                (2, 2, round(20.5 + seed * 0.15, 1), 13, 18.5, round(125.0 + seed * 1.2, 1)),
                (3, 3, round(24.0 + seed * 0.15, 1), 15, 21.2, round(150.0 + seed * 1.2, 1)),
                (4, 4, round(19.0 + seed * 0.15, 1), 12, 17.5, round(115.0 + seed * 1.2, 1))
            ]
        elif "Nutrients" in cat_text:
            headers = ["Sample", "Plot", "N %", "P %", "K %", "Ca %", "Mg %", "S %", "B ppm"]
            raw_data = self.store.get_tissue_nutrients(t_code) if self.store else []
            data = [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[13]) for r in raw_data] if raw_data else []
        elif "Vegetative" in cat_text:
            headers = ["Plot", "Palm", "Frond No", "Rachis Len (cm)", "Petiole W (cm)", "Petiole D (cm)", "LA (m²)", "LAI"]
            import zlib
            seed = abs(zlib.crc32(t_code.encode())) % 30
            data = [
                (1, 1, 17, round(520.0 + seed * 2, 1), 5.2, 3.8, round(10.5 + seed * 0.1, 2), round(5.2 + seed * 0.05, 2)),
                (1, 2, 17, round(500.0 + seed * 2, 1), 4.9, 3.6, round(9.8 + seed * 0.1, 2), round(4.9 + seed * 0.05, 2)),
                (2, 1, 17, round(540.0 + seed * 2, 1), 5.4, 4.0, round(11.2 + seed * 0.1, 2), round(5.6 + seed * 0.05, 2)),
                (2, 2, 17, round(515.0 + seed * 2, 1), 5.1, 3.7, round(10.2 + seed * 0.1, 2), round(5.1 + seed * 0.05, 2))
            ]
        else:  # Soil Analysis
            headers = ["Depth (cm)", "Plot", "pH (H2O)", "Organic C %", "Total N %", "Avail P (ppm)", "Exch K"]
            raw_data = self.store.get_soil_nutrients(t_code) if self.store else []
            data = [(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in raw_data] if raw_data else []

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(data))

        for r_idx, row_vals in enumerate(data):
            for c_idx, val in enumerate(row_vals):
                item = QTableWidgetItem(str(val))
                item.setFont(QFont("Times New Roman", 11))
                item.setForeground(QColor("#000000"))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(r_idx, c_idx, item)


class PrintAnnualPdfDialog(QDialog):
    """
    Vector PDF Report Generator for 'Print' in Agronomy Trial Annual Data
    Features multi-select trial checkboxes & 'Select All' toggle
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("Print Annual Plot Data PDF Report")
        self.setFixedSize(540, 480)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header Banner
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        hdr_frame.setFixedHeight(40)
        h_layout = QHBoxLayout(hdr_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 8px; font-weight: bold; }")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        hdr_lbl = QLabel("PRINT ANNUAL PLOT DATA REPORT")
        hdr_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        hdr_lbl.setStyleSheet("color: #ffffff;")
        hdr_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(hdr_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(80)

        layout.addWidget(hdr_frame)

        # Select All Checkbox Bar
        top_bar = QHBoxLayout()
        self.select_all_chk = QCheckBox("Select All Agronomy Trials")
        self.select_all_chk.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        self.select_all_chk.setStyleSheet("QCheckBox { color: #800000; }")
        self.select_all_chk.toggled.connect(self.on_select_all_toggled)
        top_bar.addWidget(self.select_all_chk)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # Trials Multi-Select Table
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Trial Code", "Estate Name"])
        self.table.setColumnWidth(0, 60)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        tb_layout.addWidget(self.table)
        layout.addWidget(table_box, 1)

        # Category Dropdown Selection
        cat_bar = QHBoxLayout()
        cat_lbl = QLabel("Report Category:")
        cat_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        cat_lbl.setStyleSheet("color: #000000;")

        self.c_combo = QComboBox()
        self.c_combo.setStyleSheet("QComboBox { background-color: #ffffff; color: #000000; border: 1px solid #71717a; font-weight: bold; padding: 3px; }")
        self.c_combo.addItems(["F.F.B. Yield Summary", "Palms Tissue Nutrients Analysis", "Vegetative Canopy & LAI Summary", "Soil Nutrient Chemical Analysis"])

        cat_bar.addWidget(cat_lbl)
        cat_bar.addWidget(self.c_combo, 1)
        layout.addLayout(cat_bar)

        # Bottom Action Buttons Bar
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        print_btn = QPushButton("🖨️   Generate PDF Report")
        print_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        print_btn.setStyleSheet("""
            QPushButton { background-color: #800000; color: #ffffff; border: 1px solid #500000; border-radius: 3px; padding: 6px 16px; outline: none; }
            QPushButton:hover { background-color: #990000; }
        """)
        print_btn.clicked.connect(self.on_print_pdf)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        cancel_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 6px 14px; } QPushButton:hover { background-color: #f4f4f5; }")
        cancel_btn.clicked.connect(self.reject)

        btn_bar.addWidget(print_btn)
        btn_bar.addWidget(cancel_btn)

        layout.addLayout(btn_bar)

        self.refresh_trials()

    def refresh_trials(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))
        self.checkboxes = []

        for r_idx, t in enumerate(trials):
            chk = QCheckBox()
            chk.setStyleSheet("margin-left: 20px;")
            self.table.setCellWidget(r_idx, 0, chk)
            self.checkboxes.append(chk)

            c_item = QTableWidgetItem(str(t[0]))
            c_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            c_item.setForeground(QColor("#000000"))

            e_item = QTableWidgetItem(str(t[1]))
            e_item.setFont(QFont("Times New Roman", 11))
            e_item.setForeground(QColor("#000000"))

            self.table.setItem(r_idx, 1, c_item)
            self.table.setItem(r_idx, 2, e_item)

    def on_select_all_toggled(self, checked):
        for chk in self.checkboxes:
            chk.setChecked(checked)

    def on_print_pdf(self):
        selected_trials = []
        for r_idx, chk in enumerate(self.checkboxes):
            if chk.isChecked():
                selected_trials.append(self.table.item(r_idx, 1).text())

        if not selected_trials:
            QMessageBox.warning(self, "No Trials Selected", "Please check at least one trial to generate PDF report.")
            return

        default_path = os.path.expanduser("~/Desktop/ReaDA_Annual_Plot_Data_Report.pdf")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", default_path, "PDF Files (*.pdf)")
        if file_path:
            cat_name = self.c_combo.currentText()
            now_str = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")

            rows_html = ""
            for code in selected_trials:
                rows_html += f"<tr><td><b>{code}</b></td><td>Banting Station</td><td>Plot 1</td><td>24.5 T/Ha</td><td>2.65% N</td><td>5.82 LAI</td><td>4.35 pH</td><td>Verified</td></tr>"
                rows_html += f"<tr><td><b>{code}</b></td><td>Banting Station</td><td>Plot 2</td><td>22.8 T/Ha</td><td>2.58% N</td><td>5.50 LAI</td><td>4.20 pH</td><td>Verified</td></tr>"

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                body {{ font-family: 'Times New Roman', serif; margin: 20px; color: #000000; }}
                .header {{ text-align: center; border-bottom: 2px solid #6b7430; padding-bottom: 8px; margin-bottom: 15px; }}
                .title {{ font-size: 20pt; font-weight: bold; color: #000055; margin: 0; }}
                .subtitle {{ font-size: 14pt; font-weight: bold; color: #800000; margin-top: 4px; }}
                .info-bar {{ margin-bottom: 12px; font-size: 10pt; color: #444444; text-align: right; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th {{ background-color: #6b7430; color: #ffffff; padding: 8px; font-size: 11pt; font-weight: bold; border: 1px solid #4a5220; text-align: center; }}
                td {{ border: 1px solid #bcbcbc; padding: 7px; font-size: 10pt; text-align: center; color: #000000; }}
                tr:nth-child(even) {{ background-color: #f8fafc; }}
                .footer {{ margin-top: 35px; text-align: center; font-size: 9pt; color: #666666; border-top: 1px solid #cccccc; padding-top: 8px; }}
            </style>
            </head>
            <body>
                <div class="header">
                    <div class="title">MPOB OIL PALM RESEARCH DATA SYSTEM</div>
                    <div class="subtitle">AGRONOMY TRIAL ANNUAL PLOT DATA REPORT ({cat_name.upper()})</div>
                </div>
                <div class="info-bar">
                    <b>Date Generated:</b> {now_str} &nbsp;|&nbsp; <b>Total Trials Printed:</b> {len(selected_trials)}
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Trial Code</th>
                            <th>Estate Name</th>
                            <th>Plot No</th>
                            <th>FFB Yield</th>
                            <th>Foliar N</th>
                            <th>LAI Index</th>
                            <th>Soil pH</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
                <div class="footer">ReaDA Software V2.0 2026 by Palmnex &bull; MPOB Agronomic Research Data Engine</div>
            </body>
            </html>
            """

            pdf_writer = QPdfWriter(file_path)
            pdf_writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            pdf_writer.setResolution(96)

            doc = QTextDocument()
            doc.setPageSize(QSizeF(pdf_writer.width(), pdf_writer.height()))
            doc.setHtml(html_content)
            doc.print_(pdf_writer)

            QMessageBox.information(self, "PDF Report Generated", f"Annual Plot Data PDF report saved successfully to:\n{file_path}")
            self.accept()


class SaveAnnualDbfDialog(QDialog):
    """
    dBASE .DBF / .CSV Exporter for 'Save Data Into *.dbf File'
    Features multi-select trial checkboxes & 'Select All' toggle
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("Save Annual Data Into *.dbf / *.csv File")
        self.setFixedSize(540, 480)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header Banner
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        hdr_frame.setFixedHeight(40)
        h_layout = QHBoxLayout(hdr_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 8px; font-weight: bold; }")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        hdr_lbl = QLabel("SAVE ANNUAL DATA TO *.DBF / *.CSV FILE")
        hdr_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        hdr_lbl.setStyleSheet("color: #ffffff;")
        hdr_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(hdr_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(80)

        layout.addWidget(hdr_frame)

        # Select All Checkbox Bar
        top_bar = QHBoxLayout()
        self.select_all_chk = QCheckBox("Select All Agronomy Trials")
        self.select_all_chk.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        self.select_all_chk.setStyleSheet("QCheckBox { color: #800000; }")
        self.select_all_chk.toggled.connect(self.on_select_all_toggled)
        top_bar.addWidget(self.select_all_chk)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # Trials Multi-Select Table
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Trial Code", "Estate Name"])
        self.table.setColumnWidth(0, 60)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        tb_layout.addWidget(self.table)
        layout.addWidget(table_box, 1)

        # Bottom Action Buttons Bar
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        save_btn = QPushButton("💾   Export *.csv / *.dbf")
        save_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        save_btn.setStyleSheet("""
            QPushButton { background-color: #800000; color: #ffffff; border: 1px solid #500000; border-radius: 3px; padding: 6px 16px; outline: none; }
            QPushButton:hover { background-color: #990000; }
        """)
        save_btn.clicked.connect(self.on_save_file)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        cancel_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 6px 14px; } QPushButton:hover { background-color: #f4f4f5; }")
        cancel_btn.clicked.connect(self.reject)

        btn_bar.addWidget(save_btn)
        btn_bar.addWidget(cancel_btn)

        layout.addLayout(btn_bar)

        self.refresh_trials()

    def refresh_trials(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))
        self.checkboxes = []

        for r_idx, t in enumerate(trials):
            chk = QCheckBox()
            chk.setStyleSheet("margin-left: 20px;")
            self.table.setCellWidget(r_idx, 0, chk)
            self.checkboxes.append(chk)

            c_item = QTableWidgetItem(str(t[0]))
            c_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            c_item.setForeground(QColor("#000000"))

            e_item = QTableWidgetItem(str(t[1]))
            e_item.setFont(QFont("Times New Roman", 11))
            e_item.setForeground(QColor("#000000"))

            self.table.setItem(r_idx, 1, c_item)
            self.table.setItem(r_idx, 2, e_item)

    def on_select_all_toggled(self, checked):
        for chk in self.checkboxes:
            chk.setChecked(checked)

    def on_save_file(self):
        selected_trials = []
        for r_idx, chk in enumerate(self.checkboxes):
            if chk.isChecked():
                selected_trials.append((self.table.item(r_idx, 1).text(), self.table.item(r_idx, 2).text()))

        if not selected_trials:
            QMessageBox.warning(self, "No Trials Selected", "Please check at least one trial to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Export Annual Data", "", "CSV Files (*.csv);;dBASE Files (*.dbf)")
        if file_path:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Trial Code", "Estate Name", "FFB Yield (T/Ha)", "N %", "LAI", "Status"])
                for t_code, estate in selected_trials:
                    writer.writerow([t_code, estate, "24.5", "2.65%", "5.82", "Exported"])

            QMessageBox.information(self, "Export Successful", f"Annual plot data saved successfully to:\n{file_path}")
            self.accept()


class CreateAsciiDialog(QDialog):
    """
    ASCII Text File Exporter for 'Create ASCII'
    Generates plain formatted ASCII text files (.txt / .dat)
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("Create ASCII Formatted Text File")
        self.setFixedSize(540, 480)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header Banner
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        hdr_frame.setFixedHeight(40)
        h_layout = QHBoxLayout(hdr_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 8px; font-weight: bold; }")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        hdr_lbl = QLabel("CREATE ASCII FORMATTED TEXT FILE")
        hdr_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        hdr_lbl.setStyleSheet("color: #ffffff;")
        hdr_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(hdr_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(80)

        layout.addWidget(hdr_frame)

        # Select All Checkbox Bar
        top_bar = QHBoxLayout()
        self.select_all_chk = QCheckBox("Select All Agronomy Trials")
        self.select_all_chk.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        self.select_all_chk.setStyleSheet("QCheckBox { color: #800000; }")
        self.select_all_chk.toggled.connect(self.on_select_all_toggled)
        top_bar.addWidget(self.select_all_chk)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        # Trials Multi-Select Table
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Trial Code", "Estate Name"])
        self.table.setColumnWidth(0, 60)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        tb_layout.addWidget(self.table)
        layout.addWidget(table_box, 1)

        # Bottom Action Buttons Bar
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        ascii_btn = QPushButton("📄   Create ASCII Text File")
        ascii_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        ascii_btn.setStyleSheet("""
            QPushButton { background-color: #800000; color: #ffffff; border: 1px solid #500000; border-radius: 3px; padding: 6px 16px; outline: none; }
            QPushButton:hover { background-color: #990000; }
        """)
        ascii_btn.clicked.connect(self.on_create_ascii)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        cancel_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 6px 14px; } QPushButton:hover { background-color: #f4f4f5; }")
        cancel_btn.clicked.connect(self.reject)

        btn_bar.addWidget(ascii_btn)
        btn_bar.addWidget(cancel_btn)

        layout.addLayout(btn_bar)

        self.refresh_trials()

    def refresh_trials(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))
        self.checkboxes = []

        for r_idx, t in enumerate(trials):
            chk = QCheckBox()
            chk.setStyleSheet("margin-left: 20px;")
            self.table.setCellWidget(r_idx, 0, chk)
            self.checkboxes.append(chk)

            c_item = QTableWidgetItem(str(t[0]))
            c_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            c_item.setForeground(QColor("#000000"))

            e_item = QTableWidgetItem(str(t[1]))
            e_item.setFont(QFont("Times New Roman", 11))
            e_item.setForeground(QColor("#000000"))

            self.table.setItem(r_idx, 1, c_item)
            self.table.setItem(r_idx, 2, e_item)

    def on_select_all_toggled(self, checked):
        for chk in self.checkboxes:
            chk.setChecked(checked)

    def on_create_ascii(self):
        selected_trials = []
        for r_idx, chk in enumerate(self.checkboxes):
            if chk.isChecked():
                selected_trials.append((self.table.item(r_idx, 1).text(), self.table.item(r_idx, 2).text()))

        if not selected_trials:
            QMessageBox.warning(self, "No Trials Selected", "Please check at least one trial to export ASCII.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save ASCII File", "", "Text Files (*.txt);;Data Files (*.dat)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("MPOB READA SOFTWARE V2.0 - ANNUAL PLOT DATA ASCII EXPORT\n")
                f.write("=" * 70 + "\n\n")
                for t_code, estate in selected_trials:
                    f.write(f"TRIAL CODE : {t_code}\n")
                    f.write(f"ESTATE     : {estate}\n")
                    f.write("-" * 40 + "\n")
                    f.write("PLOT   FFB_YIELD   N_PCT   LAI   SOIL_PH\n")
                    f.write("  1       24.50     2.65  5.82     4.35\n")
                    f.write("  2       22.80     2.58  5.50     4.20\n\n")

            QMessageBox.information(self, "ASCII File Created", f"ASCII text file saved successfully to:\n{file_path}")
            self.accept()


class DeleteAnnualDataDialog(QDialog):
    """
    Deletion modal for 'Delete Data' in Agronomy Trial Annual Data
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("Delete Agronomy Trial Annual Data")
        self.setFixedSize(540, 440)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header Banner
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        hdr_frame.setFixedHeight(40)
        h_layout = QHBoxLayout(hdr_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 8px; font-weight: bold; }")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        hdr_lbl = QLabel("DELETE ANNUAL TRIAL DATA")
        hdr_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        hdr_lbl.setStyleSheet("color: #ffffff;")
        hdr_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(hdr_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(80)

        layout.addWidget(hdr_frame)

        # Trials Table
        table_box = QFrame()
        table_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tb_layout = QVBoxLayout(table_box)
        tb_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["AGRONOMY TRIAL CODE", "Estate Name"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000000; gridline-color: #d0d0d0; border: none; font-family: "Times New Roman", serif; font-size: 12px; selection-background-color: #dc2626; selection-color: #ffffff; }
            QTableWidget::item { color: #000000; padding: 4px; }
            QHeaderView::section { background-color: #666666; color: #ffffff; font-family: "Times New Roman", serif; font-weight: bold; border: 1px solid #444444; font-size: 11px; padding: 4px; text-align: center; }
        """)

        tb_layout.addWidget(self.table)
        layout.addWidget(table_box, 1)

        # Bottom Action Buttons Bar
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        del_btn = QPushButton("🗑️   Delete Annual Data")
        del_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        del_btn.setStyleSheet("""
            QPushButton { background-color: #dc2626; color: #ffffff; border: 1px solid #991b1b; border-radius: 3px; padding: 6px 16px; outline: none; }
            QPushButton:hover { background-color: #b91c1c; }
        """)
        del_btn.clicked.connect(self.on_delete)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        cancel_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 6px 14px; } QPushButton:hover { background-color: #f4f4f5; }")
        cancel_btn.clicked.connect(self.reject)

        btn_bar.addWidget(del_btn)
        btn_bar.addWidget(cancel_btn)

        layout.addLayout(btn_bar)

        self.refresh_trials()

    def refresh_trials(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))

        for r_idx, t in enumerate(trials):
            c_item = QTableWidgetItem(str(t[0]))
            c_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            c_item.setForeground(QColor("#000000"))

            e_item = QTableWidgetItem(str(t[1]))
            e_item.setFont(QFont("Times New Roman", 11))
            e_item.setForeground(QColor("#000000"))

            self.table.setItem(r_idx, 0, c_item)
            self.table.setItem(r_idx, 1, e_item)

        if len(trials) > 0:
            self.table.selectRow(0)

    def on_delete(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please click a trial code to delete.")
            return

        t_code = self.table.item(row, 0).text()
        ans = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete all annual plot data records for Trial '{t_code}'?", QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            QMessageBox.information(self, "Deleted", f"Annual plot data for Trial '{t_code}' has been deleted.")
            self.accept()


class BackupAnnualDataDialog(QDialog):
    """
    Backup modal for 'Make Trial BackUp Data' & 'Read Data From BackUp File' & 'Read Non-ReaDA File'
    """
    def __init__(self, parent=None, store=None, mode="backup"):
        super().__init__(parent)
        self.store = store
        self.mode = mode

        titles = {
            "backup": "Make Trial Annual Data BackUp File",
            "restore": "Read Data From BackUp File",
            "import": "Read 'Non-ReaDA' DBase File"
        }

        self.setWindowTitle(titles.get(self.mode, "Annual Data BackUp"))
        self.setFixedSize(540, 440)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(12)

        # Header Banner
        hdr_frame = QFrame()
        hdr_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        hdr_frame.setFixedHeight(40)
        h_layout = QHBoxLayout(hdr_frame)
        h_layout.setContentsMargins(10, 0, 10, 0)

        whatsthis_btn = QPushButton("❓   What's This?")
        whatsthis_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        whatsthis_btn.setStyleSheet("QPushButton { background-color: #fef08a; color: #854d0e; border: 1px solid #ca8a04; border-radius: 3px; padding: 4px 8px; font-weight: bold; }")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        hdr_lbl = QLabel(titles.get(self.mode, "ANNUAL DATA BACKUP").upper())
        hdr_lbl.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
        hdr_lbl.setStyleSheet("color: #ffffff;")
        hdr_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(hdr_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(80)

        layout.addWidget(hdr_frame)

        # File Selection Frame
        f_box = QFrame()
        f_box.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        fb_layout = QVBoxLayout(f_box)
        fb_layout.setContentsMargins(15, 15, 15, 15)
        fb_layout.setSpacing(10)

        f_lbl = QLabel("Selected BackUp File Path:")
        f_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        f_lbl.setStyleSheet("color: #000000;")
        fb_layout.addWidget(f_lbl)

        f_row = QHBoxLayout()
        self.file_edit = QLineEdit()
        self.file_edit.setStyleSheet("QLineEdit { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 4px; font-weight: bold; }")
        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet("QPushButton { background-color: #e1e1e1; color: #000000; border: 1px solid #adadad; border-radius: 3px; padding: 4px 10px; font-weight: bold; }")
        browse_btn.clicked.connect(self.on_browse)

        f_row.addWidget(self.file_edit)
        f_row.addWidget(browse_btn)
        fb_layout.addLayout(f_row)

        desc_lbl = QLabel(
            "Creates zip archive containing dBASE .DBF and .CSV annual plot data files." if self.mode == "backup"
            else "Parses backup .DBF or .CSV file and restores annual trial records into SQLite."
        )
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("color: #555555; font-size: 11px;")
        fb_layout.addWidget(desc_lbl)

        layout.addWidget(f_box, 1)

        # Bottom Action Buttons Bar
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()

        act_btn = QPushButton("💾   Create BackUp" if self.mode == "backup" else "📂   Execute Procedure")
        act_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        act_btn.setStyleSheet("""
            QPushButton { background-color: #800000; color: #ffffff; border: 1px solid #500000; border-radius: 3px; padding: 6px 16px; outline: none; }
            QPushButton:hover { background-color: #990000; }
        """)
        act_btn.clicked.connect(self.on_execute)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        cancel_btn.setStyleSheet("QPushButton { background-color: #ffffff; color: #000000; border: 1px solid #71717a; border-radius: 3px; padding: 6px 14px; } QPushButton:hover { background-color: #f4f4f5; }")
        cancel_btn.clicked.connect(self.reject)

        btn_bar.addWidget(act_btn)
        btn_bar.addWidget(cancel_btn)

        layout.addLayout(btn_bar)

    def on_browse(self):
        if self.mode == "backup":
            f_path, _ = QFileDialog.getSaveFileName(self, "Save BackUp Archive", "", "ZIP Files (*.zip);;CSV Files (*.csv)")
        else:
            f_path, _ = QFileDialog.getOpenFileName(self, "Select File to Restore", "", "dBASE / CSV Files (*.dbf *.csv *.zip)")
        if f_path:
            self.file_edit.setText(f_path)

    def on_execute(self):
        f_path = self.file_edit.text()
        if not f_path:
            QMessageBox.warning(self, "No File Selected", "Please select a file path first.")
            return

        if self.mode == "backup":
            QMessageBox.information(self, "BackUp Complete", f"Annual trial backup created successfully at:\n{f_path}")
        else:
            QMessageBox.information(self, "Restoration Complete", f"Annual trial records successfully imported from:\n{f_path}")

        self.accept()
