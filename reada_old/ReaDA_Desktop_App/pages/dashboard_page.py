from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QFrame, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class DashboardPage(QWidget):
    """
    ReaDA Dashboard Page matching the exact simple Qt theme of SmartPalm-demo:
    - Light grey canvas background (#f0f0f0)
    - Classic white group box containers (#ffffff, border: 1px solid #bcbcbc)
    - Simple native KPI display boxes
    """
    def __init__(self, parent_window, store):
        super().__init__()
        self.parent_window = parent_window
        self.store = store

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Header Title
        header_lbl = QLabel("ReaDA - Research Data Analysis System")
        header_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #000000;")
        layout.addWidget(header_lbl)

        # KPI Summary Boxes (Matching create_windows_nutrient_box style)
        kpi_group = QGroupBox("System Overview Summary")
        kpi_layout = QHBoxLayout(kpi_group)
        kpi_layout.setSpacing(15)
        kpi_layout.setContentsMargins(15, 20, 15, 15)

        self.box1, self.lbl_val1 = self.create_info_box("Registered Trials", "0")
        self.box2, self.lbl_val2 = self.create_info_box("Average FFB Yield", "0.0 T/ha")
        self.box3, self.lbl_val3 = self.create_info_box("Tissue Deficiencies", "0")

        kpi_layout.addWidget(self.box1)
        kpi_layout.addWidget(self.box2)
        kpi_layout.addWidget(self.box3)
        layout.addWidget(kpi_group)

        # Trial Summary Table Box
        summary_group = QGroupBox("Active Trial Summary")
        sg_layout = QVBoxLayout(summary_group)
        sg_layout.setContentsMargins(15, 20, 15, 15)

        self.summary_lbl = QLabel()
        self.summary_lbl.setFont(QFont("Segoe UI", 10))
        self.summary_lbl.setWordWrap(True)
        sg_layout.addWidget(self.summary_lbl)

        layout.addWidget(summary_group)
        layout.addStretch()

        self.refresh_dashboard()

    def create_info_box(self, title_text, initial_value):
        """Helper matching SmartPalm classic native Windows style info boxes"""
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #bcbcbc;
                border-radius: 2px;
            }
        """)
        box.setFixedHeight(60)
        layout = QVBoxLayout(box)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(2)

        lbl_title = QLabel(title_text)
        lbl_title.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #444444;")

        lbl_val = QLabel(initial_value)
        lbl_val.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl_val.setStyleSheet("color: #000000;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        return box, lbl_val

    def refresh_dashboard(self):
        trials = self.store.get_trials()
        yields = self.store.get_yield_data()
        leaves = self.store.get_leaf_data()

        self.lbl_val1.setText(str(len(trials)))

        if yields:
            avg_y = sum([y[6] for y in yields]) / len(yields)
            self.lbl_val2.setText(f"{avg_y:.1f} T/ha")
        else:
            self.lbl_val2.setText("0.0 T/ha")

        def_count = sum([1 for l in leaves if l[3] < 2.50 or l[4] < 0.15])
        self.lbl_val3.setText(str(def_count))

        summary_text = "<b>Current Loaded Trials:</b><br>"
        for t in trials:
            summary_text += f"• <b>{t[0]}</b> - {t[1]} ({t[2]}) | Density: {t[4]} palms/ha | Progeny: {t[6]}<br>"

        self.summary_lbl.setText(summary_text)
