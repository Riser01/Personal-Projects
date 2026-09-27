/**
 * Client controller for Murder Mystery Engine
 */

let currentSession = null;
let activeSuspectId = null;

// DOM Elements
const caseSelector = document.getElementById("caseSelector");
const caseTitle = document.getElementById("caseTitle");
const caseVictim = document.getElementById("caseVictim");
const caseScene = document.getElementById("caseScene");
const caseSynopsis = document.getElementById("caseSynopsis");
const timeOfDeath = document.getElementById("timeOfDeath");
const turnCounter = document.getElementById("turnCounter");
const suspectsList = document.getElementById("suspectsList");
const chatHistory = document.getElementById("chatHistory");
const questionForm = document.getElementById("questionForm");
const questionInput = document.getElementById("questionInput");
const cluesList = document.getElementById("cluesList");
const clueCount = document.getElementById("clueCount");
const activeSuspectHeader = document.getElementById("activeSuspectHeader");
const activeSuspectSubheader = document.getElementById("activeSuspectSubheader");
const courtroomBtn = document.getElementById("courtroomBtn");
const accusationModal = document.getElementById("accusationModal");
const closeModalBtn = document.getElementById("closeModalBtn");
const cancelAccusationBtn = document.getElementById("cancelAccusationBtn");
const submitAccusationBtn = document.getElementById("submitAccusationBtn");
const accuseSuspectSelect = document.getElementById("accuseSuspectSelect");
const accuseWeaponInput = document.getElementById("accuseWeaponInput");
const accuseMotiveInput = document.getElementById("accuseMotiveInput");
const scoreModal = document.getElementById("scoreModal");
const restartBtn = document.getElementById("restartBtn");

// Initialize Session
async function loadSession(caseId = "case_blackwood") {
  try {
    const res = await fetch(`/api/session?case_id=${caseId}`);
    currentSession = await res.json();
    renderCaseDetails();
    renderSuspects();
    renderClues(currentSession.unlocked_clues);
    chatHistory.innerHTML = `
      <div class="text-center py-12 text-zinc-500 text-xs italic">
        Select a suspect on the left and ask questions to uncover contradictions.
      </div>
    `;
    if (currentSession.suspects && currentSession.suspects.length > 0) {
      selectSuspect(currentSession.suspects[0].id);
    }
  } catch (err) {
    console.error("Failed to load session:", err);
  }
}

function renderCaseDetails() {
  caseTitle.textContent = currentSession.title;
  caseVictim.textContent = currentSession.victim;
  caseScene.textContent = currentSession.crime_scene;
  caseSynopsis.textContent = currentSession.synopsis;
  timeOfDeath.textContent = currentSession.time_of_death;
  turnCounter.textContent = `Turns Left: ${currentSession.remaining_turns}`;
}

function renderSuspects() {
  suspectsList.innerHTML = "";
  accuseSuspectSelect.innerHTML = "";

  currentSession.suspects.forEach((s) => {
    // Left card
    const card = document.createElement("div");
    card.id = `card-${s.id}`;
    card.className = `p-3 rounded-xl border border-zinc-800 bg-zinc-950/60 hover:border-amber-500/50 cursor-pointer transition text-xs space-y-1.5 ${activeSuspectId === s.id ? 'border-amber-500 bg-amber-500/10' : ''}`;
    card.onclick = () => selectSuspect(s.id);

    card.innerHTML = `
      <div class="flex items-center justify-between">
        <strong class="text-white text-xs">${s.name}</strong>
        <span class="text-[10px] text-zinc-400 font-mono">${s.role}</span>
      </div>
      <p class="text-[11px] text-zinc-400 line-clamp-2">${s.bio}</p>
      <div class="text-[10px] text-zinc-500"><strong class="text-zinc-400">Alibi:</strong> ${s.alibi}</div>
    `;
    suspectsList.appendChild(card);

    // Modal option
    const opt = document.createElement("option");
    opt.value = s.id;
    opt.textContent = `${s.name} (${s.role})`;
    accuseSuspectSelect.appendChild(opt);
  });
}

function selectSuspect(suspectId) {
  activeSuspectId = suspectId;
  const suspect = currentSession.suspects.find((s) => s.id === suspectId);
  if (!suspect) return;

  activeSuspectHeader.textContent = `Interrogating: ${suspect.name}`;
  activeSuspectSubheader.textContent = `${suspect.role} · Memory checkpointer active`;

  // Highlight selected card
  document.querySelectorAll("#suspectsList > div").forEach((el) => {
    el.classList.remove("border-amber-500", "bg-amber-500/10");
  });
  const activeCard = document.getElementById(`card-${suspectId}`);
  if (activeCard) activeCard.classList.add("border-amber-500", "bg-amber-500/10");
}

function renderClues(clues) {
  clueCount.textContent = `${clues.length} Unlocked`;
  if (!clues || clues.length === 0) {
    cluesList.innerHTML = `
      <div class="text-center py-8 text-zinc-500 text-xs italic">
        Clues unlock when your interrogation touches crucial keywords or contradictions.
      </div>
    `;
    return;
  }

  cluesList.innerHTML = clues
    .map((c) => `
      <div class="p-3 bg-zinc-950/70 border border-amber-500/30 rounded-xl space-y-1 text-xs animate-fade-in shadow-md">
        <div class="flex items-center justify-between">
          <span class="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">
            ${c.category}
          </span>
          <i class="fa-solid fa-fingerprint text-amber-500/60"></i>
        </div>
        <h4 class="font-bold text-white text-xs">${c.title}</h4>
        <p class="text-zinc-400 text-[11px] leading-relaxed">${c.description}</p>
      </div>
    `)
    .join("");
}

// Question Submission
questionForm.onsubmit = async (e) => {
  e.preventDefault();
  const q = questionInput.value.trim();
  if (!q || !activeSuspectId) return;

  questionInput.value = "";
  appendChatMessage("Detective", q, true);

  try {
    const res = await fetch("/api/interrogate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ suspect_id: activeSuspectId, question: q }),
    });
    const data = await res.json();

    appendChatMessage(data.suspect_name, data.answer, false);
    turnCounter.textContent = `Turns Left: ${data.remaining_turns}`;

    if (data.clues_unlocked && data.clues_unlocked.length > 0) {
      // Re-fetch full clue list
      const cluesRes = await fetch("/api/clues");
      const fullClues = await cluesRes.json();
      renderClues(fullClues);
    }
  } catch (err) {
    appendChatMessage("System", "Failed to contact suspect agent.", false);
  }
};

function appendChatMessage(sender, text, isUser) {
  const msg = document.createElement("div");
  msg.className = `p-3 rounded-xl text-xs space-y-1 ${
    isUser 
      ? 'bg-amber-600/15 border border-amber-500/30 text-zinc-100 ml-6' 
      : 'bg-zinc-950/80 border border-zinc-800 text-zinc-200 mr-6'
  }`;

  msg.innerHTML = `
    <div class="flex items-center justify-between">
      <strong class="${isUser ? 'text-amber-400' : 'text-zinc-300'} font-semibold">${sender}</strong>
      <span class="text-[10px] text-zinc-500 font-mono">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
    </div>
    <p class="leading-relaxed">${text}</p>
  `;

  chatHistory.appendChild(msg);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Prompt Chips
document.querySelectorAll(".prompt-chip").forEach((btn) => {
  btn.onclick = () => {
    questionInput.value = btn.textContent.replace(/^"|"$/g, "");
    questionInput.focus();
  };
});

// Modal Handlers
courtroomBtn.onclick = () => accusationModal.classList.remove("hidden");
closeModalBtn.onclick = () => accusationModal.classList.add("hidden");
cancelAccusationBtn.onclick = () => accusationModal.classList.add("hidden");

// Submit Accusation
submitAccusationBtn.onclick = async () => {
  const accusedId = accuseSuspectSelect.value;
  const weapon = accuseWeaponInput.value.trim();
  const motive = accuseMotiveInput.value.trim();

  if (!weapon || !motive) {
    alert("Please state both the murder weapon and your motive theory.");
    return;
  }

  try {
    const res = await fetch("/api/accuse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        accused_suspect_id: accusedId,
        accused_weapon: weapon,
        motive_theory: motive,
        cited_clue_ids: [],
      }),
    });
    const scorecard = await res.json();
    accusationModal.classList.add("hidden");
    showScorecard(scorecard);
  } catch (err) {
    alert("Error submitting indictment.");
  }
};

function showScorecard(scorecard) {
  const scoreIcon = document.getElementById("scoreIcon");
  const scoreTitle = document.getElementById("scoreTitle");
  const scoreRank = document.getElementById("scoreRank");
  const scoreTotal = document.getElementById("scoreTotal");
  const scoreCulpritMatch = document.getElementById("scoreCulpritMatch");
  const scoreWeaponMatch = document.getElementById("scoreWeaponMatch");
  const scoreMotivePoints = document.getElementById("scoreMotivePoints");
  const truthCulprit = document.getElementById("truthCulprit");
  const truthMotive = document.getElementById("truthMotive");
  const truthWeapon = document.getElementById("truthWeapon");

  if (scorecard.is_solved) {
    scoreIcon.className = "w-16 h-16 rounded-full mx-auto flex items-center justify-center text-3xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
    scoreIcon.innerHTML = `<i class="fa-solid fa-trophy"></i>`;
    scoreTitle.textContent = "CASE SOLVED!";
  } else {
    scoreIcon.className = "w-16 h-16 rounded-full mx-auto flex items-center justify-center text-3xl bg-red-500/20 text-red-400 border border-red-500/30";
    scoreIcon.innerHTML = `<i class="fa-solid fa-skull"></i>`;
    scoreTitle.textContent = "CASE UNSOLVED!";
  }

  scoreRank.textContent = scorecard.rank;
  scoreTotal.textContent = `${scorecard.total_score} / 100`;
  scoreCulpritMatch.textContent = scorecard.culprit_match ? "✓ Correct" : "✗ Wrong Suspect";
  scoreCulpritMatch.className = scorecard.culprit_match ? "text-emerald-400" : "text-red-400";
  scoreWeaponMatch.textContent = scorecard.weapon_match ? "✓ Identified" : "✗ Inaccurate";
  scoreWeaponMatch.className = scorecard.weapon_match ? "text-emerald-400" : "text-amber-400";
  scoreMotivePoints.textContent = `${scorecard.motive_score} / 40 Pts`;

  truthCulprit.textContent = scorecard.ground_truth_culprit;
  truthMotive.textContent = scorecard.ground_truth_motive;
  truthWeapon.textContent = scorecard.ground_truth_weapon;

  scoreModal.classList.remove("hidden");
}

restartBtn.onclick = () => {
  scoreModal.classList.add("hidden");
  loadSession(caseSelector.value);
};

caseSelector.onchange = (e) => {
  loadSession(e.target.value);
};

// Start
loadSession();
