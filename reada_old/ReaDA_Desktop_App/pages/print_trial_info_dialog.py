from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt, QSizeF
from PySide6.QtGui import QFont, QColor, QTextDocument, QPageSize, QPdfWriter
import os
import datetime

class PrintTrialInfoDialog(QDialog):
    """
    Print Trial Main Information to PDF Dialog (Screenshot 18 / PDF Fix)
    - Fixes tiny PDF output by setting 96 DPI resolution and full-page A4 scaling!
    - Renders clean, professional vector PDF report readable on any PDF viewer
    """
    def __init__(self, parent=None, store=None):
        super().__init__(parent)
        self.store = store

        self.setWindowTitle("Printing Trial Main Information to PDF")
        self.setFixedSize(560, 560)
        self.setStyleSheet("background-color: #dcdcdc;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(8)

        # Header Title & Subheader
        title_lbl = QLabel("Printing Trial Main Information")
        title_lbl.setFont(QFont("Times New Roman", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #000000; border: none; background: transparent;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_lbl = QLabel("Select Trials To Be Printed To PDF Report")
        subtitle_lbl.setFont(QFont("Times New Roman", 14, QFont.Weight.Bold))
        subtitle_lbl.setStyleSheet("color: #800000; border: none; background: transparent;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_lbl)
        layout.addWidget(subtitle_lbl)

        # Select All Control Bar
        select_all_bar = QHBoxLayout()
        self.chk_select_all = QCheckBox("Select All Trials")
        self.chk_select_all.setFont(QFont("Times New Roman", 12, QFont.Weight.Bold))
        self.chk_select_all.setStyleSheet("color: #000000; padding: 2px;")
        self.chk_select_all.stateChanged.connect(self.on_toggle_select_all)

        select_all_bar.addWidget(self.chk_select_all)
        select_all_bar.addStretch()
        layout.addLayout(select_all_bar)

        # Table View: AGRONOMY TRIAL CODE with Checkbox column
        table_container = QFrame()
        table_container.setStyleSheet("background-color: #ffffff; border: 1px solid #71717a; border-radius: 4px;")
        tc_layout = QVBoxLayout(table_container)
        tc_layout.setContentsMargins(0, 0, 0, 0)
        tc_layout.setSpacing(0)

        banner_lbl = QLabel("AGRONOMY TRIAL CODE LIST")
        banner_lbl.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
        banner_lbl.setStyleSheet("background-color: #f0f0f0; color: #000000; border-bottom: 1px solid #71717a; padding: 4px;")
        banner_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tc_layout.addWidget(banner_lbl)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Select", "Trial Code", "Estate"])
        self.table.setColumnWidth(0, 70)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
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
                background-color: #f5f5f5;
                color: #000000;
                font-family: "Times New Roman", serif;
                font-weight: bold;
                border: 1px solid #c0c0c0;
                font-size: 12px;
                padding: 4px;
            }
        """)

        tc_layout.addWidget(self.table)
        layout.addWidget(table_container, 1)

        # Prompt & Action Buttons
        prompt_lbl = QLabel(">> Select Trials to Generate PDF Report <<")
        prompt_lbl.setFont(QFont("Times New Roman", 13, QFont.Weight.Bold))
        prompt_lbl.setStyleSheet("color: #ca8a04; border: none; background: transparent;")
        prompt_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(prompt_lbl)

        btn_qss = """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #71717a;
                border-radius: 4px;
                font-family: "Times New Roman", serif;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 18px;
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

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)

        print_btn = QPushButton("🖨️   Generate PDF Report")
        print_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        print_btn.setStyleSheet(btn_qss)
        print_btn.setFixedHeight(34)
        print_btn.clicked.connect(self.on_generate_pdf)

        cancel_btn = QPushButton("❌   Cancel - Exit")
        cancel_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cancel_btn.setStyleSheet(btn_qss)
        cancel_btn.setFixedHeight(34)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(print_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_layout.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(btn_layout)

        self.refresh_table()

    def refresh_table(self):
        trials = self.store.get_trials() if self.store else []
        self.table.setRowCount(len(trials))

        for row_idx, t in enumerate(trials):
            chk_item = QTableWidgetItem()
            chk_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            chk_item.setCheckState(Qt.CheckState.Checked if row_idx == 0 else Qt.CheckState.Unchecked)

            code_item = QTableWidgetItem(str(t[0]))
            code_item.setFont(QFont("Times New Roman", 11, QFont.Weight.Bold))
            code_item.setForeground(QColor("#000000"))

            estate_item = QTableWidgetItem(str(t[1]))
            estate_item.setFont(QFont("Times New Roman", 11))
            estate_item.setForeground(QColor("#000000"))

            self.table.setItem(row_idx, 0, chk_item)
            self.table.setItem(row_idx, 1, code_item)
            self.table.setItem(row_idx, 2, estate_item)

    def on_toggle_select_all(self, state):
        is_checked = (state == Qt.CheckState.Checked.value or state == Qt.CheckState.Checked)
        target_state = Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked
        for r in range(self.table.rowCount()):
            item = self.table.item(r, 0)
            if item:
                item.setCheckState(target_state)

    def on_generate_pdf(self):
        trials = self.store.get_trials() if self.store else []
        selected_trials = []

        for r in range(self.table.rowCount()):
            chk_item = self.table.item(r, 0)
            if chk_item and chk_item.checkState() == Qt.CheckState.Checked:
                if r < len(trials):
                    selected_trials.append(trials[r])

        if not selected_trials:
            QMessageBox.warning(self, "No Selection", "Please check at least one trial to generate PDF report.")
            return

        default_path = os.path.expanduser(f"~/Desktop/ReaDA_Trial_Main_Info_Report.pdf")

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report", default_path,
            "PDF Files (*.pdf);;All Files (*)"
        )

        if save_path:
            try:
                now_str = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
                rows_html = ""
                for t in selected_trials:
                    rows_html += f"""
                    <tr>
                        <td><b>{t[0]}</b></td>
                        <td>{t[1]}</td>
                        <td>{t[2]}</td>
                        <td>{t[3]}</td>
                        <td>{t[4]}</td>
                        <td>{t[5]}</td>
                        <td>{t[6]}</td>
                    </tr>
                    """

                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                    body {{
                        font-family: 'Times New Roman', serif;
                        margin: 20px;
                        color: #000000;
                    }}
                    .header {{
                        text-align: center;
                        border-bottom: 2px solid #6b7430;
                        padding-bottom: 8px;
                        margin-bottom: 15px;
                    }}
                    .title {{
                        font-size: 20pt;
                        font-weight: bold;
                        color: #000055;
                        margin: 0;
                    }}
                    .subtitle {{
                        font-size: 14pt;
                        font-weight: bold;
                        color: #800000;
                        margin-top: 4px;
                    }}
                    .info-bar {{
                        margin-bottom: 12px;
                        font-size: 10pt;
                        color: #444444;
                        text-align: right;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    }}
                    th {{
                        background-color: #6b7430;
                        color: #ffffff;
                        padding: 8px;
                        font-size: 11pt;
                        font-weight: bold;
                        border: 1px solid #4a5220;
                        text-align: center;
                    }}
                    td {{
                        border: 1px solid #bcbcbc;
                        padding: 7px;
                        font-size: 10pt;
                        text-align: center;
                        color: #000000;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f8fafc;
                    }}
                    .footer {{
                        margin-top: 35px;
                        text-align: center;
                        font-size: 9pt;
                        color: #666666;
                        border-top: 1px solid #cccccc;
                        padding-top: 8px;
                    }}
                </style>
                </head>
                <body>
                    <div class="header">
                        <div class="title">MPOB OIL PALM RESEARCH DATA SYSTEM</div>
                        <div class="subtitle">TRIAL MAIN INFORMATION REPORT</div>
                    </div>
                    <div class="info-bar">
                        <b>Date Generated:</b> {now_str} &nbsp;|&nbsp; <b>Total Selected Trials:</b> {len(selected_trials)}
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Trial Code</th>
                                <th>Estate / Station</th>
                                <th>Group</th>
                                <th>Planting Year</th>
                                <th>Density (palms/ha)</th>
                                <th>Treatments</th>
                                <th>Progeny</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                    <div class="footer">
                        ReaDA Software V2.0 2026 by Palmnex &bull; MPOB Agronomic Research Data Engine
                    </div>
                </body>
                </html>
                """

                # QPdfWriter setup with 96 DPI resolution for full A4 page fit!
                pdf_writer = QPdfWriter(save_path)
                pdf_writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
                pdf_writer.setResolution(96)  # Standard 96 DPI matches HTML pixel & point sizes!

                doc = QTextDocument()
                doc.setPageSize(QSizeF(pdf_writer.width(), pdf_writer.height()))
                doc.setHtml(html_content)
                doc.print_(pdf_writer)

                QMessageBox.information(
                    self, "PDF Report Generated",
                    f"Successfully generated PDF report for {len(selected_trials)} trial(s)!\n\nFile Location:\n{save_path}"
                )
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "PDF Generation Failed", f"Could not create PDF report:\n{str(e)}")
