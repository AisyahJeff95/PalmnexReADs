from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox,
    QPushButton, QFrame, QTextEdit, QSpinBox, QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

class NewTrialInfoDialog(QDialog):
    """
    Exact replica of Original ReaDA 'New Trial Info' / 'Edit Trial Info' Window (Screenshot 12)
    - Dark Navy Header Banner 'Trial Main Information'
    - Trial Code, Estate, Planting Year, Planting Density inputs
    - Extra Plot Treatment & Sub Plot Treatment checkboxes
    - Treatment Factor 1..7 Labels & Total Count input
    - Treatment Factor Information scrollable text box
    - Save Data? Yes / No action panel
    - Properly overwrites records when editing instead of creating duplicates!
    """
    def __init__(self, parent=None, store=None, trial_data=None):
        super().__init__(parent)
        self.store = store
        self.trial_data = trial_data
        self.is_edit = trial_data is not None
        self.original_trial_code = trial_data[0] if (self.is_edit and trial_data) else None

        title_text = f"Editing Trial Information [{self.original_trial_code}]" if self.is_edit else "New Trial Main Information"
        self.setWindowTitle(title_text)
        self.setFixedSize(760, 580)
        self.setStyleSheet("background-color: #dcdcdc;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        # -----------------------------------------------------------------
        # 1. Dark Navy Header Banner
        # -----------------------------------------------------------------
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #000055; border: 1px solid #000033; border-radius: 3px;")
        header_frame.setFixedHeight(45)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_lbl = QLabel("Trial   Main   Information")
        header_lbl.setFont(QFont("Times New Roman", 18, QFont.Weight.Bold))
        header_lbl.setStyleSheet("color: #ffffff; letter-spacing: 2px; border: none; background: transparent;")
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header_lbl)

        main_layout.addWidget(header_frame)

        # -----------------------------------------------------------------
        # 2. Main Form Grid & Right Save Panel
        # -----------------------------------------------------------------
        body_layout = QHBoxLayout()
        body_layout.setSpacing(15)

        # LEFT FORM AREA
        form_container = QVBoxLayout()
        form_container.setSpacing(10)

        # Top Inputs: Trial Code, Estate, Planting Year, Planting Density
        top_inputs_box = QFrame()
        top_inputs_box.setStyleSheet("""
            QLineEdit, QSpinBox {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 3px;
                font-family: "Segoe UI", sans-serif;
                font-size: 12px;
                padding: 2px 4px;
            }
            QLabel {
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                color: #000000;
            }
        """)
        top_grid = QVBoxLayout(top_inputs_box)
        top_grid.setContentsMargins(10, 10, 10, 10)
        top_grid.setSpacing(8)

        # Row 1: Trial code
        r1 = QHBoxLayout()
        lbl_code = QLabel("Trial code  :")
        lbl_code.setFixedWidth(100)
        self.code_edit = QLineEdit()
        self.code_edit.setFixedWidth(120)
        r1.addWidget(lbl_code)
        r1.addWidget(self.code_edit)
        r1.addStretch()
        top_grid.addLayout(r1)

        # Row 2: Estate
        r2 = QHBoxLayout()
        lbl_estate = QLabel("Estate       :")
        lbl_estate.setFixedWidth(100)
        self.estate_edit = QLineEdit()
        self.estate_edit.setFixedWidth(240)
        r2.addWidget(lbl_estate)
        r2.addWidget(self.estate_edit)
        r2.addStretch()
        top_grid.addLayout(r2)

        # Row 3: Planting Year & Planting Density
        r3 = QHBoxLayout()
        lbl_yr = QLabel("Planting Year :")
        lbl_yr.setFixedWidth(100)
        self.year_edit = QSpinBox()
        self.year_edit.setRange(1950, 2030)
        self.year_edit.setValue(2022)
        self.year_edit.setFixedWidth(80)

        lbl_den = QLabel("Planting Density")
        self.density_edit = QSpinBox()
        self.density_edit.setRange(50, 300)
        self.density_edit.setValue(148)
        self.density_edit.setFixedWidth(80)

        r3.addWidget(lbl_yr)
        r3.addWidget(self.year_edit)
        r3.addSpacing(40)
        r3.addWidget(lbl_den)
        r3.addWidget(self.density_edit)
        r3.addStretch()
        top_grid.addLayout(r3)

        form_container.addWidget(top_inputs_box)

        # Checkbox Options Frame
        chk_box = QFrame()
        chk_box.setStyleSheet("""
            QFrame {
                background-color: #c8c8c8;
                border: 1px solid #a0a0a0;
                border-radius: 4px;
            }
            QCheckBox {
                font-family: "Times New Roman", serif;
                font-weight: bold;
                font-size: 13px;
                color: #000000;
            }
        """)
        chk_layout = QVBoxLayout(chk_box)
        chk_layout.setContentsMargins(15, 8, 15, 8)
        chk_layout.setSpacing(6)

        self.chk_extra = QCheckBox("Trial With Extra Plot Treatment")
        self.chk_subplot = QCheckBox("Trial With Sub Plot As Treatment Factor")

        chk_layout.addWidget(self.chk_extra)
        chk_layout.addWidget(self.chk_subplot)
        form_container.addWidget(chk_box)

        # Treatment Factor Section
        tf_box = QFrame()
        tf_box.setStyleSheet("background-color: #dcdcdc;")
        tf_layout = QVBoxLayout(tf_box)
        tf_layout.setContentsMargins(0, 0, 0, 0)
        tf_layout.setSpacing(6)

        tf_header = QLabel("Treatment Factor")
        tf_header.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        tf_header.setStyleSheet("background-color: #b0b0b0; color: #800000; padding: 4px 10px; border-radius: 3px;")

        tf_layout.addWidget(tf_header)

        # Grid of Factors (Left) + Factor Info Box (Right)
        tf_content = QHBoxLayout()
        tf_content.setSpacing(15)

        # Factor Labels 1..7 (Left)
        factors_layout = QVBoxLayout()
        factors_layout.setSpacing(4)

        lbl_lbl = QLabel("Label")
        lbl_lbl.setFont(QFont("Times New Roman", 10, QFont.Weight.Bold))
        lbl_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        factors_layout.addWidget(lbl_lbl)

        self.factor_edits = []
        for i in range(1, 8):
            row = QHBoxLayout()
            row.setSpacing(5)
            f_lbl = QLabel(f"Factor {i}")
            f_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            f_lbl.setStyleSheet("color: #000000;")
            
            f_edit = QLineEdit()
            f_edit.setFixedWidth(50)
            f_edit.setMaxLength(5)

            row.addWidget(f_lbl)
            row.addWidget(f_edit)
            factors_layout.addLayout(row)
            self.factor_edits.append(f_edit)

        # Set default values for N, P, K
        self.factor_edits[0].setText("N")
        self.factor_edits[1].setText("P")
        self.factor_edits[2].setText("K")

        # Total Count Box
        tot_box = QFrame()
        tot_box.setStyleSheet("background-color: #c0c0c0; border: 1px solid #999999; border-radius: 3px;")
        tot_layout = QHBoxLayout(tot_box)
        tot_layout.setContentsMargins(5, 3, 5, 3)
        tot_lbl = QLabel("Total No. Of\nTreatment Factor :")
        tot_lbl.setFont(QFont("Times New Roman", 9, QFont.Weight.Bold))
        self.tot_edit = QSpinBox()
        self.tot_edit.setRange(1, 7)
        self.tot_edit.setValue(3)
        self.tot_edit.setFixedWidth(45)

        tot_layout.addWidget(tot_lbl)
        tot_layout.addWidget(self.tot_edit)
        factors_layout.addWidget(tot_box)

        tf_content.addLayout(factors_layout)

        # Factor Info Right Text Area
        info_container = QVBoxLayout()
        info_container.setSpacing(0)

        info_header = QLabel("Treatment Factor Information")
        info_header.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        info_header.setStyleSheet("background-color: #666666; color: #ffffff; padding: 4px; border: 1px solid #444444; border-top-left-radius: 3px; border-top-right-radius: 3px;")
        info_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.info_text = QTextEdit()
        self.info_text.setStyleSheet("background-color: #ffffff; color: #000000; border: 1px solid #444444; font-family: 'Segoe UI', sans-serif;")
        self.info_text.setPlaceholderText("Enter detailed treatment factor description, fertilizer rates, and trial notes...")

        info_container.addWidget(info_header)
        info_container.addWidget(self.info_text)

        tf_content.addLayout(info_container, 1)
        tf_layout.addLayout(tf_content)
        form_container.addWidget(tf_box)

        body_layout.addLayout(form_container, 3)

        # -----------------------------------------------------------------
        # RIGHT ACTION PANEL (Save Data? Yes / No)
        # -----------------------------------------------------------------
        right_panel = QFrame()
        right_panel.setFixedWidth(150)
        right_panel.setStyleSheet("background-color: #c8c8c8; border: 1px solid #a0a0a0; border-radius: 4px;")

        rp_layout = QVBoxLayout(right_panel)
        rp_layout.setContentsMargins(15, 20, 15, 20)
        rp_layout.setSpacing(15)
        rp_layout.addStretch()

        save_lbl = QLabel("Save Data ?")
        save_lbl.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        save_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        save_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_save_yes = QPushButton("✔️  Yes")
        btn_save_yes.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        btn_save_yes.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        btn_save_yes.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000080;
                border: 1px solid #71717a;
                border-radius: 4px;
                padding: 6px;
                outline: none;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:hover {
                background-color: #e0f2fe;
                border-color: #0284c7;
            }
        """)
        btn_save_yes.clicked.connect(self.on_save_yes)

        btn_save_no = QPushButton("🚫  No")
        btn_save_no.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        btn_save_no.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        btn_save_no.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #800000;
                border: 1px solid #71717a;
                border-radius: 4px;
                padding: 6px;
                outline: none;
            }
            QPushButton:focus {
                outline: none;
            }
            QPushButton:hover {
                background-color: #fee2e2;
                border-color: #dc2626;
            }
        """)
        btn_save_no.clicked.connect(self.reject)

        rp_layout.addWidget(save_lbl)
        rp_layout.addWidget(btn_save_yes)
        rp_layout.addWidget(btn_save_no)
        rp_layout.addStretch()

        body_layout.addWidget(right_panel)
        main_layout.addLayout(body_layout)

        # Pre-fill if editing existing trial
        if self.is_edit and self.trial_data:
            self.code_edit.setText(str(self.trial_data[0]))
            self.estate_edit.setText(str(self.trial_data[1]))
            try:
                self.year_edit.setValue(int(self.trial_data[3]))
            except Exception:
                pass
            try:
                self.density_edit.setValue(int(self.trial_data[4]))
            except Exception:
                pass

    def on_save_yes(self):
        trial_code = self.code_edit.text().strip()
        estate = self.estate_edit.text().strip()
        pl_year = self.year_edit.value()
        pl_density = self.density_edit.value()
        tot_factor = f"F{self.tot_edit.value()}"
        progeny = "DxP AVROS"

        if not trial_code:
            QMessageBox.warning(self, "Input Required", "Please enter a valid Trial Code.")
            return

        if self.store:
            if self.is_edit and self.original_trial_code:
                # Overwrite existing record!
                self.store.update_trial(self.original_trial_code, trial_code, estate, "MPOB", pl_year, pl_density, tot_factor, progeny)
                QMessageBox.information(self, "Data Updated", f"Trial '{self.original_trial_code}' updated to '{trial_code}' successfully!")
            else:
                # Insert new trial!
                self.store.add_trial(trial_code, estate, "MPOB", pl_year, pl_density, tot_factor, progeny)
                QMessageBox.information(self, "Data Saved", f"Trial '{trial_code}' saved successfully to ACFSINFO.DBF!")
            self.accept()
        else:
            self.accept()
