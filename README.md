# Automated Attendance Marker with Screenshot & Email Notification

This Python script automatically monitors a Google Form (used for attendance), fills in your name and ID when it becomes available, submits it, captures a screenshot for proof, and sends an email notification with the screenshot attached.

---

## Features

- Continuously checks if the attendance form is open
- Automatically fills in your name and ID
- Submits the form once available
- Saves a timestamped screenshot after submission
- Sends an email with the screenshot as proof

---

## Requirements

- Google Chrome
- ChromeDriver (matching your Chrome version)
- Python 3.x
- Gmail account with [App Password](https://support.google.com/accounts/answer/185833?hl=en) enabled

---

## Python Libraries Used

- `selenium`
- `smtplib`
- `email`
- `datetime`
- `os`
- `time`

Install Selenium using pip if you haven't already:

```bash
pip install selenium


