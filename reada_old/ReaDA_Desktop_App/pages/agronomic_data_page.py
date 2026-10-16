from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QSpinBox,
    QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class AddLeafDialog(QDialog):
    """Simple Modal for adding leaf sample reading"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Leaf Reading")
        self.setFixedSize(340, 300)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.code_edit = QLineEdit("PR1998/1")
        self.palm_edit = QSpinBox()
        self.palm_edit.setRange(1, 9999)
        self.palm_edit.setValue(105)

        self.n_edit = QDoubleSpinBox()
        self.n_edit.setRange(0, 5)
        self.n_edit.setValue(2.65)

        self.p_edit = QDoubleSpinBox()
        self.p_edit.setRange(0, 2)
        self.p_edit.setValue(0.16)

        self.k_edit = QDoubleSpinBox()
        self.k_edit.setRange(0, 5)
        self.k_edit.setValue(1.18)

        self.ca_edit = QDoubleSpinBox()
        self.ca_edit.setRange(0, 5)
        self.ca_edit.setValue(0.58)

        self.mg_edit = QDoubleSpinBox()
        self.mg_edit.setRange(0, 5)
        self.mg_edit.setValue(0.32)

        self.b_edit = QDoubleSpinBox()
        self.b_edit.setRange(0, 100)
        self.b_edit.setValue(18.5)

        form.addRow("Trial Code:", self.code_edit)
        form.addRow("Palm No:", self.palm_edit)
        form.addRow("Nitrogen N (%):", self.n_edit)
        form.addRow("Phosphorus P (%):", self.p_edit)
        form.addRow("Potassium K (%):", self.k_edit)
        form.addRow("Calcium Ca (%):", self.ca_edit)
        form.addRow("Magnesium Mg (%):", self.mg_edit)
        form.addRow("Boron B (ppm):", self.b_edit)

        layout.addLayout(form)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Save Reading")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        btn_box.addWidget(cancel_btn)
        btn_box.addWidget(save_btn)
        layout.addLayout(btn_box)

    def get_data(self):
        return (
            self.code_edit.text().strip(),
            self.palm_edit.value(),
            self.n_edit.value(),
            self.p_edit.value(),
            self.k_edit.value(),
            self.ca_edit.value(),
            self.mg_edit.value(),
            self.b_edit.value()
        )


class AddYieldDialog(QDialog):
    """Simple Modal for adding FFB Yield record"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Yield Entry")
        self.setFixedSize(340, 260)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.code_edit = QLineEdit("PR1998/1")
        self.year_edit = QLineEdit("2023")
        self.palm_edit = QSpinBox()
        self.palm_edit.setRange(1, 9999)
        self.palm_edit.setValue(101)

        self.bunch_no_edit = QSpinBox()
        self.bunch_no_edit.setRange(0, 100)
        self.bunch_no_edit.setValue(18)

        self.bunch_wt_edit = QDoubleSpinBox()
        self.bunch_wt_edit.setRange(0, 1000)
        self.bunch_wt_edit.setValue(285.0)

        self.yield_edit = QDoubleSpinBox()
        self.yield_edit.setRange(0, 100)
        self.yield_edit.setValue(25.5)

        form.addRow("Trial Code:", self.code_edit)
        form.addRow("Year:", self.year_edit)
        form.addRow("Palm No:", self.palm_edit)
        form.addRow("Bunch Count:", self.bunch_no_edit)
        form.addRow("Bunch Weight (kg):", self.bunch_wt_edit)
        form.addRow("FFB Yield (T/ha):", self.yield_edit)

        layout.addLayout(form)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Save Yield")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        btn_box.addWidget(cancel_btn)
        btn_box.addWidget(save_btn)
        layout.addLayout(btn_box)

    def get_data(self):
        return (
            self.code_edit.text().strip(),
            self.year_edit.text().strip(),
            self.palm_edit.value(),
            self.bunch_no_edit.value(),
            self.bunch_wt_edit.value(),
            self.yield_edit.value()
        )


class AgronomicDataPage(QWidget):
    """Simple ReaDA Agronomic Data Grid Page"""
    def __init__(self, parent_window, store):
        super().__init__()
        self.parent_window = parent_window
        self.store = store

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        group_box = QGroupBox("Field Readings & Laboratory Data")
        gb_layout = QVBoxLayout(group_box)
        gb_layout.setContentsMargins(15, 20, 15, 15)

        # Action Buttons
        btn_bar = QHBoxLayout()
        add_leaf_btn = QPushButton("Add Leaf Reading")
        add_leaf_btn.clicked.connect(self.on_add_leaf)

        add_yield_btn = QPushButton("Add FFB Yield Entry")
        add_yield_btn.clicked.connect(self.on_add_yield)

        btn_bar.addStretch()
        btn_bar.addWidget(add_leaf_btn)
        btn_bar.addWidget(add_yield_btn)
        gb_layout.addLayout(btn_bar)

        # Tabs
        self.tabs = QTabWidget()

        # Tab 1: Leaf
        self.leaf_table = QTableWidget()
        self.leaf_table.setColumnCount(9)
        self.leaf_table.setHorizontalHeaderLabels([
            "Trial Code", "Palm No", "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)",
            "Calcium (Ca)", "Magnesium (Mg)", "Boron (B)", "Actions"
        ])
        self.leaf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.leaf_table, "Leaf Tissue Analysis")

        # Tab 2: Yield
        self.yield_table = QTableWidget()
        self.yield_table.setColumnCount(7)
        self.yield_table.setHorizontalHeaderLabels([
            "Trial Code", "Year", "Palm No", "Bunch Count",
            "Weight (kg)", "FFB Yield (T/ha)", "Actions"
        ])
        self.yield_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.yield_table, "FFB Yield Recording")

        # Tab 3: Veg
        self.veg_table = QTableWidget()
        self.veg_table.setColumnCount(8)
        self.veg_table.setHorizontalHeaderLabels([
            "Trial Code", "Palm No", "Frond Length (m)", "Frond Area (m²)",
            "Palm Height (m)", "Girth (m)", "No. Fronds", "Actions"
        ])
        self.veg_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabs.addTab(self.veg_table, "Vegetative Measurements")

        gb_layout.addWidget(self.tabs)
        layout.addWidget(group_box)

        self.refresh_all_tables()

    def refresh_all_tables(self):
        self.refresh_leaf_table()
        self.refresh_yield_table()
        self.refresh_veg_table()

    def refresh_leaf_table(self):
        leaf_rows = self.store.get_leaf_data()
        self.leaf_table.setRowCount(len(leaf_rows))
        for r_idx, row in enumerate(leaf_rows):
            self.leaf_table.setItem(r_idx, 0, QTableWidgetItem(str(row[1])))
            self.leaf_table.setItem(r_idx, 1, QTableWidgetItem(f"#{row[2]}"))

            n_item = QTableWidgetItem(f"{row[3]:.2f}%")
            if row[3] < 2.50:
                n_item.setBackground(QColor("#fee2e2"))
            self.leaf_table.setItem(r_idx, 2, n_item)

            p_item = QTableWidgetItem(f"{row[4]:.2f}%")
            if row[4] < 0.15:
                p_item.setBackground(QColor("#fee2e2"))
            self.leaf_table.setItem(r_idx, 3, p_item)

            self.leaf_table.setItem(r_idx, 4, QTableWidgetItem(f"{row[5]:.2f}%"))
            self.leaf_table.setItem(r_idx, 5, QTableWidgetItem(f"{row[6]:.2f}%"))
            self.leaf_table.setItem(r_idx, 6, QTableWidgetItem(f"{row[7]:.2f}%"))
            self.leaf_table.setItem(r_idx, 7, QTableWidgetItem(f"{row[8]:.1f} ppm"))

            del_btn = QPushButton("Delete")
            del_btn.setFixedHeight(24)
            del_btn.clicked.connect(lambda _, rec_id=row[0]: self.on_delete_record('leaf_data', rec_id))
            self.leaf_table.setCellWidget(r_idx, 8, del_btn)

    def refresh_yield_table(self):
        yield_rows = self.store.get_yield_data()
        self.yield_table.setRowCount(len(yield_rows))
        for r_idx, row in enumerate(yield_rows):
            self.yield_table.setItem(r_idx, 0, QTableWidgetItem(str(row[1])))
            self.yield_table.setItem(r_idx, 1, QTableWidgetItem(str(row[2])))
            self.yield_table.setItem(r_idx, 2, QTableWidgetItem(f"#{row[3]}"))
            self.yield_table.setItem(r_idx, 3, QTableWidgetItem(f"{row[4]} bunches"))
            self.yield_table.setItem(r_idx, 4, QTableWidgetItem(f"{row[5]:.1f} kg"))

            y_item = QTableWidgetItem(f"{row[6]:.1f} T/ha")
            y_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            self.yield_table.setItem(r_idx, 5, y_item)

            del_btn = QPushButton("Delete")
            del_btn.setFixedHeight(24)
            del_btn.clicked.connect(lambda _, rec_id=row[0]: self.on_delete_record('yield_data', rec_id))
            self.yield_table.setCellWidget(r_idx, 6, del_btn)

    def refresh_veg_table(self):
        veg_rows = self.store.get_veg_data()
        self.veg_table.setRowCount(len(veg_rows))
        for r_idx, row in enumerate(veg_rows):
            self.veg_table.setItem(r_idx, 0, QTableWidgetItem(str(row[1])))
            self.veg_table.setItem(r_idx, 1, QTableWidgetItem(f"#{row[2]}"))
            self.veg_table.setItem(r_idx, 2, QTableWidgetItem(f"{row[3]:.2f} m"))
            self.veg_table.setItem(r_idx, 3, QTableWidgetItem(f"{row[4]:.1f} m²"))
            self.veg_table.setItem(r_idx, 4, QTableWidgetItem(f"{row[5]:.2f} m"))
            self.veg_table.setItem(r_idx, 5, QTableWidgetItem(f"{row[6]:.2f} m"))
            self.veg_table.setItem(r_idx, 6, QTableWidgetItem(f"{row[7]}"))

            del_btn = QPushButton("Delete")
            del_btn.setFixedHeight(24)
            del_btn.clicked.connect(lambda _, rec_id=row[0]: self.on_delete_record('veg_data', rec_id))
            self.veg_table.setCellWidget(r_idx, 7, del_btn)

    def on_add_leaf(self):
        dialog = AddLeafDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.store.add_leaf_record(*dialog.get_data())
            self.refresh_all_tables()
            if hasattr(self.parent_window, 'dashboard_page'):
                self.parent_window.dashboard_page.refresh_dashboard()

    def on_add_yield(self):
        dialog = AddYieldDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.store.add_yield_record(*dialog.get_data())
            self.refresh_all_tables()
            if hasattr(self.parent_window, 'dashboard_page'):
                self.parent_window.dashboard_page.refresh_dashboard()

    def on_delete_record(self, table_name, rec_id):
        reply = QMessageBox.question(self, "Delete Record", "Delete selected record?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.store.delete_record(table_name, 'ID', rec_id)
            self.refresh_all_tables()
            if hasattr(self.parent_window, 'dashboard_page'):
                self.parent_window.dashboard_page.refresh_dashboard()
