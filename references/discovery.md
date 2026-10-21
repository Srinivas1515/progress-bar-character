# Discovery (Phase 1)

Contents: how to ask, Block 1 video, Block 2 mascot, Block 3 animation style, Block 4 background colour, the Project Brief card.

## How to ask

Four short question blocks, one block per message (or two small ones together if the user is clearly in a hurry). Use tappable options where the interface offers them and plain questions where the answer is free text. Never ask what the conversation already answers. After each block, reflect the answer in one line so the user can correct it. Suggestions come from the video, so the video block always goes first.

## Block 1: the video and the basics

Ask:
1. What is the video? (ad, song / music video, DJ or dance track, vlog, tutorial, short film, product demo, other) and what is it about?
2. Its purpose: what should viewers feel or do at the end? (buy, subscribe, remember the brand, enjoy the song)
3. Extra detail by type:
   - **Ad / brand**: company name, brand, product or service, brand colours, tagline, whether there is a logo, the audience, any tone limits (premium, playful, kids).
   - **Song / music video**: language, genre, mood, tempo (BPM if known), who it is for, any imagery in the lyrics. Ask if it is a DJ / dance / EDM track.
   - **Other**: the topic and the tone.
4. Video tool for the mascot clips and the **run time** of the progress bar in seconds (the mascot's run time equals the main video's length). Tool caps: Higgsfield up to 30 s per shot (60 s = 2 shots); Google Flow 10 s per shot; any other tool: ask for its maximum seconds per generation, default 10 s if unknown. If the user states a different cap, use theirs.
5. The video's frame: **9:16** (reel, short, story) or **16:9** (YouTube, landscape).

## Block 2: what is the mascot?

Ask: "What is in your mind for the progress-bar mascot: a **character** (person), an **object**, or an **animal**? Do you already have one?"

- Has one: ask for the upload (image, sheet, logo, or a clear description). Everything later is built from it (see "Existing mascot" in `sheets.md`).
- No idea yet: propose 2-3 concepts that fit the video using the table below, each in one line, and let the user pick or mix.
- Objects can be anything with a believable way of moving: a ball, paper plane, scooter, guitar pick, coin, logo mark. Brand logos become "logo mechanics" (see `sheets.md`).

The animation must match the video and add value. Test every concept with: "if this mascot were removed, would the video lose something?"

### Concept suggestions by video type

| Video | Character ideas | Object / logo ideas | Animal ideas |
|---|---|---|---|
| Ad for a brand | A new original person in the brand's uniform or colours, who fits the audience (courier, barista, student, chef) | The logo mark that rolls, builds itself or bounces; the product on wheels | A brand-fit animal (fast: cheetah; trustworthy: dog; premium: swan) |
| Song, pop / romantic | A boy or girl vibing: headphones, casual or festive outfit that fits the lyrics | A heart, vinyl record, paper plane | A bird or butterfly |
| DJ / EDM / dance track | A DJ-styled character: headphones, LED jacket, sunglasses, neon sneakers, glow accents | A speaker, vinyl disc, equaliser bars | A cat or fox in DJ gear |
| Folk / devotional / festive | A character in matching traditional attire and accessories | A lamp, kite, drum | Peacock, elephant (respect cultural meaning) |
| Hip-hop / rap | Oversized hoodie, chain, cap, sneakers | Boombox, sneaker | Panther, crow |
| Tutorial / education | Curious student or friendly robot | A pencil, book, magnifying glass | Owl, bee |
| Gaming / tech | A pixel hero, small robot | Controller, chip, rocket | A pixel pet |
| Travel / food / fitness | Backpacker, chef, runner | Suitcase, pan, kettlebell | Companion animal matching the theme |

Rules for concepts:
- Never recreate a real, named person (artist, celebrity, athlete). Use an original character inspired by the mood.
- The mascot should not clash with the topic or culture of the video. When unsure, ask.
- For an ad, the mascot should support the brand, never mock a competitor or imply claims the ad does not make.

## Block 3: animation style

Ask: "Which animation style do you want?" If the user is unsure, suggest 3 styles that suit the video and mascot, with a one-line reason each. Offer the list below as the menu.

| Style | Looks like | Suits |
|---|---|---|
| 2D hand-drawn ink and pencil | Black ink outlines, cross-hatching, soft painted fills | Storybook, emotional, character-led videos, most songs |
| Flat vector / motion graphics | Clean shapes, flat colour, no outlines or thin ones | Brand and tech ads, explainers, logos |
| Cel-shaded anime | Crisp lines, two-tone shading | Pop songs, youth content, gaming |
| 3D stylised toy / clay | Soft rounded 3D, simple textures | Kids, product ads, friendly brands |
| Pixel art / 8-bit | Chunky pixels, limited palette | Gaming, retro, tech |
| Paper cut-out / collage | Layered paper shapes with slight shadow | Folk, festive, craft, food |
| Neon line / glow | Thin glowing outlines | DJ, EDM, night events (works best on black) |
| Watercolour storybook | Soft wash colour, loose lines | Gentle, family, wellness |

Notes:
- Style drives every sheet, storyboard and shot: write it once in the Project Brief and reuse the exact wording.
- Very detailed styles (painterly, realistic 3D) are harder to keep consistent over 6-10 clips and cost more fine detail in a small mascot. Say so when the user picks one, and suggest a simpler cousin if the run is long.
- If the user has a character in a style already, that style wins.

## Block 4: background colour lock

The animated shots use ONE flat colour for every clip so the mascot can be removed in the edit. The user must choose exactly one of these three:

| Colour | HEX | RGB | Removed in the edit with |
|---|---|---|---|
| Green screen | `#00FF00` | 0, 255, 0 | Chroma key |
| Black | `#000000` | 0, 0, 0 | Screen / Add blend |
| White | `#FFFFFF` | 255, 255, 255 | Multiply blend |

Recommend one after reading the mascot design (or ask for its main colours first), using this clash check:
- Green screen: the mascot has no green, and no semi-transparent parts (thin hair, glass, smoke). Good for any colourful design. Risk: green light on edges (spill).
- Black: the mascot has no large black or very dark areas (black hair, dark clothes vanish under Screen). Best for bright, neon or glowing designs.
- White: the mascot has no large white or very light areas (white shirts, highlights turn see-through under Multiply). Best for dark or ink-style designs.
- If the design clashes with the first choice, recommend the next best colour or a small design change (for example a rim light, a coloured outline or a different shirt colour). Let the user decide.

Once locked, write the colour into every sheet-to-shot prompt as the shot background. The reference sheets in Phase 2 and 4 stay mid-grey; only the shots, storyboards and size preview use the locked colour.

## Project Brief card

After Block 4, post this card and ask the user to confirm. Keep it updated at every gate and re-post it when something changes; later phases read from it.

```
PROJECT BRIEF
Video: <type, topic, purpose, brand or song details>
Tool and cap: <tool, max seconds per generation>   Run time: <seconds>   Frame: <9:16 or 16:9>
Mascot: <character / object / animal> - <concept, or "user's own">
Animation style: <style, one exact wording>
Background colour (locked): <Green #00FF00 / Black #000000 / White #FFFFFF>
Motion rule: carried right on a moving ground at one constant speed, enters at 0:00, leaves on the last frame (speed from the planner: <% per s>)
Status: [ ] character sheet  [ ] action plan  [ ] support sheets  [ ] size & placement  [ ] storyboard  [ ] final prompts
```
