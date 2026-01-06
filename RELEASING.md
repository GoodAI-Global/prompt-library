# Releasing

This document describes the release process for the Enterprise Prompt Library.

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes to prompt output formats or removed prompts
- **MINOR**: New prompts, new categories, new features
- **PATCH**: Bug fixes, documentation updates, prompt refinements

## Release Checklist

### Before Release

1. **Update CHANGELOG.md**
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD

   ### Added
   - New features

   ### Changed
   - Updated features

   ### Fixed
   - Bug fixes
   ```

2. **Run all checks**
   ```bash
   make all
   ```

3. **Verify documentation**
   - README is current
   - All new prompts documented
   - Examples tested

### Creating a Release

1. **Create release branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b release/vX.Y.Z
   ```

2. **Update version references**
   - Update version in CHANGELOG.md
   - Verify dates are correct

3. **Commit and push**
   ```bash
   git add .
   git commit -m "chore: prepare release vX.Y.Z"
   git push origin release/vX.Y.Z
   ```

4. **Create Pull Request**
   - Title: `Release vX.Y.Z`
   - Description: Copy from CHANGELOG

5. **After PR merge, create tag**
   ```bash
   git checkout main
   git pull origin main
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin vX.Y.Z
   ```

6. **Create GitHub Release**
   - Go to Releases > Draft a new release
   - Select tag `vX.Y.Z`
   - Title: `vX.Y.Z`
   - Description: Copy from CHANGELOG
   - Publish release

## Release Types

### Patch Release (X.Y.Z)
- Typo fixes in prompts
- Documentation improvements
- Example corrections
- No output format changes

### Minor Release (X.Y.0)
- New prompts
- New categories
- New templates
- New evaluation test cases
- Backward compatible

### Major Release (X.0.0)
- Breaking output format changes
- Removed prompts
- Major restructuring
- Requires migration guide

## Post-Release

1. **Announce release**
   - Update any dependent projects
   - Notify users of breaking changes (major only)

2. **Monitor issues**
   - Watch for bug reports
   - Prepare hotfix if needed

## Hotfix Process

For critical bugs in production:

1. Create branch from tag:
   ```bash
   git checkout vX.Y.Z
   git checkout -b hotfix/vX.Y.Z+1
   ```

2. Fix the issue

3. Update CHANGELOG

4. Create PR and merge

5. Tag new version:
   ```bash
   git tag -a vX.Y.Z+1 -m "Hotfix vX.Y.Z+1"
   git push origin vX.Y.Z+1
   ```

## Version History

See [CHANGELOG.md](./CHANGELOG.md) for complete version history.
