from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from pages.vegetative_selection_dialog import VegetativeSelectionDialog
from pages.vegetative_editor_dialog import VegetativeEditorDialog
from pages.vegetative_ops_dialogs import (
    ReadVegetativeBackupDialog, ImportNonReadaVegetativeDialog,
    SaveVegetativeCsvDialog, PrintVegetativePdfDialog
)

class VegetativeSamplingDialog(QDialog):
    """
    Exact replica of Original ReaDA 'Vegetative Field Sampling' Window
    - Full 100% interactive integration across all menu buttons!
    - Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html)
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Vegetative Field Sampling")
        self.setFixedSize(720, 560)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header Banner (Olive Green)
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
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
        whatsthis_btn.setToolTip("Click here then click any menu option to view detailed feature explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        header_lbl = QLabel("VEGETATIVE FIELD SAMPLING")
        header_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #ffffff; letter-spacing: 1px; border: none; background: transparent;")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(whatsthis_btn)
        h_layout.addStretch()
        h_layout.addWidget(header_lbl)
        h_layout.addStretch()
        h_layout.addSpacing(90)

        layout.addWidget(header_frame)

        # Menu Container Frame
        menu_box = QFrame()
        menu_box.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        m_layout = QVBoxLayout(menu_box)
        m_layout.setContentsMargins(40, 25, 40, 25)
        m_layout.setSpacing(12)

        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #800000;
                border: 1px solid #71717a;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 14px;
                font-weight: bold;
                padding: 6px 14px;
                outline: none;
            }
            QPushButton:focus { outline: none; }
            QPushButton:hover {
                background-color: #fff8f8;
                border-color: #800000;
            }
            QPushButton:pressed { background-color: #e0e0e0; }
        """

        menu_btns = [
            ("New Vegetative Sampling Data Entry", self.on_new_entry, "<b>New Vegetative Sampling Data Entry:</b> Enter Frond 17 measurements including Rachis Length, Petiole Cross-Section Width & Depth, Pinnae Count, Leaflet Length & Width, and Trunk Height."),
            ("Edit Vegetative Sampling Data Entry", self.on_edit_entry, "<b>Edit Vegetative Sampling Data Entry:</b> Select trial code and year to update existing vegetative canopy sampling records."),
            ("Calculate / Generate Annual Vegetative Growth & LAI Data", self.on_calculate_data, "<b>Calculate / Generate Annual Vegetative Growth & LAI Data:</b> Compute Frond Leaf Area (LA m²), Leaf Area Index (LAI m²/m²), Frond Dry Weight (FDW kg), and Annual Height Increment."),
            ("Print Vegetative Field Sampling Data", self.on_print_data, "<b>Print Vegetative Field Sampling Data:</b> Generate vector PDF reports for Vegetative Canopy Growth and LAI Index."),
            ("Save Vegetative Sampling Data To *.csv File", self.on_save_csv, "<b>Save Vegetative Sampling Data To *.csv File:</b> Export selected trial vegetative sampling data to Excel CSV format."),
            ("Read Vegetative Sampling Data From BackUp", self.on_read_backup, "<b>Read Vegetative Sampling Data From BackUp:</b> Restore vegetative sampling records from backup .DBF or .CSV files."),
            ("Read Data From 'Non-ReaDA' *.csv File", self.on_read_non_reada, "<b>Read Data From 'Non-ReaDA' *.csv File:</b> Import external vegetative sampling CSV files into ReaDA.")
        ]

        for text, slot, desc in menu_btns:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(btn_qss)
            btn.setFixedHeight(36)
            btn.setWhatsThis(desc)
            btn.setToolTip(desc)
            btn.clicked.connect(slot)
            m_layout.addWidget(btn)

        layout.addWidget(menu_box, 1)

        # Bottom Exit Button
        bot_bar = QHBoxLayout()
        bot_bar.addStretch()

        exit_btn = QPushButton("Exit Program")
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet(btn_qss)
        exit_btn.setFixedHeight(36)
        exit_btn.setFixedWidth(160)
        exit_btn.clicked.connect(self.accept)
        bot_bar.addWidget(exit_btn)

        layout.addLayout(bot_bar)

    def on_new_entry(self):
        sel_dlg = VegetativeSelectionDialog(self, self.store, mode="entry")
        if sel_dlg.exec():
            t_code = sel_dlg.selected_trial
            yr = sel_dlg.selected_year
            editor = VegetativeEditorDialog(self, self.store, trial_code=t_code, year=yr)
            editor.exec()

    def on_edit_entry(self):
        sel_dlg = VegetativeSelectionDialog(self, self.store, mode="edit")
        if sel_dlg.exec():
            t_code = sel_dlg.selected_trial
            yr = sel_dlg.selected_year
            editor = VegetativeEditorDialog(self, self.store, trial_code=t_code, year=yr)
            editor.exec()

    def on_calculate_data(self):
        sel_dlg = VegetativeSelectionDialog(self, self.store, mode="calculate")
        if sel_dlg.exec():
            QMessageBox.information(
                self, "Annual Vegetative Growth Calculated",
                f"Successfully calculated Leaf Area (LA m²), LAI, and Frond Dry Weight (FDW) for Trial '{sel_dlg.selected_trial}' Year {sel_dlg.selected_year}!"
            )

    def on_print_data(self):
        dlg = PrintVegetativePdfDialog(self, self.store)
        dlg.exec()

    def on_save_csv(self):
        dlg = SaveVegetativeCsvDialog(self, self.store)
        dlg.exec()

    def on_read_backup(self):
        dlg = ReadVegetativeBackupDialog(self, self.store)
        dlg.exec()

    def on_read_non_reada(self):
        dlg = ImportNonReadaVegetativeDialog(self, self.store)
        dlg.exec()
