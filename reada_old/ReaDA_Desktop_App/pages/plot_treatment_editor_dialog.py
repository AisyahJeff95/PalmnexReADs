from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox,
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class PlotTreatmentEditorDialog(QDialog):
    """
    Interactive Plot Treatment Factor Level Editor
    - Standard QSpinBox buttons restored
    - Font color explicitly set to sharp black (#000000)
    """
    def __init__(self, parent=None, store=None, trial_code="PR1998/1", estate="Banting Station"):
        super().__init__(parent)
        self.store = store
        self.trial_code = trial_code
        self.estate = estate

        self.setWindowTitle(f"Plot Treatment Factor Mapping - [{self.trial_code}]")
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

        header_lbl = QLabel("Plot Treatment Factor Level Mapping")
        header_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #ffffff; letter-spacing: 1px; border: none; background: transparent;")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(header_lbl)

        main_layout.addWidget(header_frame)

        # -----------------------------------------------------------------
        # 2. Trial Info & Auto-Generate Control Bar
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

        gen_lbl = QLabel("Total Plots:")
        gen_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        gen_lbl.setStyleSheet("color: #000000;")

        self.num_plots_spin = QSpinBox()
        self.num_plots_spin.setRange(1, 200)
        self.num_plots_spin.setValue(36)
        self.num_plots_spin.setFixedWidth(65)
        self.num_plots_spin.setStyleSheet("""
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

        gen_btn = QPushButton("⚡ Auto-Generate Plots")
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
        gen_btn.clicked.connect(self.on_auto_generate)

        ctrl_layout.addWidget(gen_lbl)
        ctrl_layout.addWidget(self.num_plots_spin)
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Plot No.", "Factor 1 (N Level)", "Factor 2 (P Level)", "Factor 3 (K Level)", "Extra Plot", "Sub Plot Factor"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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

        add_row_btn = QPushButton("➕ Add Plot Row")
        add_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        add_row_btn.setStyleSheet(btn_qss)
        add_row_btn.clicked.connect(self.on_add_row)

        del_row_btn = QPushButton("🗑️ Delete Selected Plot")
        del_row_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        del_row_btn.setStyleSheet(btn_qss)
        del_row_btn.clicked.connect(self.on_delete_row)

        save_btn = QPushButton("💾 Save Plot Treatments")
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
        save_btn.clicked.connect(self.on_save_treatments)

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
        records = self.store.get_plot_treatments(self.trial_code) if self.store else []
        if not records:
            records = [(i, 0, 0, 0, "None", "Standard") for i in range(1, 13)]

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
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Segoe UI", sans-serif;
                font-size: 12px;
                padding: 2px 4px;
            }
        """

        for row_idx, r in enumerate(records):
            plot_item = QTableWidgetItem(str(r[0]))
            plot_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            plot_item.setForeground(QColor("#000000"))
            plot_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Standard QSpinBox with sharp black text (#000000)
            f1_spin = QSpinBox()
            f1_spin.setRange(0, 10)
            f1_spin.setValue(int(r[1]))
            f1_spin.setStyleSheet(spin_qss)
            f1_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

            f2_spin = QSpinBox()
            f2_spin.setRange(0, 10)
            f2_spin.setValue(int(r[2]))
            f2_spin.setStyleSheet(spin_qss)
            f2_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

            f3_spin = QSpinBox()
            f3_spin.setRange(0, 10)
            f3_spin.setValue(int(r[3]))
            f3_spin.setStyleSheet(spin_qss)
            f3_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

            extra_edit = QLineEdit(str(r[4]))
            extra_edit.setStyleSheet(line_qss)

            sub_edit = QLineEdit(str(r[5]))
            sub_edit.setStyleSheet(line_qss)

            self.table.setItem(row_idx, 0, plot_item)
            self.table.setCellWidget(row_idx, 1, f1_spin)
            self.table.setCellWidget(row_idx, 2, f2_spin)
            self.table.setCellWidget(row_idx, 3, f3_spin)
            self.table.setCellWidget(row_idx, 4, extra_edit)
            self.table.setCellWidget(row_idx, 5, sub_edit)

    def on_auto_generate(self):
        num_plots = self.num_plots_spin.value()
        records = []
        for i in range(1, num_plots + 1):
            f1 = (i - 1) % 3
            f2 = ((i - 1) // 3) % 3
            f3 = ((i - 1) // 9) % 3
            records.append((i, f1, f2, f3, "None", "Standard"))

        self.populate_table(records)
        QMessageBox.information(self, "Plots Generated", f"Auto-generated {num_plots} plots with balanced factor levels!")

    def on_add_row(self):
        curr_rows = self.table.rowCount()
        next_plot = curr_rows + 1
        new_rec = (next_plot, 0, 0, 0, "None", "Standard")
        records = []

        for r in range(curr_rows):
            p_no = int(self.table.item(r, 0).text())
            f1 = self.table.cellWidget(r, 1).value()
            f2 = self.table.cellWidget(r, 2).value()
            f3 = self.table.cellWidget(r, 3).value()
            extra = self.table.cellWidget(r, 4).text()
            sub = self.table.cellWidget(r, 5).text()
            records.append((p_no, f1, f2, f3, extra, sub))

        records.append(new_rec)
        self.populate_table(records)

    def on_delete_row(self):
        curr_row = self.table.currentRow()
        if curr_row >= 0:
            self.table.removeRow(curr_row)
        else:
            QMessageBox.warning(self, "No Selection", "Please click a row to delete.")

    def on_save_treatments(self):
        records = []
        for r in range(self.table.rowCount()):
            try:
                p_no = int(self.table.item(r, 0).text())
                f1 = self.table.cellWidget(r, 1).value()
                f2 = self.table.cellWidget(r, 2).value()
                f3 = self.table.cellWidget(r, 3).value()
                extra = self.table.cellWidget(r, 4).text().strip()
                sub = self.table.cellWidget(r, 5).text().strip()
                records.append((p_no, f1, f2, f3, extra, sub))
            except Exception:
                pass

        if self.store:
            self.store.save_plot_treatments(self.trial_code, records)
            QMessageBox.information(self, "Saved", f"Saved {len(records)} plot treatment factor mapping(s) for Trial '{self.trial_code}'!")
            self.accept()
        else:
            self.accept()
