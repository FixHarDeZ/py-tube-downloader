Create a new versioned release. Steps:

1. Run `git status` to check for uncommitted changes. If there are any, ask the user whether to commit them first (with what message) before proceeding. Do not auto-commit.

2. Run `git tag --list 'v*' --sort=-v:refname | head -5` to find the latest tag. Determine the next version:
   - Default bump is **patch** (v1.0.0 → v1.0.1)
   - If the user passed an argument (e.g. `/release minor` or `/release 1.2.0`), use that instead:
     - `major` → bump major, reset minor+patch
     - `minor` → bump minor, reset patch
     - `patch` → bump patch only
     - A bare version string like `1.2.0` → use as-is (prefix `v` if missing)
   - Confirm the new version with the user before tagging.

3. Run `git log <previous_tag>..HEAD --oneline` to collect commits for the changelog.

4. Draft a release title and changelog from those commits. Present it to the user for approval before continuing.

5. Once approved:
   - `git tag <new_version>`
   - `git push origin main`
   - `git push origin <new_version>`
   - `gh release create <new_version> --title "<title>" --notes "<changelog>"`

6. Print the release URL returned by `gh release create`.
