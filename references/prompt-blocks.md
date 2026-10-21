# Prompt blocks (Phase 7, also used for storyboards)

Contents: reference tags, identity lock, short lock, background blocks, moving-ground lock, signature-colour lock, shot template, writing rules, example.

## Reference tags

Refer to the uploaded sheets with whatever tag the tool uses. Default: `@image1` = approved character (or object, or animal) sheet, `@image2` = expression (or state) sheet, `@image3` = action sheet. Tools accept different numbers of references: always send the character sheet and the expression sheet, add the action sheet if allowed; the workflow and dimensions sheets are for planning and checking. If the tool has no tags, write "the attached character sheet" and so on. Say which tags were used so the user can swap them.

## Identity lock (fill from the approved sheets; paste at the top of every shot)

Fill every bracket from what is actually drawn. Delete lines that do not apply. Leave no brackets in the output.

```
IDENTITY AND STYLE LOCK
@image1 is the only source for the mascot's body, outfit, proportions and drawing style. @image2 is the only source for its facial expressions. @image3 is the reference for its poses. Match all three 100%.

MASCOT (from @image1)
[A <age> <person / animal / object>, <proportions>, <face or shape details>. <Hair, fur, markings or key shapes>; the silhouette is identical in every frame.]

OUTFIT AND PARTS (from @image1)
- [Top / body covering]
- [Bottom]
- [Footwear or feet]
- [Signature item: material, colour (hex), shape, how it attaches]
The signature item is [colour + hex] in every frame; hue and saturation never change.

STYLE (from @image1)
[Exact animation style wording from the Project Brief, e.g. 2D hand-drawn animation on twos, bold black ink outlines, pencil cross-hatching, soft shading.] Line weight, shading and colour fills stay identical from first frame to last.

FACE ACTING (from @image2)
Use only the labelled expressions on @image2: [labels]. Copy eyebrow angle, eye size, mouth shape and head tilt of the named expression exactly. Transitions take 4-6 frames.

CONTINUITY LOCKS
One mascot only, in one continuous style. Outfit, silhouette, proportions and signature-item colour are identical in every frame. The sheet layouts, labels and text never appear in the video.
```

For an object, replace face acting with "STATE ACTING (from @image2)" and use the object's state labels. For a logo, add "The logo's shapes and HEX colours match @image1 exactly in every frame; no text is rendered."

## Short lock (for tools with a character limit)

```
Follow @image1 exactly for the design and style, @image2 for expressions and @image3 for poses. [One sentence: mascot, outfit, signature item with colour hex.] Style: [style wording], identical in every frame. Expressions only from the labelled faces in @image2. One mascot, no text or sheet layout in the video, outfit, silhouette and signature colour identical in every frame.
```

## Background blocks (use the one locked in the Project Brief, in every shot)

**Green screen (#00FF00)**
```
BACKGROUND: The entire frame is flat pure chroma-key green (#00FF00, RGB 0,255,0), uniform from edge to edge, an empty clean void. The mascot's ground contact is shown only by pose. The mascot is lit by neutral white ambient light, so no green light falls on its edges, and it contains no green of its own. Full colour exactly as @image1.
```

**Black (#000000)**
```
BACKGROUND: The entire frame is flat pure black (#000000, RGB 0,0,0), uniform from edge to edge, an empty clean void. The mascot's ground contact is shown only by pose. A soft neutral rim light (5600K, 20% intensity) from behind and above traces the edges of any dark parts so every outline stays readable against the black. Full colour exactly as @image1.
```

**White (#FFFFFF)**
```
BACKGROUND: The entire frame is flat pure white (#FFFFFF, RGB 255,255,255), uniform from edge to edge, an empty clean paper-white void. The mascot's ground contact is shown only by pose. The mascot keeps its exact rendering from @image1 with clear outlines, and has no large pure-white areas of its own.
```

The sheets themselves are mid-grey (see `sheets.md`); these blocks are for shots, storyboards and the size preview only.

## Moving-ground lock (paste in every shot, fill the numbers from the planner)

```
MOTION LOCK
An invisible ground under the mascot moves to screen right at a constant <v>% of the frame width per second (about <px> px per second at <video width> px wide), from the first frame to the last, carrying the mascot to the right at exactly that speed in every second, whatever it is doing. The mascot's feet stay planted on the ground and travel with it. When it walks, its legs move at a natural walking rhythm like a person on a treadmill; when it stands, waves, dances, crouches or flies, it keeps being carried at the same speed. The speed never increases, decreases or pauses; drama comes from pose and cloth movement only.
```

## Signature-colour lock (add to POSITIVE LOCKS)

`The <item> stays <colour + hex> in every frame, same on every shot; shadows on it deepen to a darker <colour>, never to brown, black or grey.` If the sheet is black-and-grey with one colour accent, say that the accent is the only colour element.

## Shot template

Every shot is a sealed prompt: the generator remembers nothing about earlier shots. Paste the identity lock and the background block above it, then:

```
SCENE CONTEXT
[One or two sentences: what happens in this shot and where the mascot is going.]

FIRST FRAME
[Shot 1: at 0.0 s the front edge of the mascot (<nose / hand / cape tip>) is already just inside the left edge of the frame, about <sliver>% of the frame width, and the rest of the mascot is outside the frame. Never an empty frame.]
[Shots 2+: the previous shot's HANDOFF CARD, pasted word for word.]

FORMAT
One continuous <N>-second shot, <21:9 or 16:9>, static locked-off camera, 47 degree field of view, side-on at the mascot's chest height, no drift. The mascot is <gen%> of the frame height; the ground line sits at <ground%> of the frame height. x-positions are the mascot's centre as a percent of the frame width from the left edge.

ACTION
[Timed beats. 10 s shots: 2-4 s beats. 20-30 s shots: 3-5 s beats. Each beat: seconds, what the mascot does while being carried, how far (degrees, km/h of the cloth wind), which expression label, centre x at the end of the beat (from the planner's table).]
[The final beat reaches the HANDOFF CARD state below.]

HANDOFF CARD (end of this shot = first frame of the next)
[centre x with front and rear edges | ground or air height | facing | pose and walk-cycle phase | carry speed | expression | signature-item state]
[Final shot instead: the mascot is carried out of the right edge and on the last frame its rear edge (<cape tail / heel>) leaves the right edge, so the last frame shows only the clean background.]

PHYSICS
[Mass, inertia and cloth, fur or part behaviour; wind speed and direction in km/h.]

AUDIO
Silent.

POSITIVE LOCKS
Single mascot, style of the character sheet. [MOTION LOCK.] [Signature-colour lock.] [Background colour, uniform, with no floor, shadow or particles.] The mascot ends at centre x=<..>% in <pose>.
```

Order matters: subject and first frame, then format and camera, then action, then physics. Keep the camera static: if it moves, x-position no longer equals progress. Paste the MOTION LOCK in every shot.

## Writing rules

- **Positive phrasing.** "Stays upright with feet planted", not "does not fall".
- **Visible and measurable.** Degrees for body angles, km/h for speed, % of frame width for position, seconds for beats. Left and right are as seen from the camera.
- **Expressions by label.** "Face changes to DETERMINED from @image2: brows lowered, jaw set." The label wins over free description.
- **Real physics.** Cloth, fur and parts respond to wind and motion; animals and objects move as the sheets say.
- **Handoff is explicit.** The last beat of shot N and the FIRST FRAME of shot N+1 are the same text, including the walk-cycle phase and the carry speed.
- **Constant speed.** Never write words that change the carry speed (dash, sprint, zoom off, skid, stop, freeze). Write drama as pose, cloth and expression.
- **Direction of travel.** Moving right is screen right. A back view means the mascot faces away from the camera, so the signature item covers its back.
- **No generator-specific syntax** other than the reference tags. Do not name cameras, lenses or directors.
- **One tool's cap decides the shot length.** Never exceed it.

## Example beat block (10 s shot 1, wind-blown cape, black background, 9:16 video)

```
ACTION
0-3 s: carried right at 1.77% of frame width per second; the tip of the crimson cape fills the left 4% of the frame at 0.0 s, the boy's raised hand follows, then his shoulders, face HAPPY, as he is carried in; centre x from -2% to 3%.
3-7 s: fully inside the frame, he plants both fists on his hips with his back toward the camera and holds the hero pose, chin lifted; cape sweeps to screen right in a 15 km/h wind; centre x to 10%.
7-10 s: he pivots to face screen right and starts a treadmill-style walk, legs at a natural rhythm, right foot forward at the end, arms swinging 20 degrees; centre x reaches 15.2%.
```
