# Bug Report for Anthropic - Claude Code CLI Status Indicator

## How to Submit This Report

### Option 1: GitHub Issues (PREFERRED)
1. Go to: https://github.com/anthropics/claude-code/issues
2. Click "New Issue"
3. Copy/paste the bug report below
4. Submit

### Option 2: Email
- Send to: support@anthropic.com
- Subject: "Claude Code CLI - Status Indicator Bug Report"
- Copy/paste the bug report below

### Option 3: In-CLI Feedback
- When back in Claude Code, type: `/feedback`
- Paste the summary section

---

## Bug Report

### Issue Title
Claude Code CLI status indicator disappears during long operations

### Environment
- **Product**: Claude Code CLI
- **Version**: Current (pre-8.1 update as of 2025-08-14)
- **OS**: macOS [adjust if different]
- **Issue frequency**: Intermittent but regular (past 3-4 releases)

### Description
During extended work sessions where Claude is processing tasks independently, the status indicator that normally shows:
- Status message (e.g., "Thinking" or similar)
- Token counter (incrementing numbers)
- Activity indicators

...completely disappears from the CLI interface.

### Impact
When returning to check on Claude's progress after leaving it to work independently:
- Cannot tell if Claude is still actively working
- No visual indication of processing status
- Creates uncertainty about whether:
  - Work is proceeding normally
  - Claude has stopped and is waiting for input
  - A crash or hang has occurred

### Expected Behavior
- Status indicator should remain visible throughout processing
- Token counter should continue incrementing
- Some form of activity indicator should persist

### Actual Behavior
- Status indicator disappears entirely
- No visual feedback that processing continues
- Terminal appears idle despite active work

### Reproduction Steps
1. Give Claude a large task set to work on independently
2. Let Claude work for extended period (30+ minutes)
3. Return to terminal
4. Observe that status indicators have disappeared

### Workaround
Currently asking Claude directly "are you still working?" to confirm, but this interrupts the work flow.

### Suggested Fix
- Ensure status indicator remains visible during all processing
- Add periodic status updates for long-running operations
- Consider adding timestamp to last status update

### User Impact
This is particularly problematic for users who:
- Leave Claude to work independently for hours
- Need confidence that processing is continuing
- Want to monitor progress without interrupting

---

## Additional Context

This issue affects user confidence in the tool's reliability during autonomous work sessions. When the status indicator disappears, users cannot distinguish between:
- Active processing (good)
- Waiting for input (needs attention)
- Hung/crashed state (needs restart)

The issue has persisted across multiple releases, suggesting it may be a fundamental UI update problem rather than a regression.

---

*Report prepared: 2025-08-14*
*Feel free to add any additional details about your specific system configuration*