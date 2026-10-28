# Ozempic off patent: motion-graphics sample (red / black / white)

A 15 s graphics-only sample showing what the motion toolkit can do for a topic reel. In a real reel these graphics sit in clear wall space beside Ron and are cut to his lines; the music bed here only stands in for his voice.

| Time | Beat | Tool |
|---|---|---|
| 0–2.6 s | Hook: ₹10,850/month counts up (Wegovy, before 20 Mar 2026) over a rising riser; red glow builds | GSAP + counter driven from HyperFrames time |
| 2.6–5.6 s | Turn: price struck out, screen shake, a 3D padlock opens and falls, "OFF PATENT" stamp, generic "₹1,290/month" | Remotion 3D overlay (`tools/remotion-3d` PatentUnlock) + GSAP |
| 5.6–8.4 s | What the drug is: a 3D injection pen, "Semaglutide: the drug inside Ozempic & Wegovy" | Three.js |
| 8.4–11.8 s | What happened: Patent ends 20 Mar 2026 → 7+ companies launch → prices crash (up to ~90% lower) | GSAP flowchart |
| 11.8–15 s | Payoff: 3D bars brand vs generic, "88% less" (₹1,290 vs ₹10,850), sources line | Three.js + GSAP |

Facts were checked via Business Today, 20–21 Mar 2026: Natco launched at ₹1,290/month (multi-dose vial, lower strengths); Wegovy costs ₹10,850–16,400/month; 7+ companies launched at ₹1,290–4,200/month; reported price falls of up to ~90%. 88% = 1 − 1,290 / 10,850.

Sound: `assets/sfx/riser.wav` and `bed.wav` are synthesised by `build/synth.py` (no licence needed); thump, tick, rise, swoosh, whoosh, digits and popsoft come from Ron's library.

Render: `npx hyperframes@0.8.183 render --quality delivery -o renders/raw.mp4`, then `bash build/master.sh renders/raw.mp4 renders/ozempic-motion-sample.mp4` (−14 LUFS).
