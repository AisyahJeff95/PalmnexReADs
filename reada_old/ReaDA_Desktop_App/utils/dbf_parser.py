import os
import struct
import csv

class DBFParser:
    @staticmethod
    def parse_file(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            return DBFParser.parse_csv(file_path)
        elif ext == '.dbf':
            return DBFParser.parse_dbf(file_path)
        else:
            raise ValueError("Unsupported file format. Please select a .DBF or .CSV file.")

    @staticmethod
    def parse_csv(file_path):
        table_name = os.path.splitext(os.path.basename(file_path))[0].upper()
        records = []
        with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
            reader = csv.DictReader(f)
            fields = [{'name': col, 'type': 'C'} for col in (reader.fieldnames or [])]
            for row in reader:
                clean_row = {}
                for k, v in row.items():
                    if k is None: continue
                    val = v.strip() if v else ''
                    try:
                        if '.' in val:
                            clean_row[k] = float(val)
                        else:
                            clean_row[k] = int(val)
                    except ValueError:
                        clean_row[k] = val
                records.append(clean_row)
        return {'table_name': table_name, 'fields': fields, 'records': records}

    @staticmethod
    def parse_dbf(file_path):
        table_name = os.path.splitext(os.path.basename(file_path))[0].upper()
        with open(file_path, 'rb') as f:
            data = f.read()

        if len(data) < 32:
            raise ValueError("Invalid DBF file header")

        version, year, month, day, num_records, header_len, record_len = struct.unpack('<BBBBIHH', data[:12])
        
        fields = []
        idx = 32
        while idx < header_len - 1 and idx + 32 <= len(data):
            field_name = data[idx:idx+11].rstrip(b'\x00').decode('latin1', errors='ignore').strip()
            field_type = chr(data[idx+11])
            field_len = data[idx+16]
            field_dec = data[idx+17]
            if field_name:
                fields.append({'name': field_name, 'type': field_type, 'len': field_len, 'dec': field_dec})
            idx += 32

        records = []
        record_data = data[header_len:]
        for r in range(num_records):
            r_start = r * record_len
            if r_start + record_len > len(record_data):
                break
            deleted = record_data[r_start]
            if deleted == 0x2A:  # Skip deleted record marker '*'
                continue
            rec_buf = record_data[r_start+1:r_start+record_len]
            row_dict = {}
            f_idx = 0
            for field in fields:
                fname = field['name']
                ftype = field['type']
                flen = field['len']
                fdec = field['dec']
                raw_val = rec_buf[f_idx:f_idx+flen].decode('latin1', errors='ignore').strip()
                if not raw_val:
                    row_dict[fname] = None
                elif ftype in ('N', 'F'):
                    try:
                        row_dict[fname] = float(raw_val) if fdec > 0 else int(raw_val)
                    except ValueError:
                        row_dict[fname] = raw_val
                else:
                    row_dict[fname] = raw_val
                f_idx += flen
            records.append(row_dict)

        return {'table_name': table_name, 'fields': fields, 'records': records}
