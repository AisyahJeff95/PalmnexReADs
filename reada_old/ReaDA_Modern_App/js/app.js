/**
 * ReaDA Modern Web Application Launcher & Event Router
 */

import { DataStore } from './data_store.js';
import { DBFParser } from './dbf_parser.js';
import { ChartEngine } from './charts.js';
import { UIComponents } from './ui_components.js';

class ReaDAApp {
  constructor() {
    this.store = new DataStore();
    this.currentNav = 'dashboard';
    this.currentSubTab = 'leaf';
    this.init();
  }

  init() {
    this.bindEvents();
    this.render();
  }

  bindEvents() {
    // Navigation items
    document.querySelectorAll('.nav-item button').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const target = e.currentTarget.getAttribute('data-nav');
        this.switchNav(target);
      });
    });

    // Sub-tabs in Data Grid
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const targetTab = e.currentTarget.getAttribute('data-tab');
        this.switchSubTab(targetTab);
      });
    });

    // Theme toggle
    const themeBtn = document.getElementById('btn-theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
      });
    }

    // Modal controls
    const addTrialBtn = document.getElementById('btn-add-trial');
    if (addTrialBtn) {
      addTrialBtn.addEventListener('click', () => this.openModal('modal-add-trial'));
    }

    const addLeafBtn = document.getElementById('btn-add-leaf');
    if (addLeafBtn) {
      addLeafBtn.addEventListener('click', () => this.openModal('modal-add-leaf'));
    }

    const addYieldBtn = document.getElementById('btn-add-yield');
    if (addYieldBtn) {
      addYieldBtn.addEventListener('click', () => this.openModal('modal-add-yield'));
    }

    document.querySelectorAll('.modal-close').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const modal = e.currentTarget.closest('.modal-overlay');
        if (modal) modal.classList.remove('active');
      });
    });

    // Forms submission
    const formTrial = document.getElementById('form-add-trial');
    if (formTrial) {
      formTrial.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(formTrial);
        const trial = {
          TRIAL_CODE: formData.get('TRIAL_CODE'),
          ESTATE: formData.get('ESTATE'),
          GROUP: formData.get('GROUP') || 'MPOB',
          PL_YEAR: Number(formData.get('PL_YEAR')) || 2020,
          PL_DENSITY: Number(formData.get('PL_DENSITY')) || 148,
          TOT_FACTOR: formData.get('TOT_FACTOR') || 'F3',
          PROGENY: formData.get('PROGENY') || 'DxP'
        };
        this.store.addTrial(trial);
        this.closeModal('modal-add-trial');
        formTrial.reset();
        this.render();
      });
    }

    const formLeaf = document.getElementById('form-add-leaf');
    if (formLeaf) {
      formLeaf.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(formLeaf);
        const leafRec = {
          TRIAL_CODE: formData.get('TRIAL_CODE'),
          PALM_NO: Number(formData.get('PALM_NO')) || 1,
          TISSUE_N: parseFloat(formData.get('TISSUE_N')) || 0,
          TISSUE_P: parseFloat(formData.get('TISSUE_P')) || 0,
          TISSUE_K: parseFloat(formData.get('TISSUE_K')) || 0,
          TISSUE_CA: parseFloat(formData.get('TISSUE_CA')) || 0,
          TISSUE_MG: parseFloat(formData.get('TISSUE_MG')) || 0,
          TISSUE_B: parseFloat(formData.get('TISSUE_B')) || 0
        };
        this.store.addLeafRecord(leafRec);
        this.closeModal('modal-add-leaf');
        formLeaf.reset();
        this.render();
      });
    }

    const formYield = document.getElementById('form-add-yield');
    if (formYield) {
      formYield.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(formYield);
        const yieldRec = {
          TRIAL_CODE: formData.get('TRIAL_CODE'),
          YEAR_CODE: formData.get('YEAR_CODE') || '2023',
          PALM_NO: Number(formData.get('PALM_NO')) || 1,
          BUNCH_NO: Number(formData.get('BUNCH_NO')) || 0,
          BUNCH_WT: parseFloat(formData.get('BUNCH_WT')) || 0,
          FFB_YIELD: parseFloat(formData.get('FFB_YIELD')) || 0
        };
        this.store.addYieldRecord(yieldRec);
        this.closeModal('modal-add-yield');
        formYield.reset();
        this.render();
      });
    }

    // File Drag & Drop Import
    const dropzone = document.getElementById('file-dropzone');
    const fileInput = document.getElementById('file-input');

    if (dropzone && fileInput) {
      dropzone.addEventListener('click', () => fileInput.click());

      dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });

      dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

      dropzone.addEventListener('drop', async (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          await this.handleFileUpload(e.dataTransfer.files[0]);
        }
      });

      fileInput.addEventListener('change', async (e) => {
        if (e.target.files && e.target.files.length > 0) {
          await this.handleFileUpload(e.target.files[0]);
        }
      });
    }

    // Reset Store Button
    const resetBtn = document.getElementById('btn-reset-data');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (confirm("Reset database to initial MPOB sample trials?")) {
          this.store.resetToDefault();
          this.render();
        }
      });
    }
  }

  async handleFileUpload(file) {
    try {
      const parsed = await DBFParser.parseFile(file);
      const importedCount = this.store.importParsedDBF(parsed);
      alert(`Success! Imported ${importedCount} records from ${file.name} into ReaDA.`);
      this.render();
    } catch (err) {
      alert(`Error reading file: ${err.message}`);
    }
  }

  switchNav(navTarget) {
    this.currentNav = navTarget;
    document.querySelectorAll('.nav-item button').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-nav') === navTarget);
    });

    document.querySelectorAll('.view-panel').forEach(panel => {
      panel.style.display = panel.id === `panel-${navTarget}` ? 'block' : 'none';
    });

    this.render();
  }

  switchSubTab(tabTarget) {
    this.currentSubTab = tabTarget;
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-tab') === tabTarget);
    });

    document.querySelectorAll('.subtab-panel').forEach(panel => {
      panel.style.display = panel.id === `subpanel-${tabTarget}` ? 'block' : 'none';
    });

    this.render();
  }

  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
  }

  handleDelete = (category, id) => {
    this.store.deleteRecord(category, id);
    this.render();
  };

  render() {
    const state = this.store.state;

    // Update KPI Metric Cards
    const totalTrials = state.trials.length;
    const avgYield = (state.yieldData.reduce((acc, curr) => acc + (curr.FFB_YIELD || 0), 0) / (state.yieldData.length || 1)).toFixed(1);
    const deficientLeaves = state.leafData.filter(l => (l.TISSUE_N || 0) < 2.50 || (l.TISSUE_P || 0) < 0.15).length;

    const elTotalTrials = document.getElementById('kpi-total-trials');
    if (elTotalTrials) elTotalTrials.textContent = totalTrials;

    const elAvgYield = document.getElementById('kpi-avg-yield');
    if (elAvgYield) elAvgYield.textContent = `${avgYield} T/ha`;

    const elDeficient = document.getElementById('kpi-deficient');
    if (elDeficient) elDeficient.textContent = deficientLeaves;

    // Render Dashboard Charts
    if (this.currentNav === 'dashboard') {
      ChartEngine.renderYieldTrend('chart-yield-trend', state.yieldData);
      ChartEngine.renderNutrientRadar('chart-nutrient-radar', state.leafData[0]);
    }

    // Render Tables
    UIComponents.renderTrialsTable(state.trials, 'table-trials-container', this.handleDelete);
    UIComponents.renderLeafTable(state.leafData, 'table-leaf-container', this.handleDelete);
    UIComponents.renderYieldTable(state.yieldData, 'table-yield-container', this.handleDelete);
    UIComponents.renderVegTable(state.vegData, 'table-veg-container', this.handleDelete);
  }
}

// Bootstrap on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new ReaDAApp();
});
