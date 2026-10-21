/**
 * AI Subscription Hub - Client Controller
 * Handles live state, control center actions, routing, and UI rendering.
 */

let state = null;
let routerDraft = null;
let currentTab = 'home';
const TAB_PATHS = { home: '/', apps: '/my-apps', chatbots: '/my-chatbots', providers: '/llm-providers', router: '/router', activity: '/activity' };
const tabFromPath = path => Object.keys(TAB_PATHS).find(tab => TAB_PATHS[tab] === path) || 'home';
let selectedProvider = null;
let selectedApp = null;
let addAppWizard = null; // {type, preset} being connected, or null

const $ = id => document.getElementById(id);

function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

function tell(message, isError = false) {
  const toast = $('bridge-toast');
  if (!toast) return;
  if (!message) {
    toast.hidden = true;
    toast.textContent = '';
    return;
  }
  toast.textContent = message;
  toast.className = 'b-toast' + (isError ? ' b-toast-error' : '');
  toast.hidden = false;
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.hidden = true;
  }, 5000);
}

async function post(path, data = {}) {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(result.error || `HTTP ${response.status} failed`);
  }
  return result;
}

// Preference management
function loadPreferences() {
  const advanced = localStorage.getItem('hub-advanced') === 'true';
  const theme = localStorage.getItem('hub-theme') || 'auto';
  const savedTab = tabFromPath(location.pathname);
  
  const advToggle = $('bridge-advanced');
  if (advToggle) advToggle.checked = advanced;
  applyTheme(theme);
  
  if (!advanced && ['router', 'activity'].includes(savedTab)) {
    currentTab = 'home';
  } else {
    currentTab = savedTab;
  }
}

function applyTheme(theme) {
  document.documentElement.style.removeProperty('color-scheme');
  if (theme === 'dark' || theme === 'light') {
    document.documentElement.style.colorScheme = theme;
  }
  localStorage.setItem('hub-theme', theme);
  syncThemePresentation(theme);
}

function syncThemePresentation(theme) {
  const isDark = theme === 'dark' || (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
  const button = $('bridge-theme');
  if (button) {
    const label = `Switch to ${isDark ? 'light' : 'dark'} mode`;
    button.setAttribute('aria-label', label);
    button.title = label;
  }
  document.documentElement.dataset.mode = isDark ? 'dark' : 'light';
  document.querySelector('meta[name="theme-color"]').content = isDark ? '#1d202a' : '#ffffff';
}

function toggleTheme() {
  const current = localStorage.getItem('hub-theme') || 'auto';
  const isDark = current === 'dark' || (current === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
  const next = isDark ? 'light' : 'dark';
  applyTheme(next);
  tell(`Theme switched to ${next} mode.`);
}

const isChatbot = a => a.category === 'chatbot' || a.type === 'chatbot' || (a.type && a.type.toLowerCase().includes('agent'));

function switchTab(tab, push = true) {
  currentTab = tab;
  if (location.pathname !== TAB_PATHS[tab]) history[push ? 'pushState' : 'replaceState'](null, '', TAB_PATHS[tab]);
  selectedProvider = null;
  selectedApp = null;
  addAppWizard = null;
  
  document.querySelectorAll('#bridge-nav button').forEach(btn => {
    btn.setAttribute('aria-current', btn.dataset.tab === tab ? 'page' : 'false');
  });

  document.querySelectorAll('.b-page').forEach(page => {
    page.hidden = page.id !== `page-${tab}`;
  });

  render();
}

const PROVIDER_METADATA = {
  claude: { name: 'Claude (Claude Code)', initial: 'Cl' },
  codex: { name: 'ChatGPT (Codex)', initial: 'Ch' },
  agy: { name: 'Gemini (Antigravity)', initial: 'Ge' },
  grok: { name: 'Grok(Build)', initial: 'Gr' }
};

function getProviderMeta(rawName) {
  const key = String(rawName || '').toLowerCase().trim();
  return PROVIDER_METADATA[key] || {
    name: rawName,
    initial: (rawName || 'P').slice(0, 2).toUpperCase()
  };
}

// Shortest window first: session / 5h, then daily, weekly, monthly; unknown names keep their order.
function periodRank(name) {
  const n = String(name).toLowerCase();
  if (/session|\d\s*h(ou)?r?s?(\b|_|$)|hour/.test(n)) return 0;
  if (/day|daily/.test(n)) return 1;
  if (/week/.test(n)) return 2;
  if (/month/.test(n)) return 3;
  return 4;
}

function quotaEntries(limits = {}) {
  return Object.entries(limits)
    .filter(([, v]) => v && typeof v.remaining_pct === 'number')
    .sort(([a], [b]) => periodRank(a) - periodRank(b));
}

function getProviderHeadroom(provider) {
  const entries = quotaEntries(provider.limits);
  if (!entries.length) return -1;
  return Math.min(...entries.map(([, v]) => v.remaining_pct));
}

function accountState(p, headroom) {
  if (p.status === 'login_required' || (!p.running && p.reason?.toLowerCase().includes('login'))) {
    return ['Login needed', 'b-warn'];
  }
  if (!p.running) {
    return ['Stopped', 'b-neutral'];
  }
  // headroom < 0 means no quota data yet (see getProviderHeadroom)
  if (headroom < 0) {
    return ['Unknown', 'b-neutral'];
  }
  if (headroom === 0) {
    return ['Quota depleted', 'b-depleted'];
  }
  if (headroom >= 0 && headroom < 20) {
    return ['Running low', 'b-warn'];
  }
  return ['Connected', ''];
}

function statusClass(status) {
  if (status === 'running') return '';
  if (status === 'failed' || status === 'unreachable') return 'b-depleted';
  if (status === 'starting' || status === 'login_required') return 'b-warn';
  return 'b-neutral';
}

function statusLabel(status, running) {
  const labels = {running: 'Running', failed: 'Failed', unreachable: 'Unreachable',
                  starting: 'Starting', login_required: 'Login needed'};
  return labels[status] || (running ? 'Running' : 'Stopped');
}

// ----------------- LOG VIEWER -----------------

let logTimer = null;

function closeLogViewer() {
  clearInterval(logTimer);
  logTimer = null;
  $('log-viewer')?.remove();
}

function logLineClass(line) {
  if (/\b(FAIL|ERROR|Traceback|EXIT [1-9])/.test(line)) return 'b-log-err';
  if (/\bWARN/.test(line)) return 'b-log-warn';
  return '';
}

async function refreshLogViewer(name) {
  const body = $('log-viewer-body');
  if (!body) return;
  try {
    const response = await fetch(`/api/logs?name=${encodeURIComponent(name)}&lines=300`, {cache: 'no-store'});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
    const atBottom = body.scrollTop + body.clientHeight >= body.scrollHeight - 24;
    body.innerHTML = data.lines.length
      ? data.lines.map(l => `<div class="${logLineClass(l)}">${esc(l)}</div>`).join('')
      : '<div class="b-sub">No log output yet.</div>';
    if (atBottom) body.scrollTop = body.scrollHeight;
  } catch (error) {
    body.innerHTML = `<div class="b-log-err">${esc(error.message)}</div>`;
  }
}

function openLogViewer(name) {
  closeLogViewer();
  const overlay = document.createElement('div');
  overlay.id = 'log-viewer';
  overlay.className = 'b-log-overlay';
  overlay.innerHTML = `
    <div class="b-log-panel" role="dialog" aria-label="Log viewer">
      <div class="b-between">
        <strong>${esc(name === 'router' ? 'Router' : getProviderMeta(name).name)} log</strong>
        <button type="button" class="b-button" onclick="closeLogViewer()">Close</button>
      </div>
      <div id="log-viewer-body" class="b-log-body"></div>
    </div>`;
  overlay.addEventListener('click', e => { if (e.target === overlay) closeLogViewer(); });
  document.body.appendChild(overlay);
  refreshLogViewer(name).then(() => { const b = $('log-viewer-body'); if (b) b.scrollTop = b.scrollHeight; });
  logTimer = setInterval(() => refreshLogViewer(name), 3000);
}

// ----------------- RENDER FUNCTIONS -----------------

function render() {
  if (!state) return;
  renderServiceStatus();
  
  switch (currentTab) {
    case 'home':
      renderHome();
      break;
    case 'apps':
    case 'chatbots':
      renderApps();
      break;
    case 'providers':
      renderProviders();
      break;
    case 'router':
      renderRouter();
      break;
    case 'activity':
      renderActivity();
      break;
  }
}

function renderServiceStatus() {
  const total = (state.providers || []).length;
  const runningCount = (state.providers || []).filter(p => p.running).length;
  const stoppedNames = (state.providers || []).filter(p => !p.running).map(p => getProviderMeta(p.name).name).join(', ');
  const routerOn = !!state.router_running;
  const fullyReady = total > 0 && runningCount === total && routerOn;
  const partiallyReady = runningCount > 0 || routerOn;

  // Card 1: AI Hub Service
  const btnStartAll = $('ctl-start-all');
  const btnStopAll = $('ctl-stop-all');
  const tagAll = $('cc-tag-all');
  const reasonAll = $('cc-reason-all');
  if (tagAll) {
    tagAll.className = 'b-tag ' + (fullyReady ? '' : partiallyReady ? 'b-warn' : 'b-neutral');
    tagAll.innerHTML = `<span class="b-dot"></span> ${fullyReady ? 'Online' : partiallyReady ? 'Partially online' : 'Offline'}`;
  }
  if (reasonAll) {
    reasonAll.className = 'b-cc-reason ' + (fullyReady ? 'ok' : partiallyReady ? 'warn' : '');
    reasonAll.textContent = fullyReady ? '✓ All services online (providers + gateway)'
                          : partiallyReady ? `⚠ Partial: ${runningCount}/${total} providers · gateway ${routerOn ? 'ready' : 'stopped'}`
                          : '○ All services offline';
  }
  if (btnStartAll) {
    btnStartAll.disabled = fullyReady;
    btnStartAll.textContent = partiallyReady && !fullyReady ? 'Start remaining' : 'Start';
    btnStartAll.title = fullyReady
      ? 'All services are currently online'
      : partiallyReady
        ? `Start what is stopped: ${[stoppedNames, routerOn ? '' : 'main gateway'].filter(Boolean).join(', ')}`
        : 'Start all providers and the main gateway';
  }
  if (btnStopAll) {
    btnStopAll.disabled = !partiallyReady;
    btnStopAll.title = !partiallyReady
      ? 'All services are currently offline'
      : 'Stop all providers and the main gateway';
  }

  // Sub Box: LLM Providers
  const btnProxiesStart = $('ctl-providers-start');
  const btnProxiesStop = $('ctl-providers-stop');
  const tagProxies = $('cc-tag-proxies');
  const reasonProxies = $('cc-reason-proxies');
  const proxiesAllRunning = total > 0 && runningCount === total;
  if (tagProxies) {
    tagProxies.className = 'b-tag ' + (proxiesAllRunning ? '' : runningCount > 0 ? 'b-warn' : 'b-neutral');
    tagProxies.innerHTML = `<span class="b-dot"></span> ${proxiesAllRunning ? 'Connected' : runningCount > 0 ? `${runningCount}/${total} Connected` : 'Stopped'}`;
  }
  if (reasonProxies) {
    reasonProxies.className = 'b-cc-reason ' + (proxiesAllRunning ? 'ok' : runningCount > 0 ? 'warn' : '');
    reasonProxies.textContent = proxiesAllRunning ? `✓ All ${total} LLM providers connected`
                              : runningCount > 0 ? `⚠ ${runningCount} of ${total} LLM providers connected`
                              : '○ No providers connected';
  }
  if (btnProxiesStart) {
    btnProxiesStart.disabled = proxiesAllRunning;
    btnProxiesStart.textContent = runningCount > 0 && !proxiesAllRunning ? `Start remaining (${total - runningCount})` : 'Start';
    btnProxiesStart.title = proxiesAllRunning
      ? `All ${total} LLM providers are connected`
      : runningCount > 0 ? `Start the stopped providers: ${stoppedNames}` : 'Connect all LLM providers';
  }
  if (btnProxiesStop) {
    btnProxiesStop.disabled = runningCount === 0;
    btnProxiesStop.title = runningCount === 0
      ? 'No LLM providers are currently connected'
      : 'Disconnect all LLM providers';
  }

  // Sub Box: Main Gateway
  const btnRouterStart = $('ctl-router-start');
  const btnRouterStop = $('ctl-router-stop');
  const tagRouter = $('cc-tag-router');
  const reasonRouter = $('cc-reason-router');
  if (tagRouter) {
    tagRouter.className = 'b-tag ' + (routerOn ? '' : 'b-neutral');
    tagRouter.innerHTML = `<span class="b-dot"></span> ${routerOn ? 'Ready' : 'Stopped'}`;
  }
  if (reasonRouter) {
    reasonRouter.className = 'b-cc-reason ' + (routerOn ? 'ok' : '');
    reasonRouter.textContent = routerOn ? '✓ Ready for app requests' : '○ Gateway offline';
  }
  if (btnRouterStart) {
    btnRouterStart.disabled = routerOn;
    btnRouterStart.title = routerOn
      ? 'Main gateway is ready'
      : 'Start the main gateway';
  }
  if (btnRouterStop) {
    btnRouterStop.disabled = !routerOn;
    btnRouterStop.title = !routerOn
      ? 'Main gateway is stopped'
      : 'Stop the main gateway';
  }

  // Card 4: Provider Status Extractor
  const reasonRefresh = $('cc-reason-refresh');
  if (reasonRefresh) {
    const lastGathered = (state.providers || []).map(p => p.gathered_at).filter(Boolean).sort().reverse()[0];
    reasonRefresh.className = 'b-cc-reason';
    reasonRefresh.textContent = lastGathered ? `Synced: ${lastGathered}` : 'Ready to extract quotas & models';
  }
}

async function refreshUsageTop(btn) {
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Refreshing...';
  }
  try {
    await post('/api/providers/refresh', {});
    tell('Provider usage and models refreshed successfully.');
    await refreshState();
  } catch (err) {
    tell(err.message, true);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Refresh usage';
    }
  }
}

function openAppButton(item) {
  return item.can_open
    ? `<button type="button" class="b-button" data-app-type="${esc(item.category)}" data-app-name="${esc(item.dir)}" onclick="openApp(this.dataset.appType, this.dataset.appName)">Open</button>`
    : `<button type="button" class="b-button" disabled title="Opening ${esc(item.category)} apps from the dashboard is not supported">Open</button>`;
}

function instanceCard(item) {
  return `<div class="b-int-instance"><span>${esc(item.label || item.name)}</span>${openAppButton(item)}</div>`;
}

async function openApp(type, name) {
  tell(`Opening ${name}...`);
  try {
    await post('/api/apps/open', { type, name });
    tell(`Opened ${name}.`);
  } catch (error) {
    tell(error.message, true);
  }
}

function renderHome() {
  // Quota Roster
  const roster = $('home-roster');
  if (roster) {
    const sorted = [...(state.providers || [])].sort((a, b) => getProviderHeadroom(b) - getProviderHeadroom(a));
    if (!sorted.length) {
      roster.innerHTML = '<div class="b-empty">No providers registered.</div>';
    } else {
      roster.innerHTML = sorted.map(p => {
        const meta = getProviderMeta(p.name);
        const entries = quotaEntries(p.limits);
        const headroom = getProviderHeadroom(p);
        const [stateLabel, stateTone] = accountState(p, headroom);
        const loginButton = stateLabel === 'Login needed'
          ? `<button type="button" class="b-button b-primary" onclick="loginProvider('${esc(p.name)}')">Log in</button>` : '';
        const statusTag = `<span class="b-tag ${stateTone}"><span class="b-dot"></span> ${stateLabel}</span>${loginButton}`;

        // Keep providers comparable: one without a session-length window shows "session N/A" before its weekly one.
        const sessionNA = entries.length && !entries.some(([period]) => periodRank(period) === 0)
          ? `<div class="b-period">
              <div class="b-quota-head"><span>session left</span><strong>N/A</strong></div>
              <div class="b-reset b-unknown">Not reported by CLI</div>
            </div>` : '';
        const limitsHtml = entries.length ? sessionNA + entries.map(([period, v]) => {
          const pct = Math.max(0, Math.min(100, v.remaining_pct));
          const meterClass = pct <= 0 ? 'b-empty-meter' : pct < 20 ? 'b-low' : '';
          return `
            <div class="b-period">
              <div class="b-quota-head">
                <span>${esc(period)} left</span>
                <strong>${pct}%</strong>
              </div>
              <div class="b-meter ${meterClass}" role="meter" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100">
                <span style="width: ${pct}%"></span>
              </div>
              <div class="b-reset">${v.resets ? 'Resets ' + esc(v.resets) : 'Active'}</div>
              ${Number.isFinite(v.tokens_remaining) ? `<div class="b-reset">${v.tokens_remaining.toLocaleString()} tokens available</div>` : ''}
            </div>`;
        }).join('') : '<div class="b-sub b-small">Unknown</div>';

        return `
          <article class="b-roster-group" data-provider-group="${esc(p.name)}" aria-label="${esc(meta.name)} quota">
            <div class="b-provider-identity">
              <span class="b-monogram">${meta.initial}</span>
              <div>
                <h3>${esc(meta.name)}</h3>
                <span class="b-sub b-small">1 account</span>
              </div>
            </div>
            <div class="b-roster-accounts">
              <div class="b-account-line">
                <div class="b-account-identity">
                  <strong>Default account</strong>
                  ${statusTag}
                </div>
                <div class="b-limit-list">
                  ${limitsHtml}
                </div>
              </div>
            </div>
          </article>`;
      }).join('');
    }
  }

  // Chatbots Summary on Home (grouped by chatbot type)
  const homeChatbots = $('home-chatbots-summary');
  if (homeChatbots) {
    const allApps = state.apps || [];
    const appTypes = state.app_types || [];
    const chatbots = allApps.filter(isChatbot);
    if (!chatbots.length) {
      homeChatbots.innerHTML = '<div class="b-empty">No chatbot clients registered yet.</div>';
    } else {
      const byType = {};
      chatbots.forEach(cb => {
        const typeKey = cb.type || 'chatbot';
        byType[typeKey] = byType[typeKey] || [];
        byType[typeKey].push(cb);
      });

      homeChatbots.innerHTML = Object.entries(byType).map(([type, list]) => {
        const typeInfo = appTypes.find(t => t.name === type || t.title === type);
        const count = list.length;
        const countSummary = `(${count} ${count === 1 ? 'instance' : 'instances'})`;
        const tl = type.toLowerCase();

        let title = typeInfo ? typeInfo.title : type;
        let desc = typeInfo ? typeInfo.description : '';
        if (!desc) {
          if (tl.includes('claude')) desc = 'Claude Code CLI agent routed through the gateway';
          else if (tl.includes('codex') || tl.includes('chatgpt')) desc = 'ChatGPT Codex CLI agent routed through the gateway';
          else if (tl.includes('gemini') || tl.includes('antigravity') || tl.includes('agy')) desc = 'Gemini Antigravity CLI agent routed through the gateway';
          else if (tl.includes('grok')) desc = 'Grok Build CLI agent routed through the gateway';
          else desc = 'CLI coding agent routed through the gateway';
        }

        return `
          <div class="b-int-card">
            <h3>${esc(title)} <span class="b-sub b-small" style="font-weight: normal; margin-left: 6px;">${countSummary}</span></h3>
            <p class="b-sub">${esc(desc)}</p>
            <div class="b-int-instances">${list.map(instanceCard).join('')}</div>
          </div>`;
      }).join('');
    }
  }

  // Workspace Apps Summary on Home (grouped by app type)
  const homeApps = $('home-apps-summary');
  if (homeApps) {
    const allApps = state.apps || [];
    const appTypes = state.app_types || [];
    const workspaceApps = allApps.filter(a => !isChatbot(a));
    if (!workspaceApps.length) {
      homeApps.innerHTML = '<div class="b-empty">No workspace apps registered yet.</div>';
    } else {
      const byType = {};
      workspaceApps.forEach(a => {
        const typeKey = a.type || a.category || 'app';
        byType[typeKey] = byType[typeKey] || [];
        byType[typeKey].push(a);
      });

      homeApps.innerHTML = Object.entries(byType).map(([type, list]) => {
        const typeInfo = appTypes.find(t => t.name === type || t.title === type) || {
          title: type.charAt(0).toUpperCase() + type.slice(1),
          description: ''
        };
        const count = list.length;
        const countSummary = `(${count} ${count === 1 ? 'instance' : 'instances'})`;
        return `
          <div class="b-int-card">
            <h3>${esc(typeInfo.title)} <span class="b-sub b-small" style="font-weight: normal; margin-left: 6px;">${countSummary}</span></h3>
            <p class="b-sub">${esc(typeInfo.description || 'Connected workspace integration')}</p>
            <div class="b-int-instances">${list.map(instanceCard).join('')}</div>
          </div>`;
      }).join('');
    }
  }
}

const APP_KINDS = {
  apps: { container: 'apps-container', plural: 'Apps', eyebrow: 'Your workspace', match: a => !isChatbot(a),
    types: t => t.name !== 'chatbot', intro: 'Each registered app maps an integration into your local workspace.' },
  chatbots: { container: 'chatbots-container', plural: 'Chatbots', eyebrow: 'Your AI agents', match: isChatbot,
    types: t => t.name === 'chatbot', intro: 'Each registered chatbot routes a CLI agent through the bridge.' },
};

// One "Connect <name> instance" entry per app type, or per CLI preset when the type registers by preset.
const connectLabel = ({ type, preset, name }) => `Connect ${name} instance`;
const connectTargets = types => types.flatMap(t => t.preset_field === 'preset'
  ? t.presets.map(preset => ({ type: t.name, preset, name: t.preset_names[preset] }))
  : [{ type: t.name, preset: '', name: t.name.charAt(0).toUpperCase() + t.name.slice(1) }]);
function renderApps() {
  const kind = APP_KINDS[currentTab];
  const container = $(kind.container);
  if (!container) return;

  if (addAppWizard) {
    renderAddAppWizard(container);
    return;
  }

  if (selectedApp !== null) {
    renderAppDetail(container);
    return;
  }

  const appTypes = state.app_types || [];
  const apps = (state.apps || []).map((a, idx) => ({ ...a, idx })).filter(kind.match);

  const connectTypes = appTypes.filter(kind.types);
  let html = `
    <div class="b-top">
      <div class="b-eyebrow">${kind.eyebrow}</div>
      <div class="b-between">
        <h1>My ${kind.plural}</h1>
        <div class="b-row">
          ${connectTargets(connectTypes).map(target => `<button type="button" class="b-button b-primary" onclick="openAddAppWizard('${esc(target.type)}', '${esc(target.preset)}', '${esc(target.name)}')">＋ ${esc(connectLabel(target))}</button>`).join('')}
          ${currentTab === 'apps' ? `<button type="button" class="b-button" onclick="tell('Integrating a brand-new app: to be implemented.')">＋ Integrate new app</button>` : ''}
        </div>
      </div>
      <p class="b-sub">${kind.intro}</p>
    </div>`;

  if (!apps.length) {
    html += `<div class="b-empty">No ${kind.plural.toLowerCase()} connected yet. Use the buttons above to connect one.</div>`;
  } else {
    // Group by type
    const byType = {};
    apps.forEach(a => {
      byType[a.type] = byType[a.type] || [];
      byType[a.type].push(a);
    });

    for (const [type, list] of Object.entries(byType)) {
      const typeInfo = appTypes.find(t => t.name === type) || { title: type, description: '' };
      html += `
        <section class="b-section">
          <div class="b-section-head">
            <div>
              <div class="b-eyebrow">App type</div>
              <h2>${esc(typeInfo.title)}</h2>
            </div>
            <span class="b-sub b-small">${list.length} registered</span>
          </div>
          <p class="b-sub b-small" style="max-width:680px; margin-bottom:14px">${esc(typeInfo.description)}</p>
          <div class="b-app-list">
            ${list.map(item => `
              <div class="b-app-row">
                <div class="b-app-icon">${type === 'obsidian' ? '◇' : '◈'}</div>
                <div class="b-grow">
                  <h3>${esc(item.label || item.name)}</h3>
                  <p class="b-sub">Path: ${esc(item.path)} ${item.vault_type ? '· Preset: ' + esc(item.vault_type) : ''}</p>
                </div>
                <div class="b-row">
                  <span class="b-tag ${item.target_exists ? '' : 'b-warn'}">
                    <span class="b-dot"></span> ${item.target_exists ? 'Configured' : 'Missing Target'}
                  </span>
                  ${openAppButton(item)}
                  <button type="button" class="b-button" onclick="selectApp(${item.idx})">Settings</button>
                </div>
              </div>
            `).join('')}
          </div>
        </section>`;
    }
  }

  container.innerHTML = html;
}

function renderAppDetail(container) {
  const app = state.apps[selectedApp];
  if (!app) {
    selectedApp = null;
    renderApps();
    return;
  }

  const kind = APP_KINDS[currentTab];
  container.innerHTML = `
    <div class="b-top">
      <div class="b-eyebrow">My ${kind.plural}</div>
      <div class="b-between">
        <h1>${esc(app.label || app.name)}</h1>
        <div class="b-row">
          <button type="button" class="b-button" onclick="selectApp(null)">← Back to ${kind.plural}</button>
        </div>
      </div>
      <p class="b-sub">${esc(app.type)} integration settings</p>
    </div>
    <div class="b-panel">
      <div class="b-between">
        <h2>Connection Settings</h2>
        <span class="b-tag"><span class="b-dot"></span> Registered</span>
      </div>
      <label class="b-field">
        App Folder
        <input type="text" readonly value="${esc(app.path)}">
      </label>
      <label class="b-field">
        Configuration Target File
        <input type="text" readonly value="${esc(app.target)}">
      </label>
      ${app.vault_type ? `
        <label class="b-field">
          Preset
          <input type="text" readonly value="${esc(app.vault_type)}">
        </label>` : ''}
      <div class="b-between" style="margin-top:22px">
        <span></span>
        <button type="button" class="b-button b-primary" onclick="reapplyApp('${esc(app.category)}', '${esc(app.dir)}')">Re-apply Configuration</button>
      </div>
    </div>`;
}

function renderAddAppWizard(container) {
  const kind = APP_KINDS[currentTab];
  const singleName = currentTab === 'chatbots'; // chatbot: folder (Browse), then one free-text name (id is derived from it)
  const types = (state.app_types || []).filter(t => t.name === addAppWizard.type);
  const pathField = `<label class="b-field">
          Workspace Folder Path
          <span style="display:flex; gap:8px">
            <input id="wiz-path" placeholder="C:/path/to/workspace" oninput="fillWizardName()" style="flex:1">
            <button type="button" class="b-button" onclick="browseWizardFolder()">Browse…</button>
          </span>
          <small id="wiz-path-help"></small>
        </label>`;
  container.innerHTML = `
    <div class="b-top">
      <div class="b-eyebrow">My ${kind.plural}</div>
      <div class="b-between">
        <h1>${esc(connectLabel(addAppWizard))}</h1>
        <button type="button" class="b-button" onclick="closeAddAppWizard()">Cancel</button>
      </div>
      <p class="b-sub">Add a local workspace folder to route LLM requests through the bridge.</p>
    </div>
    <div class="b-panel" style="max-width:680px; margin:auto">
      <form id="wizard-form" onsubmit="submitAddApp(event)">
        ${singleName ? pathField : ''}
        <label class="b-field" ${singleName ? 'hidden' : ''}>
          App Type
          <select id="wiz-type" required onchange="updateWizardPresets()">
            ${types.map(t => `<option value="${esc(t.name)}">${esc(t.title || t.name)}</option>`).join('')}
          </select>
        </label>
        <label class="b-field">
          ${singleName ? 'Name' : 'Instance ID'} (defaults to the folder name)
          <input id="wiz-name" placeholder="${singleName ? 'My Claude project' : 'my-wiki'}" oninput="this.dataset.edited = this.value ? '1' : ''">
        </label>
        ${singleName ? '' : `<label class="b-field">
          Display Label
          <input id="wiz-label" placeholder="My Research Wiki">
        </label>`}
        ${singleName ? '' : pathField}
        <div id="wiz-preset-container" ${singleName ? 'hidden' : ''}></div>
        <div class="b-between" style="margin-top:24px">
          <button type="button" class="b-button" onclick="closeAddAppWizard()">Cancel</button>
          <button type="submit" class="b-button b-primary">Register Workspace</button>
        </div>
      </form>
    </div>`;
  updateWizardPresets();
}

function updateWizardPresets() {
  const selType = $('wiz-type')?.value;
  const typeObj = (state.app_types || []).find(t => t.name === selType);
  const container = $('wiz-preset-container');
  if (!container) return;

  if (typeObj && typeObj.presets && typeObj.presets.length) {
    const choices = addAppWizard.preset ? [addAppWizard.preset] : typeObj.presets;
    container.innerHTML = `
      <label class="b-field">
        ${esc(typeObj.preset_label)}
        <select id="wiz-preset">
          ${choices.map(p => `<option value="${esc(p)}">${esc(p)}</option>`).join('')}
        </select>
      </label>`;
  } else {
    container.innerHTML = '';
  }
  $('wiz-path').required = !!typeObj?.path_required;
  $('wiz-path-help').textContent = typeObj?.path_required
    ? 'Enter the folder to configure. It will be created if needed.'
    : 'Leave blank to use the registration folder.';
}

async function browseWizardFolder() {
  try {
    const res = await post('/api/apps/pick-folder', {});
    if (!res.path) return;
    $('wiz-path').value = res.path;
    fillWizardName();
  } catch (err) {
    tell(err.message, true);
  }
}

function folderName() {
  return ($('wiz-path')?.value || '').trim().replace(/[\\/]+$/, '').split(/[\\/]/).pop();
}

function fillWizardName() {
  const name = $('wiz-name');
  if (!name.dataset.edited) name.value = folderName();
}

function wizardName() {
  return $('wiz-name')?.value.trim() || folderName();
}

function selectApp(idx) {
  selectedApp = idx;
  renderApps();
}

function openAddAppWizard(type, preset, name) {
  addAppWizard = { type, preset, name };
  renderApps();
}

function closeAddAppWizard() {
  addAppWizard = null;
  renderApps();
}

// A chatbot is identified by its workspace path; its instance folder under registered_apps is that
// path's own folder name (already a legal name), with -2, -3... if two workspaces share one.
const normalizePath = path => path.replace(/[\\/]+$/, '').replace(/\\/g, '/').toLowerCase();
const samePath = (a, b) => normalizePath(a) === normalizePath(b);

function instanceIdForPath(type) {
  const base = folderName();
  let id = base;
  for (let n = 2; (state.apps || []).some(a => a.category === type && a.dir === id); n++) id = `${base}-${n}`;
  return id;
}

async function submitAddApp(e) {
  e.preventDefault();
  const type = $('wiz-type').value;
  const preset = $('wiz-preset')?.value || '';
  const chatbotForm = currentTab === 'chatbots';
  const label = chatbotForm ? wizardName() : $('wiz-label').value;
  const path = $('wiz-path').value;
  if (chatbotForm) {
    if (!folderName()) return tell('Pick a workspace folder.', true);
    if ((state.apps || []).some(a => a.category === type && samePath(a.path, path))) {
      return tell('A chatbot is already registered for this folder.', true);
    }
  }
  const name = chatbotForm ? instanceIdForPath(type) : wizardName();

  try {
    const typeObj = (state.app_types || []).find(t => t.name === type);
    const payload = { type, name, label, path };
    if (preset) payload[typeObj.preset_field] = preset;
    await post('/api/apps/register', payload);
    tell(`App ${label || name} registered successfully!`);
    addAppWizard = null;
    await refreshState();
  } catch (err) {
    tell(err.message, true);
  }
}

async function reapplyApp(type, name) {
  try {
    await post('/api/apps/apply', { type, name });
    tell(`Applied configuration to ${name}.`);
    await refreshState();
  } catch (err) {
    tell(err.message, true);
  }
}

function renderProviders() {
  const container = $('providers-container');
  if (!container) return;

  if (selectedProvider) {
    renderProviderDetail(container);
    return;
  }

  const providers = state.providers || [];
  const isAdv = $('bridge-advanced')?.checked;

  let html = `
    <div class="b-top">
      <div class="b-eyebrow">Subscriptions</div>
      <div class="b-between">
        <h1>LLM Providers</h1>
        <span>
          ${(state.addable_providers || []).length ? `<select id="add-provider-select" aria-label="Provider to add">${state.addable_providers.map(n => `<option value="${n}">${n}</option>`).join('')}</select>
          <button type="button" class="b-button" onclick="addProvider(this)">Add provider</button>` : ''}
          <button type="button" class="b-button" onclick="refreshProviders(this)">Refresh Usage</button>
        </span>
      </div>
      <p class="b-sub">Manage local CLI logins, tool execution, and model mappings for each provider.</p>
    </div>`;

  if (!providers.length) {
    html += '<div class="b-empty">No providers configured. Check registered_providers/ directory.</div>';
  } else if (isAdv) {
    // Advanced Table View
    html += `
      <div class="b-panel b-table-wrap">
        <table>
          <thead>
            <tr>
              <th>Provider</th>
              <th>Status</th>
              <th>Port</th>
              <th>Quota</th>
              <th>Tools</th>
              <th>Controls</th>
            </tr>
          </thead>
          <tbody>
            ${providers.map(p => {
              const meta = getProviderMeta(p.name);
              const entries = quotaEntries(p.limits);
              const quotaStr = entries.map(([k, v]) => `${k}: ${v.remaining_pct}%`).join(', ') || 'None';
              const enabledTools = (p.tools?.enabled || []).join(', ') || 'None';
              return `
                <tr>
                  <td><strong>${esc(meta.name)}</strong></td>
                  <td>
                    <span class="b-tag ${p.running ? '' : 'b-neutral'}">
                      <span class="b-dot"></span> ${p.running ? 'Running' : 'Stopped'}
                    </span>
                  </td>
                  <td class="b-mono">${p.port}</td>
                  <td>${esc(quotaStr)}</td>
                  <td><span class="b-sub b-small">${esc(enabledTools)}</span></td>
                  <td>
                    <div class="b-row">
                      <button type="button" class="b-button" onclick="openProviderDetail('${esc(p.name)}')">Settings</button>
                      <button type="button" class="b-button" onclick="loginProvider('${esc(p.name)}')">Log in</button>
                    </div>
                  </td>
                </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>`;
  } else {
    // Standard Card Grid View
    html += `
      <div class="b-provider-grid">
        ${providers.map(p => {
          const meta = getProviderMeta(p.name);
          const headroom = getProviderHeadroom(p);
          const entries = quotaEntries(p.limits);

          return `
            <article class="b-provider-card">
              <div class="b-between">
                <div class="b-account-name">
                  <span class="b-monogram">${meta.initial}</span>
                  <div>
                    <strong>${esc(meta.name)}</strong>
                    <div class="b-sub b-small">Port ${p.port} · ${p.plan || 'CLI login'}</div>
                  </div>
                </div>
                <button type="button" class="b-button" onclick="openProviderDetail('${esc(p.name)}')">Settings</button>
              </div>
              <div class="b-nested-accounts">
                <div class="b-between" style="margin-bottom:8px">
                  <span class="b-tag ${statusClass(p.status)}">
                    <span class="b-dot"></span> ${esc(statusLabel(p.status, p.running))}
                  </span>
                  <span>
                    <button type="button" class="b-button" onclick="openLogViewer('${esc(p.name)}')">View log</button>
                    <button type="button" class="b-button" onclick="loginProvider('${esc(p.name)}')">CLI Sign-in</button>
                    <button type="button" class="b-button" onclick="validateProvider(this, '${esc(p.name)}')">Validate</button>
                  </span>
                </div>
                ${p.reason && p.status !== 'running' ? `<div class="b-reason ${statusClass(p.status)}">${esc(p.reason)}</div>` : ''}
                <div class="b-limit-list">
                  ${entries.length ? entries.map(([period, v]) => `
                    <div class="b-period">
                      <div class="b-quota-head">
                        <span>${esc(period)} left</span>
                        <strong>${v.remaining_pct}%</strong>
                      </div>
                      <div class="b-meter ${v.remaining_pct < 20 ? 'b-low' : ''}">
                        <span style="width: ${v.remaining_pct}%"></span>
                      </div>
                    </div>`).join('') : '<div class="b-sub b-small">Quota not available</div>'}
                </div>
              </div>
            </article>`;
        }).join('')}
      </div>`;
  }

  container.innerHTML = html;
}

function renderProviderDetail(container) {
  const p = (state.providers || []).find(x => x.name === selectedProvider);
  if (!p) {
    selectedProvider = null;
    renderProviders();
    return;
  }

  const meta = getProviderMeta(p.name);
  const tools = p.tools || {};
  const availableTools = tools.available || [];
  const enabledTools = tools.enabled || [];
  const models = p.models || [];

  container.innerHTML = `
    <div class="b-top">
      <div class="b-eyebrow">LLM Providers</div>
      <div class="b-between">
        <h1>${esc(meta.name)} Settings</h1>
        <button type="button" class="b-button" onclick="openProviderDetail(null)">← Back to Providers</button>
      </div>
      <p class="b-sub">Configure CLI tools, models, and authentication for ${esc(meta.name)}.</p>
    </div>
    <div class="b-two">
      <div class="b-panel">
        <h2>Allowed Tools</h2>
        <p class="b-sub b-small" style="margin:6px 0 14px">Allow this provider to execute tools during client handoffs.</p>
        ${availableTools.length ? availableTools.map(t => `
          <label class="b-check">
            <input type="checkbox" ${enabledTools.includes(t) ? 'checked' : ''} onchange="toggleProviderTool('${esc(p.name)}', '${esc(t)}', this.checked)">
            ${esc(t)}
          </label>
        `).join('') : '<p class="b-sub b-small">No tools declared in config.</p>'}
      </div>
      <div class="b-panel">
        <h2>CLI Authentication</h2>
        <p class="b-sub b-small" style="margin:6px 0 14px">Launch interactive CLI terminal to authenticate your subscription.</p>
        <button type="button" class="b-button b-primary" onclick="loginProvider('${esc(p.name)}')">Open Terminal Sign-In</button>
        <h2 style="margin-top:24px">Quota History</h2>
        <div id="quota-history" class="b-sub b-small">Loading…</div>
        <h2 style="margin-top:24px">Available Models</h2>
        <div class="b-review">
          ${models.length ? models.slice(0, 5).map(m => `
            <div>
              <span>${esc(typeof m === 'string' ? m : m.name)}</span>
              <span class="b-mono b-sub">${esc(typeof m === 'string' ? m : m.id)}</span>
            </div>
          `).join('') : '<div class="b-sub b-small">No exported models available.</div>'}
        </div>
      </div>
    </div>`;
  loadQuotaHistory(p.name);
}

const HISTORY_COLORS = ['var(--b-accent-fill)', 'var(--b-ok)', 'var(--b-warn)', 'var(--b-danger)'];

function historyChart(points) {
  const periods = [...new Set(points.flatMap(pt => Object.keys(pt.remaining)))];
  const t0 = points[0].t, span = Math.max(1, points[points.length - 1].t - t0);
  const W = 360, H = 120, pad = 4;
  const x = t => pad + (t - t0) / span * (W - 2 * pad);
  const y = v => pad + (100 - v) / 100 * (H - 2 * pad);
  const lines = periods.map((period, i) => {
    const pts = points.filter(pt => typeof pt.remaining[period] === 'number')
      .map(pt => `${x(pt.t).toFixed(1)},${y(pt.remaining[period]).toFixed(1)}`).join(' ');
    return `<polyline fill="none" stroke="${HISTORY_COLORS[i % HISTORY_COLORS.length]}" stroke-width="2" points="${pts}"/>`;
  }).join('');
  const legend = periods.map((period, i) =>
    `<span style="color:${HISTORY_COLORS[i % HISTORY_COLORS.length]}">● ${esc(period)}</span>`).join(' &nbsp; ');
  const first = new Date(t0 * 1000).toLocaleString();
  return `<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;background:var(--b-soft);border-radius:8px" role="img" aria-label="Remaining quota over time">
      <line x1="0" x2="${W}" y1="${y(20)}" y2="${y(20)}" stroke="var(--b-line)" stroke-dasharray="3 3"/>${lines}</svg>
    <div class="b-between b-small" style="margin-top:4px"><span>${legend}</span><span class="b-sub">100% top · since ${esc(first)}</span></div>`;
}

async function loadQuotaHistory(name) {
  try {
    const response = await fetch(`/api/history?name=${encodeURIComponent(name)}&days=7`, {cache: 'no-store'});
    const data = await response.json();
    const box = $('quota-history');
    if (!box) return;
    box.innerHTML = data.points && data.points.length > 1
      ? historyChart(data.points)
      : 'Not enough snapshots yet. Remaining quota is recorded about every 5 minutes while the dashboard is open.';
  } catch (error) {
    const box = $('quota-history');
    if (box) box.textContent = error.message;
  }
}

function openProviderDetail(name) {
  selectedProvider = name;
  renderProviders();
}

async function toggleProviderTool(provider, tool, enabled) {
  try {
    await post('/api/providers/tools', { provider, tool, enabled });
    tell(`${provider} tools updated. Restart the proxy to apply changes.`);
    await refreshState();
  } catch (err) {
    tell(err.message, true);
  }
}

function renderRouter() {
  const container = $('router-container');
  if (!container) return;

  if (!routerDraft) {
    routerDraft = structuredClone(state.router || {});
    routerDraft.mode = routerDraft.mode || 'usage';
    routerDraft.custom_order = routerDraft.custom_order || [];
    routerDraft.providers = routerDraft.providers || {};
  }

  const isUsage = routerDraft.mode === 'usage';

  container.innerHTML = `
    <div class="b-top">
      <div class="b-eyebrow">Advanced</div>
      <div class="b-between">
        <h1>Router Configuration</h1>
        <button type="button" class="b-button b-primary" onclick="saveRouter()">Save Changes</button>
      </div>
      <p class="b-sub">Select provider selection strategy and tier model mappings.</p>
    </div>
    <div class="b-two" style="margin-bottom:18px">
      <button type="button" class="b-choice" aria-pressed="${isUsage}" onclick="setRouteMode('usage')">
        <strong>Spread work across providers</strong>
        <small>Route each semantic tier to the provider with the highest remaining quota.</small>
      </button>
      <button type="button" class="b-choice" aria-pressed="${!isUsage}" onclick="setRouteMode('custom')">
        <strong>Use my preferred provider first</strong>
        <small>Prioritize providers strictly by your custom order below.</small>
      </button>
    </div>
    <div class="b-two">
      <div class="b-panel">
        <h2>Preferred Provider Order</h2>
        <p class="b-sub b-small" style="margin:6px 0 12px">Fallback priority order:</p>
        ${(routerDraft.custom_order || []).map((name, i) => `
          <div class="b-order-row">
            <span class="b-rank">${i + 1}</span>
            <span class="b-grow"><strong>${esc(name)}</strong></span>
            <button type="button" class="b-icon-button" onclick="moveRouterOrder(${i}, -1)" ${i === 0 ? 'disabled' : ''} aria-label="Move up">↑</button>
            <button type="button" class="b-icon-button" onclick="moveRouterOrder(${i}, 1)" ${i === routerDraft.custom_order.length - 1 ? 'disabled' : ''} aria-label="Move down">↓</button>
          </div>
        `).join('')}
      </div>
      <div class="b-panel">
        <h2>Semantic Tiers Mapping</h2>
        <p class="b-sub b-small" style="margin:6px 0 12px">Exact model IDs resolved for fast, medium, and reasoning tiers.</p>
        <div class="b-table-wrap">
          <table>
            <thead>
              <tr>
                <th>Provider</th>
                <th>Tier</th>
                <th>Model</th>
                <th>Effort</th>
              </tr>
            </thead>
            <tbody>
              ${Object.entries(routerDraft.providers || {}).flatMap(([pName, pObj]) => {
                pObj.effort = pObj.effort || {};
                pObj.tiers = pObj.tiers || {};
                const provInfo = (state.providers || []).find(p => p.name === pName);
                const availableModels = (provInfo?.models || []).map(m => typeof m === 'string' ? m : m.id);

                return Object.entries(pObj.tiers).map(([tier, model]) => `
                  <tr>
                    <td><strong>${esc(pName)}</strong></td>
                    <td><span class="b-tag b-neutral">${esc(tier)}</span></td>
                    <td>
                      <select onchange="updateTierModel('${esc(pName)}', '${esc(tier)}', this.value)" aria-label="${pName} ${tier} model">
                        ${availableModels.includes(model) ? '' : `<option value="${esc(model)}">${esc(model)}</option>`}
                        ${availableModels.map(m => `<option value="${esc(m)}" ${m === model ? 'selected' : ''}>${esc(m)}</option>`).join('')}
                      </select>
                    </td>
                    <td>
                      <select onchange="updateTierEffort('${esc(pName)}', '${esc(tier)}', this.value)" aria-label="${pName} ${tier} effort">
                        ${['', 'low', 'medium', 'high', 'xhigh', 'max'].map(eff => `
                          <option value="${esc(eff)}" ${eff === (pObj.effort[tier] || '') ? 'selected' : ''}>${eff || 'default'}</option>
                        `).join('')}
                      </select>
                    </td>
                  </tr>`);
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>`;
}

function setRouteMode(mode) {
  if (routerDraft) routerDraft.mode = mode;
  renderRouter();
}

function moveRouterOrder(index, offset) {
  const next = index + offset;
  const list = routerDraft.custom_order;
  [list[index], list[next]] = [list[next], list[index]];
  renderRouter();
}

function updateTierModel(provider, tier, model) {
  if (routerDraft?.providers?.[provider]?.tiers) {
    routerDraft.providers[provider].tiers[tier] = model;
  }
}

function updateTierEffort(provider, tier, effort) {
  if (routerDraft?.providers?.[provider]) {
    routerDraft.providers[provider].effort = routerDraft.providers[provider].effort || {};
    routerDraft.providers[provider].effort[tier] = effort;
  }
}

async function saveRouter() {
  try {
    const res = await post('/api/router', routerDraft);
    tell(res.restart_required ? 'Router settings saved! Restart the router to apply.' : 'Router settings saved!');
    await refreshState();
  } catch (err) {
    tell(err.message, true);
  }
}

function renderActivity() {
  const container = $('activity-container');
  if (!container) return;

  const filter = $('activity-filter')?.value || 'all';
  let list = state.activity || [];
  if (filter !== 'all') {
    list = list.filter(item => item.status === filter);
  }

  container.innerHTML = `
    <div class="b-top">
      <div class="b-eyebrow">Advanced</div>
      <div class="b-between">
        <h1>Recent Activity</h1>
        <button type="button" class="b-button" onclick="openLogViewer('router')">Router log</button>
        <label class="b-field" style="margin:0; width:180px">
          <select id="activity-filter" onchange="renderActivity()">
            <option value="all" ${filter === 'all' ? 'selected' : ''}>All Requests</option>
            <option value="Completed" ${filter === 'Completed' ? 'selected' : ''}>Completed</option>
            <option value="Failed" ${filter === 'Failed' ? 'selected' : ''}>Failed</option>
          </select>
        </label>
      </div>
      <p class="b-sub">Inspect recent LLM prompts, proxy routes, and execution events.</p>
    </div>
    <div class="b-panel b-table-wrap">
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>ID</th>
            <th>Provider</th>
            <th>Model</th>
            <th>Path / Event</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${!list.length ? '<tr><td colspan="6" class="b-empty">No activity matching filter.</td></tr>' : list.map(item => `
            <tr>
              <td><span class="b-mono">${esc(item.when)}</span></td>
              <td><span class="b-mono">${esc(item.id)}</span></td>
              <td><strong>${esc(item.provider)}</strong></td>
              <td><span class="b-mono">${esc(item.model)}</span></td>
              <td><span class="b-mono b-sub">${esc(item.router?.event || item.path)}</span></td>
              <td>
                <span class="b-tag ${item.status === 'Completed' ? '' : 'b-warn'}">
                  <span class="b-dot"></span> ${esc(item.status)}
                </span>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>`;
}

// ----------------- CONTROL ACTIONS -----------------

function logConsole(message, isError = false) {
  const el = $('ctl-console-output');
  if (el) {
    const time = new Date().toLocaleTimeString();
    el.textContent = `[${time}] ${message}`;
    el.style.color = isError ? 'var(--b-danger)' : 'var(--b-ink)';
  }
}

async function startAll(btn) {
  if (btn) btn.disabled = true;
  logConsole('Starting all providers and the router...');
  tell('Starting all providers and router...');
  try {
    const res = await post('/api/control/all-start', {});
    logConsole(res.output || 'Done.');
    setTimeout(refreshState, 2000);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function stopAll(btn) {
  if (btn) btn.disabled = true;
  logConsole('Stopping the router and all providers...');
  tell('Stopping all bridge services...');
  try {
    const res = await post('/api/control/all-stop', {});
    logConsole(res.output || 'Done.');
    setTimeout(refreshState, 1500);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function startAllProxies(btn) {
  if (btn) btn.disabled = true;
  logConsole('Starting all providers...');
  tell('Launching all provider proxies...');
  try {
    const res = await post('/api/control/providers', {});
    logConsole(res.output || 'Started.');
    setTimeout(refreshState, 2000);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function stopAllProxies(btn) {
  if (btn) btn.disabled = true;
  logConsole('Stopping all providers...');
  tell('Stopping all provider proxies...');
  try {
    const res = await post('/api/control/providers-stop', {});
    logConsole(res.output || 'Done.');
    setTimeout(refreshState, 1500);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function validateProvider(btn, name) {
  btn.disabled = true;
  tell(`Validating ${name} (capture + parse, ~30s)...`);
  try {
    const res = await post('/api/providers/validate', { provider: name });
    tell(`${name}: ${res.remaining_pct != null ? res.remaining_pct + '% quota remaining' : 'quota unknown'}, ${res.models_count ?? "?"} model(s).`);
    await refreshState();
  } catch (error) {
    tell(error.message, true);
  } finally {
    btn.disabled = false;
  }
}

async function addProvider(btn) {
  const name = $('add-provider-select')?.value;
  if (!name) return;
  btn.disabled = true;
  try {
    await post('/api/providers/add', { provider: name });
    tell(`Added ${name}. Log in to its CLI, then use Start to validate usage capture.`);
    await refreshState();
  } catch (error) {
    tell(error.message, true);
  } finally {
    btn.disabled = false;
  }
}

async function refreshProviders(btn) {
  if (btn) btn.disabled = true;
  logConsole('Refreshing provider usage and models...');
  tell('Refreshing provider quotas...');
  try {
    const res = await post('/api/control/refresh', {});
    logConsole(res.output || 'Started.');
    setTimeout(refreshState, 3000);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function startRouter(btn) {
  if (btn) btn.disabled = true;
  logConsole('Starting the router (port 8090)...');
  tell('Launching router process...');
  try {
    const res = await post('/api/control/router', {});
    logConsole(res.output || 'Started.');
    setTimeout(refreshState, 1500);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function stopRouter(btn) {
  if (btn) btn.disabled = true;
  logConsole('Stopping the router...');
  tell('Stopping router...');
  try {
    const res = await post('/api/control/router-stop', {});
    logConsole(res.output || 'Done.');
    setTimeout(refreshState, 1000);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function restartRouter(btn) {
  if (btn) btn.disabled = true;
  logConsole('Restarting the router...');
  tell('Restarting router...');
  try {
    await post('/api/control/router-stop', {});
    setTimeout(async () => {
      const res = await post('/api/control/router', {});
      logConsole(res.output || 'Router restarted.');
      setTimeout(refreshState, 1500);
    }, 800);
  } catch (e) {
    logConsole(`Error: ${e.message}`, true);
    tell(e.message, true);
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function launchProvider(name, btn) {
  if (btn) btn.disabled = true;
  tell(`Launching ${name} proxy...`);
  try {
    await post('/api/providers/launch', { provider: name });
    setTimeout(refreshState, 1500);
  } catch (e) {
    tell(e.message, true);
  }
}

async function stopProvider(name, btn) {
  if (btn) btn.disabled = true;
  tell(`Stopping ${name} proxy...`);
  try {
    await post('/api/providers/stop', { provider: name });
    setTimeout(refreshState, 1000);
  } catch (e) {
    tell(e.message, true);
  }
}

async function restartProvider(name, btn) {
  if (btn) btn.disabled = true;
  tell(`Restarting ${name} proxy...`);
  try {
    await post('/api/providers/restart', { provider: name });
    setTimeout(refreshState, 1500);
  } catch (e) {
    tell(e.message, true);
  }
}

async function loginProvider(name) {
  tell(`Opening CLI login terminal for ${name}...`);
  try {
    await post('/api/providers/login', { provider: name });
  } catch (e) {
    tell(e.message, true);
  }
}

async function updateProviderPort(name, port) {
  const p = parseInt(port, 10);
  if (!p || p < 1024 || p > 65535) {
    tell('Invalid port: choose between 1024 and 65535', true);
    return;
  }
  tell(`Port for ${name} set to ${p}. Takes effect on next launch.`);
  try {
    await post('/api/providers/launch', { provider: name, port: p });
  } catch {
    // Port saved in config even if not launched immediately
  }
}

// ----------------- STATE FETCH -----------------

async function refreshState() {
  const attempts = 4;
  for (let attempt = 1; ; attempt++) {
    try {
      const response = await fetch('/api/state', { cache: 'no-store' });
      if (!response.ok) throw new Error('State fetch failed');
      state = await response.json();
      break;
    } catch (err) {
      if (attempt === attempts) {
        tell('Could not connect to dashboard server.', true);
        return;
      }
      await new Promise(resolve => setTimeout(resolve, 500 * attempt));
    }
  }
  try {
    render();
  } catch (err) {
    console.error(err);
    tell(`Dashboard failed to render: ${err.message}`, true);
  }
}

// ----------------- INITIALIZATION -----------------

window.addEventListener('DOMContentLoaded', () => {
  loadPreferences();
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const theme = localStorage.getItem('hub-theme') || 'auto';
    if (theme === 'auto') syncThemePresentation(theme);
  });

  // Navigation click handlers
  document.querySelectorAll('#bridge-nav button').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });

  // Advanced mode toggle
  const advToggle = $('bridge-advanced');
  if (advToggle) {
    advToggle.addEventListener('change', e => {
      const isAdv = e.target.checked;
      localStorage.setItem('hub-advanced', String(isAdv));
      document.querySelectorAll('.b-adv-only').forEach(el => el.hidden = !isAdv);
      if (!isAdv && ['router', 'activity'].includes(currentTab)) {
        switchTab('home');
      } else {
        render();
      }
    });
    // Set initial visibility
    document.querySelectorAll('.b-adv-only').forEach(el => el.hidden = !advToggle.checked);
  }

  // Theme toggle button
  const themeBtn = $('bridge-theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', toggleTheme);
  }

  // Control Center button listeners
  $('ctl-start-all')?.addEventListener('click', e => startAll(e.target));
  $('ctl-stop-all')?.addEventListener('click', e => stopAll(e.target));
  $('ctl-providers-start')?.addEventListener('click', e => startAllProxies(e.target));
  $('ctl-providers-stop')?.addEventListener('click', e => stopAllProxies(e.target));
  $('ctl-router-start')?.addEventListener('click', e => startRouter(e.target));
  $('ctl-router-stop')?.addEventListener('click', e => stopRouter(e.target));
  $('ctl-refresh-usage')?.addEventListener('click', e => refreshProviders(e.target));

  switchTab(currentTab, false);
  window.addEventListener('popstate', () => switchTab(tabFromPath(location.pathname), false));
  refreshState();
  // Auto refresh every 15s when not modifying router draft
  setInterval(() => {
    if (currentTab !== 'router') {
      refreshState();
    }
  }, 15000);
});
