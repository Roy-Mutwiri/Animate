const views = {
  generate: ["Generate Clips", "Create vertical 30-50 second clips from a YouTube stream."],
  review: ["Review Manifest", "Inspect captions, timings, and clip status before posting."],
  upload: ["Upload Queue", "Preview first, then post with a random 1-15 minute gap and no post-count limit."],
};

const state = {
  manifests: [],
  accounts: [],
  activeManifest: "",
  activeAccount: localStorage.getItem("activeTikTokAccount") || "main",
  analyzeTimer: null,
  uploadBudget: null,
  accountLimits: [],
};

const $ = (selector) => document.querySelector(selector);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const text = await response.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    const error = new Error(`Server returned non-JSON response (${response.status}). Refresh the app or restart the local server.`);
    error.userMessage = {
      title: "Server response could not be read.",
      cause: "The app expected JSON but received an HTML/error page from the local server.",
      steps: ["Refresh this page.", "If it repeats, stop and restart the local server.", "Check that the URL is the TikTok Poster app, not a stale route."],
    };
    throw error;
  }
  if (!response.ok) {
    const message = typeof data.error === "string" ? data.error : data.error?.title || "Request failed";
    const error = new Error(message);
    error.userMessage = typeof data.error === "object" && data.error ? data.error : null;
    throw error;
  }
  return data;
}

function solutionHtml(userMessage) {
  const steps = userMessage && Array.isArray(userMessage.steps) ? userMessage.steps : [];
  return `
    <div class="solution-box">
      <strong>${escapeHtml(userMessage?.title || "Action needed")}</strong>
      <span>${escapeHtml(userMessage?.cause || "")}</span>
      ${steps.length ? `<ol>${steps.map((step) => `<li>${escapeHtml(step)}</li>`).join("")}</ol>` : ""}
    </div>
  `;
}

function switchView(name) {
  document.querySelectorAll(".nav-item").forEach((btn) => btn.classList.toggle("active", btn.dataset.view === name));
  document.querySelectorAll(".view").forEach((view) => view.classList.toggle("active", view.id === name));
  $("#viewTitle").textContent = views[name][0];
  $("#viewSub").textContent = views[name][1];
}

function formPayload(form) {
  const data = new FormData(form);
  const payload = {};
  for (const [key, value] of data.entries()) {
    payload[key] = value;
  }
  form.querySelectorAll("input[type='number']").forEach((input) => {
    payload[input.name] = Number(input.value);
  });
  form.querySelectorAll("input[type='checkbox']").forEach((input) => {
    payload[input.name] = input.checked;
  });
  return payload;
}

function durationLine(data) {
  return `${data.title ? `${data.title} - ` : ""}${data.durationLabel} - estimated ${data.minClipCount}-${data.maxClipCount} clips, recommended ${data.recommendedClipCount}`;
}

async function analyzeCurrentLink() {
  const form = $("#generateForm");
  const youtube = form.youtube.value.trim();
  const minSeconds = Number(form.minSeconds.value || 30);
  const maxSeconds = Number(form.maxSeconds.value || 50);
  if (!youtube || !youtube.startsWith("http")) {
    $("#analysisBox").innerHTML = `<strong>Paste a YouTube link to analyze duration and estimate clip count.</strong><span>Choose Face + charts or Face only before generating.</span>`;
    return;
  }
  $("#analysisBox").innerHTML = `<strong>Analyzing YouTube video...</strong><span>This reads metadata first, before downloading the stream.</span>`;
  try {
    const data = await api(`/api/analyze?youtube=${encodeURIComponent(youtube)}&minSeconds=${minSeconds}&maxSeconds=${maxSeconds}`);
    form.count.value = data.recommendedClipCount;
    const duplicateText = data.existingManifests && data.existingManifests.length
      ? ` This link already has manifest(s): ${data.existingManifests.join(", ")}. Check "Regenerate even if this link already has a manifest" to create a new one.`
      : "";
    $("#analysisBox").innerHTML = `<strong>${escapeHtml(durationLine(data))}</strong><span>Clip count was filled automatically.${escapeHtml(duplicateText)}</span>`;
  } catch (error) {
    $("#analysisBox").innerHTML = `<strong>Could not analyze link.</strong><span>${escapeHtml(error.message)}</span>`;
  }
}

async function refreshAccounts() {
  const data = await api("/api/accounts");
  state.accounts = data.accounts || [];
  if (!state.accounts.some((account) => account.account === state.activeAccount)) {
    state.activeAccount = state.accounts[0]?.account || "main";
  }
  const markup = state.accounts
    .map((account) => {
      const session = account.loggedIn ? "Saved session" : "Needs login";
      const label = `${account.displayName || account.account} - ${account.account} - ${session}`;
      return `<option value="${escapeHtml(account.account)}">${escapeHtml(label)}</option>`;
    })
    .join("");
  $("#activeAccountSelect").innerHTML = markup;
  $("#uploadAccountSelect").innerHTML = markup;
  $("#activeAccountSelect").value = state.activeAccount;
  $("#uploadAccountSelect").value = state.activeAccount;
  localStorage.setItem("activeTikTokAccount", state.activeAccount);
}

async function refreshAccountLimits() {
  try {
    const data = await api("/api/account-limits");
    state.accountLimits = data.accounts || [];
    renderAccountLimitBar();
  } catch (error) {
    $("#accountLimitBar").innerHTML = `<article class="limit-card limited"><strong>Limit status unavailable</strong><span>${escapeHtml(error.message)}</span></article>`;
  }
}

function renderAccountLimitBar() {
  const limited = state.accountLimits.filter((account) => account.limited);
  if (!limited.length) {
    $("#accountLimitBar").innerHTML = `<article class="limit-card ok"><strong>Account limits clear</strong><span>No active countdowns. Live posts still stop on real TikTok quota or rate-limit errors.</span></article>`;
    return;
  }
  $("#accountLimitBar").innerHTML = limited
    .map((account) => {
      const budget = account.budget || {};
      const seconds = Number(budget.seconds_until_next || 0);
      const reset = formatResetTime(Number(budget.next_allowed_at || budget.blocked_until || 0));
      return `<article class="limit-card limited">
        <div>
          <strong>${escapeHtml(account.displayName || account.account)} <span>${escapeHtml(account.account)}</span></strong>
          <span>${escapeHtml(account.limitReason || "Posting limit")} - ${Number(budget.used_24h || 0)}/${Number(budget.daily_cap || 0)} posts in the automation window</span>
        </div>
        <div class="countdown" data-reset-at="${Number(budget.next_allowed_at || budget.blocked_until || 0)}">${escapeHtml(formatWaitSeconds(seconds))}</div>
        <span class="reset-at">Resets ${escapeHtml(reset)}</span>
      </article>`;
    })
    .join("");
}

async function autoDetectMissingAccountNames() {
  const missing = state.accounts.filter((account) => account.loggedIn && !account.detected);
  for (const account of missing.slice(0, 2)) {
    try {
      await api("/api/account-name", { method: "POST", body: JSON.stringify({ account: account.account }) });
    } catch {
      // Keep the saved label if TikTok does not expose the username for this session.
    }
  }
  if (missing.length) {
    await refreshAccounts();
  }
}

function scheduleAnalyze() {
  clearTimeout(state.analyzeTimer);
  state.analyzeTimer = setTimeout(analyzeCurrentLink, 700);
}

async function refreshManifests() {
  const data = await api("/api/manifests");
  state.manifests = data.manifests;
  renderManifestOptions();
  await refreshUploadQueueSummary();
}

function renderManifestOptions() {
  const selects = [$("#manifestSelect"), $("#uploadManifestSelect")];
  for (const select of selects) {
    const previous = select.value || state.activeManifest;
    select.innerHTML = "";
    for (const manifest of state.manifests) {
      const option = document.createElement("option");
      option.value = manifest.path;
      option.textContent = manifest.displayName || `${manifest.name} (${manifest.count})`;
      select.appendChild(option);
    }
    if (previous) select.value = previous;
  }
  if (!state.activeManifest && state.manifests[0]) state.activeManifest = state.manifests[0].path;
}

async function loadManifest() {
  const selected = $("#manifestSelect").value || state.activeManifest;
  if (!selected) {
    $("#manifestRows").innerHTML = "";
    $("#manifestStats").innerHTML = `<span class="chip">No manifests yet</span>`;
    return;
  }
  state.activeManifest = selected;
  const data = await api(`/api/manifest?path=${encodeURIComponent(selected)}`);
  const counts = data.rows.reduce((acc, row) => {
    acc[row.status] = (acc[row.status] || 0) + 1;
    return acc;
  }, {});
  $("#manifestStats").innerHTML = [
    `<span class="chip">${data.rows.length} total</span>`,
    ...Object.entries(counts).map(([key, value]) => `<span class="chip">${value} ${key}</span>`),
  ].join("");
  $("#manifestRows").innerHTML = data.rows
    .map(
      (row) => `<tr>
        <td>${row.index}</td>
        <td>${row.status}</td>
        <td>${Number(row.duration_seconds).toFixed(0)}s</td>
        <td class="caption-cell">${escapeHtml(row.caption)}</td>
        <td class="clip-cell">${escapeHtml(row.clip_path)}</td>
      </tr>`
    )
    .join("");
}

async function refreshJobs() {
  const data = await api("/api/jobs");
  const priority = { running: 0, queued: 1, stopping: 2, failed: 3, stopped: 4, complete: 5 };
  const jobs = (data.jobs || [])
    .filter((job) => !(job.status === "complete" && job.title === "TikTok login"))
    .slice()
    .sort((a, b) => {
    const left = priority[a.status] ?? 9;
    const right = priority[b.status] ?? 9;
    return left - right;
  });
  $("#jobCount").textContent = jobs.length;
  $("#jobsList").innerHTML =
    jobs
      .map((job) => {
        const logs = Array.isArray(job.logs) ? job.logs.join("\n") : "";
        const progress = job.progress || {};
        const percent = Number(progress.percent || 0);
        const total = Number(progress.total || 0);
        const current = Number(progress.current || 0);
        const label = progress.label || "";
        const canStop = ["queued", "running", "stopping"].includes(job.status || "queued");
        const userMessage = job.userMessage || null;
        return `<article class="job">
          <div class="job-head">
            <strong>${escapeHtml(job.title || "Job")} ${escapeHtml(job.id || "")}</strong>
            <div class="job-actions">
              <span class="status ${escapeHtml(job.status || "queued")}">${escapeHtml(job.status || "queued")}</span>
              ${canStop ? `<button class="job-stop" data-job-id="${escapeHtml(job.id || "")}" title="Stop this job" aria-label="Stop this job">X</button>` : ""}
            </div>
          </div>
          <div class="progress"><span style="width: ${percent}%"></span></div>
          <div class="progress-label">${escapeHtml(label)}${total ? ` - ${current}/${total} - ${percent}%` : ""}</div>
          ${userMessage ? solutionHtml(userMessage) : ""}
          <details class="technical-log">
            <summary>Technical log</summary>
            <pre>${escapeHtml(logs || "Waiting for output...")}</pre>
          </details>
        </article>`;
      })
      .join("") || `<div class="chip">No jobs running</div>`;
  document.querySelectorAll(".job-stop").forEach((button) => {
    button.addEventListener("click", async () => {
      const jobId = button.dataset.jobId;
      if (!jobId) return;
      await api("/api/stop-job", { method: "POST", body: JSON.stringify({ jobId }) });
      await refreshJobs();
    });
  });
}

async function refreshAccountStatus() {
  const account = state.activeAccount || "main";
  try {
    const data = await api(`/api/account?account=${encodeURIComponent(account)}`);
    const el = $("#accountStatus");
    el.className = `account-status ${data.loggedIn ? "ok" : "missing"}`;
    el.textContent = data.loggedIn
      ? `Logged in as ${data.displayName || account}. Saved label: ${account}.${data.detected ? "" : " Username not detected yet."}`
      : `Not logged in for label "${account}". Use Open TikTok first.`;
  } catch (error) {
    $("#accountStatus").textContent = error.message;
  }
}

async function refreshPostedHistory() {
  const account = $("#uploadAccountSelect").value || state.activeAccount || "main";
  try {
    const data = await api(`/api/posts?account=${encodeURIComponent(account)}`);
    const posts = data.posts || [];
    $("#postCount").textContent = posts.length;
    $("#postsList").innerHTML = posts.length
      ? posts
          .slice(0, 50)
          .map(
            (post) => `<article class="post-item">
              <div class="job-head">
                <strong>${escapeHtml(post.account || "unknown")}</strong>
                <span>${escapeHtml(post.uploadedAt || "")}</span>
              </div>
              <div class="caption-cell">${escapeHtml(post.caption || "No caption stored")}</div>
              <div class="clip-cell">${escapeHtml(post.clipPath || "")}</div>
            </article>`
          )
          .join("")
      : `<div class="chip">No posted records for ${escapeHtml(account)} yet</div>`;
  } catch (error) {
    $("#postsList").innerHTML = `<div class="chip">${escapeHtml(error.message)}</div>`;
  }
}

async function refreshUploadQueueSummary() {
  const selected = $("#uploadManifestSelect").value || state.activeManifest;
  const account = $("#uploadAccountSelect").value || state.activeAccount || "main";
  if (!selected) {
    $("#uploadQueueSummary").textContent = "No manifest selected.";
    $("#uploadBudgetSummary").textContent = "Select an account to see posting budget.";
    return;
  }
  try {
    const [data, budget] = await Promise.all([
      api(`/api/manifest?path=${encodeURIComponent(selected)}`),
      api(`/api/upload-budget?account=${encodeURIComponent(account)}`),
    ]);
    const counts = data.rows.reduce((acc, row) => {
      acc[row.status] = (acc[row.status] || 0) + 1;
      return acc;
    }, {});
    state.uploadBudget = budget;
    $("#uploadQueueSummary").textContent = `${counts.ready || 0} ready, ${counts.uploaded || 0} uploaded, ${counts.failed || 0} failed. Live upload will continue from the next ready clip and stop on any TikTok quota signal.`;
    const wait = formatWaitSeconds(Number(budget.seconds_until_next || 0));
    const unlimited = Number(budget.daily_cap || 0) <= 0;
    $("#uploadBudgetSummary").textContent = budget.remaining_24h > 0
      ? (unlimited
          ? "No posting limit for this account. Posts are spaced by the delay below."
          : `${budget.remaining_24h} of ${budget.daily_cap} live posts remain for this account in the current 24-hour automation window.`)
      : `Posting is paused for this account (TikTok blocked it). Next safe window opens in about ${wait}.`;
    $("#uploadBudgetSummary").className = `mode-note wide ${budget.remaining_24h <= 0 ? "live" : ""}`;
    updateUploadMode();
    await refreshAccountLimits();
  } catch (error) {
    state.uploadBudget = null;
    $("#uploadQueueSummary").textContent = error.message;
    $("#uploadBudgetSummary").textContent = "Could not load posting budget.";
    updateUploadMode();
    await refreshAccountLimits();
  }
}

function updateUploadMode() {
  const dryRun = $("#uploadForm").dryRun.checked;
  const budget = state.uploadBudget;
  const liveLocked = !dryRun && budget && Number(budget.remaining_24h || 0) <= 0;
  $("#uploadModeNote").className = `mode-note wide ${dryRun ? "" : "live"}`;
  if (dryRun) {
    $("#uploadModeNote").textContent = "Preview only is on. This will check every ready clip and will not post to TikTok.";
  } else if (liveLocked) {
    $("#uploadModeNote").textContent = `Live upload is paused because TikTok blocked this account. It clears in about ${formatWaitSeconds(Number(budget.seconds_until_next || 0))}.`;
  } else {
    $("#uploadModeNote").textContent = "Live upload is on. There is no post-count limit. Posts are spaced by the delay you set, and the run stops immediately only if TikTok itself returns a quota or rate-limit signal.";
  }
  $("#uploadSubmitBtn").disabled = Boolean(liveLocked);
  $("#uploadSubmitBtn").textContent = dryRun ? "Preview all ready clips" : liveLocked ? "Live posting paused" : "Post now";
}

function formatWaitSeconds(totalSeconds) {
  const seconds = Math.max(0, Math.round(totalSeconds || 0));
  if (seconds <= 0) return "now";
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.ceil((seconds % 3600) / 60);
  if (hours && minutes) return `${hours}h ${minutes}m`;
  if (hours) return `${hours}h`;
  return `${minutes}m`;
}

function formatResetTime(timestampSeconds) {
  const timestamp = Number(timestampSeconds || 0);
  if (!timestamp) return "when the cooldown clears";
  return new Date(timestamp * 1000).toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function tickAccountCountdowns() {
  document.querySelectorAll("[data-reset-at]").forEach((el) => {
    const resetAt = Number(el.dataset.resetAt || 0);
    if (!resetAt) return;
    const seconds = Math.max(0, Math.ceil(resetAt - Date.now() / 1000));
    el.textContent = formatWaitSeconds(seconds);
  });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[char]);
}

document.querySelectorAll(".nav-item").forEach((btn) => {
  btn.addEventListener("click", () => switchView(btn.dataset.view));
});

$("#refreshBtn").addEventListener("click", async () => {
  await refreshManifests();
  await loadManifest();
  await refreshJobs();
});

$("#stopAllBtn").addEventListener("click", async () => {
  if (!confirm("Stop every running job? Current browser or render commands may finish their current step before stopping.")) {
    return;
  }
  await api("/api/stop", { method: "POST", body: JSON.stringify({}) });
  await refreshJobs();
});

$("#loadManifestBtn").addEventListener("click", loadManifest);

["youtube", "minSeconds", "maxSeconds"].forEach((name) => {
  $("#generateForm")[name].addEventListener("input", scheduleAnalyze);
});

$("#generateForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  try {
    await api("/api/generate", { method: "POST", body: JSON.stringify(payload) });
    switchView("review");
    await refreshJobs();
  } catch (error) {
    $("#analysisBox").innerHTML = `<strong>Generate stopped.</strong><span>${escapeHtml(error.message)}</span>`;
  }
});

function setActiveAccount(account) {
  state.activeAccount = account || "main";
  localStorage.setItem("activeTikTokAccount", state.activeAccount);
  $("#activeAccountSelect").value = state.activeAccount;
  $("#uploadAccountSelect").value = state.activeAccount;
}

function nextAccountLabel() {
  const labels = new Set(state.accounts.map((account) => account.account));
  for (let index = 2; index < 1000; index += 1) {
    const label = `account${index}`;
    if (!labels.has(label)) return label;
  }
  return `account${Date.now()}`;
}

async function addAccountAndOpenLogin() {
  const form = $("#addAccountForm");
  const button = $("#addAccountBtn");
  const payload = formPayload(form);
  payload.account = String(payload.account || "").trim() || nextAccountLabel();
  button.disabled = true;
  $("#accountStatus").className = "account-status";
  $("#accountStatus").textContent = `Creating label "${payload.account}" and opening TikTok login...`;
  try {
    const data = await api("/api/account", { method: "POST", body: JSON.stringify(payload) });
    form.reset();
    await refreshAccounts();
    setActiveAccount(data.account);
    await refreshAccountStatus();
    await refreshPostedHistory();
    await api("/api/login", { method: "POST", body: JSON.stringify({ account: data.account, forceOpen: true }) });
    await refreshJobs();
    $("#accountStatus").textContent = `Opening TikTok QR browser for "${data.account}". Scan the QR in the browser window.`;
  } catch (error) {
    $("#accountStatus").className = "account-status missing";
    $("#accountStatus").textContent = error.message;
  } finally {
    button.disabled = false;
  }
}

$("#addAccountBtn").addEventListener("click", addAccountAndOpenLogin);
$("#addAccountForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  await addAccountAndOpenLogin();
});

$("#openAccountBtn").addEventListener("click", async () => {
  const account = $("#activeAccountSelect").value || state.activeAccount || "main";
  setActiveAccount(account);
  await api("/api/login", { method: "POST", body: JSON.stringify({ account, forceOpen: true }) });
  await refreshJobs();
  await refreshAccounts();
  await autoDetectMissingAccountNames();
  await refreshAccountStatus();
  await refreshPostedHistory();
});

$("#detectAccountBtn").addEventListener("click", async () => {
  const account = state.activeAccount || "main";
  $("#accountStatus").textContent = "Detecting TikTok username from saved session...";
  await api("/api/account-name", { method: "POST", body: JSON.stringify({ account }) });
  await refreshAccounts();
  await refreshAccountStatus();
});

$("#forgetAccountBtn").addEventListener("click", async () => {
  const account = state.activeAccount || "main";
  if (account === "main") return;
  if (!confirm(`Forget label "${account}" from the dropdown? This does not delete TikTok itself.`)) return;
  await api("/api/account-forget", { method: "POST", body: JSON.stringify({ account }) });
  state.activeAccount = "main";
  await refreshAccounts();
  await refreshAccountStatus();
  await refreshPostedHistory();
});

$("#activeAccountSelect").addEventListener("change", async (event) => {
  setActiveAccount(event.currentTarget.value);
  await refreshAccountStatus();
  await refreshPostedHistory();
});

$("#uploadAccountSelect").addEventListener("change", async (event) => {
  setActiveAccount(event.currentTarget.value);
  await refreshAccountStatus();
  await refreshUploadQueueSummary();
  await refreshPostedHistory();
});
$("#uploadForm").dryRun.addEventListener("change", updateUploadMode);
$("#uploadManifestSelect").addEventListener("change", refreshUploadQueueSummary);

$("#uploadForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = formPayload(event.currentTarget);
  if (!payload.dryRun && state.uploadBudget && Number(state.uploadBudget.remaining_24h || 0) <= 0) {
    $("#jobsList").innerHTML = `<article class="job failed-immediate">
      <div class="job-head">
        <strong>Upload did not start</strong>
        <span class="status stopped">locked</span>
      </div>
      ${solutionHtml({
        title: "Live posting is locked for this account.",
        cause: `The next safe posting window opens in about ${formatWaitSeconds(Number(state.uploadBudget.seconds_until_next || 0))}.`,
        steps: ["Use Preview only for now.", "Wait for the countdown to clear before posting again.", "Do not keep retrying live uploads while TikTok is limiting the account."],
      })}
    </article>`;
    await refreshAccountLimits();
    return;
  }
  if (
    !payload.dryRun
    && !confirm(
      `Live upload is on. Post all ready clips with no post-count limit? Each post waits a random ${payload.delayMinSeconds}-${payload.delayMaxSeconds} seconds. The run will stop only if TikTok itself returns a quota or rate-limit signal.`
    )
  ) {
    return;
  }
  try {
    await api("/api/upload", { method: "POST", body: JSON.stringify(payload) });
    await refreshJobs();
    await refreshUploadQueueSummary();
    await refreshPostedHistory();
    await refreshAccountLimits();
  } catch (error) {
    const userMessage = error.userMessage || {
      title: "Upload could not start.",
      cause: error.message,
      steps: ["Fix the message above, then try again."],
    };
    $("#jobsList").innerHTML = `<article class="job failed-immediate">
      <div class="job-head">
        <strong>Upload did not start</strong>
        <span class="status failed">failed</span>
      </div>
      ${solutionHtml(userMessage)}
    </article>`;
  }
});

async function boot() {
  await refreshAccounts();
  await refreshAccountLimits();
  await autoDetectMissingAccountNames();
  await refreshManifests();
  await loadManifest();
  await refreshJobs();
  await refreshAccountStatus();
  updateUploadMode();
  await refreshUploadQueueSummary();
  await refreshPostedHistory();
  setInterval(async () => {
    tickAccountCountdowns();
  }, 1000);
  setInterval(async () => {
    await refreshJobs();
    await refreshManifests();
    await refreshPostedHistory();
    await refreshAccountLimits();
  }, 3000);
}

boot().catch((error) => {
  $("#jobsList").innerHTML = `<div class="job"><pre>${escapeHtml(error.message)}</pre></div>`;
});
