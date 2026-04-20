(function () {
  const QUESTION_BANK = Array.isArray(window.questions) ? window.questions : [];
  const PASSING_SCORE_FULL_EXAM = 84;
  const FULL_EXAM_SIZE = 120;
  const STORAGE_PREFIX = "nyc-permit-sim";

  const screens = {
    home: document.getElementById("screen-home"),
    pre: document.getElementById("screen-pre"),
    question: document.getElementById("screen-question"),
    results: document.getElementById("screen-results"),
    mastery: document.getElementById("screen-mastery"),
  };

  const examCardGrid = document.getElementById("exam-card-grid");
  const preTitle = document.getElementById("pre-title");
  const preKicker = document.getElementById("pre-kicker");
  const beginExamButton = document.getElementById("begin-exam-button");
  const preBackButton = document.getElementById("pre-back-button");

  const questionExamPill = document.getElementById("question-exam-pill");
  const questionCounter = document.getElementById("question-counter");
  const questionScorePill = document.getElementById("question-score-pill");
  const progressFill = document.getElementById("progress-fill");
  const questionCategory = document.getElementById("question-category");
  const questionText = document.getElementById("question-text");
  const answerList = document.getElementById("answer-list");
  const feedbackBox = document.getElementById("feedback-box");
  const nextQuestionButton = document.getElementById("next-question-button");

  const resultsKicker = document.getElementById("results-kicker");
  const resultsTitle = document.getElementById("results-title");
  const resultsScore = document.getElementById("results-score");
  const resultsPercentage = document.getElementById("results-percentage");
  const resultsBadge = document.getElementById("results-badge");
  const resultsSubtitle = document.getElementById("results-subtitle");
  const wrongSummary = document.getElementById("wrong-summary");
  const wrongAnswerList = document.getElementById("wrong-answer-list");
  const retryButton = document.getElementById("retry-button");
  const resultsHomeButton = document.getElementById("results-home-button");

  const masteryTitle = document.getElementById("mastery-title");
  const masteryCopy = document.getElementById("mastery-copy");
  const restartExamButton = document.getElementById("restart-exam-button");
  const masteryHomeButton = document.getElementById("mastery-home-button");

  const questionsById = new Map(QUESTION_BANK.map((question) => [question.id, question]));
  const questionsByExam = {
    1: QUESTION_BANK.filter((question) => question.exam === 1),
    2: QUESTION_BANK.filter((question) => question.exam === 2),
    3: QUESTION_BANK.filter((question) => question.exam === 3),
  };

  let state = createDefaultState();

  function createDefaultState(examNumber = null) {
    return {
      currentExam: examNumber,
      phase: "home",
      currentRound: 1,
      poolSize: 0,
      currentIndex: 0,
      correctCount: 0,
      wrongCount: 0,
      wrongPool: [],
      answers: [],
      sessionQuestions: [],
      pendingPool: [],
      masteryAchieved: false,
      masteryRounds: null,
      lastCompleted: null,
      updatedAt: Date.now(),
    };
  }

  function storageKey(examNumber) {
    return `${STORAGE_PREFIX}-exam-${examNumber}`;
  }

  function loadSavedState(examNumber) {
    try {
      const raw = window.localStorage.getItem(storageKey(examNumber));
      if (!raw) {
        return null;
      }

      const parsed = JSON.parse(raw);
      return {
        ...createDefaultState(examNumber),
        ...parsed,
        currentExam: examNumber,
      };
    } catch (error) {
      console.error("Unable to load saved state", error);
      return null;
    }
  }

  function saveState() {
    if (!state.currentExam) {
      return;
    }

    state.updatedAt = Date.now();
    window.localStorage.setItem(storageKey(state.currentExam), JSON.stringify(state));
  }

  function removeState(examNumber) {
    window.localStorage.removeItem(storageKey(examNumber));
  }

  function shuffle(items) {
    const array = [...items];
    for (let i = array.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }

  function setActiveScreen(name) {
    Object.entries(screens).forEach(([screenName, node]) => {
      node.classList.toggle("is-active", screenName === name);
    });
  }

  function showHome() {
    renderHomeCards();
    setActiveScreen("home");
  }

  function prepareFreshExam(examNumber) {
    state = createDefaultState(examNumber);
    state.phase = "pre";
    state.pendingPool = questionsByExam[examNumber].map((question) => question.id);
    state.poolSize = state.pendingPool.length;
    saveState();
    renderPreScreen();
  }

  function renderPreScreen() {
    preKicker.textContent = state.currentRound > 1 ? `Exam ${state.currentExam} retry round` : "Exam setup";
    preTitle.textContent =
      state.currentRound > 1
        ? `Exam ${state.currentExam} — Retry Round ${state.currentRound}`
        : `Exam ${state.currentExam} — Full Practice Test`;

    beginExamButton.textContent =
      state.currentRound > 1 ? `Begin Retry Round (${state.pendingPool.length} questions)` : "Begin Exam";

    setActiveScreen("pre");
  }

  function startRound(poolIds) {
    const shuffledPool = shuffle(poolIds);
    state.phase = "question";
    state.poolSize = shuffledPool.length;
    state.currentIndex = 0;
    state.correctCount = 0;
    state.wrongCount = 0;
    state.wrongPool = [];
    state.answers = [];
    state.pendingPool = [];
    state.sessionQuestions = shuffledPool.map((id) => ({
      id,
      optionOrder: shuffle([0, 1, 2, 3]),
      selectedIndex: null,
    }));
    saveState();
    renderQuestion();
  }

  function beginExam() {
    const nextPool =
      state.pendingPool.length > 0
        ? state.pendingPool
        : questionsByExam[state.currentExam].map((question) => question.id);
    startRound(nextPool);
  }

  function getCurrentQuestionState() {
    return state.sessionQuestions[state.currentIndex] || null;
  }

  function getCurrentQuestion() {
    const sessionQuestion = getCurrentQuestionState();
    if (!sessionQuestion) {
      return null;
    }
    return questionsById.get(sessionQuestion.id);
  }

  function renderQuestion() {
    const sessionQuestion = getCurrentQuestionState();
    const question = getCurrentQuestion();
    if (!sessionQuestion || !question) {
      return;
    }

    questionExamPill.textContent = `Exam ${state.currentExam} • Round ${state.currentRound}`;
    questionCounter.textContent = `Question ${state.currentIndex + 1} / ${state.poolSize}`;
    questionScorePill.textContent = `Correct: ${state.correctCount} | Wrong: ${state.wrongCount}`;
    questionCategory.textContent = question.category;
    questionText.textContent = question.question;

    const answeredCount = state.answers.length;
    progressFill.style.width = `${(answeredCount / state.poolSize) * 100}%`;

    answerList.innerHTML = "";
    const answerIsLocked = sessionQuestion.selectedIndex !== null;

    sessionQuestion.optionOrder.forEach((optionIndex, displayIndex) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "answer-button";
      button.style.animationDelay = `${displayIndex * 60}ms`;
      button.disabled = answerIsLocked;
      button.dataset.index = String(displayIndex);

      const badge = document.createElement("span");
      badge.className = "answer-badge";
      badge.textContent = String.fromCharCode(65 + displayIndex);

      const copy = document.createElement("span");
      copy.className = "answer-copy";
      copy.textContent = question.options[optionIndex];

      button.appendChild(badge);
      button.appendChild(copy);

      if (answerIsLocked) {
        if (optionIndex === question.correct) {
          button.classList.add("correct");
        }
        if (
          sessionQuestion.selectedIndex === displayIndex &&
          optionIndex !== question.correct
        ) {
          button.classList.add("wrong");
        }
      }

      button.addEventListener("click", () => selectAnswer(displayIndex));
      answerList.appendChild(button);
    });

    if (answerIsLocked) {
      const selectedOriginalIndex = sessionQuestion.optionOrder[sessionQuestion.selectedIndex];
      const isCorrect = selectedOriginalIndex === question.correct;
      feedbackBox.hidden = false;
      feedbackBox.className = `feedback-box ${isCorrect ? "correct" : "wrong"}`;

      if (isCorrect) {
        feedbackBox.innerHTML = `<strong>Correct.</strong> ${question.explanation}`;
      } else {
        feedbackBox.innerHTML =
          `<strong>Not quite.</strong> You chose: <span class="wrong-choice">${question.options[selectedOriginalIndex]}</span><br>` +
          `Correct answer: <span class="correct-choice">${question.options[question.correct]}</span><br>` +
          `${question.explanation}`;
      }

      nextQuestionButton.disabled = false;
    } else {
      feedbackBox.hidden = true;
      feedbackBox.className = "feedback-box";
      feedbackBox.textContent = "";
      nextQuestionButton.disabled = true;
    }

    setActiveScreen("question");
  }

  function selectAnswer(displayIndex) {
    const sessionQuestion = getCurrentQuestionState();
    const question = getCurrentQuestion();

    if (!sessionQuestion || !question || sessionQuestion.selectedIndex !== null) {
      return;
    }

    sessionQuestion.selectedIndex = displayIndex;
    const selectedOriginalIndex = sessionQuestion.optionOrder[displayIndex];
    const isCorrect = selectedOriginalIndex === question.correct;

    if (isCorrect) {
      state.correctCount += 1;
    } else {
      state.wrongCount += 1;
      state.wrongPool.push(question.id);
    }

    state.answers.push({
      questionId: question.id,
      question: question.question,
      category: question.category,
      isCorrect,
      selectedOption: question.options[selectedOriginalIndex],
      correctOption: question.options[question.correct],
      explanation: question.explanation,
    });

    saveState();
    renderQuestion();
  }

  function nextQuestion() {
    const sessionQuestion = getCurrentQuestionState();
    if (!sessionQuestion || sessionQuestion.selectedIndex === null) {
      return;
    }

    if (state.currentIndex < state.poolSize - 1) {
      state.currentIndex += 1;
      saveState();
      renderQuestion();
      return;
    }

    endRound();
  }

  function getPassingThreshold(totalQuestions) {
    if (totalQuestions === FULL_EXAM_SIZE) {
      return PASSING_SCORE_FULL_EXAM;
    }
    return Math.ceil(totalQuestions * 0.7);
  }

  function endRound() {
    const total = state.poolSize;
    const score = state.correctCount;
    const percentage = total === 0 ? 0 : Math.round((score / total) * 100);

    state.lastCompleted = {
      exam: state.currentExam,
      round: state.currentRound,
      total,
      score,
      percentage,
      wrongItems: state.answers.filter((entry) => !entry.isCorrect),
      wrongPool: [...state.wrongPool],
    };

    if (state.wrongPool.length === 0) {
      state.phase = "mastery";
      state.masteryAchieved = true;
      state.masteryRounds = state.currentRound;
      saveState();
      renderMastery();
      return;
    }

    state.phase = "results";
    saveState();
    renderResults();
  }

  function animateScore(totalScore, totalQuestions) {
    let current = 0;
    const step = Math.max(1, Math.ceil(totalScore / 18));
    resultsScore.textContent = `0 / ${totalQuestions}`;

    const timer = window.setInterval(() => {
      current = Math.min(totalScore, current + step);
      resultsScore.textContent = `${current} / ${totalQuestions}`;
      if (current >= totalScore) {
        window.clearInterval(timer);
      }
    }, 24);
  }

  function renderResults() {
    const snapshot = state.lastCompleted;
    if (!snapshot) {
      showHome();
      return;
    }

    const threshold = getPassingThreshold(snapshot.total);
    const passed = snapshot.score >= threshold;

    resultsKicker.textContent =
      snapshot.round === 1 ? `Exam ${snapshot.exam} complete` : `Retry round ${snapshot.round} complete`;
    resultsTitle.textContent = `Exam ${snapshot.exam} — Round ${snapshot.round} Results`;
    animateScore(snapshot.score, snapshot.total);
    resultsPercentage.textContent = `${snapshot.percentage}%`;
    resultsBadge.textContent = passed ? "PASS" : "FAIL";
    resultsBadge.className = `metric-chip ${passed ? "pass" : "fail"}`;

    if (snapshot.round === 1) {
      resultsSubtitle.textContent = `Passing score: ${PASSING_SCORE_FULL_EXAM}/${FULL_EXAM_SIZE}. Retry the questions you missed until you reach mastery.`;
    } else {
      resultsSubtitle.textContent =
        "Retry rounds keep only the questions you still miss. Mastery triggers at 100%.";
    }

    wrongSummary.textContent = `Questions You Got Wrong (${snapshot.wrongItems.length})`;
    wrongAnswerList.innerHTML = "";

    snapshot.wrongItems.forEach((item) => {
      const article = document.createElement("article");
      article.className = "wrong-answer-item";
      article.innerHTML =
        `<p class="wrong-answer-question">${item.question}</p>` +
        `<p class="wrong-answer-line"><strong>Your answer:</strong> <span class="wrong-choice">${item.selectedOption}</span></p>` +
        `<p class="wrong-answer-line"><strong>Correct answer:</strong> <span class="correct-choice">${item.correctOption}</span></p>` +
        `<p class="wrong-answer-line">${item.explanation}</p>`;
      wrongAnswerList.appendChild(article);
    });

    retryButton.textContent = `Retry Wrong Answers (${snapshot.wrongPool.length} questions)`;
    retryButton.disabled = snapshot.wrongPool.length === 0;

    setActiveScreen("results");
  }

  function retryWrongAnswers() {
    const snapshot = state.lastCompleted;
    if (!snapshot || snapshot.wrongPool.length === 0) {
      return;
    }

    state.currentRound += 1;
    state.pendingPool = [...snapshot.wrongPool];
    saveState();
    renderPreScreen();
  }

  function renderMastery() {
    masteryTitle.textContent = `Mastery Achieved — Exam ${state.currentExam}`;
    masteryCopy.textContent = `You cleared every remaining question in ${state.masteryRounds} round${
      state.masteryRounds === 1 ? "" : "s"
    }. You can restart this exam any time for a fresh shuffle.`;
    setActiveScreen("mastery");
  }

  function clearExamProgress(examNumber) {
    removeState(examNumber);
    if (state.currentExam === examNumber) {
      state = createDefaultState();
    }
    renderHomeCards();
  }

  function resumeExam(examNumber) {
    const saved = loadSavedState(examNumber);
    if (!saved) {
      prepareFreshExam(examNumber);
      return;
    }

    state = saved;
    switch (state.phase) {
      case "pre":
        renderPreScreen();
        break;
      case "question":
        renderQuestion();
        break;
      case "results":
        renderResults();
        break;
      case "mastery":
        renderMastery();
        break;
      default:
        prepareFreshExam(examNumber);
        break;
    }
  }

  function getCardStatus(saved) {
    if (!saved) {
      return {
        label: "Not Started",
        badgeClass: "fresh",
        description: "Fresh exam ready. 120 questions and adaptive retry rounds.",
        primaryAction: "start",
        primaryLabel: "Start Exam",
      };
    }

    if (saved.masteryAchieved) {
      return {
        label: "Mastered",
        badgeClass: "mastered",
        description: `Completed in ${saved.masteryRounds} round${saved.masteryRounds === 1 ? "" : "s"}. Restart for a new shuffle.`,
        primaryAction: "restart",
        primaryLabel: "Restart Exam",
      };
    }

    const roundLabel = saved.currentRound > 1 ? `Retry Round ${saved.currentRound}` : "Round 1";
    return {
      label: "In Progress",
      badgeClass: "progress",
      description: `${roundLabel} saved locally. Resume where you left off.`,
      primaryAction: "resume",
      primaryLabel: saved.currentRound > 1 ? "Resume Retry" : "Resume Exam",
    };
  }

  function renderHomeCards() {
    examCardGrid.innerHTML = "";

    [1, 2, 3].forEach((examNumber) => {
      const saved = loadSavedState(examNumber);
      const cardStatus = getCardStatus(saved);

      const article = document.createElement("article");
      article.className = "exam-card";
      article.innerHTML =
        `<div class="exam-card-header">` +
        `<div><p class="eyebrow">Practice set</p><h2 class="exam-title">Exam ${examNumber}</h2></div>` +
        `<span class="status-badge ${cardStatus.badgeClass}">${cardStatus.label}</span>` +
        `</div>` +
        `<p class="exam-meta">${cardStatus.description}</p>` +
        `<div class="exam-card-actions">` +
        `<button class="primary-button" type="button" data-action="${cardStatus.primaryAction}" data-exam="${examNumber}">${cardStatus.primaryLabel}</button>` +
        `<button class="secondary-button" type="button" data-action="restart" data-exam="${examNumber}">Restart</button>` +
        `</div>` +
        `<div class="cta-row"><button class="clear-button" type="button" data-action="clear" data-exam="${examNumber}">Clear Progress</button></div>`;

      examCardGrid.appendChild(article);
    });
  }

  function handleCardAction(event) {
    const button = event.target.closest("[data-action]");
    if (!button) {
      return;
    }

    const action = button.dataset.action;
    const examNumber = Number(button.dataset.exam);

    if (!examNumber) {
      return;
    }

    if (action === "start") {
      prepareFreshExam(examNumber);
      return;
    }

    if (action === "resume") {
      resumeExam(examNumber);
      return;
    }

    if (action === "restart") {
      removeState(examNumber);
      prepareFreshExam(examNumber);
      return;
    }

    if (action === "clear") {
      clearExamProgress(examNumber);
    }
  }

  function guardQuestionBank() {
    const bankOkay =
      QUESTION_BANK.length === 360 &&
      questionsByExam[1].length === 120 &&
      questionsByExam[2].length === 120 &&
      questionsByExam[3].length === 120;

    if (bankOkay) {
      return true;
    }

    examCardGrid.innerHTML =
      `<article class="exam-card">` +
      `<div class="exam-card-header"><div><p class="eyebrow">Data issue</p><h2 class="exam-title">Question Bank Error</h2></div></div>` +
      `<p class="exam-meta">The app expected 360 questions split into 120 per exam. Check questions.js and rebuild the dataset if needed.</p>` +
      `</article>`;
    return false;
  }

  examCardGrid.addEventListener("click", handleCardAction);
  beginExamButton.addEventListener("click", beginExam);
  preBackButton.addEventListener("click", showHome);
  nextQuestionButton.addEventListener("click", nextQuestion);
  retryButton.addEventListener("click", retryWrongAnswers);
  resultsHomeButton.addEventListener("click", showHome);
  restartExamButton.addEventListener("click", () => {
    if (!state.currentExam) {
      showHome();
      return;
    }
    removeState(state.currentExam);
    prepareFreshExam(state.currentExam);
  });
  masteryHomeButton.addEventListener("click", showHome);

  if (guardQuestionBank()) {
    showHome();
  }
})();
