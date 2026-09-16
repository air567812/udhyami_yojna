/**
 * Main Application Orchestrator for Udhyami Yojna
 * Modular ES module coordinating Voice, API, UI Rendering, and State Hub
 */

import { VoiceManager, INDIAN_LOCALES } from './voice.js';
import { extractTranscript, matchSchemes, fetchSchemes, checkHealth } from './api.js';
import {
  renderBrowserNotice,
  populateProfileForm,
  getProfileFromForm,
  renderSchemeResults,
  renderCatalog,
  showToast
} from './render.js';
import { StateHubManager } from './state-hub.js';

// DOM Elements
const elements = {
  // Navigation Tabs
  navTabs: document.querySelectorAll('.nav-tab'),
  tabPanes: document.querySelectorAll('.tab-pane'),

  // Voice Section
  browserNoticeContainer: document.getElementById('browser-notice-container'),
  localeSelect: document.getElementById('voice-locale-select'),
  micBtnContainer: document.getElementById('mic-btn-container'),
  micBtn: document.getElementById('mic-btn'),
  micStatusText: document.getElementById('mic-status-text'),
  transcriptBox: document.getElementById('transcript-box'),
  btnExtractAi: document.getElementById('btn-extract-ai'),
  btnClearTranscript: document.getElementById('btn-clear-transcript'),
  sampleChips: document.querySelectorAll('.chip-btn'),

  // Form Section
  profileForm: document.getElementById('profile-form'),
  btnSubmitProfile: document.getElementById('btn-submit-profile'),
  btnResetForm: document.getElementById('btn-reset-form'),

  // Results Section
  resultsContainer: document.getElementById('scheme-results-container'),
  resultsPlaceholder: document.getElementById('results-placeholder'),

  // Catalog Section
  catalogContainer: document.getElementById('catalog-schemes-container'),
  catalogSectorFilter: document.getElementById('catalog-sector-filter'),
  catalogCategoryFilter: document.getElementById('catalog-category-filter'),
  catalogSearchInput: document.getElementById('catalog-search-input'),

  // State Hub
  stateSelect: document.getElementById('state-hub-select'),
  stateDetailsContainer: document.getElementById('state-hub-details')
};

// Global Voice Manager Instance
let voiceManager = null;
let stateHubManager = null;
let currentWizardStep = 1;

/**
 * Initialize Application
 */
document.addEventListener('DOMContentLoaded', async () => {
  console.log('Initializing Udhyami Yojna Client v1.0.0 (india.gov.in theme)...');

  initAccessibilityControls();
  initNavTabs();
  initGlobalSearch();
  initTopicsBar();
  initWizard();
  initVoice();
  initFormActions();
  initCatalog();
  initStateHub();
  initSimulator();
  initTTS();
  initMobileQRModal();
  initModals();
  initSitemapLinks();
  initSpotlightCards();
  checkSystemStatus();
});

/**
 * GIGW 3.0 Accessibility Controls: Font Resizing & High-Contrast Mode
 */
function initAccessibilityControls() {
  const btnFontSm = document.getElementById('btn-font-sm');
  const btnFontMd = document.getElementById('btn-font-md');
  const btnFontLg = document.getElementById('btn-font-lg');
  const btnToggleContrast = document.getElementById('btn-toggle-contrast');

  const setFontSize = (size) => {
    document.body.classList.remove('font-sm', 'font-md', 'font-lg');
    if (size !== 'font-md') {
      document.body.classList.add(size);
    }
    localStorage.setItem('udhyam_font_size', size);

    [btnFontSm, btnFontMd, btnFontLg].forEach(btn => btn && btn.classList.remove('active'));
    if (size === 'font-sm' && btnFontSm) btnFontSm.classList.add('active');
    if (size === 'font-md' && btnFontMd) btnFontMd.classList.add('active');
    if (size === 'font-lg' && btnFontLg) btnFontLg.classList.add('active');
  };

  if (btnFontSm) btnFontSm.addEventListener('click', () => setFontSize('font-sm'));
  if (btnFontMd) btnFontMd.addEventListener('click', () => setFontSize('font-md'));
  if (btnFontLg) btnFontLg.addEventListener('click', () => setFontSize('font-lg'));

  // Restore saved font size
  const savedFontSize = localStorage.getItem('udhyam_font_size');
  if (savedFontSize) setFontSize(savedFontSize);

  // High Contrast Mode
  const setContrast = (isHigh) => {
    if (isHigh) {
      document.body.classList.add('high-contrast');
      if (btnToggleContrast) {
        btnToggleContrast.classList.add('active');
        btnToggleContrast.setAttribute('aria-pressed', 'true');
      }
      localStorage.setItem('udhyam_contrast', 'high');
    } else {
      document.body.classList.remove('high-contrast');
      if (btnToggleContrast) {
        btnToggleContrast.classList.remove('active');
        btnToggleContrast.setAttribute('aria-pressed', 'false');
      }
      localStorage.setItem('udhyam_contrast', 'normal');
    }
  };

  if (btnToggleContrast) {
    btnToggleContrast.addEventListener('click', () => {
      const isHigh = !document.body.classList.contains('high-contrast');
      setContrast(isHigh);
      showToast(isHigh ? 'High contrast theme enabled' : 'Standard theme enabled', 'info');
    });
  }

  // Restore saved contrast
  if (localStorage.getItem('udhyam_contrast') === 'high') {
    setContrast(true);
  }
}

/**
 * Single-Page Guided Flow: Smoothly scroll and highlight sections
 */
export function goToWizardStep(stepNumber) {
  currentWizardStep = stepNumber;

  // Ensure scheme finder tab is active if clicked from elsewhere
  const finderTab = document.getElementById('tab-btn-finder');
  if (finderTab && !finderTab.classList.contains('active')) {
    finderTab.click();
  }

  if (stepNumber === 1) {
    const el = document.getElementById('voice-section') || document.getElementById('pane-finder');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else if (stepNumber === 2) {
    const formCard = document.getElementById('profile-form-card') || document.getElementById('profile-form');
    if (formCard) {
      formCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      formCard.classList.add('auto-filled-highlight');
      setTimeout(() => formCard.classList.remove('auto-filled-highlight'), 1200);
    }
  } else if (stepNumber === 3) {
    const resultsCard = document.getElementById('results-card') || document.getElementById('results-section');
    if (resultsCard) {
      resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
}

function initWizard() {
  // Navigation Buttons
  const btnGotoStep2 = document.getElementById('btn-goto-step-2');
  if (btnGotoStep2) {
    btnGotoStep2.addEventListener('click', (e) => {
      e.preventDefault();
      goToWizardStep(2);
    });
  }

  const btnStartStep1 = document.getElementById('btn-start-step-1');
  if (btnStartStep1) {
    btnStartStep1.addEventListener('click', (e) => {
      e.preventDefault();
      goToWizardStep(1);
    });
  }

  // Print Action
  const btnPrintResults = document.getElementById('btn-print-results');
  if (btnPrintResults) {
    btnPrintResults.addEventListener('click', () => {
      window.print();
    });
  }

  // Sector Quick-Chips (1-Click preset loading)
  const sectorChips = document.querySelectorAll('.sector-chip');
  sectorChips.forEach(chip => {
    chip.addEventListener('click', () => {
      sectorChips.forEach(c => c.classList.remove('selected'));
      chip.classList.add('selected');

      const sector = chip.getAttribute('data-sector');
      const cost = chip.getAttribute('data-cost');
      const cat = chip.getAttribute('data-cat');
      const gender = chip.getAttribute('data-gender');
      const desc = chip.getAttribute('data-desc');

      if (elements.profileForm) {
        if (sector && elements.profileForm.elements['sector']) {
          elements.profileForm.elements['sector'].value = sector;
        }
        if (cost && elements.profileForm.elements['investment_needed']) {
          elements.profileForm.elements['investment_needed'].value = cost;
        }
        if (cat && elements.profileForm.elements['social_category']) {
          elements.profileForm.elements['social_category'].value = cat;
        }
        if (gender && elements.profileForm.elements['gender']) {
          elements.profileForm.elements['gender'].value = gender;
        }
        if (desc && elements.profileForm.elements['business_idea']) {
          elements.profileForm.elements['business_idea'].value = desc;
        }
        if (!elements.profileForm.elements['age'].value) {
          elements.profileForm.elements['age'].value = 30;
        }
      }

      showToast(`Selected ${sector} preset. Please verify form details below.`, 'info');
      goToWizardStep(2);
    });
  });
}

/**
 * Tab Navigation Setup with Dynamic National Portal Breadcrumbs
 */
function initNavTabs() {
  const breadcrumbCurrent = document.getElementById('breadcrumb-current-page');
  const breadcrumbSection = document.getElementById('breadcrumb-section-link');

  const titles = {
    'pane-finder': { section: 'Government Schemes & Financial Inclusion', current: 'Citizen Scheme Finder (योजना खोज)' },
    'pane-states': { section: 'Ecosystem & Infrastructure', current: 'State-Wise Entrepreneurial Hub (राज्य हब)' },
    'pane-catalog': { section: 'Catalog & Gazetted Guidelines', current: 'Master Scheme Catalog (संपूर्ण योजना सूची)' },
    'pane-sitemap': { section: 'Site Index & Governance', current: 'Detailed Sitemap (विस्तृत साइटमैप)' }
  };

  elements.navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.getAttribute('data-tab');

      elements.navTabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      elements.tabPanes.forEach(p => p.classList.remove('active'));

      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      const activePane = document.getElementById(targetId);
      if (activePane) {
        activePane.classList.add('active');
      }

      if (titles[targetId] && breadcrumbCurrent && breadcrumbSection) {
        breadcrumbSection.textContent = titles[targetId].section;
        breadcrumbCurrent.textContent = titles[targetId].current;
      }
    });
  });
}

/**
 * Universal Global Search Bar (india.gov.in style)
 */
function initGlobalSearch() {
  const searchInput = document.getElementById('global-search-input');
  const catSelect = document.getElementById('global-search-category');
  const searchBtn = document.getElementById('btn-global-search');

  const executeSearch = () => {
    const query = searchInput ? searchInput.value.trim() : '';
    const cat = catSelect ? catSelect.value : '';

    // Switch to Catalog Tab
    const catalogTab = document.getElementById('tab-btn-catalog');
    if (catalogTab) catalogTab.click();

    // Set search in catalog
    if (elements.catalogSearchInput) {
      elements.catalogSearchInput.value = query;
      elements.catalogSearchInput.dispatchEvent(new Event('input'));
    }

    if (cat) {
      if (['Manufacturing', 'Food Processing', 'Handicraft/Handloom', 'Trading'].includes(cat) && elements.catalogSectorFilter) {
        elements.catalogSectorFilter.value = cat;
        elements.catalogSectorFilter.dispatchEvent(new Event('change'));
      } else if (['Women', 'SC'].includes(cat) && elements.catalogCategoryFilter) {
        elements.catalogCategoryFilter.value = cat;
        elements.catalogCategoryFilter.dispatchEvent(new Event('change'));
      }
    }

    showToast(`Showing schemes for "${query || cat || 'All Categories'}"`, 'info');
  };

  if (searchBtn) searchBtn.addEventListener('click', executeSearch);
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        executeSearch();
      }
    });
  }
}

/**
 * Quick Focus Sectors Pills Bar (india.gov.in pattern)
 */
function initTopicsBar() {
  const topicPills = document.querySelectorAll('.npi-topic-pill');
  topicPills.forEach(pill => {
    pill.addEventListener('click', () => {
      topicPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const topic = pill.getAttribute('data-topic') || '';

      // Switch to catalog
      const catalogTab = document.getElementById('tab-btn-catalog');
      if (catalogTab) catalogTab.click();

      // Clear search
      if (elements.catalogSearchInput) {
        elements.catalogSearchInput.value = '';
      }

      if (['Women', 'SC', 'Divyangjan'].includes(topic) && elements.catalogCategoryFilter) {
        elements.catalogCategoryFilter.value = topic;
        elements.catalogCategoryFilter.dispatchEvent(new Event('change'));
        if (elements.catalogSectorFilter) elements.catalogSectorFilter.value = '';
      } else if (elements.catalogSectorFilter) {
        elements.catalogSectorFilter.value = topic;
        elements.catalogSectorFilter.dispatchEvent(new Event('change'));
        if (elements.catalogCategoryFilter) elements.catalogCategoryFilter.value = '';
      }

      showToast(`Filter applied: ${topic || 'All Schemes'}`, 'info');
    });
  });
}

/**
 * Voice Recognition & Web Speech API setup
 */
function initVoice() {
  // Populate Language Selector
  if (elements.localeSelect) {
    elements.localeSelect.innerHTML = INDIAN_LOCALES.map(loc => `
      <option value="${loc.code}">${loc.label}</option>
    `).join('');
  }

  // Create Voice Manager
  voiceManager = new VoiceManager({
    defaultLocale: elements.localeSelect ? elements.localeSelect.value : 'hi-IN',
    onTranscriptUpdate: (text, isFinal) => {
      if (elements.transcriptBox) {
        elements.transcriptBox.textContent = text;
      }
    },
    onStateChange: (isRecording, statusMsg) => {
      if (!elements.micBtnContainer || !elements.micStatusText) return;

      if (isRecording) {
        elements.micBtnContainer.classList.add('recording');
        elements.micBtn.setAttribute('aria-pressed', 'true');
        elements.micStatusText.classList.add('active');
        elements.micStatusText.textContent = '🔴 Listening... Speak clearly / बोलिए, सुना जा रहा है...';
      } else {
        elements.micBtnContainer.classList.remove('recording');
        elements.micBtn.setAttribute('aria-pressed', 'false');
        elements.micStatusText.classList.remove('active');
        elements.micStatusText.textContent = 'Click microphone to speak / बोलने के लिए माइक दबाएं';
      }
    },
    onError: (errorMsg) => {
      showToast(errorMsg, 'error');
    }
  });

  // Feature detection banner
  renderBrowserNotice(elements.browserNoticeContainer, voiceManager.isSupported);

  // Locale switcher
  if (elements.localeSelect) {
    elements.localeSelect.addEventListener('change', (e) => {
      voiceManager.setLocale(e.target.value);
      showToast(`Language set to ${e.target.options[e.target.selectedIndex].text}`, 'info');
    });
  }

  // Mic Button Click
  if (elements.micBtn) {
    elements.micBtn.addEventListener('click', () => {
      voiceManager.toggle();
    });
  }

  // Clear Transcript
  if (elements.btnClearTranscript) {
    elements.btnClearTranscript.addEventListener('click', () => {
      voiceManager.clearTranscript();
      if (elements.transcriptBox) {
        elements.transcriptBox.textContent = '';
      }
    });
  }

  // AI Extract Button
  if (elements.btnExtractAi) {
    elements.btnExtractAi.addEventListener('click', async () => {
      await handleExtractTranscript();
    });
  }

  // Sample prompt chips
  elements.sampleChips.forEach(chip => {
    chip.addEventListener('click', async () => {
      const sampleText = chip.getAttribute('data-sample');
      if (sampleText) {
        voiceManager.setTranscript(sampleText);
        showToast('Sample text loaded into speech box.', 'info');
      }
    });
  });
}

/**
 * Handle AI Extraction from Transcript
 */
async function handleExtractTranscript() {
  const text = elements.transcriptBox ? elements.transcriptBox.textContent.trim() : '';
  if (!text) {
    showToast('Please speak into the mic or enter some details in the text box first.', 'error');
    return;
  }

  // Stop recording if active
  if (voiceManager && voiceManager.isRecording) {
    voiceManager.stop();
  }

  const origBtnText = elements.btnExtractAi.innerHTML;
  elements.btnExtractAi.disabled = true;
  elements.btnExtractAi.innerHTML = `
    <div class="loading-spinner" style="width: 16px; height: 16px;"></div>
    <span>Extracting with AI...</span>
  `;

  try {
    const lang = elements.localeSelect ? elements.localeSelect.value : 'hi-IN';
    const result = await extractTranscript(text, lang);

    if (result && result.profile) {
      populateProfileForm(elements.profileForm, result.profile);
      showToast('Details extracted successfully! Please review fields below.', 'success');
      goToWizardStep(2);
    }
  } catch (err) {
    console.error('Extraction error:', err);
    showToast(`Extraction error: ${err.message}`, 'error');
  } finally {
    elements.btnExtractAi.disabled = false;
    elements.btnExtractAi.innerHTML = origBtnText;
  }
}

/**
 * Profile Form Actions & Scheme Matching
 */
function initFormActions() {
  if (!elements.profileForm) return;

  elements.profileForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleFormSubmit();
  });

  if (elements.btnResetForm) {
    elements.btnResetForm.addEventListener('click', () => {
      elements.profileForm.reset();
      showToast('Form reset.', 'info');
    });
  }
}

/**
 * Handle Scheme Matching Submission
 */
async function handleFormSubmit() {
  const profile = getProfileFromForm(elements.profileForm);

  // Transition to Step 3 so results container and loader are immediately visible
  goToWizardStep(3);

  if (elements.resultsPlaceholder) {
    elements.resultsPlaceholder.style.display = 'none';
  }

  elements.resultsContainer.innerHTML = `
    <div class="gov-card">
      <div class="loader-container">
        <div class="loading-spinner dark"></div>
        <div class="loader-text">Evaluating eligibility across Central and State government schemes...</div>
        <p style="font-size: 13px; color: var(--text-muted);">
          Calculating rule-based criteria matches, income caps, and generating personalized guidance.
        </p>
      </div>
    </div>
  `;

  // Scroll to results
  elements.resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

  try {
    const response = await matchSchemes(profile);
    renderSchemeResults(elements.resultsContainer, response);
    showToast(`Found ${response.total_matched} eligible schemes!`, 'success');
  } catch (err) {
    console.error('Matching failure:', err);
    elements.resultsContainer.innerHTML = `
      <div class="gov-card" style="border-left: 5px solid var(--danger);">
        <h4 style="color: var(--danger); font-size: 18px;">Eligibility Evaluation Error</h4>
        <p style="margin-top: 8px;">${err.message}</p>
        <button class="btn btn-secondary btn-sm" style="margin-top: 14px;" onclick="document.getElementById('step-nav-2').click()">
          Review Profile Details
        </button>
      </div>
    `;
    showToast(`Error: ${err.message}`, 'error');
  }
}

/**
 * Catalog Browser Tab
 */
function initCatalog() {
  const loadCatalogSchemes = async () => {
    if (!elements.catalogContainer) return;

    elements.catalogContainer.innerHTML = `
      <div class="loader-container">
        <div class="loading-spinner dark"></div>
        <div class="loader-text">Loading schemes...</div>
      </div>
    `;

    try {
      const filters = {
        sector: elements.catalogSectorFilter ? elements.catalogSectorFilter.value : '',
        category: elements.catalogCategoryFilter ? elements.catalogCategoryFilter.value : '',
        search: elements.catalogSearchInput ? elements.catalogSearchInput.value.trim() : ''
      };

      const schemes = await fetchSchemes(filters);
      renderCatalog(elements.catalogContainer, schemes);
    } catch (err) {
      elements.catalogContainer.innerHTML = `<p style="color: var(--danger);">Failed to load scheme catalog.</p>`;
    }
  };

  // Initial load
  loadCatalogSchemes();

  // Filter change listeners
  if (elements.catalogSectorFilter) {
    elements.catalogSectorFilter.addEventListener('change', loadCatalogSchemes);
  }
  if (elements.catalogCategoryFilter) {
    elements.catalogCategoryFilter.addEventListener('change', loadCatalogSchemes);
  }
  if (elements.catalogSearchInput) {
    let timeout = null;
    elements.catalogSearchInput.addEventListener('input', () => {
      clearTimeout(timeout);
      timeout = setTimeout(loadCatalogSchemes, 300);
    });
  }
}

/**
 * State Discovery Hub Tab
 */
function initStateHub() {
  stateHubManager = new StateHubManager({
    selectElement: elements.stateSelect,
    detailsContainer: elements.stateDetailsContainer
  });
  stateHubManager.init();
}

/**
 * Checks system health and server connectivity
 */
async function checkSystemStatus() {
  const health = await checkHealth();
  const statusEl = document.getElementById('system-status-indicator');
  const statusPill = document.getElementById('system-status-pill');

  if (health.status === 'healthy') {
    if (statusEl) statusEl.style.backgroundColor = '#4CAF50';
    if (statusPill) statusPill.title = `FastAPI Online | Model: ${health.gemini_model || 'Local'}`;
  } else {
    if (statusEl) statusEl.style.backgroundColor = '#FF9800';
  }
}

/**
 * Innovative Feature 1: Interactive Subsidy & Bank EMI Simulator
 */
function initSimulator() {
  const slider = document.getElementById('sim-capital-slider');
  const display = document.getElementById('sim-capital-display');
  const catSelect = document.getElementById('sim-category-select');
  const locSelect = document.getElementById('sim-location-select');
  const secSelect = document.getElementById('sim-sector-select');

  const subsidyPctEl = document.getElementById('sim-subsidy-pct');
  const marginPctEl = document.getElementById('sim-margin-pct');
  const loanPctEl = document.getElementById('sim-loan-pct');

  const barSubsidy = document.getElementById('sim-bar-subsidy');
  const barMargin = document.getElementById('sim-bar-margin');
  const barLoan = document.getElementById('sim-bar-loan');

  const metricSubsidy = document.getElementById('sim-metric-subsidy');
  const metricMargin = document.getElementById('sim-metric-margin');
  const metricLoan = document.getElementById('sim-metric-loan');
  const metricEmi = document.getElementById('sim-metric-emi');

  const btnApply = document.getElementById('btn-sim-apply');

  if (!slider) return;

  const updateSim = () => {
    const capital = parseInt(slider.value, 10) || 1000000;
    const isSpecial = catSelect ? catSelect.value === 'Special' : true;
    const isRural = locSelect ? locSelect.value === 'Rural' : true;

    // Subsidy calculation based on PMEGP rules
    let subsidyPct = 15;
    if (isSpecial) {
      subsidyPct = isRural ? 35 : 25;
    } else {
      subsidyPct = isRural ? 25 : 15;
    }

    const marginPct = isSpecial ? 5 : 10;
    const loanPct = Math.max(0, 100 - (subsidyPct + marginPct));

    const subsidyAmt = Math.round(capital * (subsidyPct / 100));
    const marginAmt = Math.round(capital * (marginPct / 100));
    const loanAmt = Math.round(capital * (loanPct / 100));

    // EMI calculation: 8.5% annual interest, 7-year tenure (84 months)
    const monthlyRate = 0.085 / 12;
    const numMonths = 84;
    const emi = loanAmt > 0
      ? Math.round((loanAmt * monthlyRate * Math.pow(1 + monthlyRate, numMonths)) / (Math.pow(1 + monthlyRate, numMonths) - 1))
      : 0;

    // Update displays
    display.textContent = new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(capital);

    if (subsidyPctEl) subsidyPctEl.textContent = `${subsidyPct}%`;
    if (marginPctEl) marginPctEl.textContent = `${marginPct}%`;
    if (loanPctEl) loanPctEl.textContent = `${loanPct}%`;

    if (barSubsidy) {
      barSubsidy.style.width = `${subsidyPct}%`;
      barSubsidy.textContent = `${subsidyPct}%`;
    }
    if (barMargin) {
      barMargin.style.width = `${marginPct}%`;
      barMargin.textContent = `${marginPct}%`;
    }
    if (barLoan) {
      barLoan.style.width = `${loanPct}%`;
      barLoan.textContent = `${loanPct}%`;
    }

    const formatRupee = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

    if (metricSubsidy) metricSubsidy.textContent = formatRupee(subsidyAmt);
    if (metricMargin) metricMargin.textContent = formatRupee(marginAmt);
    if (metricLoan) metricLoan.textContent = formatRupee(loanAmt);
    if (metricEmi) metricEmi.textContent = formatRupee(emi);
  };

  slider.addEventListener('input', updateSim);
  if (catSelect) catSelect.addEventListener('change', updateSim);
  if (locSelect) locSelect.addEventListener('change', updateSim);
  if (secSelect) secSelect.addEventListener('change', updateSim);

  if (btnApply) {
    btnApply.addEventListener('click', () => {
      const capital = parseInt(slider.value, 10);
      const isSpecial = catSelect ? catSelect.value === 'Special' : true;
      const isRural = locSelect ? locSelect.value === 'Rural' : true;
      const sector = secSelect ? secSelect.value : 'Manufacturing';

      const inputCapital = document.getElementById('input-capital');
      const selectSector = document.getElementById('select-sector');
      const selectCategory = document.getElementById('select-category');
      const selectUrbanRural = document.getElementById('select-urban-rural');

      if (inputCapital) inputCapital.value = capital;
      if (selectSector) selectSector.value = sector;
      if (selectCategory) selectCategory.value = isSpecial ? 'SC' : 'General';
      if (selectUrbanRural) selectUrbanRural.value = isRural ? 'Rural' : 'Urban';

      goToWizardStep(2);
      showToast(`Applied ₹${(capital / 100000).toFixed(1)}L (${sector}) to Profile Form!`, 'success');
    });
  }

  updateSim();
}

/**
 * Innovative Feature 3: Vernacular TTS (Text-to-Speech)
 */
function initTTS() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-tts-listen');
    if (!btn) return;

    if (!('speechSynthesis' in window)) {
      showToast('Text-to-speech not supported in this browser.', 'info');
      return;
    }

    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      document.querySelectorAll('.btn-tts-listen.playing').forEach(b => {
        b.classList.remove('playing');
        b.innerHTML = '<span>🔊 बोलकर सुनें (Listen)</span>';
      });
      if (btn.classList.contains('playing')) return;
    }

    const textToSpeak = decodeURIComponent(btn.dataset.tts || '');
    if (!textToSpeak) return;

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.rate = 0.95;

    // Check for Hindi voices
    const voices = window.speechSynthesis.getVoices();
    const hiVoice = voices.find(v => v.lang && (v.lang.includes('hi') || v.name.includes('Hindi')));
    if (hiVoice) {
      utterance.voice = hiVoice;
      utterance.lang = 'hi-IN';
    }

    btn.classList.add('playing');
    btn.innerHTML = '<span>⏹️ रुकें (Stop)</span>';

    utterance.onend = () => {
      btn.classList.remove('playing');
      btn.innerHTML = '<span>🔊 बोलकर सुनें (Listen)</span>';
    };

    utterance.onerror = () => {
      btn.classList.remove('playing');
      btn.innerHTML = '<span>🔊 बोलकर सुनें (Listen)</span>';
    };

    window.speechSynthesis.speak(utterance);
  });
}

/**
 * Innovative Feature 4: Mobile Continuity QR Modal
 */
function initMobileQRModal() {
  const modal = document.getElementById('npi-qr-modal');
  const btnOpen = document.getElementById('btn-open-qr');
  const btnClose = document.getElementById('btn-close-qr');

  if (btnOpen && modal) {
    btnOpen.addEventListener('click', () => modal.classList.add('active'));
  }

  if (btnClose && modal) {
    btnClose.addEventListener('click', () => modal.classList.remove('active'));
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.remove('active');
    });
  }
}

/**
 * Spotlight Scheme Cards 1-Click Action
 */
function initSpotlightCards() {
  document.querySelectorAll('.spotlight-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const presetKey = btn.dataset.preset;
      const presets = {
        'manufacturing': { age: 32, gender: 'Male', category: 'General', urban_rural: 'Urban', capital: 2500000, sector: 'Manufacturing', education: 'Graduate', is_new_business: true },
        'handicraft': { age: 29, gender: 'Female', category: 'SC', urban_rural: 'Rural', capital: 300000, sector: 'Handicraft/Handloom', education: '10th Pass', is_new_business: true },
        'retail': { age: 26, gender: 'Male', category: 'OBC', urban_rural: 'Urban', capital: 50000, sector: 'Trading', education: '8th Pass', is_new_business: true }
      };

      const preset = presets[presetKey] || presets['manufacturing'];
      populateProfileForm(elements.profileForm, preset);
      goToWizardStep(2);
      showToast(`Loaded ${btn.closest('.spotlight-card').querySelector('.spotlight-title').textContent}!`, 'info');
    });
  });
}

/**
 * Accessible Government Modal System (GIGW 3.0 & WCAG 2.1 AA)
 */
function initModals() {
  const openModal = (modalId) => {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
      const closeBtn = modal.querySelector('[data-close]') || modal.querySelector('.gov-modal-close-icon');
      if (closeBtn) closeBtn.focus();
    }
  };

  const closeModal = (modal) => {
    if (modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }
  };

  // Trigger links (footer & sitemap)
  document.querySelectorAll('.footer-modal-trigger, .sitemap-modal-link').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = trigger.getAttribute('data-modal');
      if (modalId) openModal(modalId);
    });
  });

  // Close buttons with [data-close]
  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = btn.getAttribute('data-close');
      const modal = document.getElementById(modalId) || btn.closest('.gov-modal-backdrop');
      closeModal(modal);
    });
  });

  // Backdrop click to close
  document.querySelectorAll('.gov-modal-backdrop').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
  });

  // ESC key to close any active modal
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const activeModal = document.querySelector('.gov-modal-backdrop.active');
      if (activeModal) closeModal(activeModal);
    }
  });
}

/**
 * Interactive Detailed Sitemap Links Router
 */
function initSitemapLinks() {
  // Footer sitemap link
  const footerSitemapLink = document.getElementById('footer-link-sitemap');
  if (footerSitemapLink) {
    footerSitemapLink.addEventListener('click', (e) => {
      e.preventDefault();
      const sitemapTab = document.getElementById('tab-btn-sitemap');
      if (sitemapTab) {
        sitemapTab.click();
        const sitemapPane = document.getElementById('pane-sitemap');
        if (sitemapPane) sitemapPane.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  // Links inside sitemap grid
  document.querySelectorAll('.sitemap-nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const tabId = link.getAttribute('data-tab');
      if (tabId) {
        const tabBtn = document.getElementById(`tab-btn-${tabId.replace('pane-', '')}`);
        if (tabBtn) tabBtn.click();
      }

      const scrollTarget = link.getAttribute('data-scroll');
      if (scrollTarget) {
        setTimeout(() => {
          const el = document.getElementById(scrollTarget);
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
      }

      const stateTarget = link.getAttribute('data-state');
      if (stateTarget && elements.stateSelect) {
        elements.stateSelect.value = stateTarget;
        elements.stateSelect.dispatchEvent(new Event('change'));
      }

      const filterTarget = link.getAttribute('data-filter');
      if (filterTarget && elements.profileForm) {
        if (['Women', 'SC'].includes(filterTarget) && elements.profileForm.elements['social_category']) {
          elements.profileForm.elements['social_category'].value = filterTarget;
        } else if (elements.profileForm.elements['sector']) {
          elements.profileForm.elements['sector'].value = filterTarget;
        }
        goToWizardStep(2);
        showToast(`Filtered for ${filterTarget} schemes. Verify form below.`, 'info');
      }
    });
  });
}


