from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QWhatsThis, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from pages.new_trial_info_dialog import NewTrialInfoDialog
from pages.edit_trial_selection_dialog import EditTrialSelectionDialog
from pages.read_backup_dialog import ReadBackupDialog
from pages.save_csv_dialog import SaveCsvDialog
from pages.delete_trial_dialog import DeleteTrialDialog
from pages.print_trial_info_dialog import PrintTrialInfoDialog
from pages.edit_treatment_selection_dialog import EditTreatmentSelectionDialog
from pages.edit_palm_selection_dialog import EditPalmSelectionDialog

from pages.treatment_ops_dialogs import (
    ReadTreatmentBackupDialog, ImportNonReadaTreatmentDialog,
    SaveTreatmentCsvDialog, DeleteTreatmentDialog, PrintTreatmentPdfDialog
)
from pages.palm_ops_dialogs import (
    ReadPalmBackupDialog, ImportNonReadaPalmDialog,
    SavePalmCsvDialog, DeletePalmDialog, PrintPalmPdfDialog
)

class TrialMainInfoDialog(QDialog):
    """
    Exact replica of Original ReaDA 'TRIAL MAIN INFORMATION' Window (Screenshot 1)
    - Full 100% interactive integration across all left, top-right, and bottom-right procedures!
    - Integrated with Qt QWhatsThis Help Mechanism (https://doc.qt.io/qt-6/qwhatsthis.html)
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store
        self.setWindowTitle("Trial Main Information")
        self.setFixedSize(820, 560)
        self.setStyleSheet("background-color: #e8e8e8;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Header Banner (Olive Green)
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        header_frame.setFixedHeight(45)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 10, 0)

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
        whatsthis_btn.setToolTip("Click here then click any button to view detailed feature explanations (QWhatsThis).")
        whatsthis_btn.clicked.connect(lambda: QWhatsThis.enterWhatsThisMode())

        header_lbl = QLabel("TRIAL MAIN INFORMATION")
        header_lbl.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #ffffff; letter-spacing: 1px; border: none; background: transparent;")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(whatsthis_btn)
        header_layout.addStretch()
        header_layout.addWidget(header_lbl)
        header_layout.addStretch()
        header_layout.addSpacing(90)

        layout.addWidget(header_frame)

        # Main Grid Layout
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(15)

        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #800000;
                border: 1px solid #71717a;
                border-radius: 4px;
                font-family: "Times New Roman", "Segoe UI", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 12px;
                outline: none;
            }
            QPushButton:focus { outline: none; }
            QPushButton:hover { background-color: #fff8f8; border-color: #800000; }
            QPushButton:pressed { background-color: #e0e0e0; }
        """

        # LEFT PANEL (Trial Info)
        left_box = QFrame()
        left_box.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        left_layout = QVBoxLayout(left_box)
        left_layout.setContentsMargins(20, 25, 20, 25)
        left_layout.setSpacing(14)

        left_btns = [
            ("New Trial Info", self.on_new_trial, "<b>New Trial Info:</b> Create a new agronomy trial record with Trial Code, Estate Name, Manager, and Planting Year."),
            ("Edit Trial Info", self.on_edit_trial, "<b>Edit Trial Info:</b> Select and update existing trial information, planting dates, and estate metadata."),
            ("Read Info From BackUp", self.on_read_backup, "<b>Read Info From BackUp:</b> Restore trial main information from backup .DBF or .CSV files."),
            ("Save Info Into *.csv File", self.on_save_csv, "<b>Save Info Into *.csv File:</b> Export selected trial main info to Excel-compatible CSV files."),
            ("Delete Trial Info", self.on_delete_trial, "<b>Delete Trial Info:</b> Remove selected agronomy trial records from the SQLite database."),
            ("Print Trial Info", self.on_print_info, "<b>Print Trial Info:</b> Generate vector PDF reports for trial main information.")
        ]

        for text, slot, desc in left_btns:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(btn_qss)
            btn.setFixedHeight(36)
            btn.setWhatsThis(desc)
            btn.setToolTip(desc)
            btn.clicked.connect(slot)
            left_layout.addWidget(btn)

        grid_layout.addWidget(left_box, 1)

        # RIGHT PANELS (Treatments & Palm Numbering)
        right_container = QVBoxLayout()
        right_container.setSpacing(15)

        right_top_box = QFrame()
        right_top_box.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        rt_layout = QVBoxLayout(right_top_box)
        rt_layout.setContentsMargins(20, 15, 20, 15)
        rt_layout.setSpacing(8)

        rt_btns = [
            ("Entry / Editing Plot Treatment", self.on_edit_plot_treatment, "<b>Entry / Editing Plot Treatment:</b> Configure Factor 1 (N), Factor 2 (P), Factor 3 (K), Extra Plots, and Sub Plot factors."),
            ("Read Treatment Back Up File", self.on_read_treatment_backup, "<b>Read Treatment Back Up File:</b> Restore treatment factor mapping from backup .DBF or .CSV files."),
            ("Treatment From 'Non-ReaDA' CSV File", self.on_import_treatment_csv, "<b>Treatment From 'Non-ReaDA' CSV File:</b> Import external treatment CSV data into ReaDA."),
            ("Save Treatment Into *.csv File", self.on_save_treatment_csv, "<b>Save Treatment Into *.csv File:</b> Export plot treatment mappings into CSV format."),
            ("Delete Trial Plot Treatment", self.on_delete_treatment, "<b>Delete Trial Plot Treatment:</b> Delete treatment mappings for selected trial codes."),
            ("Print Trial Plot Treatment", self.on_print_treatment, "<b>Print Trial Plot Treatment:</b> Generate vector PDF report for plot treatments.")
        ]

        for text, slot, desc in rt_btns:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(btn_qss)
            btn.setFixedHeight(32)
            btn.setWhatsThis(desc)
            btn.setToolTip(desc)
            btn.clicked.connect(slot)
            rt_layout.addWidget(btn)

        right_bot_box = QFrame()
        right_bot_box.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        rb_layout = QVBoxLayout(right_bot_box)
        rb_layout.setContentsMargins(20, 15, 20, 15)
        rb_layout.setSpacing(8)

        rb_btns = [
            ("Entry/Edit On Palm Numbering", self.on_edit_palm_numbering, "<b>Entry/Edit On Palm Numbering:</b> Configure palm numbering layout, Palm Status (Record, Border, Missing), and Progeny Tags."),
            ("Read Palm Number Back Up File", self.on_read_palm_backup, "<b>Read Palm Number Back Up File:</b> Restore palm numbering layouts from backup .DBF or .CSV files."),
            ("Palm Number From 'Non-ReaDA' CSV File", self.on_import_palm_csv, "<b>Palm Number From 'Non-ReaDA' CSV File:</b> Import external palm layout CSV data into ReaDA."),
            ("Save Palm Number Into *.csv File", self.on_save_palm_csv, "<b>Save Palm Number Into *.csv File:</b> Export palm numbering layouts to CSV files."),
            ("Delete Plot Palm Numbering", self.on_delete_palm, "<b>Delete Plot Palm Numbering:</b> Delete palm numbering layouts for selected trial codes."),
            ("Print Plot Palm Number", self.on_print_palm, "<b>Print Plot Palm Number:</b> Generate vector PDF report for palm numbering layouts.")
        ]

        for text, slot, desc in rb_btns:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(btn_qss)
            btn.setFixedHeight(32)
            btn.setWhatsThis(desc)
            btn.setToolTip(desc)
            btn.clicked.connect(slot)
            rb_layout.addWidget(btn)

        right_container.addWidget(right_top_box)
        right_container.addWidget(right_bot_box)

        grid_layout.addLayout(right_container, 2)
        layout.addLayout(grid_layout)

        # Bottom Exit Button
        bot_bar = QHBoxLayout()
        bot_bar.addStretch()

        exit_btn = QPushButton("Exit Main Info Procedure")
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet(btn_qss)
        exit_btn.setFixedHeight(34)
        exit_btn.clicked.connect(self.accept)
        bot_bar.addWidget(exit_btn)

        layout.addLayout(bot_bar)

    def on_new_trial(self):
        dlg = NewTrialInfoDialog(self, self.store)
        dlg.exec()

    def on_edit_trial(self):
        dlg = EditTrialSelectionDialog(self, self.store)
        dlg.exec()

    def on_read_backup(self):
        dlg = ReadBackupDialog(self, self.store)
        dlg.exec()

    def on_save_csv(self):
        dlg = SaveCsvDialog(self, self.store)
        dlg.exec()

    def on_delete_trial(self):
        dlg = DeleteTrialDialog(self, self.store)
        dlg.exec()

    def on_print_info(self):
        dlg = PrintTrialInfoDialog(self, self.store)
        dlg.exec()

    # Plot Treatment Handlers
    def on_edit_plot_treatment(self):
        dlg = EditTreatmentSelectionDialog(self, self.store)
        dlg.exec()

    def on_read_treatment_backup(self):
        dlg = ReadTreatmentBackupDialog(self, self.store)
        dlg.exec()

    def on_import_treatment_csv(self):
        dlg = ImportNonReadaTreatmentDialog(self, self.store)
        dlg.exec()

    def on_save_treatment_csv(self):
        dlg = SaveTreatmentCsvDialog(self, self.store)
        dlg.exec()

    def on_delete_treatment(self):
        dlg = DeleteTreatmentDialog(self, self.store)
        dlg.exec()

    def on_print_treatment(self):
        dlg = PrintTreatmentPdfDialog(self, self.store)
        dlg.exec()

    # Palm Numbering Handlers
    def on_edit_palm_numbering(self):
        dlg = EditPalmSelectionDialog(self, self.store)
        dlg.exec()

    def on_read_palm_backup(self):
        dlg = ReadPalmBackupDialog(self, self.store)
        dlg.exec()

    def on_import_palm_csv(self):
        dlg = ImportNonReadaPalmDialog(self, self.store)
        dlg.exec()

    def on_save_palm_csv(self):
        dlg = SavePalmCsvDialog(self, self.store)
        dlg.exec()

    def on_delete_palm(self):
        dlg = DeletePalmDialog(self, self.store)
        dlg.exec()

    def on_print_palm(self):
        dlg = PrintPalmPdfDialog(self, self.store)
        dlg.exec()
