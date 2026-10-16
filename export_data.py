import os
import glob
import struct
import sqlite3
import csv

def parse_dbf(dbf_path):
    """
    Parses a dBase / FoxPro DBF file and returns field definitions and rows.
    """
    with open(dbf_path, 'rb') as f:
        data = f.read()
    
    if len(data) < 32:
        return [], []
        
    version, year, month, day, num_records, header_len, record_len = struct.unpack('<BBBBIHH', data[:12])
    
    fields = []
    idx = 32
    while idx < header_len - 1 and idx + 32 <= len(data):
        field_name = data[idx:idx+11].rstrip(b'\x00').decode('latin1').strip()
        field_type = chr(data[idx+11])
        field_len = data[idx+16]
        field_dec = data[idx+17]
        if field_name:
            fields.append((field_name, field_type, field_len, field_dec))
        idx += 32
    
    record_data = data[header_len:]
    rows = []
    for r in range(num_records):
        r_start = r * record_len
        if r_start + record_len > len(record_data):
            break
        deleted = record_data[r_start]
        if deleted == 0x2A:  # Skip deleted record marker '*'
            continue
        rec_buf = record_data[r_start+1:r_start+record_len]
        row_vals = []
        f_idx = 0
        for fname, ftype, flen, fdec in fields:
            raw_val = rec_buf[f_idx:f_idx+flen].decode('latin1', errors='ignore').strip()
            if not raw_val:
                row_vals.append(None)
            elif ftype in ('N', 'F'):
                try:
                    if fdec > 0:
                        row_vals.append(float(raw_val))
                    else:
                        row_vals.append(int(raw_val))
                except ValueError:
                    row_vals.append(raw_val)
            else:
                row_vals.append(raw_val)
            f_idx += flen
        rows.append(row_vals)
        
    return fields, rows

def export_to_csv(fields, rows, csv_path):
    headers = [f[0] for f in fields]
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"✅ Exported CSV: {csv_path} ({len(rows)} records)")

def export_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all .DBF files in current directory and Extracted subfolder
    dbf_paths = glob.glob(os.path.join(base_dir, '*.DBF')) + glob.glob(os.path.join(base_dir, '*.dbf')) + \
                glob.glob(os.path.join(base_dir, 'Extracted', '*.DBF')) + glob.glob(os.path.join(base_dir, 'Extracted', '*.dbf'))
                
    dbf_paths = list(set(dbf_paths))
    
    if not dbf_paths:
        print("No .DBF files found.")
        return

    sqlite_path = os.path.join(base_dir, 'ReaDA_Database.sqlite')
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    
    for dbf_path in dbf_paths:
        fname = os.path.splitext(os.path.basename(dbf_path))[0].upper()
        fields, rows = parse_dbf(dbf_path)
        if fields:
            csv_path = os.path.join(base_dir, f'{fname}.csv')
            export_to_csv(fields, rows, csv_path)
            
            # Export to SQLite
            cols_def = []
            for field_name, ftype, flen, fdec in fields:
                col_type = 'REAL' if (ftype in ('N', 'F') and fdec > 0) else ('INTEGER' if ftype in ('N', 'F') else 'TEXT')
                cols_def.append(f'"{field_name}" {col_type}')
                
            cur.execute(f'DROP TABLE IF EXISTS "{fname}"')
            cur.execute(f'CREATE TABLE "{fname}" ({", ".join(cols_def)})')
            placeholders = ', '.join(['?'] * len(fields))
            cur.executemany(f'INSERT INTO "{fname}" VALUES ({placeholders})', rows)
            print(f"🗄️ SQLite Table '{fname}' updated ({len(rows)} rows).")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    export_all()
