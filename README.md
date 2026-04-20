# NYC Permit Exam Simulator

Static web app for New York permit practice with:

- 3 exams
- 120 questions per exam
- wrong-answer retry rounds
- localStorage progress saving
- offline usage after files are present locally

## Files

- `index.html` - app shell and screen structure
- `style.css` - all styling and responsive layout
- `app.js` - exam flow, retry logic, mastery handling, localStorage
- `questions.js` - generated 360-question dataset
- `build_questions.py` - dataset generator
- `NYC_Permit_Test_PRD.md` - copied PRD for in-project reference
- `permit_quiz_patterns.md` - source-study notes used during planning

## Rebuild the dataset

```bash
python build_questions.py
```

## Verify the project

```bash
python verify_project.py
```

## Run

Open `index.html` in a modern browser.

## Notes

- The app stores per-exam progress in the browser with keys that begin with `nyc-permit-sim`.
- The question set was structured from the reviewed NY permit manual and practice-quiz patterns in this workspace.
