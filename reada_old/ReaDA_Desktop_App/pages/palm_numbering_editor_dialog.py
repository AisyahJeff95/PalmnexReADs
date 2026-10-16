from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QComboBox,
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class PalmNumberingEditorDialog(QDialog):
    """
    Interactive Palm Numbering & Layout Editor
    - Standard QSpinBox buttons restored
    - Font color explicitly set to sharp black (#000000)
    """
    def __init__(self, parent=None, store=None, trial_code="PR1998/1", estate="Banting Station"):
        super().__init__(parent)
        self.store = store
        self.trial_code = trial_code
        self.estate = estate

        self.setWindowTitle(f"Plot Palm Numbering Configuration - [{self.trial_code}]")
        self.setFixedSize(780, 600)
        self.setStyleSheet("background-color: #dcdcdc;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(12)

        # -----------------------------------------------------------------
        # 1. Dark Navy Banner Header
        # -----------------------------------------------------------------
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #000055; border: 1px solid #000033; border-radius: 3px;")
        header_frame.setFixedHeight(45)
        h_layout = QHBoxLayout(header_frame)
        h_layout.setContentsMargins(0, 0, 0, 0)

        header_lbl = QLabel("Plot Palm Numbering & Layout Configuration")
        header_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #ffffff; letter-spacing: 1px; border: none; background: transparent;")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(header_lbl)

        main_layout.addWidget(header_frame)

        # -----------------------------------------------------------------
        # 2. Trial Info & Auto-Fill Control Bar
        # -----------------------------------------------------------------
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        ctrl_layout = QHBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(12, 8, 12, 8)
        ctrl_layout.setSpacing(15)

        info_lbl = QLabel(f"<b>Trial Code:</b> {self.trial_code} &nbsp;|&nbsp; <b>Estate:</b> {self.estate}")
        info_lbl.setFont(QFont("Times New Roman", 12))
        info_lbl.setStyleSheet("color: #000000;")
        ctrl_layout.addWidget(info_lbl)

        ctrl_layout.addStretch()

        gen_lbl = QLabel("Palms / Plot:")
        gen_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        gen_lbl.setStyleSheet("color: #000000;")

        self.palms_per_plot_spin = QSpinBox()
        self.palms_per_plot_spin.setRange(1, 55)
        self.palms_per_plot_spin.setValue(16)
        self.palms_per_plot_spin.setFixedWidth(65)
        self.palms_per_plot_spin.setStyleSheet("""
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
        """)

        gen_btn = QPushButton("⚡ Auto-Fill Palms for Plots")
        gen_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        gen_btn.setStyleSheet("""
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
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        gen_btn.clicked.connect(self.on_auto_fill_palms)

        ctrl_layout.addWidget(gen_lbl)
        ctrl_layout.addWidget(self.palms_per_plot_spin)
        ctrl_layout.addWidget(gen_btn)

        main_layout.addWidget(ctrl_frame)

        # -----------------------------------------------------------------
        # 3. Main Grid Table Editor
        # -----------------------------------------------------------------
        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Plot No.", "Palm No.", "Palm Status", "Progeny Code", "Remarks"
        ])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 80)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
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
            QTableWidget::item {
                color: #000000;
                padding: 4px;
            }
            QHeaderView::section {
                background-color: #666666;
                color: #ffffff;
                font-family: "Times New Roman", serif;
                font-weight: bold;
                border: 1px solid #444444;
                font-size: 12px;
                padding: 4px;
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
            QPushButton:focus {
                outline: none;
            }
            QPushButton:hover {
                background-color: #f4f4f5;
                border-color: #800000;
                color: #800000;
            }
            QPushButton:pressed {
                background-color: #e4e4e7;
            }
        """

        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        add_row_btn = QPushButton("➕ Add Palm Row")
        add_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        add_row_btn.setStyleSheet(btn_qss)
        add_row_btn.clicked.connect(self.on_add_row)

        del_row_btn = QPushButton("🗑️ Delete Selected Palm")
        del_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        del_row_btn.setStyleSheet(btn_qss)
        del_row_btn.clicked.connect(self.on_delete_row)

        save_btn = QPushButton("💾 Save Palm Numbering")
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
            QPushButton:hover {
                background-color: #990000;
            }
        """)
        save_btn.clicked.connect(self.on_save_palms)

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
        records = self.store.get_palm_numbering(self.trial_code) if self.store else []
        if not records:
            records = [
                (1, 1, "Record Palm", "DxP AVROS", "Active"),
                (1, 2, "Record Palm", "DxP AVROS", "Active"),
                (1, 3, "Guard / Border Palm", "DxP AVROS", "Border Buffer"),
                (1, 4, "Dead / Missing", "DxP AVROS", "Replaced 2024")
            ]

        self.populate_table(records)

    def populate_table(self, records):
        self.table.setRowCount(len(records))
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
        line_qss = """
            QLineEdit, QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Segoe UI", sans-serif;
                font-size: 12px;
                padding: 2px 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                selection-background-color: #0078d7;
            }
        """
        for row_idx, r in enumerate(records):
            p_no_spin = QSpinBox()
            p_no_spin.setRange(1, 200)
            p_no_spin.setValue(int(r[0]))
            p_no_spin.setStyleSheet(spin_qss)
            p_no_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

            palm_no_spin = QSpinBox()
            palm_no_spin.setRange(1, 200)
            palm_no_spin.setValue(int(r[1]))
            palm_no_spin.setStyleSheet(spin_qss)
            palm_no_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

            status_combo = QComboBox()
            status_combo.setStyleSheet(line_qss)
            status_combo.addItems(["Record Palm", "Guard / Border Palm", "Dead / Missing"])
            status_combo.setCurrentText(str(r[2]))

            prog_edit = QLineEdit(str(r[3]))
            prog_edit.setStyleSheet(line_qss)

            rem_edit = QLineEdit(str(r[4]))
            rem_edit.setStyleSheet(line_qss)

            self.table.setCellWidget(row_idx, 0, p_no_spin)
            self.table.setCellWidget(row_idx, 1, palm_no_spin)
            self.table.setCellWidget(row_idx, 2, status_combo)
            self.table.setCellWidget(row_idx, 3, prog_edit)
            self.table.setCellWidget(row_idx, 4, rem_edit)

    def on_auto_fill_palms(self):
        palms_count = self.palms_per_plot_spin.value()
        treats = self.store.get_plot_treatments(self.trial_code) if self.store else []
        plot_numbers = [t[0] for t in treats] if treats else list(range(1, 5))

        records = []
        for plot_no in plot_numbers:
            for p in range(1, palms_count + 1):
                status = "Guard / Border Palm" if (p == 1 or p == palms_count) else "Record Palm"
                records.append((plot_no, p, status, "DxP AVROS", "Active"))

        self.populate_table(records)
        QMessageBox.information(self, "Palms Generated", f"Auto-generated {palms_count} palms across {len(plot_numbers)} plot(s)!")

    def on_add_row(self):
        curr_rows = self.table.rowCount()
        new_rec = (1, curr_rows + 1, "Record Palm", "DxP AVROS", "Active")
        records = []

        for r in range(curr_rows):
            p_no = self.table.cellWidget(r, 0).value()
            palm_no = self.table.cellWidget(r, 1).value()
            status = self.table.cellWidget(r, 2).currentText()
            prog = self.table.cellWidget(r, 3).text()
            rem = self.table.cellWidget(r, 4).text()
            records.append((p_no, palm_no, status, prog, rem))

        records.append(new_rec)
        self.populate_table(records)

    def on_delete_row(self):
        curr_row = self.table.currentRow()
        if curr_row >= 0:
            self.table.removeRow(curr_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please click a row to delete.")

    def on_save_palms(self):
        records = []
        for r in range(self.table.rowCount()):
            try:
                p_no = self.table.cellWidget(r, 0).value()
                palm_no = self.table.cellWidget(r, 1).value()
                status = self.table.cellWidget(r, 2).currentText()
                prog = self.table.cellWidget(r, 3).text().strip()
                rem = self.table.cellWidget(r, 4).text().strip()
                records.append((p_no, palm_no, status, prog, rem))
            except Exception:
                pass

        if self.store:
            self.store.save_palm_numbering(self.trial_code, records)
            QMessageBox.information(self, "Saved", f"Saved {len(records)} palm numbering record(s) for Trial '{self.trial_code}'!")
            self.accept()
        else:
            self.accept()
