# PRD: NYC Road Test Permit Mock Exam Web App

---

## 1. PROJECT OVERVIEW

**Product Name:** NYC Permit Practice — Road Test Exam Simulator  
**Type:** Single-file or multi-file static web application (HTML/CSS/JS, no backend required)  
**Target User:** NYC residents studying for the NY DMV written permit test  
**Goal:** Simulate the real NYC permit exam experience across 3 full exams of 120 questions each, with an adaptive wrong-answer retry loop that repeats until mastery.

---

## 2. QUESTION DATA — SOURCING INSTRUCTIONS

**Priority 1 — Scrape from your own data source:**
- Check any documents, PDFs, or datasets you have on NYC permit test questions.
- Extract all Q&A pairs: question text, 4 answer options (A/B/C/D), and the correct answer.
- Categorize each question if possible (e.g., Road Signs, Traffic Laws, Right of Way, Speed Limits, DUI/Alcohol, Parking, Emergencies).

**Priority 2 — If you have no data to scrape:**
- Pull questions from the official NYS DMV handbook: https://dmv.ny.gov/driver-license/get-driver-license-permit
- Supplement with practice questions from:
  - https://www.dmv-written-test.com/new-york/
  - https://driving-tests.org/new-york/
  - https://www.epermittest.com/new-york
- Aim for questions that reflect actual NY DMV test content: signs, signals, laws, alcohol/drug rules, right-of-way, speed limits, fines/penalties.

**Question Pool Target:**
- **360 total questions** (3 exams × 120 questions each)
- All 360 questions must be unique — no repeats across exams
- Each question must have exactly 4 answer options
- One and only one correct answer per question
- Store all questions in a structured JS array or JSON file (see Section 7)

---

## 3. CORE FEATURES

### 3.1 Three Full Exams
- Exam 1, Exam 2, Exam 3 — each with 120 unique questions
- User can select which exam to take from the home screen
- Each exam is independent (separate progress, separate wrong-answer pools)

### 3.2 Exam Flow
1. User selects an exam
2. Questions are presented one at a time
3. User selects an answer (A, B, C, or D)
4. Immediate feedback:
   - ✅ Correct: green highlight, brief confirmation
   - ❌ Wrong: red highlight on selected answer + green highlight on correct answer + a short explanation if available
5. User clicks "Next" to proceed
6. After all 120 questions: show Results Screen

### 3.3 Results Screen
- Total score (e.g., 94/120)
- Percentage
- Pass/Fail indicator (NYS passing score is 70% — 84/120)
- List of all wrong answers (question + what user chose + correct answer)
- Two buttons:
  - **"Retry Wrong Answers"** — starts a new sub-exam with only the wrong questions
  - **"Back to Menu"**

### 3.4 Wrong Answer Retry Loop (Per Exam)
This is the adaptive mastery loop. It works per exam independently.

**Loop logic:**
```
Round 1: Take full 120-question exam
  → Get some wrong
Round 2 (Retry): Take exam with only wrong questions from Round 1
  → Get some wrong again
Round 3 (Retry): Take exam with only wrong questions from Round 2
  → Repeat until score is 100%
When score = 100%:
  → Show "Mastery Achieved" screen
  → Option to restart that exam from scratch (reshuffled)
```

**Important:**
- Wrong questions from each retry round replace the pool — only carry forward what's still wrong
- Questions should be **reshuffled** every retry round (randomize order)
- Answer choices should also be **reshuffled** each round (randomize A/B/C/D order)

### 3.5 Session Persistence (localStorage)
- Store wrong-answer pools per exam in `localStorage`
- If user closes and reopens the browser:
  - Resume where they left off in the retry loop
  - Show "Resume [Exam X] Retry Round [N]" on the home screen
- Store keys per exam: `exam1_wrong`, `exam2_wrong`, `exam3_wrong`, `exam1_round`, etc.
- Add a "Clear Progress" button per exam on the home screen

---

## 4. UI/UX DESIGN SPECIFICATION

### 4.1 Aesthetic Direction
**Theme:** Clean, authoritative, NYC-inspired — think MTA signage meets modern gov-tech  
**Color Palette:**
- Background: `#0d1117` (near-black)
- Surface/Cards: `#161b22`
- Accent Primary: `#2563eb` (strong blue — DMV/gov blue)
- Accent Correct: `#16a34a` (green)
- Accent Wrong: `#dc2626` (red)
- Text Primary: `#f0f6fc`
- Text Secondary: `#8b949e`
- Border: `#30363d`

**Typography:**
- Display/Headers: `"Barlow Condensed"` (bold, condensed — feels official)
- Body/Questions: `"DM Sans"` or `"IBM Plex Sans"`
- Load from Google Fonts

**Feel:** Government-serious but modern. Not boring. High contrast. Clean grid. Feels like a real test environment.

### 4.2 Screen Breakdown

#### Screen 1: Home / Exam Select
- Large header: "NYC PERMIT EXAM SIMULATOR"
- Subtitle: "3 Full Practice Exams • Adaptive Retry • 120 Questions Each"
- Three exam cards side by side:
  - Exam 1, Exam 2, Exam 3
  - Each card shows: title, status (Not Started / In Progress / Mastered), current retry round if applicable
  - Buttons: "Start Exam" or "Resume Retry" or "Restart"
  - Small "Clear Progress" link below each card
- Footer: "Based on official NYS DMV handbook content"

#### Screen 2: Pre-Exam Info Screen
- Exam title (e.g., "Exam 1 — Full Practice Test")
- Rules list:
  - 120 questions
  - Passing score: 70% (84/120)
  - No time limit
  - Wrong answers will be tracked for retry
- "Begin Exam" button

#### Screen 3: Question Screen
- Top bar:
  - Left: Exam name + "Round [N]"
  - Center: Question counter "Question 14 / 120"
  - Right: Score tracker "Correct: 13 | Wrong: 0"
- Progress bar (thin, full width, fills as questions are answered)
- Question text (large, readable — at least 18px)
- 4 answer buttons (full-width, stacked vertically):
  - Default: dark surface, white text, blue left border
  - Hover: slight blue glow
  - Selected correct: green background + ✓ icon
  - Selected wrong: red background + ✗ icon + correct answer highlighted green
- "Next Question" button (appears after answer is selected, disabled until then)
- Optional: small category tag on question (e.g., "Road Signs")

#### Screen 4: Results Screen
- Large score display: "94 / 120"
- Percentage ring or bar
- PASS / FAIL badge (green or red)
- Section: "Questions You Got Wrong" — collapsible list:
  - Each item shows: question text, your answer (red), correct answer (green)
- Two CTA buttons:
  - "Retry Wrong Answers ([N] questions)" — primary
  - "Back to Menu" — secondary

#### Screen 5: Mastery Screen (triggers when retry round = 100%)
- Full-screen overlay or dedicated screen
- "🏆 Mastery Achieved — Exam [X]"
- Confetti or animation (CSS-only or canvas)
- Summary of how many rounds it took
- Button: "Restart Exam from Scratch" | "Back to Menu"

---

## 5. INTERACTION & FUNCTIONAL RULES

- **Every button must work.** No dead links, no placeholder actions.
- After selecting an answer, the user cannot change it — lock all 4 options.
- The "Next Question" button should only appear/activate after an answer is selected.
- Wrong answer feedback must always show: which answer the user picked AND which is correct.
- Questions and answer choices must be reshuffled on every new round (including retry rounds).
- The app must function fully offline (no API calls, no server).
- No time limit — this is a study tool, not a timed test.

---

## 6. DATA STRUCTURE

Store all questions in a JavaScript array. Each question object must follow this schema:

```js
{
  id: 1,                          // Unique integer across all exams
  exam: 1,                        // Which exam this belongs to: 1, 2, or 3
  category: "Road Signs",         // Category string (for display tag)
  question: "What does a red octagon sign mean?",
  options: [
    "Yield to oncoming traffic",
    "Stop completely",
    "Slow down ahead",
    "No entry"
  ],
  correct: 1,                     // Index of correct answer (0-based)
  explanation: "A red octagon is always a STOP sign under US traffic law."
                                  // Optional but recommended — shown after wrong answer
}
```

- 360 total question objects
- `exam: 1` → questions 1–120
- `exam: 2` → questions 121–240
- `exam: 3` → questions 241–360
- Store in `questions.js` (or inline in `index.html` if single-file)

---

## 7. FILE STRUCTURE

```
nyc-permit-exam/
│
├── index.html          ← Main app shell, all screens rendered here
├── style.css           ← All styles (or inline in <style> tag)
├── app.js              ← All logic: routing, exam engine, localStorage, scoring
├── questions.js        ← All 360 question objects exported as a JS array
└── README.md           ← Optional: notes for future updates
```

If building as a **single-file app**, everything goes into `index.html` in this order:
1. `<head>` with Google Fonts + meta tags
2. `<style>` block — all CSS
3. `<body>` — all screen HTML (screens hidden/shown via JS)
4. `<script>` — questions array first, then app logic

---

## 8. STEP-BY-STEP BUILD GUIDE

Follow these steps in order:

### Step 1: Source & Structure Questions
- Scrape or find 360 unique NYC permit test Q&As
- Format them into the JS object schema defined in Section 6
- Validate: every question has 4 options, one correct index, belongs to exam 1/2/3
- Save as `questions.js`

### Step 2: Build HTML Skeleton
- Create `index.html`
- Add 5 `<div>` sections (one per screen): `#screen-home`, `#screen-pre`, `#screen-question`, `#screen-results`, `#screen-mastery`
- All screens hidden by default (`display: none`) except home
- Add Google Fonts link in `<head>`

### Step 3: Build CSS
- Apply color palette from Section 4.1 using CSS variables (`:root`)
- Style each screen component: cards, buttons, progress bar, answer options, result badges
- Add hover states, transitions (200–300ms ease), and focus-visible outlines for accessibility
- Make it responsive: works on mobile (375px+) and desktop
- Answer buttons: full-width, min 56px height, left border accent, pointer cursor
- Correct/wrong states applied via `.correct` and `.wrong` CSS classes toggled by JS

### Step 4: Build App Logic (`app.js`)
Implement in this order:

1. **State object** — holds: `currentExam`, `currentRound`, `currentIndex`, `score`, `wrongPool`, `answers`
2. **`loadExam(examNumber)`** — filters questions by exam, shuffles, sets state, shows pre-screen
3. **`startRound(pool)`** — takes question array, shuffles, renders first question
4. **`renderQuestion(index)`** — displays question text + shuffled options, resets button states
5. **`selectAnswer(optionIndex)`** — locks buttons, checks correct, applies green/red classes, shows explanation if wrong, logs to wrongPool, updates score counter, shows Next button
6. **`nextQuestion()`** — increments index, calls renderQuestion or endRound
7. **`endRound()`** — calculates score, renders results screen, saves wrongPool to localStorage
8. **`retryWrong()`** — loads wrongPool as new round, increments round counter, calls startRound
9. **`checkMastery()`** — if wrongPool is empty after a round, show mastery screen
10. **`saveProgress()`** — writes state to localStorage after every question
11. **`loadProgress()`** — on home screen load, checks localStorage for in-progress exams
12. **`clearProgress(examNumber)`** — wipes localStorage keys for that exam, resets card UI

### Step 5: Wire Up All Buttons
- Every button must have an event listener or `onclick` handler
- No button should be a dead end
- Test every possible click path:
  - Home → Pre → Question → Results → Retry → Results → Retry → Mastery → Home
  - Home → Pre → Question → Results → Back to Menu → Home
  - Home → Clear Progress → Home (reset)

### Step 6: localStorage Integration
- On every answer submission: save `{ wrongPool, round, index, score }` per exam
- On page load: check localStorage, update home screen cards accordingly
- On "Clear Progress": remove only that exam's keys

### Step 7: Polish & Animations
- Progress bar: smooth CSS `transition: width 0.3s ease`
- Answer buttons: fade in on question load (`@keyframes fadeInUp` with stagger delay)
- Results screen: score count-up animation (JS `setInterval` from 0 to final score)
- Mastery screen: CSS confetti or particle burst (canvas or pure CSS `@keyframes`)
- Hover on exam cards: subtle lift (`transform: translateY(-3px)`, `box-shadow` glow)

### Step 8: Testing Checklist
Before shipping, verify:
- [ ] All 360 questions load correctly
- [ ] No duplicate question IDs
- [ ] Every wrong answer shows correct answer highlighted
- [ ] Retry loop only shows previous round's wrong questions
- [ ] 100% score triggers mastery screen (not results screen)
- [ ] localStorage saves and restores correctly after page refresh
- [ ] Clear Progress fully resets that exam
- [ ] All 3 exams work independently
- [ ] App works on mobile (test at 375px width)
- [ ] No console errors

---

## 9. PASSING CRITERIA (NYS DMV Standard)

- NYS permit test passing score: **70% correct**
- For 120 questions: passing = **84 or more correct**
- Display PASS in green if ≥ 84, FAIL in red if < 84
- Show this threshold clearly on the pre-exam screen and results screen

---

## 10. OUT OF SCOPE (Do Not Build)

- User accounts or login
- Backend server or database
- Timed exam mode
- Leaderboards
- Analytics/tracking
- PDF export of results

---

## 11. DELIVERABLE

A fully working static web app — either:
- **Single file:** `index.html` (all CSS + JS inline) — preferred for portability
- **OR multi-file:** `index.html` + `style.css` + `app.js` + `questions.js`

The app must run by opening `index.html` in any modern browser with no build step, no server, no dependencies other than Google Fonts (loaded via CDN).

---

*PRD Version 1.0 — NYC Permit Exam Simulator*
