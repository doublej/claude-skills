# Request Translation

Turn a plain-language request into a sound identity Suno can render. Without a
reference there is no fingerprint to match, so invent one: commit to a lineage,
design a signature, and translate every abstract word into an audible cause.

## Sort the request into five kinds of words

| Kind | Example words | Becomes |
|---|---|---|
| subject | "about my grandmother's garden", "leaving Amsterdam" | lyric engine, title, imagery |
| mood | sad, dreamy, hopeful, epic, cozy, dark | audible traits (lexicon below) |
| scene | late-night drive, rainy café, summer rooftop | pulse, palette, space |
| use | workout, wedding entrance, study, intro, lullaby | tempo, density, vocal presence, form |
| genre hint | "something electronic", "kinda indie", "old-school" | lineage to sharpen, never paste as-is |

Every word lands in exactly one field. Subject words go into Lyrics and Title,
never into Style. Mood, scene, and use words go into Style only after
translation.

## Sharpen the genre hint into one lineage

Vague genre words render as Suno's median: generic pop with piano and strings.
Replace each hint with one specific lineage and era.

- "electronic" → pick one: 2010s French touch filter house, 90s UK garage,
  Detroit techno, 80s Italo disco, ambient dub.
- "indie" → pick one: jangly 80s C86 guitar pop, 2000s dance-punk, bedroom
  pop, slowcore.
- "old-school" → name the decade and the scene the rest of the request implies.
- No hint at all → derive the lineage from scene and use, then state it as an
  assumption outside the Suno fields.

Choose the narrower, more characterful option when two fit. Specific lineages
carry a whole bundle of groove, palette, and production that a generic label
leaves to chance.

## Translate mood words into audible causes

Never pass an abstract adjective through alone. Name what the listener hears
that produces the feeling. Keep the adjective only when it rides beside its
cause (`dreamy, slow-attack pads`).

| Word | Audible causes |
|---|---|
| dreamy | slow-attack pads, chorus-soaked guitar, long reverb tails, vocal set back in the mix |
| sad | slow harmonic rhythm, minor or modal, sparse arrangement, exposed close-mic vocal |
| melancholic but hopeful | minor verses lifting to a major-key chorus, rising melodic contour |
| epic | wide dynamic build, low brass or taiko, stacked choir, long crescendo to a full-band peak |
| chill | 80–95 BPM, laid-back swing, soft transients, warm Rhodes, rounded peaks |
| cozy | close dry room, nylon guitar or felt piano, soft breathy vocal, small ensemble |
| dark | low register, minor, sub-heavy bass, sparse high end, restrained vocal |
| energetic | 120+ BPM, driving eighth-note bass, bright hats, shouted or belted hooks |
| nostalgic | era-specific palette (tape saturation, analog synths, vinyl-warm drums) |
| romantic | slow 6/8 or half-time, lush strings or Rhodes, intimate lead, tender harmonies |
| angry | distorted guitars or bass, fast attack, clipped shouted delivery, dry tight drums |
| mysterious | unresolved chords, sparse percussion, reverse textures, whispered or low vocal |
| playful | bouncy syncopation, pizzicato or marimba, call-and-response, bright major key |
| raw | dry close mics, minimal overdubs, live takes, audible room |
| uplifting | major key, four-on-the-floor or driving pulse, rising chorus melody, gang vocals |
| cinematic | orchestral swells, wide stereo, dynamic contrast, patient intro |

Words not in the table: ask what a listener would physically hear, and write that.
Phrase every cause positively. A negation in Style (`no drums`) makes v6 add
the thing; put unwanted elements in Exclude.

## Translate scene and use into constraints

| Use | Constraints |
|---|---|
| workout, running | 125–150 BPM, steady pulse, short breakdowns, chanted hook |
| study, focus, background | instrumental by default, low density, even dynamics, loop-friendly |
| sleep, lullaby | 60–70 BPM, soft dynamics, brushed percussion at most, gentle resolving ending |
| wedding entrance, ceremony | build from sparse to full, clear moment of arrival, warm major key |
| party, club | 118–128 BPM, strong kick, hook within the first 30 seconds, DJ-friendly intro |
| video intro, jingle | short form, hook immediately, clean ending, instrumental unless asked |
| road trip, driving | mid-up tempo, steady motorik or rock pulse, open chorus |
| gift or tribute song | vocal-forward, lyrics built from the details given, sincere not saccharine |

A scene sets the space and palette: "rainy café" means dry close room, brushes,
upright bass; "summer rooftop" means bright, wide, percussive, open air.

## Design the signature

A reference hands you its blindfold traits. Here, invent them. Pick one or two
traits that would let a listener recognize this song on a second listen, and
state them a notch bolder than neutral:

- an unusual instrument role (`baritone sax carrying the bassline`);
- a groove quirk (`kick drops out every fourth bar`);
- a vocal identity (`hushed low alto, doubled an octave up in choruses`);
- a production move (`everything drenched in spring reverb except the dry lead`).

Lead the Style field with the lineage, the signature, and one mood cause.
Keep every other trait in plain support. At least one leading trait must come
from mood, so the render lands with the right feeling, not only the right genre.

## Resolve conflicts before writing

Requests often carry contradictions: "chill but energetic", "sad party song".
Resolve each one on purpose, and never average the two words:

- split across time: calm verses, driving chorus;
- split across layers: danceable pulse under a melancholic minor melody;
- pick the stronger word and say so outside the Suno fields.

## Write the anchor

Before drafting fields, fix the anchor in one line shown to the user above the
fields:

`ANCHOR: <lineage + era> · signature: <trait>, <trait> · mood: <cause> · use: <constraint>`

Every revision works against this anchor, the way a reference anchors
craft-suno-songs. When feedback moves the song, update the anchor first, then
rebuild the fields from it.
