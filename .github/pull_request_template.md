# 🚀 Pull Request Title
<!-- Example: 🔐 Fix JWT authentication bug in login flow -->

---

## 📌 Summary
<!-- Briefly explain what this PR does -->
- What problem does this solve?
- What feature/bugfix is included?
- Why is this change needed?

---

## 🧩 Related Issue / Ticket
<!-- Link Jira, GitHub issue, or task -->
- Jira: [PROJECT-123]
- GitHub Issue: #45

---

## 🔄 Type of Change
<!-- Mark relevant options with an 'x' -->
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] ♻️ Refactoring
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test update
- [ ] 📚 Documentation update
- [ ] 🔧 DevOps / CI-CD changes

---

## 🛠️ Changes Made
<!-- Describe the actual implementation -->
- Added JWT validation middleware
- Fixed password reset token verification
- Updated API response structure
- Refactored service layer logic

---

## 📷 Screenshots / Demo (if applicable)
<!-- Add screenshots, GIFs, or videos -->
Before:
<!-- image -->

After:
<!-- image -->

---

## 🧪 How Has This Been Tested?
<!-- Explain how you tested your changes -->
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Edge cases tested

**Test Details:**
- Tested login with valid/invalid credentials
- Verified token expiration handling
- Checked API responses via Postman

---

## ⚠️ Breaking Changes
<!-- If yes, explain clearly -->
- [ ] Yes
- [ ] No

If yes:
- Describe what breaks
- Migration steps (if needed)

---

## 🔐 Security Considerations
<!-- Important for backend/auth-related PRs -->
- Any sensitive data exposed?
- Any authentication/authorization impact?
- Input validation handled?

---

## 📦 Dependencies Added / Updated
<!-- Mention new packages/libraries -->
- Added: `jsonwebtoken`
- Updated: `mongoose@7.0.0`

---

## ⚡ Performance Impact
<!-- Mention if performance is affected -->
- Improved API response time by ~20%
- No noticeable impact

---

## 🧹 Checklist
<!-- Ensure quality before requesting review -->
- [ ] Code follows project coding standards
- [ ] Self-review completed
- [ ] Comments added where necessary
- [ ] No unnecessary console logs
- [ ] Tests added/updated
- [ ] Documentation updated

---

## 👀 Review Notes
<!-- Anything specific reviewers should focus on -->
- Focus on authentication flow
- Check error handling logic
- Validate edge cases

---

## 📢 Additional Notes
<!-- Any extra context -->
- Future improvement: Add refresh tokens
- Known limitation: Token blacklist not implemented yet
