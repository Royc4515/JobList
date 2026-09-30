---
description: Submit the applications Roy approved - builds the tailored CVs, gets the transcript, fills each form, and waits for Roy's "שלח" before every submit.
---

You are submitting job applications that Roy has already approved. The source of
truth is `submissions/2026-09-30-packages.md` (links, form answers, notes per role).
Talk to Roy in Hebrew. Use a browser: the Desktop app's built-in Browser pane, or
Claude in Chrome - whichever is available. Roy is logged in there.

## 0. Get the latest repo
`git fetch origin` and, if `submissions/2026-09-30-packages.md` is missing, check out
`claude/hemispheric-outreach-message-sjqtfk` and pull. Read the packages file, `PROFILE.md`
and `CLAUDE.md`.

## 1. Build the application files (no help from Roy needed)
Work in `~/Documents/JobList-CVs/` (create it). **Never put these files in the repo -
it is public and they contain Roy's phone number, email and ID number.**
1. **Base CV:** find `Roy_Carmelli_CV_sep2026.docx` - first on this computer (Google
   Drive folder, Downloads, Documents); otherwise open drive.google.com in the browser,
   search for it and download it. It is the base CV Roy approved edits to.
2. **Tailored CVs:** `pip install python-docx pypdf` if needed, then
   `python scripts/tailor_cv.py <base.docx> ~/Documents/JobList-CVs`. It writes the five
   approved versions (Google, Marvell, FIL, OptimumEDA, AmazonMLIL).
3. **PDF:** export each `.docx` to PDF with Word (or LibreOffice). Open each PDF and
   check it is **exactly one page**. If one spills over, stop and tell Roy - do not
   edit the text yourself.
4. **Transcript:** if `Roy_Carmelli_Transcript_EN.pdf` is not already in Downloads,
   open Bar-Ilan's Inbar in the browser and download the **English** grade transcript
   (גיליון ציונים באנגלית). If Inbar asks for a login or a code, stop and ask Roy.
   Save it as `Roy_Carmelli_Transcript_EN.pdf`. Do not edit it.
5. **Amazon file:** merge `Roy_Carmelli_CV_AmazonMLIL.pdf` + the transcript into
   `Roy_Carmelli_CV_and_Transcript_Amazon.pdf` (pypdf).
6. Show Roy the folder listing and page counts in one short message, then continue.

## 2. Submit, one role at a time
Order: **Google, Amazon MLIL, FIL Robotics, Optimum EDA, Marvell.** For each:
1. Open the apply link from the package. If the posting is closed, say so and skip it.
2. Fill the form with the package's form answers (GPA **85.09**, graduation **Feb 2028**,
   **2-3 days/week**). Upload only that role's files:
   - Google: `Roy_Carmelli_CV_Google.pdf` + `Roy_Carmelli_Transcript_EN.pdf`
   - Amazon MLIL: `Roy_Carmelli_CV_and_Transcript_Amazon.pdf`
   - FIL: `Roy_Carmelli_CV_FIL.pdf` · Optimum EDA: `Roy_Carmelli_CV_OptimumEDA.pdf` ·
     Marvell: `Roy_Carmelli_CV_Marvell.pdf`
3. Paste that role's note from the package into any free-text / cover-letter field.
4. **Stop before the final Submit.** Send Roy a short Hebrew summary (role, file
   uploaded, answers filled, note) and wait. Click Submit **only** after Roy writes
   "שלח". Anything else - fix what he asks, or skip the role if he says so.
5. Questions the package does not answer (salary, ID number, date of birth, "how did
   you hear about us", and so on): ask Roy; never guess.

## Hard rules
- Never type passwords, create accounts, or complete 2FA - ask Roy to do it in the browser.
- Never submit without Roy's "שלח" for that specific role.
- Only these five roles. Do not apply anywhere else.

## 3. Wrap up
Use the tracker-keeper agent to record each role: Roy's "שלח" plus the portal's
success page is his explicit confirmation (CLAUDE.md), so set `status: submitted` and
`applied:` to today, with a dated note. Skipped roles get a dated note saying why. Rebuild the
dashboard, commit and push. End with a short Hebrew summary: submitted / skipped / why.
