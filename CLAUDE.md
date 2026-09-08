# Tabi Kotoba — commute Japanese trainer

## What this is
Audio-first Japanese practice for a ~30–35 min car commute, aimed at travel-level
communication, not general fluency. `index.html` is the current prototype and the
whole app so far — read it before changing anything.

## Two experience modes (already decided — don't relitigate)
- **Drive mode**: fully audio, hands-free, no screen interaction while moving.
  English prompt → Japanese prompt → listen → grade → advance, automatically.
  Beginner/Amateur/Expert difficulty controls whether a phrase is drilled as
  smaller chunks first or given whole. Implemented.
- **Review mode**: screen-based, used after the drive. Deeper feedback, progress
  detail. The original prototype shape, still the default view.

## Pronunciation grading — deliberate decision, not a gap
Owner chose **local-first, revisit cloud later** over a cloud pronunciation API,
consistent with a general preference for local control over cloud dependencies.
Don't default to adding a cloud API without asking first.
- Current stand-in: the browser's built-in SpeechRecognition (Web Speech API) —
  quietly depends on the browser vendor's servers, not the real answer.
- Target: local speech-to-text (e.g. whisper.cpp) running on-device or on the
  home server, fully offline. Note true phoneme/pitch-accent scoring is a hard
  problem regardless of where it runs — going local keeps audio on-device, it
  doesn't by itself make pronunciation scoring accurate.

## Known placeholders — replace, don't preserve
- `window.storage` calls: this persistence API only exists inside Claude.ai
  artifacts. It won't exist in a normal browser or app — replace with real
  storage (localStorage/IndexedDB for a web build, or local file/SQLite for a
  native app). The prototype already no-ops gracefully if it's missing.
- SpeechRecognition: see above.

## Longer-term shape
PWA first, same path as the owner's perfboard-layout-tool project (browser
prototype → Claude Code → PWA, possibly Tauri later). A home Proxmox server on a
mini PC is available if any heavy lifting (STT model, backend) is better run off
the phone.

## Design language — keep consistent if the UI grows
Dark indigo palette (deliberately not the default cream/terracotta AI look), one
sans-serif family, ticket/boarding-pass motif for phrase cards, a hanko-stamp
(red circle) for correct answers instead of a generic green check. Avoid uniform
rounded-corner SaaS cards, all-caps labels, and gradient accents.
