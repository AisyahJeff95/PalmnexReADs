import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QStyleFactory, QStackedWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from utils.data_store import DataStore
from pages.trial_main_info_dialog import TrialMainInfoDialog
from pages.new_trial_info_dialog import NewTrialInfoDialog
from pages.edit_trial_selection_dialog import EditTrialSelectionDialog
from pages.read_backup_dialog import ReadBackupDialog
from pages.save_csv_dialog import SaveCsvDialog
from pages.delete_trial_dialog import DeleteTrialDialog
from pages.print_trial_info_dialog import PrintTrialInfoDialog
from pages.agronomy_annual_data_dialog import AgronomyAnnualDataDialog
from pages.yield_recording_dialog import YieldRecordingDialog
from pages.vegetative_sampling_dialog import VegetativeSamplingDialog
from pages.bunch_analysis_dialog import BunchAnalysisDialog
from pages.trial_annual_data_window import TrialAnnualDataWindow


class ClickableCardBox(QFrame):
    """
    Compact Clickable Card Widget for '{ Main Information }' and '{ Annual Plot Data }'.
    Standardized Qt Quick Controls Styling with outline: none
    """
    clicked = Signal()

    def __init__(self, header_text, items):
        super().__init__()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame#card_box {
                background-color: #ffffff;
                border: 1px solid #71717a;
                border-radius: 4px;
                outline: none;
            }
            QFrame#card_box:hover {
                border: 2px solid #800000;
                background-color: #fafafa;
            }
        """)
        self.setObjectName("card_box")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 4)
        layout.setSpacing(1)

        header = QLabel(header_text)
        header.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
        header.setStyleSheet("background-color: #707838; color: #ffffff; padding: 5px; border-top-left-radius: 3px; border-top-right-radius: 3px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        for item in items:
            lbl = QLabel(item)
            lbl.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #000000; border: none; background: transparent; padding: 1px 0px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class TrialMainInfoWidget(QFrame):
    """
    Exact replica of Original ReaDA 'TRIAL MAIN INFORMATION' View (Screenshot 1 & 12 & 15 & 16 & 17 & 18)
    """
    def __init__(self, parent_window, store):
        super().__init__()
        self.parent_window = parent_window
        self.store = store
        self.setStyleSheet("QFrame { background-color: #e8e8e8; border: 1px solid #bcbcbc; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header Banner (Olive Green)
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #6b7430; border: 1px solid #4a5220; border-radius: 3px;")
        header_frame.setFixedHeight(45)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_lbl = QLabel("TRIAL MAIN INFORMATION")
        header_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #ffffff; letter-spacing: 1px; border: none;")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header_lbl)

        layout.addWidget(header_frame)

        # Standard Button QSS with outline: none
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
            QPushButton:focus {
                outline: none;
            }
            QPushButton:hover {
                background-color: #fff8f8;
                border-color: #800000;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """

        # Main Grid Layout
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(20)

        # LEFT PANEL (Trial Info)
        left_box = QFrame()
        left_box.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        left_layout = QVBoxLayout(left_box)
        left_layout.setContentsMargins(25, 30, 25, 30)
        left_layout.setSpacing(14)

        left_btns = [
            ("New Trial Info", parent_window.on_new_trial),
            ("Edit Trial Info", parent_window.on_edit_trial),
            ("Read Info From BackUp", parent_window.on_read_backup),
            ("Save Info Into *.csv File", parent_window.on_save_dbf),
            ("Delete Trial Info", parent_window.on_delete_trial),
            ("Print Trial Info", parent_window.on_print_info)
        ]

        for text, slot in left_btns:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(btn_qss)
            btn.setFixedHeight(36)
            btn.clicked.connect(slot)
            left_layout.addWidget(btn)

        grid_layout.addWidget(left_box, 1)

        # RIGHT PANELS (Treatments & Palm Numbering)
        right_container = QVBoxLayout()
        right_container.setSpacing(15)

        # Right Top Panel (Plot Treatment)
        right_top_box = QFrame()
        right_top_box.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        rt_layout = QVBoxLayout(right_top_box)
        rt_layout.setContentsMargins(25, 18, 25, 18)
        rt_layout.setSpacing(8)

        rt_btns = [
            "Entry / Editing Plot Treatment",
            "Read Treatment Back Up File",
            "Treatment From 'Non-ReaDA' CSV File",
            "Save Treatment Into *.csv File",
            "Delete Trial Plot Treatment",
            "Print Trial Plot Treatment"
        ]

        for text in rt_btns:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(btn_qss)
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda _, t=text: parent_window.on_feature_clicked(t))
            rt_layout.addWidget(btn)

        # Right Bottom Panel (Palm Numbering)
        right_bot_box = QFrame()
        right_bot_box.setStyleSheet("background-color: #e8e8e8; border: 1px solid #bcbcbc; border-radius: 4px;")
        rb_layout = QVBoxLayout(right_bot_box)
        rb_layout.setContentsMargins(25, 18, 25, 18)
        rb_layout.setSpacing(8)

        rb_btns = [
            "Entry/Edit On Palm Numbering",
            "Read Palm Number Back Up File",
            "Palm Number From 'Non-ReaDA' CSV File",
            "Save Palm Number Into *.csv File",
            "Delete Plot Palm Numbering",
            "Print Plot Palm Number"
        ]

        for text in rb_btns:
            btn = QPushButton(text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setStyleSheet(btn_qss)
            btn.setFixedHeight(32)
            btn.clicked.connect(lambda _, t=text: parent_window.on_feature_clicked(t))
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
        exit_btn.clicked.connect(parent_window.show_home_branding)
        bot_bar.addWidget(exit_btn)

        layout.addLayout(bot_bar)


class OriginalReaDAMainWindow(QMainWindow):
    """
    ReaDA Software V2.0 2026 by Palmnex
    Features No-Focus-Outline Styled Buttons across the application!
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReaDA Software V2.0 2026 by Palmnex")
        self.resize(1180, 750)
        self.setMinimumSize(900, 620)

        # Initialize SQLite Data Store
        self.store = DataStore()

        # Central Teal Background Container
        central = QWidget()
        central.setStyleSheet("background-color: #286b67;")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)

        # Qt Quick Controls Button QSS Theme with outline: none
        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 14px;
                font-weight: bold;
                padding: 6px 12px;
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
                border-color: #52525b;
            }
            QPushButton:disabled {
                background-color: #f4f4f5;
                color: #a1a1aa;
                border-color: #e4e4e7;
            }
        """

        # -----------------------------------------------------------------
        # LEFT PANEL (No Focus Outline Buttons)
        # -----------------------------------------------------------------
        left_panel = QFrame()
        left_panel.setFixedWidth(280)
        left_panel.setStyleSheet("background-color: #286b67; border: none;")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        # 1. Top Button: List Of Availabled Trial Data
        top_list_btn = QPushButton("List Of Availabled Trial Data")
        top_list_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        top_list_btn.setStyleSheet(btn_qss)
        top_list_btn.setFixedHeight(40)
        top_list_btn.clicked.connect(self.show_trial_annual_data)
        left_layout.addWidget(top_list_btn)

        # 2. { Main Information } Card Button
        main_info_box = ClickableCardBox(
            "{  Main Information  }",
            ["Trial Code", "Trial Treatments", "Trial Palm Number"]
        )
        main_info_box.clicked.connect(self.show_main_information_page)
        left_layout.addWidget(main_info_box)

        # 3. Bunch Analysis Program Button
        bunch_btn = QPushButton("Bunch Analysis Program")
        bunch_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        bunch_btn.setStyleSheet(btn_qss)
        bunch_btn.setFixedHeight(40)
        bunch_btn.clicked.connect(self.open_bunch_analysis)

        # 4. Yield Recording Program Button
        yield_btn = QPushButton("Yield Recording Program")
        yield_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        yield_btn.setStyleSheet(btn_qss)
        yield_btn.setFixedHeight(40)
        yield_btn.clicked.connect(self.open_yield_recording)

        # 5. Vegetative Field Sampling Button
        veg_btn = QPushButton("Vegetative Field Sampling")
        veg_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        veg_btn.setStyleSheet(btn_qss)
        veg_btn.setFixedHeight(40)
        veg_btn.clicked.connect(self.open_vegetative_sampling)

        left_layout.addWidget(bunch_btn)
        left_layout.addWidget(yield_btn)
        left_layout.addWidget(veg_btn)

        # 6. {Annual Plot Data} Card Button
        annual_box = ClickableCardBox(
            "{Annual Plot Data}",
            ["F.F.B. Yield", "Leaf Nutrients", "Vegetative Measurements", "Soil Nutrients"]
        )
        annual_box.clicked.connect(self.open_annual_plot_data)
        left_layout.addWidget(annual_box)

        # 7. Exit Program Button
        exit_btn = QPushButton("Exit Program")
        exit_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        exit_btn.setStyleSheet(btn_qss)
        exit_btn.setFixedHeight(40)
        exit_btn.clicked.connect(self.close)

        left_layout.addWidget(exit_btn)
        main_layout.addWidget(left_panel)

        # -----------------------------------------------------------------
        # RIGHT PANEL (QStackedWidget for Displaying Branding or Pages)
        # -----------------------------------------------------------------
        self.right_stack = QStackedWidget()

        # Page 0: Default Branding Display Area
        self.branding_page = QFrame()
        self.branding_page.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.12);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
            }
        """)
        b_layout = QVBoxLayout(self.branding_page)
        b_layout.setContentsMargins(40, 40, 40, 40)
        b_layout.setSpacing(15)

        title_lbl = QLabel("ReaDA")
        title_lbl.setFont(QFont("Times New Roman", 52, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #ffffff; letter-spacing: 2px; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_lbl = QLabel("Research Data Analysis System")
        subtitle_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        subtitle_lbl.setStyleSheet("color: #a7f3d0; border: none; background: transparent;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: rgba(255, 255, 255, 0.4); border: 1px solid rgba(255, 255, 255, 0.4);")
        divider.setFixedWidth(320)

        version_lbl = QLabel("ReaDA Software V2.0 2026 by Palmnex")
        version_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        version_lbl.setStyleSheet("color: #ffffff; border: none; background: transparent;")
        version_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        mpob_lbl = QLabel("MPOB Oil Palm Agronomic Research Data Engine")
        mpob_lbl.setFont(QFont("Segoe UI", 10))
        mpob_lbl.setStyleSheet("color: #cbd5e1; border: none; background: transparent;")
        mpob_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        b_layout.addStretch()
        b_layout.addWidget(title_lbl)
        b_layout.addWidget(subtitle_lbl)
        b_layout.addSpacing(10)
        b_layout.addWidget(divider, alignment=Qt.AlignmentFlag.AlignCenter)
        b_layout.addSpacing(10)
        b_layout.addWidget(version_lbl)
        b_layout.addWidget(mpob_lbl)
        b_layout.addStretch()

        # Page 1: TRIAL MAIN INFORMATION Page (Screenshot 1)
        self.main_info_page = TrialMainInfoWidget(self, self.store)

        # Page 2: Trial Annual Data Window (Screenshot 6)
        self.annual_data_page = TrialAnnualDataWindow(self, self.store)

        self.right_stack.addWidget(self.branding_page)
        self.right_stack.addWidget(self.main_info_page)
        self.right_stack.addWidget(self.annual_data_page)

        main_layout.addWidget(self.right_stack, 1)

    # Navigation Handlers
    def show_home_branding(self):
        self.right_stack.setCurrentIndex(0)

    def show_main_information_page(self):
        self.right_stack.setCurrentIndex(1)

    def show_trial_annual_data(self):
        self.right_stack.setCurrentIndex(2)

    def open_trial_main_info(self):
        self.show_main_information_page()

    def open_annual_plot_data(self):
        dlg = AgronomyAnnualDataDialog(self, self.store)
        dlg.exec()

    def open_yield_recording(self):
        dlg = YieldRecordingDialog(self, self.store)
        dlg.exec()

    def open_vegetative_sampling(self):
        dlg = VegetativeSamplingDialog(self, self.store)
        dlg.exec()

    def open_bunch_analysis(self):
        dlg = BunchAnalysisDialog(self, self.store)
        dlg.exec()

    # Callback actions inside Trial Main Information page
    def on_new_trial(self):
        dlg = NewTrialInfoDialog(self, self.store)
        if dlg.exec():
            self.main_info_page.update()
            if hasattr(self, 'annual_data_page'):
                self.annual_data_page.refresh_table()

    def on_edit_trial(self):
        dlg = EditTrialSelectionDialog(self, self.store)
        if dlg.exec():
            self.main_info_page.update()
            if hasattr(self, 'annual_data_page'):
                self.annual_data_page.refresh_table()

    def on_read_backup(self):
        dlg = ReadBackupDialog(self, self.store)
        if dlg.exec():
            self.main_info_page.update()
            if hasattr(self, 'annual_data_page'):
                self.annual_data_page.refresh_table()

    def on_save_dbf(self):
        dlg = SaveCsvDialog(self, self.store)
        dlg.exec()

    def on_delete_trial(self):
        dlg = DeleteTrialDialog(self, self.store)
        if dlg.exec():
            self.main_info_page.update()
            if hasattr(self, 'annual_data_page'):
                self.annual_data_page.refresh_table()

    def on_print_info(self):
        dlg = PrintTrialInfoDialog(self, self.store)
        dlg.exec()

    def on_feature_clicked(self, feature_name):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, feature_name, f"Executing: {feature_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if "Windows" in QStyleFactory.keys():
        app.setStyle(QStyleFactory.create("Windows"))
    elif "Fusion" in QStyleFactory.keys():
        app.setStyle(QStyleFactory.create("Fusion"))

    window = OriginalReaDAMainWindow()
    window.show()
    sys.exit(app.exec())
