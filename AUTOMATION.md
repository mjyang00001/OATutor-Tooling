# 🚀 OATutor Automated Content Deployment

This repository now includes automated workflows to streamline content deployment and validation. No more manual copying between repositories!

## 🎯 What's Automated

### ✅ **Automated Content Updates**
- Google Sheet changes can trigger automatic content regeneration
- Validation tests run automatically
- Content is automatically deployed to staging
- Production deployment with approval workflow

### ✅ **Easy Validation for Any Document**
- One-click validation of any Google Sheet
- No technical setup required for content editors
- Immediate feedback on content format issues

### ✅ **Streamlined Testing**
- Automated Selenium testing on content updates
- Validation results posted directly to PRs
- Easy manual testing via GitHub interface

---

## 🚀 Quick Start Guide

### For Content Editors

#### **Validate Any Google Sheet** (No setup required!)

1. Go to [GitHub Actions](https://github.com/YOUR_ORG/OATutor-Tooling/actions)
2. Click "Quick Document Validation"
3. Click "Run workflow"
4. Paste your Google Sheet URL
5. Click "Run workflow"
6. Wait 2-3 minutes for results!

**What it checks:**
- ✅ Required headers are present
- ✅ Problems have steps
- ✅ Steps have answers
- ✅ Format follows OATutor standards

#### **Generate Content from Your Sheet**

1. Same as above, but uncheck "Only validate"
2. Your content will be generated and tested automatically
3. Download the results from workflow artifacts

### For Developers

#### **Automated Content Pipeline**

**Trigger automatic updates:**
```bash
# The workflows automatically trigger on:
# - Manual dispatch (any time)
# - Schedule (daily at 6 AM UTC)
# - Webhook from Google Sheets (when configured)
```

**Manual triggers:**
- Go to Actions → "Automated Content Update" → "Run workflow"
- Provide Google Sheet URL or leave blank for full update
- Choose between incremental or full regeneration

#### **Local Validation**

Quick validate any sheet locally:
```bash
python3 scripts/validate-sheet.py "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

# With specific sheet name:
python3 scripts/validate-sheet.py "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit" "Sheet1"
```

---

## 🔧 Setup Instructions

### Prerequisites

1. **Google Sheets API Credentials**
   - Create a service account in Google Cloud Console
   - Download credentials JSON
   - Add as GitHub Secret: `GOOGLE_SHEETS_CREDENTIALS`

2. **GitHub Secrets** (Repository Settings → Secrets and variables → Actions):
   ```
   GOOGLE_SHEETS_CREDENTIALS: [Your service account JSON]
   ```

### Production Deployment Setup

1. **Configure Deployment Targets**
   - Edit `.github/workflows/deploy-production.yml`
   - Update deployment steps for your infrastructure
   - Configure staging and production environments

2. **LTI Integration** (if needed)
   - Update LTI configuration steps in deployment workflow
   - Add LTI credentials to GitHub Secrets

---

## 📊 Available Workflows

### 1. **Automated Content Update** (`content-update.yml`)
**Triggers:** Manual, Schedule, Webhook
- ✅ Processes Google Sheets → JSON conversion
- ✅ Commits changes automatically
- ✅ Triggers validation testing
- ✅ Handles both incremental and full updates

### 2. **Content Validation** (`validate-content.yml`)
**Triggers:** After content updates, PRs, Manual
- ✅ Runs Selenium testing on generated content
- ✅ Posts results to PR comments
- ✅ Uploads test artifacts
- ✅ Tests feedback submission system

### 3. **Quick Document Validation** (`quick-validate.yml`)
**Triggers:** Manual only
- ✅ **Perfect for content editors!**
- ✅ Validates any Google Sheet format
- ✅ No credentials needed for public sheets
- ✅ Generates test content (optional)
- ✅ Runs staging tests (optional)

### 4. **Deploy to Production** (`deploy-production.yml`)
**Triggers:** After validation, Manual
- ✅ Deploys to staging automatically
- ✅ Production deployment requires approval
- ✅ Includes rollback capabilities
- ✅ Updates LTI configurations
- ✅ Runs smoke tests

---

## 💡 Usage Examples

### Content Editor Workflow
```
1. Edit Google Sheet
2. Go to GitHub → Actions → "Quick Document Validation"
3. Paste sheet URL → Run workflow
4. Check results in 2-3 minutes
5. Fix any issues and repeat
```

### Developer Workflow
```
1. Content changes committed to main branch
2. Automation automatically:
   - Generates new content
   - Runs validation tests
   - Deploys to staging
   - Notifies team of results
```

### Production Deployment
```
1. Go to Actions → "Deploy to Production"
2. Choose "production" target
3. Workflow waits for manual approval
4. Approve in GitHub → Auto-deploys
5. Smoke tests run automatically
```

---

## 🐛 Troubleshooting

### Common Issues

**"Sheet not accessible" error:**
- Make sure Google Sheet is shared publicly (view access)
- Or add proper credentials to GitHub Secrets

**Validation fails:**
- Check the validation report in workflow artifacts
- Common issues: missing headers, problems without steps

**Deployment fails:**
- Check deployment configuration in workflow files
- Verify all required secrets are configured

### Getting Help

1. **Check workflow logs:** GitHub Actions → Click on failed workflow → View logs
2. **Download artifacts:** Workflow run → Artifacts section
3. **Manual validation:** Use `scripts/validate-sheet.py` locally

---

## 🔄 Migration from Manual Process

### Before (Manual):
```
Google Sheets → Manual script → Manual copy → Manual deploy
```

### After (Automated):
```
Google Sheets → Automatic processing → Auto-deploy → Notifications
```

### Benefits:
- ⚡ **Faster:** Minutes instead of hours
- 🛡️ **Safer:** Automatic testing prevents errors
- 🔄 **Consistent:** Same process every time
- 👥 **Self-service:** Content editors can validate independently
- 📊 **Trackable:** Full audit trail in GitHub

---

## 🛠️ Advanced Configuration

### Custom Deployment Targets

Edit `deploy-production.yml` to add your deployment logic:

```yaml
- name: Deploy to your infrastructure
  run: |
    # Upload to S3
    aws s3 sync deployment-package/ s3://your-bucket/

    # Deploy to servers
    ssh user@server 'deploy-content.sh'

    # Update database
    curl -X POST https://api.yourapp.com/content/update
```

### Webhook Integration

To trigger automatic updates when Google Sheets change:

1. Set up Google Apps Script webhook
2. Configure to send POST to: `https://api.github.com/repos/YOUR_ORG/OATutor-Tooling/dispatches`
3. Include authentication and event payload

### Custom Validation Rules

Edit the validation script in `quick-validate.yml` to add custom checks:

```python
# Add custom validation rules
def custom_validation(df):
    errors = []

    # Your custom checks here
    if some_condition:
        errors.append("Custom validation error")

    return errors
```

---

## 📈 Monitoring and Metrics

- **GitHub Actions logs:** Full execution details
- **Workflow artifacts:** Validation reports, test results
- **Email notifications:** Configure in workflow files
- **Slack integration:** Add webhook notifications

---

*This automation setup eliminates manual content deployment and makes validation accessible to all team members. Questions? Check the workflow logs or create a GitHub issue.*