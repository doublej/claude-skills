# Collaborative / Multiplayer UX

For real-time shared editing (Google Docs, Figma, Linear-style). The heuristics still apply; this covers the failure modes they don't name. Bar: a user should never wonder who changed what, lose their own input, or fight another cursor.

## Presence

- Avatars of everyone in the document, top-right, with a colour per person that is reused for their cursor, selection and edit highlights.
- Live cursors and selections in that colour, with a name tag that fades after ~2s idle and reappears on movement.
- Off-screen collaborators: clicking an avatar scrolls/pans to them ("follow" mode in Figma); show an edge indicator in their colour.
- Idle/away state after a few minutes; drop the cursor, keep the avatar dimmed.

## Selection and editing feel

- Local input is never blocked on the network: apply keystrokes, drags and selections instantly (optimistic), sync in the background. Any latency on typing or caret movement reads as "finicky".
- Remote edits must not move the local caret or selection, scroll the viewport, or steal focus. Transform the caret position through incoming operations (CRDT/OT libraries such as Yjs or Automerge do this; hand-rolled diffing usually does not).
- Selection basics must be native-grade before multiplayer: double-click word, triple-click paragraph, shift-extend, drag-select across blocks, keyboard selection, IME composition untouched by remote updates.
- Undo is per user: Cmd+Z reverts only my changes, never a collaborator's.

## Conflicts

- Prefer conflict-free merging (CRDT) over locks. If two people edit the same object, last-writer-wins per property is acceptable for canvas objects; text needs character-level merging.
- When a lock is unavoidable (e.g. a modal form), show who holds it in their colour and when it frees up; never silently discard the second editor's input.
- When an edit is rejected or rebased, show it: brief highlight of the changed region in the author's colour.

## Sync status (heuristic 1, visibility of system status)

- Quiet "Saved" / "Saving…" indicator; loud only when it matters: "Offline — changes saved locally, will sync" and "Couldn't sync — retrying".
- Offline edits queue locally and merge on reconnect; never show a "your changes will be lost" dialog for a transient disconnect.
- Version history with named authors and restore, so mistakes by anyone are recoverable (heuristic 3, user control).

## Review checklist

- [ ] Typing and caret movement feel instant with 300ms simulated latency
- [ ] A remote edit above my caret does not move my caret or scroll my view
- [ ] Two users editing the same paragraph both keep their text
- [ ] Undo only undoes my own changes
- [ ] Every collaborator has one consistent colour across avatar, cursor and highlights
- [ ] Going offline and back loses nothing and says so
