from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QDialog, QFormLayout, QSpinBox, QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class AddTrialDialog(QDialog):
    """Simple Modal for creating new MPOB trial entry"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Research Trial")
        self.setFixedSize(360, 300)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.code_edit = QLineEdit("PR2024/1")
        self.estate_edit = QLineEdit("Banting Station")
        self.group_edit = QLineEdit("MPOB Central")
        self.year_edit = QSpinBox()
        self.year_edit.setRange(1970, 2030)
        self.year_edit.setValue(2022)

        self.density_edit = QSpinBox()
        self.density_edit.setRange(100, 200)
        self.density_edit.setValue(148)

        self.factor_edit = QLineEdit("F3 (N x P x K)")
        self.progeny_edit = QLineEdit("DxP AVROS")

        form.addRow("Trial Code:", self.code_edit)
        form.addRow("Estate / Station:", self.estate_edit)
        form.addRow("Group:", self.group_edit)
        form.addRow("Planting Year:", self.year_edit)
        form.addRow("Density (palms/ha):", self.density_edit)
        form.addRow("Treatments:", self.factor_edit)
        form.addRow("Progeny:", self.progeny_edit)

        layout.addLayout(form)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Save Trial")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        btn_box.addWidget(cancel_btn)
        btn_box.addWidget(save_btn)
        layout.addLayout(btn_box)

    def get_data(self):
        return (
            self.code_edit.text().strip(),
            self.estate_edit.text().strip(),
            self.group_edit.text().strip(),
            self.year_edit.value(),
            self.density_edit.value(),
            self.factor_edit.text().strip(),
            self.progeny_edit.text().strip()
        )


class TrialManagementPage(QWidget):
    """ReaDA Trial Management Page styled with standard Qt Table View template"""
    def __init__(self, parent_window, store):
        super().__init__()
        self.parent_window = parent_window
        self.store = store

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        group_box = QGroupBox("Research Trial Registry (ACFSINFO)")
        gb_layout = QVBoxLayout(group_box)
        gb_layout.setContentsMargins(15, 20, 15, 15)

        # Action Bar
        top_bar = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search trial code or estate...")
        self.search_edit.textChanged.connect(self.refresh_table)

        add_btn = QPushButton("Add New Trial")
        add_btn.setFixedWidth(130)
        add_btn.clicked.connect(self.on_add_trial)

        top_bar.addWidget(self.search_edit)
        top_bar.addWidget(add_btn)
        gb_layout.addLayout(top_bar)

        # Table Widget (Standard Qt QTableView Template)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Trial Code", "Estate / Station", "Group", "Planted Year",
            "Density", "Treatments", "Progeny", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                gridline-color: #c0c0c0;
                border: 1px solid #adadad;
                font-family: "Segoe UI", "Tahoma", sans-serif;
                font-size: 11px;
                selection-background-color: #0078d7;
                selection-color: #ffffff;
            }
            QTableWidget::item {
                color: #000000;
                background-color: #ffffff;
                padding: 4px;
            }
            QTableWidget::item:alternate {
                background-color: #f8fafc;
            }
            QHeaderView::section {
                background-color: #e1e1e1;
                color: #000000;
                font-family: "Segoe UI", "Tahoma", sans-serif;
                font-weight: bold;
                border: 1px solid #adadad;
                font-size: 11px;
                padding: 5px;
                text-align: center;
            }
        """)

        gb_layout.addWidget(self.table)
        layout.addWidget(group_box)

        self.refresh_table()

    def refresh_table(self):
        filter_text = self.search_edit.text().lower().strip()
        trials = self.store.get_trials()

        filtered = [
            t for t in trials
            if filter_text in t[0].lower() or filter_text in t[1].lower() or filter_text in t[2].lower()
        ]

        self.table.setRowCount(len(filtered))
        for row_idx, t in enumerate(filtered):
            for col_idx, val in enumerate(t):
                item = QTableWidgetItem(str(val))
                item.setForeground(QColor("#000000"))
                if col_idx == 0:
                    item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                self.table.setItem(row_idx, col_idx, item)

            del_btn = QPushButton("Delete")
            del_btn.setFixedHeight(24)
            del_btn.clicked.connect(lambda _, code=t[0]: self.on_delete_trial(code))
            self.table.setCellWidget(row_idx, 7, del_btn)

    def on_add_trial(self):
        dialog = AddTrialDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data[0]:
                QMessageBox.warning(self, "Invalid Input", "Trial code cannot be empty.")
                return
            self.store.add_trial(*data)
            self.refresh_table()
            if hasattr(self.parent_window, 'dashboard_page'):
                self.parent_window.dashboard_page.refresh_dashboard()

    def on_delete_trial(self, trial_code):
        reply = QMessageBox.question(self, "Delete Trial", f"Delete trial {trial_code}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.store.delete_record('trials', 'TRIAL_CODE', trial_code)
            self.refresh_table()
            if hasattr(self.parent_window, 'dashboard_page'):
                self.parent_window.dashboard_page.refresh_dashboard()
