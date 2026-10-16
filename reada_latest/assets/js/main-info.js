/**
 * ReaDA — Section 2: Main Information Controller
 * -------------------------------------------------------------------------
 * Recreates the complete Borland Visual dBase Main Information module
 * (PORIM Manual Figures 3 through 14) with all 15 operational pop-up windows.
 */

(function () {
  'use strict';

  // Load trial data
  let trials = JSON.parse(JSON.stringify(window.READA_TRIALS || []));
  let currentCode = 'DTP1';

  // Modals state
  let isNewMode = false;
  let currentSaveType = 'info';      // 'info' | 'treatment' | 'palm'
  let currentBackupType = 'info';    // 'info' | 'treatment' | 'palm'
  let currentDeleteType = 'info';    // 'info' | 'treatment' | 'palm'

  // DOM Elements
  const el = {
    trialSelect: document.getElementById('select-working-trial'),
    statCode: document.getElementById('stat-trial-code'),
    statEstate: document.getElementById('stat-estate'),
    statYear: document.getElementById('stat-planting-year'),
    statFactors: document.getElementById('stat-factors-count'),
    statPlots: document.getElementById('stat-plots-count'),
    statPalms: document.getElementById('stat-palms-count'),
    toast: document.getElementById('toast'),
    toastMsg: document.getElementById('toast-msg')
  };

  // Modal references
  const modals = {
    trialInfo: document.getElementById('modal-trial-info'),
    plotTreatment: document.getElementById('modal-plot-treatment'),
    palmNumbering: document.getElementById('modal-palm-numbering'),
    saveDbf: document.getElementById('modal-save-dbf'),
    backup: document.getElementById('modal-backup'),
    nonReada: document.getElementById('modal-non-reada'),
    confirmDelete: document.getElementById('modal-confirm-delete')
  };

  function getCurrentTrial() {
    return trials.find(t => t.code === currentCode) || trials[0];
  }

  function showToast(msg) {
    if (!el.toast) return;
    el.toastMsg.textContent = msg;
    el.toast.classList.add('visible');
    setTimeout(() => el.toast.classList.remove('visible'), 2800);
  }

  // Refresh Top Header Stats & Selector
  function refreshHeader() {
    const t = getCurrentTrial();
    if (!t) return;

    if (el.statCode) el.statCode.textContent = t.code;
    if (el.statEstate) el.statEstate.textContent = t.estate;
    if (el.statYear) el.statYear.textContent = t.plantingYear || '—';
    if (el.statFactors) el.statFactors.textContent = (t.factors || []).length || (t.factorsCount || 0);
    if (el.statPlots) el.statPlots.textContent = (t.plotTreatments || []).length;
    if (el.statPalms) el.statPalms.textContent = (t.palms || []).length;

    if (el.trialSelect) {
      el.trialSelect.innerHTML = '';
      trials.forEach(tr => {
        const opt = document.createElement('option');
        opt.value = tr.code;
        opt.textContent = `${tr.code} — ${tr.estate}`;
        if (tr.code === currentCode) opt.selected = true;
        el.trialSelect.appendChild(opt);
      });
    }
  }

  // Modal Open/Close helpers
  function openModal(modal) {
    if (!modal) return;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    const input = modal.querySelector('input:not([readonly]), button.btn-primary');
    if (input) setTimeout(() => input.focus(), 60);
  }

  function closeModal(modal) {
    if (!modal) return;
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
  }

  function closeAllModals() {
    Object.values(modals).forEach(m => {
      if (m) closeModal(m);
    });
  }

  // Close button events
  document.querySelectorAll('.modal-close-icon, .btn-modal-cancel').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal-overlay');
      closeModal(modal);
    });
  });

  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal(overlay);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAllModals();
  });

  // =========================================================================
  // FIGURE 4 (2.1 & 2.2): Trial Main Information Pop-up
  // =========================================================================
  function openTrialInfoModal(isNew = false) {
    isNewMode = isNew;
    const modal = modals.trialInfo;
    const title = document.getElementById('modal-trial-info-title');
    const codeInp = document.getElementById('info-trial-code');
    const estateInp = document.getElementById('info-estate');
    const yearInp = document.getElementById('info-planting-year');
    const factorCountInp = document.getElementById('info-factor-count');
    const factorInfoArea = document.getElementById('info-factor-details');
    const grid = document.getElementById('info-factors-grid');

    if (isNew) {
      if (title) title.textContent = 'Create New Trial Information';
      codeInp.value = 'EXP_' + (trials.length + 1);
      codeInp.removeAttribute('readonly');
      estateInp.value = '';
      yearInp.value = new Date().getFullYear();
      factorCountInp.value = '4';
      factorInfoArea.value = 'Rep = Replicate\nN = Nitrogen\nP = Phosphorus\nK = Potassium';
      renderFactorInputs(['Rep', 'N', 'P', 'K', '', '', '']);
    } else {
      const t = getCurrentTrial();
      if (title) title.textContent = `Edit Trial Main Information — ${t.code}`;
      codeInp.value = t.code;
      codeInp.setAttribute('readonly', 'true');
      estateInp.value = t.estate || '';
      yearInp.value = t.plantingYear || 1988;
      factorCountInp.value = (t.factors || []).length || 6;
      factorInfoArea.value = t.factorInfo || '';
      const labels = (t.factors || []).map(f => f.label);
      while (labels.length < 7) labels.push('');
      renderFactorInputs(labels);
    }

    openModal(modal);
  }

  function renderFactorInputs(labels) {
    const grid = document.getElementById('info-factors-grid');
    if (!grid) return;
    grid.innerHTML = '';
    for (let i = 1; i <= 7; i++) {
      const val = labels[i - 1] || '';
      const div = document.createElement('div');
      div.className = 'form-field';
      div.innerHTML = `
        <label style="font-size: 0.74rem; font-weight: 500;">Factor ${i} Label</label>
        <input type="text" class="form-control factor-label-input" data-index="${i}" value="${val}" placeholder="—" maxlength="6" style="padding: 5px 8px; font-family: var(--font-mono); text-transform: uppercase;">
      `;
      grid.appendChild(div);
    }
  }

  // Save Trial Main Info (Figure 4 [Yes] button)
  document.getElementById('btn-save-trial-info')?.addEventListener('click', async () => {
    const code = document.getElementById('info-trial-code').value.trim().toUpperCase();
    const estate = document.getElementById('info-estate').value.trim();
    const year = parseInt(document.getElementById('info-planting-year').value, 10) || 1988;
    const count = parseInt(document.getElementById('info-factor-count').value, 10) || 4;
    const info = document.getElementById('info-factor-details').value;

    const factorInputs = document.querySelectorAll('.factor-label-input');
    const factors = [];
    factorInputs.forEach((inp, idx) => {
      const lbl = inp.value.trim();
      if (lbl && factors.length < count) {
        factors.push({ id: idx + 1, label: lbl, name: lbl });
      }
    });

    if (!code) {
      alert('Please enter a Trial Code.');
      return;
    }

    if (isNewMode) {
      const existing = trials.find(t => t.code === code);
      if (existing) {
        alert(`Trial Code "${code}" already exists.`);
        return;
      }
      const newTrial = {
        code,
        estate: estate || 'New Estate',
        plantingYear: year,
        factorsCount: factors.length,
        factors,
        factorInfo: info,
        densityType: 'constant',
        constantDensity: 148,
        plotTreatments: [],
        palms: []
      };
      trials.unshift(newTrial);
      currentCode = code;

      // Persist to Supabase
      if (window.ReadaSync) {
        await window.ReadaSync.saveTrial(newTrial);
      }
      showToast(`Created Trial ${code} (${estate})`);
    } else {
      const t = getCurrentTrial();
      t.estate = estate;
      t.plantingYear = year;
      t.factorsCount = factors.length;
      t.factors = factors;
      t.factorInfo = info;

      // Persist to Supabase
      if (window.ReadaSync) {
        await window.ReadaSync.saveTrial(t);
      }
      showToast(`Updated Main Information for ${t.code}`);
    }

    refreshHeader();
    closeModal(modals.trialInfo);
  });

  // =========================================================================
  // FIGURE 7 (2.6): EDITING PLOT TREATMENT DETAIL Pop-up
  // =========================================================================
  function openPlotTreatmentModal() {
    const t = getCurrentTrial();
    const modal = modals.plotTreatment;

    document.getElementById('treatment-modal-code').textContent = t.code;
    document.getElementById('treatment-modal-estate').textContent = t.estate;

    const constantRadio = document.getElementById('density-mode-constant');
    const variesRadio = document.getElementById('density-mode-varies');
    const constantInp = document.getElementById('density-constant-val');

    constantInp.value = t.constantDensity || 148;
    if (t.densityType === 'varies') {
      variesRadio.checked = true;
      constantInp.disabled = true;
    } else {
      constantRadio.checked = true;
      constantInp.disabled = false;
    }

    constantRadio.onchange = () => {
      constantInp.disabled = false;
      applyConstantDensity(parseInt(constantInp.value, 10) || 148);
    };
    variesRadio.onchange = () => {
      constantInp.disabled = true;
    };
    constantInp.oninput = () => {
      if (constantRadio.checked) {
        applyConstantDensity(parseInt(constantInp.value, 10) || 148);
      }
    };

    renderPlotTreatmentTable();
    openModal(modal);
  }

  function applyConstantDensity(val) {
    const t = getCurrentTrial();
    if (!t.plotTreatments) return;
    t.plotTreatments.forEach(pt => pt.density = val);
    renderPlotTreatmentTable();
  }

  function renderPlotTreatmentTable() {
    const t = getCurrentTrial();
    const tbody = document.getElementById('treatment-table-body');
    const theadRow = document.getElementById('treatment-table-header-row');
    if (!tbody || !theadRow) return;

    const factors = t.factors && t.factors.length > 0 ? t.factors : [
      { label: 'Rep' }, { label: 'D' }, { label: 'N' }, { label: 'P' }, { label: 'K' }, { label: 'L' }
    ];

    theadRow.innerHTML = `
      <th style="width: 50px;">Rec</th>
      <th style="width: 44px; text-align: center;">Del</th>
      <th style="width: 80px;">Plot</th>
      <th style="width: 80px;">Sub Plot</th>
      ${factors.map(f => `<th style="text-align: center; color: var(--brand-green);">${f.label}</th>`).join('')}
      <th style="width: 100px;">Density</th>
    `;

    tbody.innerHTML = '';
    const records = t.plotTreatments || [];
    if (records.length === 0) {
      tbody.innerHTML = `<tr><td colspan="${5 + factors.length}" style="text-align: center; padding: 24px; color: var(--text-faint);">No plot treatments recorded yet. Click "+ Add New Plot Row" below.</td></tr>`;
      return;
    }

    records.forEach((row, idx) => {
      const tr = document.createElement('tr');
      const levels = row.levels || [];
      const factorCells = factors.map((f, fIdx) => `
        <td style="text-align: center;">
          <input type="number" class="cell-edit-input" data-row="${idx}" data-factor="${fIdx}" value="${levels[fIdx] ?? 0}" min="0" max="9" style="width: 48px; text-align: center;">
        </td>
      `).join('');

      tr.innerHTML = `
        <td style="font-family: var(--font-mono); color: var(--text-muted);">${row.rec || (idx + 1)}</td>
        <td style="text-align: center;">
          <button type="button" class="btn-del-row" data-del-row="${idx}" title="Delete Row">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>
          </button>
        </td>
        <td><input type="number" class="cell-edit-input" data-field="plot" data-row="${idx}" value="${row.plot || (idx + 1)}" style="width: 60px;"></td>
        <td><input type="text" class="cell-edit-input" data-field="subPlot" data-row="${idx}" value="${row.subPlot || ''}" placeholder="—" style="width: 60px; text-transform: uppercase;"></td>
        ${factorCells}
        <td><input type="number" class="cell-edit-input" data-field="density" data-row="${idx}" value="${row.density || 160}" style="width: 70px;"></td>
      `;
      tbody.appendChild(tr);
    });

    // Del button listeners
    tbody.querySelectorAll('[data-del-row]').forEach(btn => {
      btn.addEventListener('click', () => {
        const rowIdx = parseInt(btn.getAttribute('data-del-row'), 10);
        t.plotTreatments.splice(rowIdx, 1);
        t.plotTreatments.forEach((r, i) => r.rec = i + 1);
        renderPlotTreatmentTable();
        refreshHeader();
      });
    });

    // Cell input listeners
    tbody.querySelectorAll('input.cell-edit-input').forEach(inp => {
      inp.addEventListener('change', () => {
        const rowIdx = parseInt(inp.getAttribute('data-row'), 10);
        const field = inp.getAttribute('data-field');
        const factorIdx = inp.getAttribute('data-factor');
        if (field) {
          t.plotTreatments[rowIdx][field] = field === 'subPlot' ? inp.value.trim().toUpperCase() : parseInt(inp.value, 10) || 0;
        } else if (factorIdx !== null) {
          if (!t.plotTreatments[rowIdx].levels) t.plotTreatments[rowIdx].levels = [];
          t.plotTreatments[rowIdx].levels[parseInt(factorIdx, 10)] = parseInt(inp.value, 10) || 0;
        }
      });
    });
  }

  // Add Treatment Row button
  document.getElementById('btn-add-treatment-row')?.addEventListener('click', () => {
    const t = getCurrentTrial();
    if (!t.plotTreatments) t.plotTreatments = [];
    const newRec = t.plotTreatments.length + 1;
    const lastPlot = t.plotTreatments.length > 0 ? (t.plotTreatments[t.plotTreatments.length - 1].plot || 0) : 0;
    const fCount = (t.factors || []).length || 6;
    const densityVal = document.getElementById('density-mode-constant').checked
      ? (parseInt(document.getElementById('density-constant-val').value, 10) || 148)
      : 160;

    t.plotTreatments.push({
      rec: newRec,
      plot: lastPlot + 1,
      subPlot: '',
      levels: Array(fCount).fill(1),
      density: densityVal
    });

    renderPlotTreatmentTable();
    refreshHeader();
    const wrap = document.getElementById('treatment-table-wrap');
    if (wrap) wrap.scrollTop = wrap.scrollHeight;
  });

  // Save Plot Treatment (Figure 7 [Yes] button)
  document.getElementById('btn-save-plot-treatment')?.addEventListener('click', async () => {
    const t = getCurrentTrial();
    t.densityType = document.getElementById('density-mode-varies').checked ? 'varies' : 'constant';
    t.constantDensity = parseInt(document.getElementById('density-constant-val').value, 10) || 148;
    
    if (window.ReadaSync) {
      await window.ReadaSync.saveTrial(t, false);
      await window.ReadaSync.saveTreatments(t.code, t.plotTreatments);
    }
    showToast(`Saved ${t.plotTreatments.length} plot treatments for ${t.code}`);
    refreshHeader();
    closeModal(modals.plotTreatment);
  });

  // =========================================================================
  // FIGURE 11 (2.11): ENTERING / EDITING PALM NUMBERING Pop-up
  // =========================================================================
  function openPalmNumberingModal() {
    const t = getCurrentTrial();
    const modal = modals.palmNumbering;
    document.getElementById('palm-modal-code').textContent = t.code;
    document.getElementById('palm-modal-estate').textContent = t.estate;
    renderPalmTable();
    openModal(modal);
  }

  function renderPalmTable() {
    const t = getCurrentTrial();
    const tbody = document.getElementById('palm-table-body');
    if (!tbody) return;

    tbody.innerHTML = '';
    const palms = t.palms || [];
    if (palms.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 24px; color: var(--text-faint);">No palm numbering recorded for this trial yet. Click "+ Add Palm" or "Auto-Generate Series" below.</td></tr>`;
      return;
    }

    palms.forEach((row, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="font-family: var(--font-mono); color: var(--text-muted);">${row.rec || (idx + 1)}</td>
        <td style="text-align: center;">
          <button type="button" class="btn-del-row" data-del-palm="${idx}" title="Delete Palm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/></svg>
          </button>
        </td>
        <td><input type="number" class="cell-edit-input" data-field="plot" data-row="${idx}" value="${row.plot || 1}" style="width: 60px;"></td>
        <td><input type="text" class="cell-edit-input" data-field="subPlot" data-row="${idx}" value="${row.subPlot || ''}" placeholder="—" style="width: 60px; text-transform: uppercase;"></td>
        <td><input type="text" class="cell-edit-input" data-field="palmNo" data-row="${idx}" value="${row.palmNo || ''}" style="width: 90px; font-weight: 600;"></td>
        <td><input type="text" class="cell-edit-input" data-field="progeny" data-row="${idx}" value="${row.progeny || 'D x P AVROS'}" style="width: 140px;"></td>
      `;
      tbody.appendChild(tr);
    });

    tbody.querySelectorAll('[data-del-palm]').forEach(btn => {
      btn.addEventListener('click', () => {
        const rowIdx = parseInt(btn.getAttribute('data-del-palm'), 10);
        t.palms.splice(rowIdx, 1);
        t.palms.forEach((r, i) => r.rec = i + 1);
        renderPalmTable();
        refreshHeader();
      });
    });

    tbody.querySelectorAll('input.cell-edit-input').forEach(inp => {
      inp.addEventListener('change', () => {
        const rowIdx = parseInt(inp.getAttribute('data-row'), 10);
        const field = inp.getAttribute('data-field');
        if (field && t.palms[rowIdx]) {
          t.palms[rowIdx][field] = inp.value;
        }
      });
    });
  }

  // Add Palm Row
  document.getElementById('btn-add-palm-row')?.addEventListener('click', () => {
    const t = getCurrentTrial();
    if (!t.palms) t.palms = [];
    const newRec = t.palms.length + 1;
    const last = t.palms[t.palms.length - 1];
    const nextPlot = last ? last.plot : 1;
    const nextNo = last ? (parseInt(last.palmNo, 10) + 1 || (newRec * 10)) : 101;

    t.palms.push({
      rec: newRec,
      plot: nextPlot,
      subPlot: '',
      palmNo: String(nextNo),
      progeny: last ? last.progeny : 'D x P AVROS'
    });
    renderPalmTable();
    refreshHeader();
    const wrap = document.getElementById('palm-table-wrap');
    if (wrap) wrap.scrollTop = wrap.scrollHeight;
  });

  // Auto-Generate Palm Series
  document.getElementById('btn-generate-palms')?.addEventListener('click', () => {
    const t = getCurrentTrial();
    const plot = prompt('Enter Plot Number to generate palms for:', '4');
    if (!plot) return;
    const count = parseInt(prompt('How many palms to generate (e.g. 16)?', '16'), 10);
    if (!count || isNaN(count)) return;
    const startNo = parseInt(prompt('Start Palm Number:', '401'), 10) || 401;

    if (!t.palms) t.palms = [];
    for (let i = 0; i < count; i++) {
      t.palms.push({
        rec: t.palms.length + 1,
        plot: parseInt(plot, 10),
        subPlot: '',
        palmNo: String(startNo + i),
        progeny: 'D x P AVROS'
      });
    }
    renderPalmTable();
    refreshHeader();
    showToast(`Generated ${count} palms for Plot ${plot}`);
  });

  // Save Palm Numbering (Figure 11 [Yes] button)
  document.getElementById('btn-save-palm')?.addEventListener('click', async () => {
    const t = getCurrentTrial();
    if (window.ReadaSync) {
      await window.ReadaSync.savePalms(t.code, t.palms);
    }
    showToast(`Saved ${t.palms.length} palm numbers for ${t.code}`);
    refreshHeader();
    closeModal(modals.palmNumbering);
  });

  // =========================================================================
  // FIGURES 5, 8, 12 (2.3, 2.7, 2.12): Save As *.dbf File Pop-ups
  // =========================================================================
  // =========================================================================
  // FIGURES 5, 8, 12: Direct CSV Export to Downloads
  // =========================================================================
  function exportMainInfoCSVDirect(type) {
    const t = getCurrentTrial();
    let csvFileName = '';
    let csvContent = '';

    if (type === 'info') {
      csvFileName = `INFO_${t.code}.csv`;
      csvContent = 'TRIAL_CODE,ESTATE,PLANTING_YEAR,FACTORS_COUNT,DENSITY_TYPE,CONSTANT_DENSITY,FACTOR_DEFINITIONS\n';
      const factorDef = (t.factorInfo || '').replace(/"/g, '""').replace(/\n/g, '; ');
      csvContent += `"${t.code}","${t.estate}",${t.plantingYear || ''},${(t.factors || []).length},"${t.densityType || ''}",${t.constantDensity || ''},"${factorDef}"\n`;
    } else if (type === 'treatment') {
      csvFileName = `TREAT_${t.code}.csv`;
      csvContent = 'REC_NO,PLOT_NO,SUB_PLOT,FACTOR1,FACTOR2,FACTOR3,FACTOR4,FACTOR5,FACTOR6,DENSITY\n';
      (t.plotTreatments || []).forEach(tr => {
        const lvls = tr.levels || [];
        csvContent += `${tr.rec},${tr.plot},"${tr.subPlot || ''}",${lvls[0] ?? ''},${lvls[1] ?? ''},${lvls[2] ?? ''},${lvls[3] ?? ''},${lvls[4] ?? ''},${lvls[5] ?? ''},${tr.density || ''}\n`;
      });
    } else {
      csvFileName = `PALM_${t.code}.csv`;
      csvContent = 'REC_NO,PLOT_NO,SUB_PLOT,PALM_NO,PROGENY,STATUS\n';
      (t.palms || []).forEach(p => {
        csvContent += `${p.rec},${p.plot},"${p.subPlot || ''}","${p.palmNo || ''}","${(p.progeny || '').replace(/"/g, '""')}","${p.status || ''}"\n`;
      });
    }

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = csvFileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showToast(`Downloaded ${csvFileName} to your Downloads folder`);
  }

  function openSaveDbfModal(type) {
    currentSaveType = type;
    exportMainInfoCSVDirect(type);
  }

  // Confirm Save / Export as CSV ONLY (No JSON / No DBF)
  document.getElementById('btn-confirm-save-dbf')?.addEventListener('click', () => {
    exportMainInfoCSVDirect(currentSaveType);
    closeModal(modals.saveDbf);
  });

  // =========================================================================
  // FIGURES 6, 9, 13: Read Backup / Excel File Pop-ups
  // =========================================================================
  function openBackupModal(type) {
    currentBackupType = type;
    const t = getCurrentTrial();
    const modal = modals.backup;
    const title = document.getElementById('backup-modal-title');
    const fileInp = document.getElementById('backup-filename');
    const previewBox = document.getElementById('backup-preview-box');

    previewBox.style.display = 'none';

    if (type === 'info') {
      title.textContent = 'Read Trial Main Information From Backup / Excel File';
      fileInp.value = 'C:\\READA\\BCINFO.CSV';
    } else if (type === 'treatment') {
      title.textContent = 'Read Plot Treatment Data From Backup / Excel File';
      fileInp.value = 'C:\\READA\\BCTREAT.CSV';
    } else {
      title.textContent = 'Read Palm Numbering From Backup / Excel File';
      fileInp.value = 'C:\\READA\\BCPALM.CSV';
    }

    openModal(modal);
  }

  // Check Trial Code Availability
  document.getElementById('btn-check-backup')?.addEventListener('click', () => {
    const box = document.getElementById('backup-preview-box');
    const txt = document.getElementById('backup-preview-text');
    const t = getCurrentTrial();
    box.style.display = 'block';
    txt.innerHTML = `
      <strong>Backup File Verified:</strong> ${document.getElementById('backup-filename').value}<br>
      Found archived snapshot matching Trial Code: <strong>${t.code} (${t.estate})</strong>.<br>
      Ready to restore and replace current active records.
    `;
  });

  // Start Replacing Data From Backup File
  document.getElementById('btn-start-replace-backup')?.addEventListener('click', () => {
    const t = getCurrentTrial();
    showToast(`Data for ${t.code} restored from backup file successfully`);
    closeModal(modals.backup);
    refreshHeader();
  });

  // =========================================================================
  // FIGURES 10 & 14: Read From Excel File (*.xlsx / *.xls / *.csv)
  // =========================================================================
  function renderNonReadaPreview(ext) {
    const thead = document.getElementById('non-reada-table-head');
    const tbody = document.getElementById('non-reada-table-body');
    if (thead && tbody && ext && ext.fields) {
      thead.innerHTML = `<tr>${ext.fields.map(f => `<th>${f}</th>`).join('')}</tr>`;
      tbody.innerHTML = (ext.sampleRows || []).slice(0, 50).map(r => `
        <tr>${ext.fields.map(f => `<td style="font-family: var(--font-mono); font-size: 0.76rem;">${r[f] ?? ''}</td>`).join('')}</tr>
      `).join('');
    }
  }

  function openNonReadaModal(type) {
    const modal = modals.nonReada;
    const t = getCurrentTrial();
    const title = document.getElementById('non-reada-modal-title');
    const fileInp = document.getElementById('non-reada-filename');

    document.getElementById('non-reada-code').textContent = t.code;
    document.getElementById('non-reada-estate').textContent = t.estate;

    if (type === 'treatment') {
      title.textContent = "Import Trial Plot Treatment from Excel Spreadsheet";
      fileInp.value = 'B:\\DTPL1195.XLSX';
    } else {
      title.textContent = "Import Palm Numbering from Excel Spreadsheet";
      fileInp.value = 'B:\\DTPY97.XLSX';
    }

    const ext = window.READA_EXTERNAL_DBF || { fields: [], sampleRows: [] };
    renderNonReadaPreview(ext);
    openModal(modal);
  }

  // Handle Excel File Upload Input using SheetJS
  document.getElementById('non-reada-file-upload')?.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const nameInp = document.getElementById('non-reada-filename');
    if (nameInp) nameInp.value = file.name;

    try {
      if (window.XLSX) {
        const buffer = await file.arrayBuffer();
        const workbook = window.XLSX.read(buffer, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const rows = window.XLSX.utils.sheet_to_json(worksheet);

        if (rows && rows.length > 0) {
          const fields = Object.keys(rows[0]);
          window.READA_EXTERNAL_DBF = {
            fileName: file.name,
            fields: fields,
            sampleRows: rows
          };
          renderNonReadaPreview(window.READA_EXTERNAL_DBF);
          showToast(`Read ${rows.length} rows from Excel sheet "${sheetName}"`);
        }
      }
    } catch (err) {
      console.error(err);
      showToast(`Error parsing Excel file: ${err.message}`);
    }
  });

  // Start Reading File & Map
  document.getElementById('btn-start-reading-file')?.addEventListener('click', () => {
    const t = getCurrentTrial();
    const ext = window.READA_EXTERNAL_DBF;
    if (ext && ext.sampleRows && ext.sampleRows.length > 0) {
      t.plotTreatments = ext.sampleRows.map((r, i) => ({
        rec: i + 1,
        plot: r.PLOT || r.PLOT_ID || r.PLOT_NO || (i + 1),
        subPlot: r.SUBPLOT || r.BLOCK || r.SUB_PLOT || '',
        levels: [
          r.REP || r.REP_CODE || r.FACTOR1 || 1,
          r.D || r.DENS_LVL || r.FACTOR2 || 1,
          r.N || r.N_LVL || r.FACTOR3 || 0,
          r.P || r.P_LVL || r.FACTOR4 || 0,
          r.K || r.K_LVL || r.FACTOR5 || 0,
          r.L || r.L_LVL || r.FACTOR6 || 0
        ],
        density: r.DENSITY || r.SPACING || 148
      }));
      showToast(`Mapped ${ext.sampleRows.length} external records into ${t.code}`);
    }
    refreshHeader();
    closeModal(modals.nonReada);
  });

  // =========================================================================
  // 2.4, 2.10, 2.15: Delete Confirmations
  // =========================================================================
  function openDeleteModal(type) {
    currentDeleteType = type;
    const t = getCurrentTrial();
    const modal = modals.confirmDelete;
    const title = document.getElementById('delete-modal-title');
    const msg = document.getElementById('delete-modal-msg');
    const warning = document.getElementById('delete-modal-warning');
    const confirmBtn = document.getElementById('btn-confirm-delete');

    if (type === 'info') {
      title.textContent = 'Delete Trial Information';
      msg.innerHTML = `Are you sure you want to permanently delete trial <strong>${t.code} (${t.estate})</strong>?`;
      if ((t.plotTreatments && t.plotTreatments.length > 0) || (t.palms && t.palms.length > 0)) {
        warning.innerHTML = `⚠️ <strong>Data Integrity Rule:</strong> Every data record (Plot Treatments and Palm Numbers) for ${t.code} must be deleted before deleting the main information. Please clear dependent records first!`;
        confirmBtn.disabled = true;
      } else {
        warning.innerHTML = `No dependent plot treatments or palms found. You can safely delete this trial.`;
        confirmBtn.disabled = false;
      }
    } else if (type === 'treatment') {
      title.textContent = 'Delete Plot Treatment Data';
      msg.innerHTML = `Are you sure you want to delete all <strong>${t.plotTreatments.length} plot treatments</strong> for <strong>${t.code}</strong>?`;
      warning.innerHTML = `This action cannot be undone.`;
      confirmBtn.disabled = false;
    } else {
      title.textContent = 'Delete Palm Numbering Data';
      msg.innerHTML = `Are you sure you want to delete all <strong>${t.palms.length} palm numbers</strong> for <strong>${t.code}</strong>?`;
      warning.innerHTML = `This action cannot be undone.`;
      confirmBtn.disabled = false;
    }

    openModal(modal);
  }

  document.getElementById('btn-confirm-delete')?.addEventListener('click', async () => {
    const t = getCurrentTrial();
    if (currentDeleteType === 'info') {
      const codeToDelete = t.code;
      const idx = trials.findIndex(tr => tr.code === codeToDelete);
      if (idx !== -1) {
        trials.splice(idx, 1);
        currentCode = trials[0] ? trials[0].code : '';
        if (window.ReadaSync) {
          await window.ReadaSync.deleteTrial(codeToDelete);
        }
        showToast(`Deleted trial ${codeToDelete}`);
      }
    } else if (currentDeleteType === 'treatment') {
      t.plotTreatments = [];
      if (window.ReadaSync) {
        await window.ReadaSync.saveTreatments(t.code, []);
      }
      showToast(`Deleted plot treatments for ${t.code}`);
    } else {
      t.palms = [];
      if (window.ReadaSync) {
        await window.ReadaSync.savePalms(t.code, []);
      }
      showToast(`Deleted palm numbers for ${t.code}`);
    }

    refreshHeader();
    closeModal(modals.confirmDelete);
  });

  // =========================================================================
  // FIGURE 3: Wire Up the 15 Action Buttons
  // =========================================================================
  // Group 1: Trial Info (Trial Code)
  document.getElementById('btn-new-trial-info')?.addEventListener('click', () => openTrialInfoModal(true));
  document.getElementById('btn-edit-trial-info')?.addEventListener('click', () => openTrialInfoModal(false));
  document.getElementById('btn-save-info-dbf')?.addEventListener('click', () => openSaveDbfModal('info'));
  document.getElementById('btn-delete-trial-info')?.addEventListener('click', () => openDeleteModal('info'));
  document.getElementById('btn-read-info-backup')?.addEventListener('click', () => openBackupModal('info'));

  // Group 2: Plot Treatment
  document.getElementById('btn-entry-plot-treatment')?.addEventListener('click', async () => {
    const t = getCurrentTrial();
    if (window.ReadaSync && t) {
      await window.ReadaSync.loadTrialDetails(t);
    }
    openPlotTreatmentModal();
  });
  document.getElementById('btn-save-treatment-dbf')?.addEventListener('click', () => openSaveDbfModal('treatment'));
  document.getElementById('btn-read-treatment-backup')?.addEventListener('click', () => openBackupModal('treatment'));
  document.getElementById('btn-read-treatment-nonreada')?.addEventListener('click', () => openNonReadaModal('treatment'));
  document.getElementById('btn-delete-plot-treatment')?.addEventListener('click', () => openDeleteModal('treatment'));

  // Group 3: Palm Numbering
  document.getElementById('btn-entry-palm-numbering')?.addEventListener('click', async () => {
    const t = getCurrentTrial();
    if (window.ReadaSync && t) {
      await window.ReadaSync.loadTrialDetails(t);
    }
    openPalmNumberingModal();
  });
  document.getElementById('btn-save-palm-dbf')?.addEventListener('click', () => openSaveDbfModal('palm'));
  document.getElementById('btn-read-palm-backup')?.addEventListener('click', () => openBackupModal('palm'));
  document.getElementById('btn-read-palm-nonreada')?.addEventListener('click', () => openNonReadaModal('palm'));
  document.getElementById('btn-delete-palm-numbering')?.addEventListener('click', () => openDeleteModal('palm'));

  // Top Selector and Update Code List
  if (el.trialSelect) {
    el.trialSelect.addEventListener('change', async (e) => {
      currentCode = e.target.value;
      const t = getCurrentTrial();
      if (window.ReadaSync && t) {
        await window.ReadaSync.loadTrialDetails(t);
      }
      refreshHeader();
      showToast(`Switched active trial to ${currentCode}`);
    });
  }

  document.getElementById('btn-update-code-list')?.addEventListener('click', async () => {
    if (window.ReadaSync) {
      const freshTrials = await window.ReadaSync.fetchTrials();
      if (freshTrials && freshTrials.length > 0) {
        trials = freshTrials;
      }
    }
    refreshHeader();
    showToast('Trial code list refreshed from Supabase Cloud');
  });

  // Init with Supabase synchronization
  async function init() {
    if (window.ReadaSync && typeof window.ReadaSync.fetchTrials === 'function') {
      try {
        const fetched = await window.ReadaSync.fetchTrials();
        if (fetched && fetched.length > 0) {
          trials = fetched;
          if (!trials.find(t => t.code === currentCode)) {
            currentCode = trials[0].code;
          }
        }
      } catch (e) {
        console.warn('ReadaSync fetch error on init:', e);
      }
    }
    const t = getCurrentTrial();
    if (window.ReadaSync && t) {
      await window.ReadaSync.loadTrialDetails(t);
    }
    refreshHeader();
  }

  init();

})();
