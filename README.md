# 9gag Top Memes of the Day -> Email (runs on GitHub Actions, no local computer needed)

This repo emails you a digest of 9gag's hot feed every 6 hours, automatically,
using GitHub's free scheduled-workflow runners. Nothing needs to run on your
own machine.

Each email has three sections — Static Images, Videos and GIFs — with the top
30 posts of each ranked by upvotes (videos and GIFs shown as animated
previews). Posts already sent in the last 26 hours are skipped, so every email
only has new memes.

## One-time setup (~5 minutes)

1. **Create a GitHub account** if you don't have one: https://github.com/join

2. **Create a new repository**
   - Click "+" (top right) -> "New repository"
   - Name it anything, e.g. `9gag-meme-emailer`
   - Set it to **Public**. The email's images are hosted on this repo's
     `meme-assets` branch, and Gmail can't load them from a private repo.
     Your Gmail credentials stay hidden as encrypted secrets either way.
   - Click "Create repository"

3. **Upload these files** to the repo (drag-and-drop works fine via the GitHub
   web UI: "Add file" -> "Upload files"), keeping the folder structure:
   - `9gag_top_meme_emailer.py`
   - `requirements.txt`
   - `.github/workflows/send-meme.yml`

4. **Create a Gmail App Password** (your normal Gmail password won't work):
   - Turn on 2-Step Verification: https://myaccount.google.com/signinoptions/two-step-verification
   - Then create an app password: https://myaccount.google.com/apppasswords
   - Choose "Mail" as the app, copy the 16-character password it gives you.

5. **Add your secrets to the repo** (this keeps your email/password out of the code):
   - In your repo: Settings -> Secrets and variables -> Actions -> "New repository secret"
   - Add three secrets:
     - `GMAIL_ADDRESS` = your Gmail address
     - `GMAIL_APP_PASSWORD` = the 16-character app password from step 4
     - `MEME_RECIPIENT` = the email address that should receive the meme

6. **Test it manually**
   - Go to the "Actions" tab in your repo
   - Click "Send Top Memes of the Day" on the left
   - Click "Run workflow" -> "Run workflow" (green button)
   - Wait a few minutes (it downloads and converts ~90 posts), refresh, click into the run to see logs / confirm success
   - Check the recipient inbox for the email

That's it — from now on it runs automatically at the times set in
`.github/workflows/send-meme.yml` (default every 6 hours), with no computer of
yours needing to be on.

## Changing the schedule

Open `.github/workflows/send-meme.yml` and edit this line:

```
- cron: "0 */6 * * *"
```

Cron format is `minute hour day month weekday`, always in **UTC**. Examples:

- `0 2 * * *`  -> 2:00 AM UTC daily (9:00 AM in Vietnam, UTC+7)
- `30 23 * * *` -> 11:30 PM UTC daily
- `0 9 * * 1-5` -> 9:00 AM UTC, weekdays only

A handy converter: https://crontab.guru (shows what a cron string means, but
you still need to convert your local time to UTC yourself, e.g. via
https://www.timeanddate.com/worldclock/converter.html)

## Notes

- GitHub Actions is free for public repos.
- The workflow keeps the images from the last 8 runs on the `meme-assets`
  branch. Emails older than that (about 2 days) lose their images; change
  `ASSET_RUNS_TO_KEEP` in the workflow to keep more.
- Sent-post history is saved in `state/sent_ids.json`, which the workflow
  commits back to the repo after each email.
- You can also trigger it manually anytime via the "Run workflow" button.
- If the run fails, check the Actions tab -> the failed run -> logs. Common
  causes: a secret is missing/misspelled, or the Gmail app password was
  revoked.
