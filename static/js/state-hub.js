/**
 * State Discovery Hub Module for Udhyami Yojna
 * Manages state selection, regional cluster exploration, and state schemes
 */
import { fetchStates, fetchStateDetails } from './api.js';
import { renderStateDetails, showToast } from './render.js';

export class StateHubManager {
  constructor(options = {}) {
    this.selectElement = options.selectElement;
    this.detailsContainer = options.detailsContainer;
    this.statesList = [];
    this.currentState = null;
  }

  async init() {
    try {
      this.statesList = await fetchStates();
      this.populateDropdown();
      if (this.statesList.length > 0) {
        // Load default state (e.g. Maharashtra or first state)
        const defaultState = this.statesList.find(s => s.state_code === 'MH') || this.statesList[0];
        this.selectElement.value = defaultState.state_code;
        await this.loadState(defaultState.state_code);
      }
    } catch (err) {
      console.error('Failed to initialize State Hub:', err);
      showToast('Could not load states list. Please refresh.', 'error');
    }

    if (this.selectElement) {
      this.selectElement.addEventListener('change', async (e) => {
        const stateCode = e.target.value;
        if (stateCode) {
          await this.loadState(stateCode);
        }
      });
    }

    // Regional Filter Buttons Setup
    const regionalBtns = document.querySelectorAll('.regional-filter-btn');
    regionalBtns.forEach(btn => {
      btn.addEventListener('click', async () => {
        regionalBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const region = btn.getAttribute('data-region') || 'All';
        this.filterByRegion(region);
      });
    });
  }

  filterByRegion(region) {
    if (!this.selectElement) return;

    let filtered = this.statesList;
    if (region && region !== 'All') {
      filtered = this.statesList.filter(s => s.region && s.region.toLowerCase() === region.toLowerCase());
    }

    this.selectElement.innerHTML = filtered.map(st => `
      <option value="${st.state_code}">
        ${st.name} ${st.name_hi ? `(${st.name_hi})` : ''} - [${st.region} India]
      </option>
    `).join('');

    if (filtered.length > 0) {
      this.selectElement.value = filtered[0].state_code;
      this.loadState(filtered[0].state_code);
    }
  }

  populateDropdown() {
    if (!this.selectElement) return;

    this.selectElement.innerHTML = this.statesList.map(st => `
      <option value="${st.state_code}">
        ${st.name} ${st.name_hi ? `(${st.name_hi})` : ''} - [${st.region} India]
      </option>
    `).join('');
  }

  async loadState(stateCode) {
    if (!this.detailsContainer) return;

    this.detailsContainer.innerHTML = `
      <div class="loader-container">
        <div class="loading-spinner dark"></div>
        <div class="loader-text">Loading ${stateCode} entrepreneurial ecosystem data...</div>
      </div>
    `;

    try {
      const stateData = await fetchStateDetails(stateCode);
      this.currentState = stateData;
      renderStateDetails(this.detailsContainer, stateData);
    } catch (err) {
      console.error(`Error loading state ${stateCode}:`, err);
      this.detailsContainer.innerHTML = `
        <div class="gov-card">
          <p style="color: var(--danger);">Failed to load state details for ${stateCode}. Please try again.</p>
        </div>
      `;
    }
  }
}
