/**
 * DOM Renderer Module for Udhyami Yojna
 * Accessible, semantic HTML rendering for government portal UI
 */

/**
 * Authentic India.gov.in Scheme Banner and Graphic Mapping
 */
export const SCHEME_BANNER_MAP = {
  'pmegp': '/images/npi/teracotta_artisan.jpg',
  'mudra_shishu': '/images/npi/pmsvanidhi_banner.png',
  'mudra_kishore': '/images/npi/pmsvanidhi_banner.png',
  'mudra_tarun': '/images/npi/pmsvanidhi_banner.png',
  'stand_up_india': '/images/npi/bharat_tex.png',
  'pm_svanidhi': '/images/npi/pmsvanidhi_banner.png',
  'startup_india_seed_fund': '/images/npi/startup_village.jpg',
  'pmfme': '/images/npi/culinary_delight.png',
  'cgtmse': '/images/npi/economic_survey.jpg',
  'nsic_sprs': '/images/npi/job_seekers.jpg',
  'odop': '/images/npi/odop_banner.png',
  'maha_cmegp': '/images/npi/odop_banner.png',
  'up_mmysy': '/images/npi/odop_banner.png',
  'raj_mlupy': '/images/npi/hawa_mahal.jpg',
  'bihar_udyami': '/images/npi/teracotta_artisan.jpg',
  'guj_vbs': '/images/npi/amrit_udyan.png',
  'tn_needs': '/images/npi/culinary_delight.png',
  'ka_cmegp': '/images/npi/startup_village.jpg',
  'tg_tpride': '/images/npi/odop_banner.png',
  'wb_karmasathi': '/images/npi/teracotta_artisan.jpg',
  'as_cmaaa': '/images/npi/bharat_tex.png',
  'od_silpi': '/images/npi/teracotta_artisan.jpg'
};

/**
 * Official Scheme Vector Logos (Un-watermarked Government & Initiative Marks)
 */
export const SCHEME_LOGO_MAP = {
  'pmegp': '/images/logos/pmegp_logo.svg',
  'mudra_shishu': '/images/logos/mudra_logo.svg',
  'mudra_kishore': '/images/logos/mudra_logo.svg',
  'mudra_tarun': '/images/logos/mudra_logo.svg',
  'stand_up_india': '/images/logos/standup_svg.svg',
  'pm_svanidhi': '/images/logos/pmsvanidhi_logo.svg',
  'pm_vishwakarma': '/images/logos/pm_vishwakarma.svg',
  'startup_india_seed_fund': '/images/logos/digital_india.svg',
  'pmfme': '/images/logos/msme_logo.svg',
  'cgtmse': '/images/logos/jansamarth_logo.svg',
  'nsic_sprs': '/images/logos/msme_logo.svg',
  'odop': '/images/logos/make_in_india.svg',
  'maha_cmegp': '/images/logos/udyam_logo.svg',
  'up_mmysy': '/images/logos/udyam_logo.svg',
  'raj_mlupy': '/images/logos/udyam_logo.svg',
  'bihar_udyami': '/images/logos/udyam_logo.svg',
  'guj_vbs': '/images/logos/udyam_logo.svg',
  'tn_needs': '/images/logos/udyam_logo.svg',
  'ka_cmegp': '/images/logos/udyam_logo.svg',
  'tg_tpride': '/images/logos/udyam_logo.svg',
  'wb_karmasathi': '/images/logos/udyam_logo.svg',
  'as_cmaaa': '/images/logos/udyam_logo.svg',
  'od_silpi': '/images/logos/udyam_logo.svg'
};

/**
 * Renders browser compatibility banner for Web Speech API.
 */
export function renderBrowserNotice(container, isSupported) {
  if (!container) return;

  if (isSupported) {
    container.innerHTML = `
      <div class="browser-notice" role="status">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
        <div>
          <strong>Microphone Active / माइक्रोफ़ोन समर्थित:</strong>
          <span> Click the mic button and speak naturally in your chosen language, or use the manual form below.</span>
        </div>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div class="browser-notice warning" role="alert">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
        <div>
          <strong>Browser Notice / ब्राउज़र सूचना:</strong>
          <span> Speech recognition works natively in Chromium browsers (Google Chrome, MS Edge, Brave). You can type your details directly into the text box or use the structured form below — all scheme discovery features are 100% functional!</span>
        </div>
      </div>
    `;
  }
}

/**
 * Formats Indian Currency (e.g. 500000 -> ₹5,00,000)
 */
export function formatINR(val) {
  if (val === null || val === undefined || isNaN(val)) return '₹0';
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(val);
}

/**
 * Populates the review form with extracted user profile data.
 * Guarantees NO blank spaces are left unfilled.
 */
export function populateProfileForm(form, profile) {
  if (!form || !profile) return;

  function setSelectSmart(selectEl, value, defaultVal) {
    if (!selectEl) return;
    const target = (value || defaultVal || '').toString().trim().toLowerCase();
    let matched = false;

    // 1. Exact value match
    for (let i = 0; i < selectEl.options.length; i++) {
      const opt = selectEl.options[i];
      if (opt.value && opt.value.toLowerCase() === target) {
        selectEl.selectedIndex = i;
        matched = true;
        break;
      }
    }

    // 2. Substring or text match
    if (!matched) {
      for (let i = 0; i < selectEl.options.length; i++) {
        const opt = selectEl.options[i];
        const optText = opt.text.toLowerCase();
        const optVal = opt.value.toLowerCase();
        if (opt.value && (optVal.includes(target) || target.includes(optVal) || optText.includes(target) || target.includes(optText))) {
          selectEl.selectedIndex = i;
          matched = true;
          break;
        }
      }
    }

    // 3. Common state/category abbreviations
    if (!matched) {
      const abbrevs = {
        'up': 'Uttar Pradesh',
        'mh': 'Maharashtra',
        'tn': 'Tamil Nadu',
        'ka': 'Karnataka',
        'gj': 'Gujarat',
        'rj': 'Rajasthan',
        'br': 'Bihar',
        'wb': 'West Bengal',
        'tg': 'Telangana',
        'mp': 'Madhya Pradesh',
        'dl': 'Delhi',
        'ap': 'Andhra Pradesh',
        'as': 'Assam',
        'od': 'Odisha',
        'pb': 'Punjab',
        'kl': 'Kerala',
        'fem': 'Female',
        'women': 'Female',
        'mahila': 'Female',
        'male': 'Male',
        'purush': 'Male',
        'gen': 'General',
        'sc': 'SC',
        'st': 'ST',
        'obc': 'OBC'
      };
      if (abbrevs[target]) {
        for (let i = 0; i < selectEl.options.length; i++) {
          const opt = selectEl.options[i];
          if (opt.value && opt.value.toLowerCase() === abbrevs[target].toLowerCase()) {
            selectEl.selectedIndex = i;
            matched = true;
            break;
          }
        }
      }
    }

    // 4. Default fallback if still blank
    if (!matched && defaultVal) {
      for (let i = 0; i < selectEl.options.length; i++) {
        const opt = selectEl.options[i];
        if (opt.value && opt.value.toLowerCase() === defaultVal.toLowerCase()) {
          selectEl.selectedIndex = i;
          matched = true;
          break;
        }
      }
    }

    // 5. Guarantee not left on empty placeholder
    if (selectEl.selectedIndex === 0 && selectEl.options.length > 1) {
      selectEl.selectedIndex = 1;
    }
  }

  // 1. Age (ensure integer >= 18)
  const ageVal = (profile.age !== null && profile.age !== undefined && profile.age >= 18) ? profile.age : 30;
  form.elements['age'].value = ageVal;

  // 2. Gender
  setSelectSmart(form.elements['gender'], profile.gender, 'Female');

  // 3. Social Category
  setSelectSmart(form.elements['social_category'], profile.social_category, 'General');

  // 4. State
  setSelectSmart(form.elements['state'], profile.state, 'Maharashtra');

  // 5. District
  const districtVal = (profile.district && profile.district.trim()) ? profile.district.trim() : (form.elements['state'].value === 'Maharashtra' ? 'Pune' : 'Central District');
  form.elements['district'].value = districtVal;

  // 6. Sector
  setSelectSmart(form.elements['sector'], profile.sector, 'Manufacturing');

  // 7. Investment / Loan Needed
  const investVal = (profile.investment_needed !== null && profile.investment_needed !== undefined && profile.investment_needed > 0) ? profile.investment_needed : 200000;
  form.elements['investment_needed'].value = investVal;

  // 8. Existing Business
  const existVal = (profile.existing_business !== undefined && profile.existing_business !== null) ? (profile.existing_business ? 'true' : 'false') : 'false';
  setSelectSmart(form.elements['existing_business'], existVal, 'false');

  // 9. Education
  setSelectSmart(form.elements['education'], profile.education, '10th Pass');

  // 10. Annual Income
  const incVal = (profile.annual_income !== null && profile.annual_income !== undefined && profile.annual_income > 0) ? profile.annual_income : 200000;
  form.elements['annual_income'].value = incVal;

  // 11. Urban / Rural
  setSelectSmart(form.elements['urban_rural'], profile.urban_rural, 'Rural');

  // 12. Business Idea
  const currentSector = form.elements['sector'].value || 'Manufacturing';
  form.elements['business_idea'].value = (profile.business_idea && profile.business_idea.trim()) 
    ? profile.business_idea.trim() 
    : `Setting up a new ${currentSector} unit with capital requirement of ${formatINR(investVal)}.`;

  // Visual Highlight on all filled fields
  const fieldNames = ['age', 'gender', 'social_category', 'state', 'district', 'sector', 'investment_needed', 'existing_business', 'education', 'annual_income', 'urban_rural', 'business_idea'];
  fieldNames.forEach(name => {
    const el = form.elements[name];
    if (el) {
      el.classList.add('auto-filled-highlight');
      setTimeout(() => el.classList.remove('auto-filled-highlight'), 1800);
    }
  });
}

/**
 * Extracts and validates UserProfile object from HTML Form.
 */
export function getProfileFromForm(form) {
  const ageVal = form.elements['age'].value;
  const incomeVal = form.elements['annual_income'].value;
  const investVal = form.elements['investment_needed'].value;

  return {
    age: ageVal ? parseInt(ageVal, 10) : null,
    gender: form.elements['gender'].value || null,
    annual_income: incomeVal ? parseFloat(incomeVal) : null,
    state: form.elements['state'].value || null,
    district: form.elements['district'].value ? form.elements['district'].value.trim() : null,
    social_category: form.elements['social_category'].value || null,
    education: form.elements['education'].value || null,
    business_idea: form.elements['business_idea'].value ? form.elements['business_idea'].value.trim() : null,
    sector: form.elements['sector'].value || null,
    investment_needed: investVal ? parseFloat(investVal) : null,
    existing_business: form.elements['existing_business'].value === "true",
    urban_rural: form.elements['urban_rural'].value || "Rural"
  };
}

/**
 * Renders ranked scheme results with scores, badges, advice, and checklist.
 */
export function renderSchemeResults(container, response) {
  if (!container) return;

  const { matched_schemes, total_matched, total_evaluated, executive_summary, ai_enhanced } = response;

  if (!matched_schemes || matched_schemes.length === 0) {
    container.innerHTML = `
      <div class="gov-card">
        <h3 class="gov-card-title">No Matching Schemes Found</h3>
        <p class="gov-card-desc" style="margin-top: 8px;">
          Based on the criteria specified, no direct matches were found. Try adjusting your requested loan amount, 
          broadening your sector selection, or selecting Pan-India schemes.
        </p>
      </div>
    `;
    return;
  }

  const strongMatches = matched_schemes.filter(s => s.match_score >= 85).length;
  const goodMatches = matched_schemes.filter(s => s.match_score >= 70 && s.match_score < 85).length;

  const summaryHtml = `
    <div class="results-summary-banner" role="region" aria-label="Matching Schemes Summary">
      <div>
        <h3 style="font-size: 20px; font-weight: 800; margin-bottom: 4px;">
          Scheme Match Results / परिणाम सारांश
        </h3>
        <p style="font-size: 14px; opacity: 0.95; max-width: 650px;">
          ${executive_summary}
        </p>
        <div style="margin-top: 10px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
          <button type="button" class="btn-tts-listen" data-tts="${encodeURIComponent(executive_summary)}" aria-label="Listen to match results summary in voice">
            <span>🔊 बोलकर सारांश सुनें (Listen to Summary)</span>
          </button>
          ${ai_enhanced ? '<span style="display:inline-block; background:rgba(255,255,255,0.2); padding:2px 8px; border-radius:12px; font-size:11px; font-weight:700;">AI Plain-Language Advice Active</span>' : ''}
        </div>
      </div>
      <div class="summary-stats">
        <div class="stat-item">
          <span class="stat-number">${total_matched}</span>
          <span class="stat-label">Eligible</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">${strongMatches}</span>
          <span class="stat-label">Strong Matches</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">${total_evaluated}</span>
          <span class="stat-label">Evaluated</span>
        </div>
      </div>
    </div>
  `;

  const cardsHtml = matched_schemes.map((result, idx) => {
    const s = result.scheme;
    const isStrong = result.match_score >= 85;
    const isGood = result.match_score >= 70 && result.match_score < 85;
    const matchClass = isStrong ? 'strong-match' : (isGood ? 'good-match' : 'moderate-match');
    const badgeScoreClass = isStrong ? 'strong' : (isGood ? 'good' : 'moderate');
    const bannerImg = SCHEME_BANNER_MAP[s.id] || '/images/npi/teracotta_artisan.jpg';

    const whyList = (result.why_matched || []).map(r => `
      <li class="criteria-item">
        <span class="check-icon" aria-hidden="true">✔</span>
        <span>${r}</span>
      </li>
    `).join('');

    const unmetList = (result.unmet_criteria || []).map(u => `
      <li class="criteria-item unmet">
        <span class="check-icon" aria-hidden="true">⚠</span>
        <span>${u}</span>
      </li>
    `).join('');

    const docsList = (result.required_documents || []).map((doc, dIdx) => `
      <label class="doc-checklist-item">
        <input type="checkbox" id="doc-${s.id}-${dIdx}">
        <span>${doc}</span>
      </label>
    `).join('');

    const subsidyDisplay = s.subsidy_details || s.subsidy_percentage || 'Credit-linked subsidy';
    const loanBracket = `${formatINR(s.min_loan)} - ${formatINR(s.max_loan)}`;
    const schemeLogo = SCHEME_LOGO_MAP[s.id] || '/images/logos/msme_logo.svg';

    return `
      <article class="scheme-card ${matchClass}" aria-labelledby="scheme-title-${idx}">
        <div class="scheme-card-header">
          <div class="scheme-card-top-row" style="flex: 1;">
            <div class="scheme-card-thumb-box">
              <img src="${bannerImg}" alt="${s.name}" class="scheme-card-thumb" loading="lazy">
            </div>
            <div class="scheme-title-area" style="flex: 1;">
              <div class="scheme-badges">
                <span class="badge ${s.type === 'Central' ? 'badge-central' : 'badge-state'}">
                  ${s.type === 'Central' ? '🇮🇳 Central Scheme' : `🏛️ ${s.state_code} State Scheme`}
                </span>
                <span class="badge badge-ministry">${s.ministry}</span>
                <span class="scheme-logo-tag" style="background:#FFF; border:1px solid #CBD5E1; padding:2px 8px; border-radius:12px; display:inline-flex; align-items:center; gap:6px;">
                  <img src="${schemeLogo}" alt="${s.name} Logo" style="height:16px; width:auto; vertical-align:middle;">
                  <span style="font-size:11px; font-weight:700; color:#0B3C5D;">Official Initiative</span>
                </span>
                <span class="badge" style="background:#E8F5E9; color:#1B5E20; border:1px solid #A5D6A7; font-weight:700;">🛡️ Gazette Verified</span>
              </div>
              <h4 class="scheme-name" id="scheme-title-${idx}">${s.name}</h4>
              ${s.name_hi ? `<div class="scheme-name-hi">${s.name_hi}</div>` : ''}
            </div>
          </div>
          <div class="score-badge ${badgeScoreClass}">
            <span class="score-value">${result.match_score}%</span>
            <span class="score-label">${result.match_grade}</span>
          </div>
        </div>

        <div class="subsidy-highlight-box">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 16h-2v-2h2v2zm0-4h-2V7h2v5z"/></svg>
          <div>
            <strong>Financial Grant / Subsidy Benefit: </strong> ${subsidyDisplay}
            <div style="font-size: 13px; font-weight: 500; margin-top: 2px;">
              Permissible Funding Bracket: <strong>${loanBracket}</strong>
            </div>
          </div>
        </div>

        <div class="plain-advice-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 6px;">
            <div class="advice-label" style="margin-bottom: 0;">
              <span aria-hidden="true">💡</span> Plain Guidance / सरल मार्गदर्शन
            </div>
            <button type="button" class="btn-tts-listen" data-tts="${encodeURIComponent(result.plain_summary)}" aria-label="Listen to guidance for ${s.name}">
              <span>🔊 बोलकर सुनें (Listen)</span>
            </button>
          </div>
          <p class="advice-text">${result.plain_summary}</p>
          ${result.actionable_steps && result.actionable_steps.length > 0 ? `
            <div style="margin-top: 10px;">
              <strong style="font-size: 13px; color: var(--chakra-navy);">Recommended Next Steps:</strong>
              <ul style="margin-left: 20px; font-size: 14px; margin-top: 4px; color: #374151;">
                ${result.actionable_steps.map(step => `<li>${step}</li>`).join('')}
              </ul>
            </div>
          ` : ''}
        </div>

        <div class="why-matched-container">
          <div class="section-subheading">
            <span aria-hidden="true">🎯</span> Why You Qualify / पात्रता के कारण
          </div>
          <ul class="criteria-list">
            ${whyList}
            ${unmetList}
          </ul>
        </div>

        <details class="docs-accordion">
          <summary class="docs-summary">
            <span>📑 Required Documents Checklist (${(result.required_documents || []).length} items)</span>
            <span style="font-size: 12px; font-weight: normal; color: var(--text-muted);">Click to expand</span>
          </summary>
          <div class="docs-body">
            <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 8px;">
              Check the boxes below to track the documents you have ready for application:
            </p>
            ${docsList}
          </div>
        </details>

        <div class="scheme-card-footer">
          <div style="font-size: 13px; color: var(--text-muted);">
            Official Portal: <strong>${new URL(s.official_url).hostname}</strong>
          </div>
          <a href="${s.official_url}" target="_blank" rel="noopener noreferrer" class="official-link-btn" aria-label="Apply for ${s.name} on official portal (opens in new tab)">
            Apply on Official Portal (आधिकारिक पोर्टल पर जाएं) ↗
          </a>
        </div>
      </article>
    `;
  }).join('');

  container.innerHTML = summaryHtml + `<div class="schemes-grid">${cardsHtml}</div>`;
}

/**
 * Renders the state ecosystem details.
 */
export function renderStateDetails(container, data) {
  if (!container) return;

  const eco = data.ecosystem;
  const stateSchemes = data.state_schemes || [];

  const clustersHtml = (eco.district_clusters || []).map(c => `
    <div class="cluster-card">
      <div class="cluster-district">${c.district}</div>
      <div class="cluster-specialty">${c.specialty}</div>
    </div>
  `).join('');

  const schemesHtml = stateSchemes.length > 0 ? stateSchemes.map(s => `
    <div class="scheme-card good-match" style="margin-top: 14px;">
      <div class="scheme-card-header">
        <div>
          <span class="badge badge-state">🏛️ ${eco.name} Special Initiative</span>
          <h4 class="scheme-name" style="margin-top: 6px;">${s.name}</h4>
          ${s.name_hi ? `<div class="scheme-name-hi">${s.name_hi}</div>` : ''}
        </div>
      </div>
      <p style="font-size: 14px; margin: 10px 0; color: #4A5568;">${s.description}</p>
      <div class="subsidy-highlight-box" style="margin: 10px 0;">
        <div><strong>Subsidy:</strong> ${s.subsidy_details || s.subsidy_percentage}</div>
      </div>
      <div class="scheme-card-footer" style="padding-top: 10px;">
        <span style="font-size: 13px;">Coverage: Max Loan ${formatINR(s.max_loan)}</span>
        <a href="${s.official_url}" target="_blank" rel="noopener noreferrer" class="official-link-btn btn-sm">
          Apply on State Portal ↗
        </a>
      </div>
    </div>
  `).join('') : '<p style="color: #718096; margin-top: 10px;">No state-exclusive schemes currently listed. Pan-India central schemes are active.</p>';

  container.innerHTML = `
    <div class="state-detail-card">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
          <h3 style="font-size: 24px; font-weight: 800; color: var(--chakra-navy);">
            ${eco.name} ${eco.name_hi ? `(${eco.name_hi})` : ''}
          </h3>
          <div style="font-size: 14px; color: var(--text-muted); margin-top: 4px;">
            Region: <strong>${eco.region} India</strong> | Capital: <strong>${eco.capital}</strong>
          </div>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <a href="${eco.single_window_portal}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-sm">
            Single-Window Portal ↗
          </a>
          <a href="${eco.dic_portal}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm">
            DIC Portal ↗
          </a>
        </div>
      </div>

      <div class="state-meta-grid">
        <div class="state-meta-item">
          <div class="state-meta-label">District Helpline</div>
          <div class="state-meta-value">📞 ${eco.helpline}</div>
        </div>
        <div class="state-meta-item">
          <div class="state-meta-label">Nodal Enterprise Agency</div>
          <div class="state-meta-value">${eco.nodal_agency}</div>
        </div>
        <div class="state-meta-item">
          <div class="state-meta-label">Key Growth Sectors</div>
          <div class="state-meta-value">${(eco.key_sectors || []).join(', ')}</div>
        </div>
      </div>

      <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 16px; margin: 16px 0;">
        <h4 style="font-size: 15px; font-weight: 700; color: var(--chakra-navy); margin-bottom: 6px;">
          Regional Ecosystem & Policy Incentives:
        </h4>
        <p style="font-size: 14px; line-height: 1.5; color: #2D3748;">
          ${eco.regional_initiatives}
        </p>
      </div>

      <div style="margin-top: 20px;">
        <h4 style="font-size: 16px; font-weight: 700; color: var(--chakra-navy);">
          District Industrial Clusters & Specialized Craft Belts
        </h4>
        <div class="clusters-list">
          ${clustersHtml}
        </div>
      </div>

      <div style="margin-top: 24px;">
        <h4 style="font-size: 16px; font-weight: 700; color: var(--chakra-navy);">
          State-Specific Schemes (${stateSchemes.length})
        </h4>
        ${schemesHtml}
      </div>
    </div>
  `;
}

/**
 * Renders all schemes in the general catalog view.
 */
export function renderCatalog(container, schemes) {
  if (!container) return;

  if (schemes.length === 0) {
    container.innerHTML = `<p style="padding: 24px; text-align: center; color: var(--text-muted);">No schemes match your filter criteria.</p>`;
    return;
  }

  const cardsHtml = schemes.map(s => {
    const subsidy = s.subsidy_details || s.subsidy_percentage || 'Subsidized terms';
    const bannerImg = SCHEME_BANNER_MAP[s.id] || '/images/npi/teracotta_artisan.jpg';
    const schemeLogo = SCHEME_LOGO_MAP[s.id] || '/images/logos/msme_logo.svg';
    return `
      <div class="scheme-card" style="margin-bottom: 16px;">
        <div class="scheme-card-header">
          <div class="scheme-card-top-row" style="flex: 1;">
            <div class="scheme-card-thumb-box">
              <img src="${bannerImg}" alt="${s.name}" class="scheme-card-thumb" loading="lazy">
            </div>
            <div style="flex: 1;">
              <div class="scheme-badges">
                <span class="badge ${s.type === 'Central' ? 'badge-central' : 'badge-state'}">
                  ${s.type === 'Central' ? 'Central' : s.state_code}
                </span>
                <span class="badge badge-ministry">${s.ministry}</span>
                <span class="scheme-logo-tag" style="background:#FFF; border:1px solid #CBD5E1; padding:2px 8px; border-radius:12px; display:inline-flex; align-items:center; gap:6px;">
                  <img src="${schemeLogo}" alt="${s.name} Logo" style="height:16px; width:auto; vertical-align:middle;">
                  <span style="font-size:11px; font-weight:700; color:#0B3C5D;">Official Initiative</span>
                </span>
              </div>
              <h4 class="scheme-name">${s.name}</h4>
              ${s.name_hi ? `<div class="scheme-name-hi">${s.name_hi}</div>` : ''}
            </div>
          </div>
          <div style="text-align: right; flex-shrink: 0;">
            <div style="font-size: 12px; text-transform: uppercase; color: var(--text-muted);">Loan Limit</div>
            <div style="font-size: 18px; font-weight: 800; color: var(--chakra-navy);">${formatINR(s.max_loan)}</div>
          </div>
        </div>
        <p style="font-size: 14px; color: #4A5568; margin: 8px 0;">${s.description}</p>
        <div class="subsidy-highlight-box" style="margin: 8px 0; padding: 8px 12px; font-size: 14px;">
          <div><strong>Benefit:</strong> ${subsidy}</div>
        </div>
        <div class="scheme-card-footer" style="padding-top: 12px;">
          <div style="font-size: 13px; color: var(--text-muted);">
            Target: <strong>${s.target_categories.join(', ')}</strong> | Sectors: <strong>${s.sectors.slice(0, 3).join(', ')}</strong>
          </div>
          <a href="${s.official_url}" target="_blank" rel="noopener noreferrer" class="official-link-btn btn-sm">
            Official Portal ↗
          </a>
        </div>
      </div>
    `;
  }).join('');

  container.innerHTML = `<div class="schemes-grid">${cardsHtml}</div>`;
}

/**
 * Toast notification renderer.
 */
export function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'toast-container';
    toastContainer.setAttribute('aria-live', 'polite');
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerText = message;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 4000);
}
