import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QGroupBox, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from utils.dbf_parser import DBFParser

class ImportExportPage(QWidget):
    """Simple ReaDA DBF & CSV Import/Export Page matching SmartPalm theme"""
    def __init__(self, parent_window, store):
        super().__init__()
        self.parent_window = parent_window
        self.store = store

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Import Group
        import_gb = QGroupBox("Import Legacy ReaDA dBase (.DBF) / CSV File")
        imp_layout = QVBoxLayout(import_gb)
        imp_layout.setContentsMargins(15, 20, 15, 15)

        desc_lbl = QLabel(
            "Select legacy dBase files (e.g. DATAVEG.DBF, ACFSLEAF.DBF, ACFSINFO.DBF) "
            "to parse and import into the modern database."
        )
        desc_lbl.setWordWrap(True)
        imp_layout.addWidget(desc_lbl)

        btn_box = QHBoxLayout()
        browse_btn = QPushButton("Browse & Import File...")
        browse_btn.setFixedWidth(180)
        browse_btn.clicked.connect(self.on_browse_file)
        btn_box.addWidget(browse_btn)
        btn_box.addStretch()
        imp_layout.addLayout(btn_box)

        # Log Console
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setPlaceholderText("Import log messages will appear here...")
        imp_layout.addWidget(self.log_edit)

        layout.addWidget(import_gb)

        # Export Group
        export_gb = QGroupBox("Database Export & Reset")
        exp_layout = QHBoxLayout(export_gb)
        exp_layout.setContentsMargins(15, 20, 15, 15)

        exp_csv_btn = QPushButton("Export Tables to CSV")
        exp_csv_btn.clicked.connect(self.on_export_csv)

        reset_btn = QPushButton("Reset to Demo Defaults")
        reset_btn.clicked.connect(self.on_reset_database)

        exp_layout.addWidget(exp_csv_btn)
        exp_layout.addWidget(reset_btn)
        exp_layout.addStretch()
        layout.addWidget(export_gb)

    def on_browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Legacy .DBF or .CSV File", "", "Database Files (*.dbf *.DBF *.csv *.CSV)"
        )
        if file_path:
            try:
                parsed = DBFParser.parse_file(file_path)
                imported = self.store.import_parsed_dbf(parsed)
                msg = f"Successfully imported {imported} records from {os.path.basename(file_path)}!"
                self.log_edit.append(f"[SUCCESS] {msg}")
                QMessageBox.information(self, "Import Successful", msg)

                if hasattr(self.parent_window, 'refresh_all_pages'):
                    self.parent_window.refresh_all_pages()
            except Exception as e:
                err_msg = f"Error importing file: {str(e)}"
                self.log_edit.append(f"[ERROR] {err_msg}")
                QMessageBox.critical(self, "Import Error", err_msg)

    def on_export_csv(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            script_path = os.path.join(base_dir, "..", "export_data.py")
            if os.path.exists(script_path):
                import subprocess
                subprocess.run(["python3", script_path], check=True)
            QMessageBox.information(self, "Export Complete", "Data tables exported to workspace CSV files!")
            self.log_edit.append("[EXPORT] Exported tables to CSV.")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))

    def on_reset_database(self):
        reply = QMessageBox.question(self, "Reset Database", "Reset all tables to initial MPOB sample trial data?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.store.reset_to_default()
            self.log_edit.append("[RESET] Database restored to initial demo defaults.")
            QMessageBox.information(self, "Reset Complete", "Database restored to demo defaults.")
            if hasattr(self.parent_window, 'refresh_all_pages'):
                self.parent_window.refresh_all_pages()
