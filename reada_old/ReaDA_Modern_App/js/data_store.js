/**
 * ReaDA Data Store & MPOB Agronomic Sample Datasets
 */

export const MPOB_OPTIMUM_THRESHOLDS = {
  LEAF: {
    N: { min: 2.50, max: 2.80, unit: '%' },
    P: { min: 0.15, max: 0.18, unit: '%' },
    K: { min: 1.00, max: 1.25, unit: '%' },
    Ca: { min: 0.50, max: 0.70, unit: '%' },
    Mg: { min: 0.25, max: 0.40, unit: '%' },
    B: { min: 15.0, max: 25.0, unit: 'ppm' },
    Cu: { min: 5.0, max: 8.0, unit: 'ppm' }
  }
};

export class DataStore {
  constructor() {
    this.storageKey = 'READA_MODERN_APP_DATA_V1';
    this.state = this.loadState();
  }

  getDefaultState() {
    return {
      trials: [
        {
          TRIAL_CODE: "PR1998/1",
          ESTATE: "Banting Station",
          GROUP: "MPOB Central",
          PL_YEAR: 1998,
          PL_DENSITY: 148,
          TOT_FACTOR: "F3",
          F1_LABEL: "N",
          F2_LABEL: "P",
          F3_LABEL: "K",
          SAMPLE_ID: "SMP-01",
          PLOT_NO: 12,
          PROGENY: "DxP AVROS"
        },
        {
          TRIAL_CODE: "PR2002/4",
          ESTATE: "Kluang Substation",
          GROUP: "MPOB Southern",
          PL_YEAR: 2002,
          PL_DENSITY: 136,
          TOT_FACTOR: "F2",
          F1_LABEL: "Mg",
          F2_LABEL: "B",
          F3_LABEL: "-",
          SAMPLE_ID: "SMP-04",
          PLOT_NO: 24,
          PROGENY: "DxP Yangambi"
        },
        {
          TRIAL_CODE: "PR2005/2",
          ESTATE: "Teluk Intan Station",
          GROUP: "MPOB Perak",
          PL_YEAR: 2005,
          PL_DENSITY: 148,
          TOT_FACTOR: "F4",
          F1_LABEL: "N",
          F2_LABEL: "P",
          F3_LABEL: "K",
          SAMPLE_ID: "SMP-08",
          PLOT_NO: 18,
          PROGENY: "DxP Calabar"
        }
      ],
      leafData: [
        { ID: 1, TRIAL_CODE: "PR1998/1", PALM_NO: 101, TISSUE_N: 2.65, TISSUE_P: 0.16, TISSUE_K: 1.18, TISSUE_CA: 0.58, TISSUE_MG: 0.32, TISSUE_B: 18.5, TISSUE_CU: 6.2 },
        { ID: 2, TRIAL_CODE: "PR1998/1", PALM_NO: 102, TISSUE_N: 2.38, TISSUE_P: 0.14, TISSUE_K: 0.92, TISSUE_CA: 0.48, TISSUE_MG: 0.22, TISSUE_B: 12.0, TISSUE_CU: 4.5 },
        { ID: 3, TRIAL_CODE: "PR2002/4", PALM_NO: 201, TISSUE_N: 2.72, TISSUE_P: 0.17, TISSUE_K: 1.22, TISSUE_CA: 0.62, TISSUE_MG: 0.38, TISSUE_B: 22.0, TISSUE_CU: 7.1 },
        { ID: 4, TRIAL_CODE: "PR2005/2", PALM_NO: 301, TISSUE_N: 2.55, TISSUE_P: 0.15, TISSUE_K: 1.05, TISSUE_CA: 0.54, TISSUE_MG: 0.28, TISSUE_B: 16.8, TISSUE_CU: 5.8 }
      ],
      soilData: [
        { ID: 1, TRIAL_CODE: "PR1998/1", PLOT_NO: 12, SOIL_PH: 4.85, SOIL_N: 0.14, SOIL_P: 18.5, SOIL_K: 0.42, SOIL_CA: 1.85, SOIL_MG: 0.68, O_CARBON: 1.65 },
        { ID: 2, TRIAL_CODE: "PR2002/4", PLOT_NO: 24, SOIL_PH: 4.40, SOIL_N: 0.11, SOIL_P: 12.2, SOIL_K: 0.28, SOIL_CA: 1.20, SOIL_MG: 0.45, O_CARBON: 1.25 },
        { ID: 3, TRIAL_CODE: "PR2005/2", PLOT_NO: 18, SOIL_PH: 5.10, SOIL_N: 0.16, SOIL_P: 22.0, SOIL_K: 0.55, SOIL_CA: 2.10, SOIL_MG: 0.82, O_CARBON: 1.95 }
      ],
      vegData: [
        { ID: 1, TRIAL_CODE: "PR1998/1", PALM_NO: 101, FROND_LENG: 5.85, FROND_AREA: 12.4, FROND_WT: 4.65, PALM_HT: 3.45, PALM_GIRTH: 2.15, N_O_FRONDS: 38 },
        { ID: 2, TRIAL_CODE: "PR1998/1", PALM_NO: 102, FROND_LENG: 5.40, FROND_AREA: 10.8, FROND_WT: 4.10, PALM_HT: 3.20, PALM_GIRTH: 1.95, N_O_FRONDS: 34 },
        { ID: 3, TRIAL_CODE: "PR2002/4", PALM_NO: 201, FROND_LENG: 6.10, FROND_AREA: 13.2, FROND_WT: 5.10, PALM_HT: 2.85, PALM_GIRTH: 2.30, N_O_FRONDS: 42 }
      ],
      yieldData: [
        { ID: 1, TRIAL_CODE: "PR1998/1", YEAR_CODE: "2023", PALM_NO: 101, BUNCH_NO: 18, BUNCH_WT: 285.5, FFB_YIELD: 24.8, BWT_TOTAL: 285.5, BNO_TOTAL: 18 },
        { ID: 2, TRIAL_CODE: "PR1998/1", YEAR_CODE: "2023", PALM_NO: 102, BUNCH_NO: 14, BUNCH_WT: 210.0, FFB_YIELD: 18.2, BWT_TOTAL: 210.0, BNO_TOTAL: 14 },
        { ID: 3, TRIAL_CODE: "PR2002/4", YEAR_CODE: "2023", PALM_NO: 201, BUNCH_NO: 22, BUNCH_WT: 360.0, FFB_YIELD: 31.4, BWT_TOTAL: 360.0, BNO_TOTAL: 22 },
        { ID: 4, TRIAL_CODE: "PR2005/2", YEAR_CODE: "2023", PALM_NO: 301, BUNCH_NO: 20, BUNCH_WT: 315.0, FFB_YIELD: 27.5, BWT_TOTAL: 315.0, BNO_TOTAL: 20 }
      ],
      bunchData: [
        { ID: 1, TRIAL_CODE: "PR1998/1", PALM_NO: 101, BWT: 16.5, FFWT: 10.8, WETMESO: 8.4, OTDM: 78.5, OTWM: 52.4, KWT: 1.25, STKWT: 0.95 },
        { ID: 2, TRIAL_CODE: "PR2002/4", PALM_NO: 201, BWT: 18.2, FFWT: 12.4, WETMESO: 9.8, OTDM: 81.2, OTWM: 54.8, KWT: 1.40, STKWT: 1.10 }
      ]
    };
  }

  loadState() {
    try {
      const saved = localStorage.getItem(this.storageKey);
      return saved ? JSON.parse(saved) : this.getDefaultState();
    } catch (e) {
      console.warn("Could not load from localStorage:", e);
      return this.getDefaultState();
    }
  }

  saveState() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.state));
    } catch (e) {
      console.error("Could not save to localStorage:", e);
    }
  }

  resetToDefault() {
    this.state = this.getDefaultState();
    this.saveState();
  }

  // CRUD Operations
  addTrial(trial) {
    this.state.trials.push(trial);
    this.saveState();
  }

  addLeafRecord(rec) {
    rec.ID = Date.now();
    this.state.leafData.push(rec);
    this.saveState();
  }

  addYieldRecord(rec) {
    rec.ID = Date.now();
    this.state.yieldData.push(rec);
    this.saveState();
  }

  addVegRecord(rec) {
    rec.ID = Date.now();
    this.state.vegData.push(rec);
    this.saveState();
  }

  deleteRecord(category, id) {
    if (this.state[category]) {
      this.state[category] = this.state[category].filter(item => item.ID !== id && item.TRIAL_CODE !== id);
      this.saveState();
    }
  }

  importParsedDBF(parsedResult) {
    const tableName = parsedResult.tableName;
    const records = parsedResult.records;
    
    if (!records || records.length === 0) return 0;
    
    if (tableName.includes('INFO') || tableName.includes('MAIN')) {
      this.state.trials.push(...records);
    } else if (tableName.includes('LEAF')) {
      this.state.leafData.push(...records);
    } else if (tableName.includes('SOIL')) {
      this.state.soilData.push(...records);
    } else if (tableName.includes('VEG') || tableName.includes('VM')) {
      this.state.vegData.push(...records);
    } else if (tableName.includes('YLD') || tableName.includes('RYLD')) {
      this.state.yieldData.push(...records);
    } else if (tableName.includes('BNCH') || tableName.includes('RBWT')) {
      this.state.bunchData.push(...records);
    } else {
      // Default to leaf or yield data
      this.state.leafData.push(...records);
    }
    
    this.saveState();
    return records.length;
  }
}
