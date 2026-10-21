# Action planning and continuity (Phase 3, and the rules used in Phases 6-7)

Contents: why continuity matters, the moving-ground rule, who decides, asking for the plan, suggesting plans, how each kind of action works while carried, the arc, the handoff rule, the Action Plan card.

## Why continuity matters

A video tool cannot generate a mascot that moves across the screen for a whole minute: Flow stops at 10 s per generation, Higgsfield at 30 s. So the minute is cut into shots. The viewer must never notice the cuts. When the clips are placed one after another on a single track (end to end, never stacked as layers) and played, the mascot must look like ONE continuous motion:
- it enters from outside the frame when the progress bar starts,
- it moves along with the progress bar the whole time,
- it leaves the frame exactly when the progress bar ends.

Only shot 1 enters from outside the frame and only the last shot leaves it. Every other joint is invisible because shot N+1 starts exactly where shot N ended.

## The moving-ground rule (constant speed, never stops)

The mascot never stands still on the screen. An invisible ground carries it to the right at ONE constant speed from the first frame to the last, whatever it is doing, like a treadmill whose belt moves the other way. Its feet stay planted on the ground and the ground carries the whole body to the right.

- **Standing, waving, looking around, dancing, posing, crouching:** the mascot performs the action while being carried; its screen position keeps advancing at the same rate.
- **Walking:** a treadmill-style walk. Legs move at a natural walking rhythm while the ground carries the mascot at the (much slower) carry speed. The feet slide slightly on the ground; the flat background hides it.
- **Flying, riding, rolling, floating:** same carry speed. The drama of a take-off comes from the pose (crouch, push-off, lift, tilt, streaming cape), not from extra speed. A flying exit lifts off and rises while still carried at the same speed.
- **No sprints, dashes, zoom-offs, skids to a stop or pauses.** Anything that changes the speed breaks the progress bar. Speed lines or cloth streaming are visual only.
- **Entrance:** at 0.0 s the front edge of the mascot (nose, hand, signature-item tip) is just inside the left edge of the frame, not an empty frame. The mascot is carried in over the first few seconds.
- **Exit:** the mascot is carried out of the right edge and its rear edge (cape tail, heel) leaves on the last frame of the last shot.

`scripts/plan_shots.py` prints the carry speed in % of frame width per second and in px per second, how many seconds the mascot needs to be fully inside the frame, when the front edge reaches the right edge, and the x-position every second. Use those numbers in every prompt.

Objects and animals follow the same rule: a ball rolls in place at its natural rolling rhythm, a cat's legs move in a natural gait, a paper plane glides, and the ground carries them right at the carry speed.

## Who decides

The user decides what the mascot does. Claude asks first, then suggests, then locks the choice. Run this phase after the character sheet is approved (Claude needs the look) and BEFORE the support sheets, so the action and workflow sheets contain exactly the poses the plan uses.

## Step 1: ask for the user's plan

Ask in one message, with the Project Brief in mind: "How do you imagine the mascot behaving as it is carried across the screen? What does it do when it arrives, along the way, and as it leaves? Any moments in the video it should react to?" Also ask:
- Ad: should it meet the product, logo or tagline near the end? Any actions the brand does not want?
- Song: should it move to the beat (head-bob, steps at the BPM), sing, dance, react to the drop or chorus?
- Other: key moments in the content.

If the user already has a plan (for example "cape flies in, hero pose, waves, walks, crouches, flies out"), keep their order and wording and fit it to the arc and to the moving-ground rule.

## Step 2: suggest one or two plans

Always offer Plan A and, when the user has no firm plan, Plan B. Build them from three inputs:
1. The video's purpose and content (Project Brief).
2. How the mascot looks: outfit, signature item, personality from the faces.
3. How that kind of thing really behaves:
   - **Person**: human motion with believable weight (walk, jump, wave, dance steps), personality in posture.
   - **Object**: its real mechanics. A ball rolls and squashes on bounces; a paper plane glides and banks; a scooter rides and leans; a coin spins and flips; a logo assembles, rotates or rolls. Nothing it could not plausibly do, unless the user wants magic.
   - **Animal**: the species' gaits and habits. A cat strolls, stalks, crouches, pounces and grooms; a bird hops, flaps and glides; a dog trots, sniffs and wags; a turtle plods.

Plan format (6-8 lines each):

```
PLAN A - <title>
Idea: <one line and why it fits the video and the mascot>
Beats (arc phase, time range and x from the planner, action while carried, expression label):
1. Entrance (0-6 s, x -2% -> 8%): ...
2. Establish (6-15 s): ...
3. Personality (15-42 s): ...
4. Build-up (42-51 s): ...
5. Exit (51-60 s): ...
Video tie-in: <how it reacts to the song, ad, content>
```

Plan B uses a different entrance, middle and exit, not the same plan reworded. Every beat must be doable while being carried at constant speed. The user picks, mixes or revises. Lock the result as the Action Plan.

## The arc

Times and positions come from the planner:
1. **Entrance** (0-10%): carried in from the left edge; the first frame is never empty.
2. **Establish** (10-25%): who it is; a pose, greeting or signature-item gesture.
3. **Personality** (25-70%): one or two traits shown while carried across the middle of the frame.
4. **Build-up** (70-85%): a clear signal that something is about to happen.
5. **Exit** (85-100%): the finale; carried out of the right edge on the last frame.

Entrance ideas: signature item enters first; a glide or hop-in; an arrival pose (hand raised, hero stance). Exit ideas: crouch, push-off and rise into flight; a leap; riding something; a last look back and wave; a final gag in the last 3 seconds. Runs under about 20 s keep entrance, one establish beat and exit; runs over 90 s add a second personality beat so something new happens every 20-30 s.

Because the mascot is always moving, place every beat by its x-position from the planner's table (interpolate between rows), and note the beat times with it.

Song videos: if BPM is known, put repeating actions on the beat (120 BPM = one beat every 0.5 s) and big moves on the bar lines (every 4 beats).

## The handoff rule

The last frame of shot N and the first frame of shot N+1 are the same frame: same x-position, same height above the ground, same facing, same pose and walk-cycle phase, same direction and carry speed, same expression, same state of the signature item (for example cape trailing left in a gentle wave), same camera. The mascot is inside the frame at every joint.

- Each shot ends in a steady, easy-to-repeat state (mid-stride at a steady rhythm, a held pose, a smooth loop), never mid-jump or mid-spin.
- Claude records each joint as a **Handoff Card** and pastes it word for word as the end state of shot N and the FIRST FRAME of shot N+1:

```
HANDOFF CARD (end of shot N = first frame of shot N+1)
centre x=15.2% (front edge 18.7%, rear edge 11.7%) | feet on the ground line | facing screen right | mid-stride, right foot forward, left arm forward, arms swinging 20 degrees | carried right at 1.77% of frame width per second, same speed as the whole run | expression HAPPY | cape trailing to screen left in a gentle wave
```

- If the tool supports a start image, the user uses the last frame of the generated shot N as the start image of shot N+1.
- If the user ever says each shot should "enter and exit the frame", the meaning is: shot 1 enters, the last shot exits, and every joint in between is seamless. Do not make each shot enter and exit on its own: the mascot would be cut in half at each seam and jump.

## Action Plan card

After the user locks the plan, post it and update the Project Brief:

```
ACTION PLAN (locked)
Title: <...>
Carry speed: <% per s, px per s from the planner>
Beats with times, centre x, action while carried and expression labels: <table>
Handoff cards: <filled in Phase 6 when the shot plan exists>
Poses and expressions needed for the support sheets: <list>
```
