# PDF Forge Script Enhancement - .tex Debugging Support

**Deploy from Smart Pins folder - Enhanced monitoring script with .tex file access**

## Files Ready for Deployment

### Enhanced Script: `watch-shared-workspace.js`
- Added .tex file generation for every test
- .tex files copied to `/workspace/shared/test-results/`
- New JSON fields: `tex_available`, `tex_path`, `tex_error`
- Separate error handling for .tex vs PDF generation

### Test Cases for Validation
- `test-failure-case.json` - Tests failure mode and error reporting
- `test-success-case.json` - Tests success mode and .tex file access

## Quick Deployment

1. **Stop daemon:** `sudo systemctl stop pdf-forge-monitor`
2. **Deploy script:** `cp watch-shared-workspace.js /workspace/shared/`
3. **Start daemon:** `sudo systemctl start pdf-forge-monitor`
4. **Confirm ready:** Check daemon status

## Testing Plan
After deployment, Claude will:
1. Submit failure test → verify `tex_available: false` with error explanation
2. Submit success test → verify `tex_available: true` with accessible .tex file
3. Confirm both scenarios work as designed

This validates the .tex debugging enhancement works in both success and failure cases.