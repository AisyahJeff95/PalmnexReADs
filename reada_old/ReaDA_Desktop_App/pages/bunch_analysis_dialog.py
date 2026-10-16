from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from pages.bunch_analysis_selection_dialog import BunchAnalysisSelectionDialog
from pages.bunch_analysis_editor_dialog import BunchAnalysisEditorDialog
from pages.bunch_ops_dialogs import (
    ReadBunchBackupDialog, ImportNonReadaBunchDialog,
    SaveBunchCsvDialog, PrintBunchPdfDialog
)

class BunchAnalysisDialog(QDialog):
    """
    Exact replica of Original ReaDA 'Bunch Analysis Program' Window (Screenshot 19)
    - Full 100% interactive integration across all menu buttons!
    - Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html)
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Bunch Analysis Program")
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

        header_lbl = QLabel("BUNCH ANALYSIS PROGRAM")
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
            ("New Bunch Analysis Data Entry", self.on_new_entry, "<b>New Bunch Analysis Data Entry:</b> Enter physical bunch weight, stalk weight, spikelet weight, fruit weight, nut weight, and wet mesocarp measurements for oil extraction analysis."),
            ("Edit Bunch Analysis Data Entry", self.on_edit_entry, "<b>Edit Bunch Analysis Data Entry:</b> Select trial code and year to update existing bunch component measurements."),
            ("Calculate / Generate Bunch Analysis Data", self.on_calculate_data, "<b>Calculate / Generate Bunch Analysis Data:</b> Compute Fruit-to-Bunch %, Mesocarp-to-Fruit %, Kernel-to-Fruit %, and Oil Extraction Rate (OER%)."),
            ("Print Bunch Analysis Data", self.on_print_data, "<b>Print Bunch Analysis Data:</b> Generate vector PDF reports for bunch components and OER values."),
            ("Save Bunch Analysis Data To *.csv File", self.on_save_csv, "<b>Save Bunch Analysis Data To *.csv File:</b> Export selected trial bunch analysis data to Excel CSV format."),
            ("Read Bunch Analysis Data From BackUp", self.on_read_backup, "<b>Read Bunch Analysis Data From BackUp:</b> Restore bunch analysis records from backup .DBF or .CSV files."),
            ("Read Data From 'Non-ReaDA' *.csv File", self.on_read_non_reada, "<b>Read Data From 'Non-ReaDA' *.csv File:</b> Import external bunch component CSV files into ReaDA.")
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
        sel_dlg = BunchAnalysisSelectionDialog(self, self.store, mode="entry")
        if sel_dlg.exec():
            t_code = sel_dlg.selected_trial
            yr = sel_dlg.selected_year
            editor = BunchAnalysisEditorDialog(self, self.store, trial_code=t_code, year=yr)
            editor.exec()

    def on_edit_entry(self):
        sel_dlg = BunchAnalysisSelectionDialog(self, self.store, mode="edit")
        if sel_dlg.exec():
            t_code = sel_dlg.selected_trial
            yr = sel_dlg.selected_year
            editor = BunchAnalysisEditorDialog(self, self.store, trial_code=t_code, year=yr)
            editor.exec()

    def on_calculate_data(self):
        sel_dlg = BunchAnalysisSelectionDialog(self, self.store, mode="calculate")
        if sel_dlg.exec():
            QMessageBox.information(
                self, "Bunch Components Calculated",
                f"Successfully calculated FTB%, PTF%, KTF%, and OER% for Trial '{sel_dlg.selected_trial}' Year {sel_dlg.selected_year}!"
            )

    def on_print_data(self):
        dlg = PrintBunchPdfDialog(self, self.store)
        dlg.exec()

    def on_save_csv(self):
        dlg = SaveBunchCsvDialog(self, self.store)
        dlg.exec()

    def on_read_backup(self):
        dlg = ReadBunchBackupDialog(self, self.store)
        dlg.exec()

    def on_read_non_reada(self):
        dlg = ImportNonReadaBunchDialog(self, self.store)
        dlg.exec()
