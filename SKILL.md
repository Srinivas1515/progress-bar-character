---
name: progress-bar-character
description: Guides a user from idea to finished prompts for a "progress-bar character", a small mascot (person, object, animal or brand logo) carried at constant speed from the left edge to the right edge along the bottom of a video, so its position is the progress, while it acts out a short story. Runs a gated workflow - discovery (video, ad brand or song, mascot, animation style, locked background colour green, black or white), character sheet, action plan chosen with the user, expression, action, workflow and body-dimension sheets, mascot size for 9:16 or 16:9, storyboards checked against uploads, then per-shot video prompts that join into one continuous motion, a position map and an editing guide. Shot length follows the tool (Higgsfield up to 30 s, Google Flow 10 s, others as stated). Use whenever the user mentions a progress bar mascot or character, a character moving across the screen as a video plays, a mascot overlay for reels, shorts, ads or songs, or animating a character sheet in continuous shots.
---

# Progress-Bar Character

A progress-bar character is a small animated mascot layered over a video. It enters from outside the frame at 0:00, it moves left to right along the bottom at the pace of the video, it performs a short story that fits the video, and it leaves the frame exactly when the video ends. Its position is the progress.

The mascot must match the video and add value to it: a brand ad gets a mascot that serves the brand, a song gets a character vibing to that song, a DJ track gets DJ costume and moves. Every choice (mascot, style, actions) comes from the video.

This skill runs as a guided project in seven phases with five approval gates. Claude cannot render images in this chat: for sheets and storyboards Claude writes prompts, the user generates them in their own tools and uploads the results, and Claude reviews the uploads. Say this once, at the first sheet.

## The two rules that define this skill

**1. One continuous motion across all shots (why the relay).** Video tools cap clip length (Flow 10 s, Higgsfield 30 s), so a one-minute mascot is generated in pieces. The user places the pieces end to end on a single track and plays them: it must look like ONE uninterrupted performance. So only shot 1 enters from outside the frame, only the last shot leaves it, and every joint between shots is invisible because shot N+1 starts exactly where shot N ended (same position, height, facing, pose, walk-cycle phase, speed, expression and signature-item state). Never make each shot enter and exit on its own: the mascot would be cut at each seam and jump.

**2. The moving ground (constant speed, never stops).** An invisible ground carries the mascot to the right at one constant speed for the whole run, like a treadmill whose belt runs the other way. Whatever the mascot does (walk, wave, look around, dance, pose, crouch, fly), its feet stay planted on the ground and the ground carries it right. Walking is a treadmill-style walk at a natural leg rhythm. No sprints, dashes, stops or pauses; drama comes from pose and cloth, never from extra speed. At 0.0 s the front edge of the mascot is just inside the left edge (never an empty frame), and the rear edge leaves the right edge on the last frame. `scripts/plan_shots.py` calculates the speed and every position.

## Rules for running the project

- **One phase at a time, never skipping a gate**, because every later step depends on it.
- **Keep the Project Brief card current** (see `references/discovery.md`). Re-post it after each gate and whenever something changes.
- **Changes cascade.** A new look sends the project back to Phase 2. New actions update the action plan, the action and workflow sheets if a pose is new, the handoff cards and the storyboard.
- **Meet the user where they are.** If they already have a character, sheets, an action idea or a storyboard, skip what is done, check it against the specs and continue.
- **Ask only what is missing.** Use tappable options where the interface has them. One phase per message.
- **Do the numbers with the scripts**, not by hand: `plan_shots.py` for shots, speed, positions and sizes; `check_frame.py` for storyboard images; `track_motion.py` for generated clips.

## The seven phases

### Phase 1: Discovery (read `references/discovery.md`)
Four question blocks in this order, because each answer drives suggestions in the next:
1. **The video** (type, topic, purpose; for an ad: company, brand, product, logo; for a song: genre, mood, BPM, DJ or not), the **tool and run time**, and the **frame** (9:16 or 16:9).
2. **The mascot**: character, object or animal; does the user already have one (upload it) or should Claude propose 2-3 concepts that fit the video.
3. **The animation style**: ask; if the user is unsure, suggest three styles that suit the video and mascot.
4. **The background colour lock**: exactly one of Green `#00FF00`, Black `#000000`, White `#FFFFFF`, with a clash check against the design.

Output: the Project Brief card. **Gate 0**: user confirms the brief.

### Phase 2: Mascot sheet (read `references/sheets.md`)
Write the character sheet prompt (or object design sheet, or animal sheet; or a sheet built from the user's own upload). All sheets use a flat mid-grey background and ordinary general lighting, never studio lighting. Review the upload. **Gate 1**: user approves the character sheet.

### Phase 3: Action plan (read `references/action-planning.md`)
The user decides what the mascot does. Ask for their plan first, then offer one or two plans of your own based on the video purpose and content, how the mascot looks, and how that kind of person, object or animal really behaves. Every action must work while being carried at constant speed. Lock the Action Plan. **Gate 2**: user approves the action plan.

### Phase 4: Support sheets (read `references/sheets.md`)
Four separate sheets, all mid-grey with general lighting, built from the approved character sheet and the action plan: expression sheet (state sheet for faceless objects; deep expression sheet for animals), action sheet, action workflow sheet (key drawings of each action over time), body dimensions sheet (proportions with measurement lines). Review each upload. **Gate 3**: user approves the sheets.

### Phase 5: Size and placement (read `references/size-and-storyboard.md`)
Confirm 9:16 or 16:9, choose a precise mascot size (not too big, not too small), run the planner for the numbers and warnings, and, if the user wants to see it, give a size-preview prompt in their frame. **Gate 4**: user approves size and placement.

### Phase 6: Shot plan and storyboard (read `references/size-and-storyboard.md` and `references/action-planning.md`)
Run the planner for the shot split, carry speed and positions, write the Handoff Cards, and give one storyboard prompt per shot. The user generates them and uploads; Claude measures them with `check_frame.py` and compares them with the sheets and the plan, then approves them or lists fixes. Repeat until they match. The user can change actions here. **Gate 5**: user says the storyboard is what they want.

### Phase 7: Final prompts and editing (read `references/prompt-blocks.md` and `references/editing-guide.md`)
Give all shot prompts at once, each in its own code block, with the shared blocks (identity lock, short lock, locked background block, motion lock), the position map and the editing guide for the locked colour. When the user comes back with generated clips, offer to check each clip and each joint with `track_motion.py`.

## Shot length by tool

Higgsfield: shots up to 30 s (a 60 s run is 2 shots). Google Flow: 10 s per generation (a 60 s run is 6 shots). Any other tool: use the maximum seconds per generation that the user states, 10 s if unknown. Shots are cap-sized with a shorter last shot for any remainder; the planner does the split.

## Other rules that must hold, and why

- **Backgrounds**: sheets are mid-grey; shots, storyboards and the size preview use the locked colour only. A flat locked colour is what lets the mascot be removed in the edit.
- **The signature colour never changes** (for example a red cape) across shots; state it in words with its hex.
- **Identity comes from the sheets.** Describe only what must be locked and say "matches the sheet 100%". Long appearance text fights the reference and causes drift.
- **Expressions come from the expression sheet labels**, so faces stay on-model.
- **Every beat has a position** from the planner's table, and every shot prompt carries the motion lock with the carry speed.
- **Actions must be physically believable** for what the mascot is (a ball rolls, a cat stalks and pounces) unless the user asks for magic.
- **Original characters only.** Do not make a likeness of a real, named person. For brand logos keep geometry and colours exact, keep text out of the animation, and only work on a logo the user says is theirs or their client's.
- **Positive phrasing, visible actions, measurable numbers** in every prompt. Silent clips, static camera.

## Files

- `references/discovery.md`: question blocks, suggestion tables, style menu, colour lock, Project Brief card.
- `references/sheets.md`: sheet look, prompts for every sheet, object, animal, logo and existing-mascot variants, review checklist.
- `references/action-planning.md`: why continuity matters, the moving-ground rule, asking for the plan, two suggested plans, arc, handoff rule.
- `references/size-and-storyboard.md`: size rules and preview prompt, storyboard prompts, verification, checking generated clips.
- `references/prompt-blocks.md`: identity lock, background blocks, motion lock, shot template, writing rules.
- `references/editing-guide.md`: assembling end to end, placing, keying or blending, speed check, troubleshooting.
- `scripts/plan_shots.py`: shot split, constant carry speed, positions, mascot size, warnings.
- `scripts/check_frame.py`: measure storyboard panels and single frames.
- `scripts/track_motion.py`: check a generated clip's speed and a joint between two clips.
