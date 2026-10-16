/**
 * ReaDA Client-Side DBF & CSV File Parser Engine
 * Parses legacy dBase / FoxPro DBF files directly in the browser.
 */

export class DBFParser {
  static async parseFile(file) {
    const filename = file.name;
    const ext = filename.split('.').pop().toLowerCase();
    
    if (ext === 'csv') {
      return await this.parseCSV(file);
    } else if (ext === 'dbf') {
      return await this.parseDBF(file);
    } else {
      throw new Error('Unsupported file format. Please upload a .DBF or .CSV file.');
    }
  }

  static async parseCSV(file) {
    const text = await file.text();
    const lines = text.split(/\r\n|\n/).filter(line => line.trim().length > 0);
    if (lines.length === 0) return { fields: [], records: [] };
    
    const headers = lines[0].split(',').map(h => h.replace(/^["']|["']$/g, '').strip?.() || h.trim());
    const records = [];
    
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(v => v.replace(/^["']|["']$/g, '').trim());
      const rec = {};
      headers.forEach((h, idx) => {
        const val = values[idx];
        rec[h] = !isNaN(val) && val !== '' ? Number(val) : val;
      });
      records.push(rec);
    }
    
    return {
      tableName: file.name.replace(/\.[^/.]+$/, "").toUpperCase(),
      fields: headers.map(h => ({ name: h, type: 'C' })),
      records
    };
  }

  static async parseDBF(file) {
    const buffer = await file.arrayBuffer();
    const view = new DataView(buffer);
    
    if (buffer.byteLength < 32) {
      throw new Error('Invalid DBF file header');
    }
    
    const version = view.getUint8(0);
    const year = 1900 + view.getUint8(1);
    const month = view.getUint8(2);
    const day = view.getUint8(3);
    const numRecords = view.getUint32(4, true);
    const headerLen = view.getUint16(8, true);
    const recordLen = view.getUint16(10, true);
    
    const fields = [];
    let offset = 32;
    const decoder = new TextDecoder('latin1');
    
    while (offset < headerLen - 1 && offset + 32 <= buffer.byteLength) {
      const fieldBytes = new Uint8Array(buffer, offset, 11);
      let fieldName = decoder.decode(fieldBytes).replace(/\0/g, '').trim();
      
      if (!fieldName) break;
      
      const fieldType = String.fromCharCode(view.getUint8(offset + 11));
      const fieldLen = view.getUint8(offset + 16);
      const fieldDec = view.getUint8(offset + 17);
      
      fields.append ? fields.append({ name: fieldName, type: fieldType, len: fieldLen, dec: fieldDec }) :
                      fields.push({ name: fieldName, type: fieldType, len: fieldLen, dec: fieldDec });
      offset += 32;
    }
    
    const records = [];
    let recOffset = headerLen;
    
    for (let r = 0; r < numRecords; r++) {
      if (recOffset + recordLen > buffer.byteLength) break;
      
      const deletedMarker = view.getUint8(recOffset);
      if (deletedMarker === 0x2A) { // '*' means deleted record
        recOffset += recordLen;
        continue;
      }
      
      const record = {};
      let fieldOffset = recOffset + 1;
      
      for (const field of fields) {
        const valBytes = new Uint8Array(buffer, fieldOffset, field.len);
        let rawVal = decoder.decode(valBytes).trim();
        
        if (rawVal === '') {
          record[field.name] = null;
        } else if (field.type === 'N' || field.type === 'F') {
          record[field.name] = field.dec > 0 ? parseFloat(rawVal) : parseInt(rawVal, 10);
        } else {
          record[field.name] = rawVal;
        }
        
        fieldOffset += field.len;
      }
      
      records.push(record);
      recOffset += recordLen;
    }
    
    return {
      tableName: file.name.replace(/\.[^/.]+$/, "").toUpperCase(),
      fields,
      records
    };
  }
}
