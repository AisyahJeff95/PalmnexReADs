/**
 * ReaDA UI Component Renderers & Modal Managers
 */

import { MPOB_OPTIMUM_THRESHOLDS } from './data_store.js';

export class UIComponents {
  static getNutrientStatus(nutrientName, val) {
    if (val === null || val === undefined || isNaN(val)) return { text: 'N/A', class: '' };
    const rule = MPOB_OPTIMUM_THRESHOLDS.LEAF[nutrientName];
    if (!rule) return { text: 'Normal', class: 'badge-optimum' };
    
    if (val < rule.min) {
      return { text: 'Deficient', class: 'badge-deficient' };
    } else if (val > rule.max) {
      return { text: 'Excess', class: 'badge-excess' };
    } else {
      return { text: 'Optimum', class: 'badge-optimum' };
    }
  }

  static renderTrialsTable(trials, containerId, onDelete) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!trials || trials.length === 0) {
      container.innerHTML = `<div style="padding:2rem;text-align:center;color:var(--text-muted);">No trials found. Click "Add Trial" or import a .DBF file.</div>`;
      return;
    }

    let rowsHtml = trials.map(t => `
      <tr>
        <td><strong>${t.TRIAL_CODE}</strong></td>
        <td>${t.ESTATE}</td>
        <td>${t.GROUP || 'MPOB'}</td>
        <td>${t.PL_YEAR || '-'}</td>
        <td>${t.PL_DENSITY || 148} palms/ha</td>
        <td><span class="badge badge-optimum">${t.TOT_FACTOR || 'F3'}</span></td>
        <td>${t.PROGENY || 'DxP'}</td>
        <td class="actions">
          <button class="btn-table-action delete" data-id="${t.TRIAL_CODE}" title="Delete Trial">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </td>
      </tr>
    `).join('');

    container.innerHTML = `
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Trial Code</th>
              <th>Estate / Station</th>
              <th>Group</th>
              <th>Planted Year</th>
              <th>Density</th>
              <th>Treatments</th>
              <th>Progeny</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;

    // Attach delete handlers
    container.querySelectorAll('.btn-table-action.delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        if (confirm(`Delete trial ${id}?`)) {
          onDelete('trials', id);
        }
      });
    });
  }

  static renderLeafTable(leafData, containerId, onDelete) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!leafData || leafData.length === 0) {
      container.innerHTML = `<div style="padding:2rem;text-align:center;color:var(--text-muted);">No leaf nutrient analysis data.</div>`;
      return;
    }

    let rowsHtml = leafData.map(l => {
      const statusN = this.getNutrientStatus('N', l.TISSUE_N);
      const statusP = this.getNutrientStatus('P', l.TISSUE_P);
      const statusK = this.getNutrientStatus('K', l.TISSUE_K);

      return `
        <tr>
          <td><strong>${l.TRIAL_CODE}</strong></td>
          <td>Palm #${l.PALM_NO || 1}</td>
          <td>${l.TISSUE_N || '-'}% <span class="badge ${statusN.class}">${statusN.text}</span></td>
          <td>${l.TISSUE_P || '-'}% <span class="badge ${statusP.class}">${statusP.text}</span></td>
          <td>${l.TISSUE_K || '-'}% <span class="badge ${statusK.class}">${statusK.text}</span></td>
          <td>${l.TISSUE_CA || '-'}%</td>
          <td>${l.TISSUE_MG || '-'}%</td>
          <td>${l.TISSUE_B || '-'} ppm</td>
          <td class="actions">
            <button class="btn-table-action delete" data-id="${l.ID}" title="Delete Record">
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </td>
        </tr>
      `;
    }).join('');

    container.innerHTML = `
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Trial Code</th>
              <th>Palm No.</th>
              <th>Nitrogen (N)</th>
              <th>Phosphorus (P)</th>
              <th>Potassium (K)</th>
              <th>Calcium (Ca)</th>
              <th>Magnesium (Mg)</th>
              <th>Boron (B)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;

    container.querySelectorAll('.btn-table-action.delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = Number(e.currentTarget.getAttribute('data-id'));
        if (confirm("Delete leaf record?")) onDelete('leafData', id);
      });
    });
  }

  static renderYieldTable(yieldData, containerId, onDelete) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!yieldData || yieldData.length === 0) {
      container.innerHTML = `<div style="padding:2rem;text-align:center;color:var(--text-muted);">No FFB yield recordings available.</div>`;
      return;
    }

    let rowsHtml = yieldData.map(y => `
      <tr>
        <td><strong>${y.TRIAL_CODE}</strong></td>
        <td>${y.YEAR_CODE || '2023'}</td>
        <td>Palm #${y.PALM_NO || 1}</td>
        <td><strong>${y.BUNCH_NO || 0}</strong> bunches</td>
        <td>${y.BUNCH_WT || 0} kg</td>
        <td><strong style="color:var(--accent-primary);">${y.FFB_YIELD || 0} T/ha</strong></td>
        <td class="actions">
          <button class="btn-table-action delete" data-id="${y.ID}" title="Delete Record">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </td>
      </tr>
    `).join('');

    container.innerHTML = `
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Trial Code</th>
              <th>Year</th>
              <th>Palm No</th>
              <th>Bunch Count</th>
              <th>Total Weight (kg)</th>
              <th>FFB Yield (Tonnes/Ha)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;

    container.querySelectorAll('.btn-table-action.delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = Number(e.currentTarget.getAttribute('data-id'));
        if (confirm("Delete yield record?")) onDelete('yieldData', id);
      });
    });
  }

  static renderVegTable(vegData, containerId, onDelete) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!vegData || vegData.length === 0) {
      container.innerHTML = `<div style="padding:2rem;text-align:center;color:var(--text-muted);">No vegetative measurements found.</div>`;
      return;
    }

    let rowsHtml = vegData.map(v => `
      <tr>
        <td><strong>${v.TRIAL_CODE}</strong></td>
        <td>Palm #${v.PALM_NO || 1}</td>
        <td>${v.FROND_LENG || '-'} m</td>
        <td>${v.FROND_AREA || '-'} m²</td>
        <td>${v.PALM_HT || '-'} m</td>
        <td>${v.PALM_GIRTH || '-'} m</td>
        <td>${v.N_O_FRONDS || '-'}</td>
        <td class="actions">
          <button class="btn-table-action delete" data-id="${v.ID}" title="Delete Record">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </td>
      </tr>
    `).join('');

    container.innerHTML = `
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Trial Code</th>
              <th>Palm No</th>
              <th>Frond Length</th>
              <th>Frond Area</th>
              <th>Palm Height</th>
              <th>Girth</th>
              <th>No. Fronds</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;

    container.querySelectorAll('.btn-table-action.delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = Number(e.currentTarget.getAttribute('data-id'));
        if (confirm("Delete vegetative record?")) onDelete('vegData', id);
      });
    });
  }
}
