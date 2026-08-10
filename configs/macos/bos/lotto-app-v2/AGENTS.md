# AGENTS.md

## Project

Lotto App v2 is the player-facing Next.js frontend consuming PlayerManager and Lotto APIs. Preserve existing routing, component, service, state, styling, and test boundaries.

Linear is the source of truth for ticket intent. For Winning Palace work, use `wp/develop` and `wp/feature/BOS-XXXX` unless the ticket or PR specifies otherwise; verify the remote base before branching.

## Build and Test

Inspect lockfiles before selecting the package manager, then prefer existing scripts:

- Install: `npm install`
- Dev server: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`
- Focused E2E: `npx playwright test <spec-or-grep>`

## UI and Data Flow

- Preserve frontend-visible API contracts unless the ticket explicitly changes the backend/frontend contract.
- Verify backend payload assumptions against PlayerManager or Lotto API evidence.
- Keep report, transaction, deposit, ticket, and export semantics aligned with backend behavior.
- Follow existing page/component/service boundaries; do not duplicate API shaping across UI components.
- Prefer existing MUI, Redux, service, and Playwright patterns over new abstractions.
- Do not edit generated files manually unless intentionally resolving tool-output drift; regenerate or verify afterward.
- For player-visible flows, cover relevant loading, success, failure, cancellation, refresh, and retry states.

## Review Rules

- Check cross-repo impact for shared payloads, reports, payment/deposit flows, and deploy configuration.
- When explicitly asked to publish review feedback, use concise English comments ordered by severity.
