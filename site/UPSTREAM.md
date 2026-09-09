# Quartz upstream

- Project: https://github.com/jackyzha0/quartz
- Version: 4.5.2
- Branch at import: v4
- Commit: d25a6eabf96751ffca56f8a8139272def7a65041
- Imported: 2026-09-09
- License: MIT, retained in LICENSE.txt

Engine sources are vendored in quartz/. package-lock.json pins the resolved dependency graph. GRIDEX changes are in quartz.config.ts, quartz.layout.ts, quartz/components/PolicyMetadata.tsx and quartz/styles/custom.scss. Content stays in ../content. No upstream history or nested .git directory is copied.

GRIDEX v0.3 also adds OriginalSearch.tsx, originalSearch.inline.ts, originalSearchCore.ts, originalSearch.scss and emitters/originalIndex.ts for local PDF evidence search. The original index is generated before site builds and emitted explicitly despite being Git-ignored.
