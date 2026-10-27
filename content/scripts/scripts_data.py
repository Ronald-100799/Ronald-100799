"""Reel scripts for Nov 2026, keyed by calendar row id. Build the Word docs with build_docs.js.

Line types: S = spoken (English; Ron adapts to Tamil/Thanglish while speaking), D = direction
(on-screen text, meme, SFX, B-roll, edit notes). Every number here comes from the row's checked
source in content_calendar.csv. Lines marked CHECK must be confirmed before filming.
"""
import json, sys

def S(t): return ["S", t]
def D(t): return ["D", t]

AUTH = "8 years in the gym, 5 of them training consistently"

SCRIPTS = {
# ============================== WEEK 1 ==============================
"R01": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX under all three lines. Jump cut on every line."),
    S("A weight-loss injection for ₹1,290 a month."), S("No diet. No gym. One shot a week?"), S("Before you book that appointment, watch this.")]),
  ("5–7s", "MEME", "fast", [D("MEME: shocked double-take on the price (your pick of a Tamil comedy reaction). Let the meme audio play.")]),
  ("7–14s", "AUTHORITY", "fast", [S(f"{AUTH}, and I read the actual trial behind this drug. Not the ads.")]),
  ("14–45s", "THE STORY", "", [
    S("Since March, the Ozempic molecule is off patent in India. Generics start around ₹1,290 a month."),
    S("Does it work? Yes. In the big STEP 1 trial, people lost about 15% of their body weight in 68 weeks. Placebo: 2.4%."),
    D("ON-SCREEN: STEP 1 trial, NEJM 2021: −14.9% vs −2.4% at 68 weeks"),
    S("So the gym is finished? No."),
    S("Here's what the ads skip. One: it's a prescription drug, and India's health ministry has warned against using it without a doctor."),
    S("Two: the most common side effects are nausea and diarrhoea."),
    S("Three: in that trial it was given along with diet and activity changes. Never instead of them.")]),
  ("45–55s", "WHY FOLLOW", "", [
    S("And nobody asks: how much of that lost weight is muscle? That's where lifting and protein come in.")]),
  ("55–75s", "CLOSE + SHARE", "fast", [
    S("Curious about it? Talk to a doctor, not a reel. And keep lifting either way."),
    S("Follow me. I read the studies so you get the truth, not the hype."),
    S("Share this with the friend who asked 'enna injection-u adhu?' They deserve the full story before spending money.")]),
]),
"R17": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Talking to your biceps."), S("Gym bros say it grows them faster."), S("Scientists laughed. Then they tested it.")]),
  ("5–7s", "MEME", "fast", [D("MEME: someone talking lovingly to an object. Comedy reaction.")]),
  ("7–14s", "AUTHORITY", "fast", [S("I've trained for 8 years. Here's what the study actually found.")]),
  ("14–50s", "THE STUDY", "", [
    S("Mind-muscle connection means focusing on the muscle working, not just moving the weight."),
    S("In 2018, researchers took 30 untrained men for 8 weeks. One group focused on squeezing the muscle. The other just focused on lifting the weight."),
    S("Biceps growth: 12.4% with the muscle focus. 6.9% without."),
    D("ON-SCREEN: Schoenfeld et al., Eur J Sport Sci 2018: 12.4% vs 6.9%"),
    S("So squeeze every rep of every exercise? No."),
    S("Strength didn't clearly improve with it, and it was a small study on beginners."),
    S("Use it on isolation moves like curls, raises and flyes. On a heavy squat, focus on moving the bar well.")]),
  ("50–55s", "FOLLOW CTA", "", [S("I break down one study like this every Tuesday. Follow so you don't miss the next one.")]),
  ("55–70s", "CLOSE + SHARE", "fast", [
    S("Bro-science? Not completely. Magic? Also no. It's a tool, for the right exercise."),
    S("Share this with the gym friend who talks to his biceps. Finally, some science on his side.")]),
]),
"R02": dict(link=("SETS", "Weekly sets planner: one page with every muscle group, a 6–10 starting range for beginners, and a box to tick per hard set."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Open on you, not the board."),
    S("Twenty sets for chest… every day?"), S("More sets, more muscle. Right?"), S("Half right. And the wrong half is why you're stuck.")]),
  ("5–7s", "MEME", "fast", [D("MEME: over-the-top 'this is too much' reaction scene.")]),
  ("7–14s", "AUTHORITY", "fast", [S("Gym Basics, episode 2. Eight years of training, and this is something I had to unlearn.")]),
  ("14–55s", "THE BOARD", "", [
    D("Reveal board: WEEKLY SETS PER MUSCLE. One number on screen early: 6–10."),
    S("Count your sets per muscle per WEEK, not per workout. And only count hard sets, the ones that end close to failure."),
    S("A 2017 meta-analysis found a dose-response: more weekly sets, more growth."),
    D("ON-SCREEN: Schoenfeld et al., J Sports Sci 2017"),
    S("So just do thirty sets? No."),
    S("If you're a beginner, you grow on far less. My recommendation: start with about 6 to 10 hard sets per muscle per week. Recover well. Add sets only when progress stalls."),
    S("The goal isn't the most you can survive. It's the least that keeps you growing.")]),
  ("55–62s", "SAVE + LINK", "", [S("Save this. And comment SETS, I'll send you my free weekly-sets planner.")]),
  ("62–80s", "CLOSE + SHARE", "fast", [
    S("Episode 3 next Wednesday: should every set go to failure? Follow so you don't miss it."),
    S("Share this with the gym buddy who trains chest six days a week. His shoulders will thank you.")]),
]),
"R18": dict(link=("REPS", "Rep-range cheat sheet: 3–6 for strength, 6–12 for most lifts, 12–30 for isolation and joint-friendly work, all taken close to failure."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Five reps for size."), S("Fifteen reps for 'toning'."), S("Both wrong, and the research proves it.")]),
  ("5–7s", "MEME", "fast", [D("MEME: confused-face reaction scene.")]),
  ("7–14s", "AUTHORITY", "fast", [S("Lifting Science, episode 1. Every Thursday, one study on this board.")]),
  ("14–55s", "THE BOARD", "", [
    S("Here's what the research shows: when sets are taken close to failure, heavy loads and light loads build similar muscle."),
    D("ON-SCREEN: Schoenfeld et al., J Strength Cond Res 2017 (meta-analysis)"),
    S("So rep range doesn't matter at all? Not quite."),
    S("Heavy loads win for strength. Light loads work for muscle, but they burn more and take longer."),
    S("And 'toning' isn't a rep range. It's building muscle and losing fat."),
    D("Board: 3–6 strength · 6–12 most lifts · 12–30 isolation. Label it 'my practical split'.")]),
  ("55–62s", "SAVE + LINK", "", [S("Save this. Comment REPS and I'll send you the one-page cheat sheet.")]),
  ("62–78s", "CLOSE + SHARE", "fast", [
    S("Next Thursday, episode 2: add weight or add reps? Follow for the series."),
    S("Share this with the friend who's scared heavy weights will make her bulky. Or who thinks light weights don't work.")]),
]),
"R03": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Quick cuts of sweets (B-roll or your own shots)."),
    S("Mysore pak. Adhirasam. Gulab jamun."), S("And your diet starts… after Diwali?"), S("That's the mistake. Here's why.")]),
  ("5–7s", "MEME", "fast", [D("MEME: relative forcing sweets on someone at a function.")]),
  ("7–12s", "AUTHORITY", "fast", [S("I track my calories, and I still plan for treats. Here's how.")]),
  ("12–50s", "THE PLAN", "", [
    S("Good news first. A study tracked people across the holiday season. Average gain: only about a third of a kilo."),
    D("ON-SCREEN: Yanovski et al., NEJM 2000: +0.37 kg over the holidays"),
    S("So it doesn't matter? No. Here's the bad news: most people never lost it afterwards. It stacks up year after year."),
    S("So, the plan. One: pick your two or three favourite sweets, not every box in the house."),
    S("Two: protein first at every meal. You'll naturally eat less of the rest."),
    S("Three: a 10-minute walk after big meals."),
    S("Four: don't 'start Monday'. Go back to normal eating at the very next meal.")]),
  ("50–70s", "CLOSE + SHARE", "fast", [
    S("The festival is one day. The damage comes from the ten days of 'adhan Diwali mudinjiduche'."),
    S("Follow me. I make fitness fit real Tamil life."),
    S("Share this with the friend who says 'diet after Diwali' every single year. This is their year.")]),
]),
"R19": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Couldn't walk after leg day?"), S("So it was a great workout… right?"), S("Your muscles disagree.")]),
  ("5–7s", "MEME", "fast", [D("MEME: struggling down the stairs / penguin walk comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of training, and this is one belief I had to unlearn.")]),
  ("12–45s", "THE TRUTH", "", [
    S("Soreness tells you something was new or hard. It doesn't tell you a muscle grew."),
    D("ON-SCREEN: Schoenfeld & Contreras, Strength Cond J 2013"),
    S("Proof? Marathon runners get badly sore, and they don't build big muscles."),
    S("And when you repeat the same workout, soreness fades… but you keep growing."),
    S("So soreness is bad? No. A little is normal. It's just a terrible scoreboard."),
    S("The real scoreboard: more reps or more weight over the weeks. Write it down.")]),
  ("45–62s", "CLOSE + SHARE", "fast", [
    S("Stop chasing pain. Chase progress."),
    S("Follow for lifting science without the bro-science."),
    S("Share this with the friend who limps after leg day like it's a trophy.")]),
]),
"R04": dict(sections=[
  ("0–4s", "HOOK STACK", "fast", [D("Rising SFX. Short reel (~45 s)."),
    S("Plus two kilos overnight after Diwali?"), S("Panic. Skip breakfast. Run 10K?"), S("Stop.")]),
  ("4–6s", "MEME", "fast", [D("MEME: over-dramatic crying scene, cut to the scale reveal.")]),
  ("6–10s", "AUTHORITY", "fast", [S("Eight years of training. Here's why festival spikes shouldn't scare you.")]),
  ("10–30s", "THE TRUTH", "", [
    S("You didn't gain two kilos of fat in one night. A sudden overnight jump is mostly water, salt and food still in your system."),
    S("Research on holiday weight shows the real average gain is small, around a third of a kilo."),
    D("ON-SCREEN: Yanovski et al., NEJM 2000"),
    S("So eat whatever, forever? No. Eat normally from tomorrow, and watch your weekly average, like I showed in my maintenance calories reel.")]),
  ("30–45s", "CLOSE + SHARE", "fast", [
    S("Follow. Next week: is your protein powder fake?"),
    S("Share this with the friend crying at the scale right now.")]),
]),
# ============================== WEEK 2 ==============================
"R05": dict(link=("PROTEIN", "Protein tub checklist: pure whey vs 'herbal' blends, how to look for third-party test reports, red flags on price, and a food-first list."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Hold your own tub to camera, label blurred (no brand names)."),
    S("Almost 70% of protein supplements tested didn't match their label."), S("Some had fungal toxins."), S("Is your tub one of them?")]),
  ("5–7s", "MEME", "fast", [D("MEME: betrayed / shocked reaction.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years in the gym, so I read this study properly. Not just the headlines.")]),
  ("12–55s", "THE REPORT", "", [
    S("The Citizens Protein Project tested 36 protein supplements sold in India. 25 of them, about 69%, had less protein than the label claimed."),
    S("About 14% had aflatoxins, mostly in plant-based and herbal blends."),
    D("ON-SCREEN: Philips et al., Medicine 2024 (no brand names on screen)"),
    S("So throw away all whey? No."),
    S("A 2025 follow-up tested 34 whey powders, and the 'medical' style powders did worse than many gym brands. So it's about choosing, not quitting."),
    D("ON-SCREEN: Citizens Protein Project 2, Medicine 2025"),
    S("How to choose: pure whey over herbal blends. Look for third-party test reports. And if the price looks too good, it is."),
    S("And ICMR's 2024 guidelines push food first: dal, curd, eggs, paneer, chicken, fish.")]),
  ("55–60s", "LINK", "", [S("Comment PROTEIN and I'll send you my checklist to check your tub.")]),
  ("60–78s", "CLOSE + SHARE", "fast", [
    S("Follow me. I read the reports so your money and your liver stay safe."),
    S("Share this with the friend who buys the cheapest tub online. It could save them more than money.")]),
]),
"R20": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Machines are for weak people."), S("Real lifters only use barbells."), S("A meta-analysis just ended this argument.")]),
  ("5–7s", "MEME", "fast", [D("MEME: ego showdown / face-off scene.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years in the gym. Here's what the data actually says.")]),
  ("12–50s", "THE STUDY", "", [
    S("A 2023 meta-analysis pooled 13 studies, over 1,000 people, comparing free weights and machines."),
    D("ON-SCREEN: Haugen et al., BMC Sports Sci Med Rehabil 2023"),
    S("Muscle growth: no difference."),
    S("So it doesn't matter at all? Not exactly. Strength is specific. Train with free weights and you get better at free-weight tests. Train on machines and you get better on machines."),
    S("Want a bigger squat? Squat. Want bigger quads? The leg press works too."),
    S("Machines are great for beginners, for training close to failure safely, and for hitting a weak muscle.")]),
  ("50–55s", "FOLLOW CTA", "", [S("One study every Tuesday. Follow for the next one.")]),
  ("55–72s", "CLOSE + SHARE", "fast", [
    S("Stop gym-shaming machines. Pick what you'll do consistently, and progress on it."),
    S("Comment: barbell or machine?"),
    S("And share this with the friend who laughs at the leg press. Then send him the study.")]),
]),
"R06": dict(link=("RIR", "One-page RIR guide: what 0–3 reps in reserve feel like, how to calibrate with one safe set to failure, and which exercises to keep at 1–3 RIR."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Open on you, not the board."),
    S("No pain, no gain."), S("Every set until you can't move."), S("Science says you're overdoing it.")]),
  ("5–7s", "MEME", "fast", [D("MEME: hero's 'one more rep' slow-motion struggle parody.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Gym Basics, episode 3. I burned out doing this in my early years. This fixed it.")]),
  ("12–55s", "THE BOARD", "", [
    D("Board: RIR = REPS IN RESERVE. 0 RIR = failure."),
    S("RIR is how many more reps you could have done. Zero means failure."),
    S("A 2023 meta-analysis found no evidence that going to failure builds more muscle than stopping a little short."),
    D("ON-SCREEN: Refalo et al., Sports Medicine 2023"),
    S("So never go to failure? No. You just don't need it on every set."),
    S("Beginner rule: stop with one to three reps in reserve. Form stays clean, recovery stays good, and you can do more quality sets."),
    S("To learn your RIR, take one set to failure on a safe exercise, like a machine curl, and see how far off your guess was.")]),
  ("55–62s", "SAVE + LINK", "", [S("Save this. Comment RIR and I'll send you my one-page RIR guide.")]),
  ("62–78s", "CLOSE + SHARE", "fast", [
    S("Episode 4 next Wednesday: how much protein do you actually need? Follow so you don't miss it."),
    S("Share this with the gym buddy who screams on every single rep.")]),
]),
"R21": dict(link=("TRACK", "Progression tracker: a simple log for sets × reps × weight per exercise, plus the add-reps-then-add-weight rule with a worked example."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Can't add weight every week?"), S("Think you've stopped progressing?"), S("You might be progressing, just not the way you think.")]),
  ("5–7s", "MEME", "fast", [D("MEME: 'level up' hero moment parody.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Lifting Science, episode 2. This is how progress keeps going when the weight won't move.")]),
  ("12–55s", "THE BOARD", "", [
    D("Board: PROGRESSIVE OVERLOAD = LOAD ↑ or REPS ↑"),
    S("Progressive overload means doing a bit more over time."),
    S("A 2022 trial in trained lifters: one group added weight, the other added reps at the same weight. Eight weeks."),
    D("ON-SCREEN: Plotkin et al., PeerJ 2022"),
    S("Muscle growth: similar. Strength: slightly better when adding weight."),
    S("So adding weight is the only way? No."),
    S("Example: 3 sets of 10 at 60 kg. Next week, 3 sets of 11. Then 12. Then go to 62.5 kg for 3 sets of 10."),
    S("Write it down. You can't progress what you don't track.")]),
  ("55–60s", "LINK", "", [S("Comment TRACK and I'll send you my free progression tracker.")]),
  ("60–78s", "CLOSE + SHARE", "fast", [
    S("Episode 3 next Thursday: how long to rest between sets. Follow for the series."),
    S("Share this with the friend who's been 'stuck' at the same weight for six months.")]),
]),
"R22": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Cardio kills your gains."), S("One treadmill session and your biceps disappear?"), S("Researchers tested it properly.")]),
  ("5–7s", "MEME", "fast", [D("MEME: running away from something, comedy chase scene.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of lifting. Here's what the research says about cardio.")]),
  ("12–48s", "THE STUDY", "", [
    S("A 2022 meta-analysis compared strength training alone with strength training plus cardio."),
    D("ON-SCREEN: Schumann et al., Sports Medicine 2022"),
    S("Muscle size and strength: no interference."),
    S("So cardio is totally free? Almost. One analysis looking at individual muscle fibres saw a small effect, mostly with running rather than cycling."),
    D("ON-SCREEN: Lundberg et al., Sports Medicine 2022"),
    S("So keep your cardio sensible. If gains are your priority, cycling and walking are easy wins. And maybe don't run a 10K right before leg day.")]),
  ("48–65s", "CLOSE + SHARE", "fast", [
    S("Your heart needs cardio. Your muscles can handle it."),
    S("Follow. I bust one lifting myth every week."),
    S("Share this with the friend who hasn't touched a treadmill since he joined the gym.")]),
]),
"R07": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX, softer than usual. Sincere tone."),
    S("Someone at home has sugar?"), S("And they've been told: just walk."), S("Walking is good. But they're missing something.")]),
  ("5–7s", "MEME", "fast", [D("MEME (keep it gentle and respectful): a parent waving off exercise advice, family comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("It's World Diabetes Day. Eight years of training, and this is the reel I most want families to see.")]),
  ("12–50s", "THE FACTS", "", [
    S("In India, about 1 in 9 adults has diabetes, and about 1 in 7 has prediabetes."),
    D("ON-SCREEN: ICMR-INDIAB study, 2023: 11.4% diabetes, 15.3% prediabetes"),
    S("Research pooling many trials found that strength training lowers HbA1c, the three-month sugar average, by about 0.3 to 0.6 points."),
    D("ON-SCREEN: umbrella review, resistance training & type 2 diabetes"),
    S("So should they lift heavy from tomorrow? No."),
    S("Start simple: chair squats, wall push-ups, resistance bands. Twice a week. With their doctor's okay.")]),
  ("50–70s", "CLOSE + SHARE", "fast", [
    S("Walking plus strength. Not walking instead of strength."),
    S("Follow for fitness that helps your whole family."),
    S("Share this to your family WhatsApp group. One reel could start the habit that changes their numbers.")]),
]),
"R08": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Rice saapta thoppai varum."), S("Every diet plan starts with: stop rice."), S("But your paati never counted carbs.")]),
  ("5–7s", "MEME", "fast", [D("MEME: grandmother serving another ladle of rice, comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years in the gym and years of tracking calories. Here's the science.")]),
  ("12–50s", "THE STUDY", "", [
    S("A big trial put 609 adults on either a healthy low-carb or a healthy low-fat diet for a full year."),
    D("ON-SCREEN: DIETFITS, JAMA 2018"),
    S("Low-carb lost about 6 kg. Low-fat about 5.3. No significant difference."),
    S("So rice is unlimited? No."),
    S("What decides fat loss is total calories. Rice is just easy to overeat because it's the base of the plate."),
    S("Fix the plate: half vegetables, a solid protein like dal, curd, egg, chicken or fish, and one measured cup of rice.")]),
  ("50–68s", "CLOSE + SHARE", "fast", [
    S("You don't have to give up your food culture to lose fat."),
    S("Follow me. I make science fit Tamil food."),
    S("Share this with the friend who replaced rice with sad oats. Let them eat in peace.")]),
]),
# ============================== WEEK 3 ==============================
"R09": dict(link=("MAALA", "41-day veg protein list: daily foods (milk, curd, paneer, dal with rice, chana, rajma, soya, peanuts) with rough protein per portion and a sample day."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Respectful tone throughout."),
    S("Maala pottachu."), S("No chicken. No eggs. Forty-one days."), S("Will your muscle disappear?")]),
  ("5–7s", "MEME", "fast", [D("MEME: a worried 'my gains!' comedy reaction. Avoid devotional scenes.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of training. Here's how to keep your gains while respecting your vow.")]),
  ("12–55s", "THE PLAN", "", [
    S("What protects muscle is simple: keep training, and keep your protein up."),
    S("ICMR's 2024 guidelines say you can get good-quality protein by combining foods, like cereals with pulses."),
    D("ON-SCREEN: ICMR-NIN Dietary Guidelines for Indians, 2024"),
    S("So veg protein is weaker? Not if you combine foods and eat enough of them."),
    S("Your daily list: milk and curd, paneer, dal with rice, chana or rajma, soya chunks, peanuts."),
    S("And unless your practice says otherwise, the vow changes your food, not your workout.")]),
  ("55–62s", "SAVE + LINK", "", [S("Save this. Comment MAALA and I'll send you a 41-day veg protein list.")]),
  ("62–78s", "CLOSE + SHARE", "fast", [
    S("Respect the vow. Keep the gains."),
    S("Follow for fitness that fits our culture."),
    S("Share this with your friend going to Sabarimala this year. Swamiye saranam Ayyappa.")]),
]),
"R23": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Show the two exercises side by side."),
    S("Same exercise."), S("Just change your arm position…"), S("…and your triceps grow about one and a half times more.")]),
  ("5–7s", "MEME", "fast", [D("MEME: mind-blown reaction.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Every Tuesday I break down one study. This one should change your arm day.")]),
  ("12–52s", "THE STUDY", "", [
    S("In a 12-week study, people trained one arm with overhead cable extensions and the other with the arm by their side."),
    D("ON-SCREEN: Maeo et al., Eur J Sport Sci 2023"),
    S("Whole triceps: plus 19.9% overhead, plus 13.5% by the side. The long head: 28.5% versus 13.9%."),
    S("So pushdowns are useless? No. They still grew."),
    S("Why the difference? The overhead position stretches the long head more. Training a muscle at longer lengths looks promising, though scientists are still confirming exactly why."),
    S("Do this: one overhead extension every arm day, with a controlled stretch at the bottom.")]),
  ("52–57s", "SAVE", "", [S("Save this for arm day.")]),
  ("57–72s", "CLOSE + SHARE", "fast", [
    S("Small change, big difference. That's science-based lifting."),
    S("Follow for one study every Tuesday."),
    S("Share this with the friend whose triceps never grow. This might be why.")]),
]),
"R10": dict(link=("GRAMS", "Protein calculator: grams per day at 1.6 g/kg for 50–100 kg, plus Indian foods with protein per portion and a 3–4 meal split."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Open on you, not the board."),
    S("Body weight times one gram of protein?"), S("Or two grams?"), S("Or 'too much protein spoils your kidneys'?")]),
  ("5–7s", "MEME", "fast", [D("MEME: maths-teacher / calculator confusion comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Gym Basics, episode 4. Let's do the maths on the board.")]),
  ("12–55s", "THE BOARD", "", [
    D("CHECK before filming: confirm the 1.6 g/kg breakpoint in the paper's results section."),
    S("A big meta-analysis of 49 trials found protein boosts muscle gains when you lift, and the benefit levelled off around 1.6 grams per kilo per day."),
    D("ON-SCREEN: Morton et al., Br J Sports Med 2018"),
    D("Board: 70 kg × 1.6 = 112 g/day"),
    S("Example: 70 kilos means about 112 grams a day."),
    S("So you need three scoops of whey? No."),
    S("Food first: curd, eggs, dal, paneer, chicken, fish, soya. Split it across three or four meals."),
    S("And if you have any kidney condition, check with your doctor first.")]),
  ("55–62s", "SAVE + LINK", "", [S("Save this. Comment GRAMS and I'll send you a protein calculator with Indian food portions.")]),
  ("62–78s", "CLOSE + SHARE", "fast", [
    S("Episode 5 next Wednesday: can you burn belly fat only? Follow."),
    S("Share this with the friend who thinks one egg a day is 'high protein'.")]),
]),
"R24": dict(link=("REST", "Rest-time guide: big compound lifts vs isolation, the 'rest until you can hit your reps' rule, and what to do between sets."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Checking your phone between sets?"), S("Lazy? Wasting your gains?"), S("Maybe not.")]),
  ("5–7s", "MEME", "fast", [D("MEME: impatient waiting / clock-watching comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Lifting Science, episode 3. One study, one board.")]),
  ("12–52s", "THE BOARD", "", [
    S("A 2024 analysis of the research found a small muscle-growth benefit when you rest longer than about 60 seconds between sets."),
    D("ON-SCREEN: Singer et al., 2024 (Bayesian meta-analysis)"),
    S("So rest ten minutes? No."),
    D("Board: BIG LIFTS 2–3 min · ISOLATION 1–2 min (label: my practical guide)"),
    S("Big lifts like squats, bench and rows: two to three minutes. Isolation like curls and raises: one to two."),
    S("Rest until you can hit your target reps again. Not until your phone battery dies."),
    S("Short rests feel pumped. But the pump isn't the goal. Reps and weight over the weeks are.")]),
  ("52–58s", "LINK", "", [S("Comment REST and I'll send you the one-page rest guide.")]),
  ("58–74s", "CLOSE + SHARE", "fast", [
    S("Episode 4 next Thursday: do slow reps build more muscle? Follow for it."),
    S("Share this with the friend who rests twenty seconds and wonders why his reps crash.")]),
]),
"R11": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Ten thousand steps a day?"), S("Can't hit it, so you walk zero?"), S("Good news from a 2025 study.")]),
  ("5–7s", "MEME", "fast", [D("MEME: lazy hero refusing to get up, comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years in fitness, and this is the most freeing study I've read this year.")]),
  ("12–45s", "THE STUDY", "", [
    S("A 2025 Lancet review pooled dozens of studies. Compared with 2,000 steps a day, 7,000 steps was linked with a 47% lower risk of death from any cause."),
    D("ON-SCREEN: Ding et al., Lancet Public Health 2025"),
    S("So ten thousand is useless? No. More is still fine. But most of the benefit shows up by around seven thousand."),
    S("Easy steps: walk while you're on calls, ten minutes after each meal, take the stairs, park a little farther.")]),
  ("45–62s", "CLOSE + SHARE", "fast", [
    S("Start where you are. Add a thousand a week."),
    S("Follow for simple science, no guilt."),
    S("Share this with the friend who says 'walking-ku time illa'. Seven thousand is doable.")]),
]),
"R25": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Ten minutes of stretching before every workout?"), S("School PT taught us that."), S("It might be costing you strength.")]),
  ("5–7s", "MEME", "fast", [D("MEME: strict school PT-master scene parody.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of lifting. Here's the warm-up research school PT never told us.")]),
  ("12–48s", "THE STUDY", "", [
    S("A systematic review found long static stretches, 60 seconds or more per muscle, reduced performance by about 4.6% right after."),
    D("ON-SCREEN: Behm et al., Appl Physiol Nutr Metab 2016"),
    S("So stretching is bad? No."),
    S("Short holds under 60 seconds changed performance by only about 1%. And dynamic warm-ups slightly improved it."),
    S("A simple warm-up: five minutes of light cardio, then two lighter sets of your first exercise."),
    S("Save the long stretching for after your session.")]),
  ("48–64s", "CLOSE + SHARE", "fast", [
    S("Follow for lifting science minus the school myths."),
    S("Share this with your gym partner who stretches for fifteen minutes and then can't lift.")]),
]),
"R12": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Creatine makes you bald."), S("Creatine damages your kidneys."), S("Both stories started somewhere. Here's where.")]),
  ("5–7s", "MEME", "fast", [D("MEME: wig-falling-off comedy reveal.")]),
  ("7–12s", "AUTHORITY", "fast", [S("I've followed the creatine research for years. Here's the honest version.")]),
  ("12–52s", "THE EVIDENCE", "", [
    S("The hair fear comes from a 2009 study on rugby players. A hormone linked to hair loss, DHT, went up. But nobody measured hair."),
    S("In 2025, a 12-week trial finally measured hair directly: 5 grams of creatine a day versus placebo."),
    S("No change in DHT. No change in hair."),
    D("ON-SCREEN: Lak et al., JISSN 2025"),
    S("So creatine is safe for everyone? Not so fast."),
    S("That trial was 12 weeks, in young, healthy men. If you have kidney disease or you're on medication, ask your doctor first.")]),
  ("52–58s", "FOLLOW CTA", "", [S("Follow. I check the studies before I recommend anything.")]),
  ("58–70s", "CLOSE + SHARE", "fast", [
    S("Share this with the friend who's scared to try creatine because of one forwarded message.")]),
]),
# ============================== WEEK 4 ==============================
"R13": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Eat only between 8 and 4…"), S("…and lose weight without dieting?"), S("A 12-month trial tested exactly this.")]),
  ("5–7s", "MEME", "fast", [D("MEME: hungry person staring at the clock, comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of training. Here's what the research actually says.")]),
  ("12–48s", "THE TRIAL", "", [
    S("139 people. 12 months. Both groups ate the same calories, but one group ate only between 8 am and 4 pm."),
    D("ON-SCREEN: Liu et al., NEJM 2022"),
    S("Result: about 8 kg versus 6.3 kg lost. And the difference wasn't statistically significant."),
    S("So fasting is useless? No."),
    S("If a time window helps you eat less, use it. If it makes you binge at night, skip it."),
    S("The magic was never the clock. It was the calories.")]),
  ("48–66s", "CLOSE + SHARE", "fast", [
    S("Comment IF if you've tried it."),
    S("Follow. I'll tell you what works, not what's trending."),
    S("Share this with the friend who skips breakfast and then eats a full biryani at 11 pm.")]),
]),
"R26": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Monday: international chest day."), S("Next chest day: next Monday."), S("Your chest is waiting too long.")]),
  ("5–7s", "MEME", "fast", [D("MEME: queue at the bench press on Monday, comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Every Tuesday, one study. This one is about your split.")]),
  ("12–50s", "THE RESEARCH", "", [
    S("A 2016 meta-analysis: when weekly sets were the same, training a muscle twice a week beat once a week for growth."),
    D("ON-SCREEN: Schoenfeld et al., Sports Medicine 2016"),
    S("So train every muscle every day? No."),
    S("Newer research suggests total weekly sets matter most. Training twice a week mainly helps you spread those sets so each one is good quality."),
    D("ON-SCREEN: 2025 meta-regression, volume & frequency"),
    S("Practical: upper-lower or full-body, hitting each muscle at least twice a week.")]),
  ("50–56s", "FOLLOW CTA", "", [S("One study every Tuesday. Follow.")]),
  ("56–70s", "CLOSE + SHARE", "fast", [
    S("Comment your split and I'll reply."),
    S("Share this with your bro-split buddy. No hate, just science.")]),
]),
"R14": dict(link=("FAT", "Fat-loss basics: deficit, protein target, weekly lifting, daily steps, and how to track the weekly average weight."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Open on you, not the board."),
    S("A thousand crunches a day."), S("Sweat belt on."), S("Same belly?")]),
  ("5–7s", "MEME", "fast", [D("MEME: TV-shop infomercial parody of a sweat belt.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Gym Basics, episode 5. The myth that refuses to die.")]),
  ("12–55s", "THE BOARD", "", [
    S("In one study, people trained just one leg for 12 weeks, around a thousand reps a session."),
    D("ON-SCREEN: Ramírez-Campillo et al., J Strength Cond Res 2013"),
    S("They lost body fat overall. But the trained leg didn't lose more fat than the other leg."),
    S("So it's settled? Honestly, not 100%. One newer study did find extra belly-fat loss from ab exercise, but it was a small study."),
    S("For most people, the belly goes when overall body fat goes."),
    D("Board: DEFICIT + PROTEIN + LIFTING + STEPS")]),
  ("55–62s", "SAVE + LINK", "", [S("Save this. Comment FAT and I'll send you my fat-loss basics.")]),
  ("62–76s", "CLOSE + SHARE", "fast", [
    S("Crunches build your abs. Fat loss shows them."),
    S("Follow. Gym Basics recap next week."),
    S("Share this with the friend who just bought a sweat belt.")]),
]),
"R27": dict(link=("SERIES", "Lifting Science recap: episodes 1–4 on one page (rep ranges, progression, rest, tempo) with the source for each."), sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Five seconds down. Five seconds up."), S("Time under tension equals more muscle?"), S("Turns out… not really.")]),
  ("5–7s", "MEME", "fast", [D("MEME: slow-motion hero walk parody.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Lifting Science, episode 4. The last one of this round.")]),
  ("12–50s", "THE BOARD", "", [
    S("A 2026 meta-analysis found rep tempo has minimal overall effect on muscle growth."),
    D("ON-SCREEN: 2026 meta-analysis on repetition tempo ('How slow should you go?')"),
    S("So control doesn't matter? No. Control matters. Slow doesn't."),
    S("Lower the weight under control. Lift with intent. No bouncing."),
    S("Super-slow reps usually just mean lighter weights.")]),
  ("50–57s", "LINK", "", [S("Comment SERIES and I'll send you the recap of all four episodes.")]),
  ("57–72s", "CLOSE + SHARE", "fast", [
    S("Follow for season 2."),
    S("Share this with the friend counting 'one thousand one' on every curl.")]),
]),
"R15": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX. Rain B-roll if you have it."),
    S("Mazhai… so no gym today?"), S("Your excuse is like the rain. It never stops."), S("Here's a 15-minute fix.")]),
  ("5–7s", "MEME", "fast", [D("MEME: lazy hero wrapped in a blanket during rain, comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of training taught me one thing: consistency beats perfect conditions.")]),
  ("12–48s", "THE PLAN", "", [
    S("Research shows light loads can build similar muscle to heavy loads, when you go close to failure."),
    D("ON-SCREEN: Schoenfeld et al., J Strength Cond Res 2017"),
    S("So home workouts equal the gym? Not exactly. Progressing is harder without weights. But it beats zero."),
    S("The 15-minute circuit: squats, push-ups, backpack rows, lunges, plank. Three rounds, close to failure."),
    D("Show each exercise for 1–2 s with a counter on screen.")]),
  ("48–64s", "CLOSE + SHARE", "fast", [
    S("Save this for the next rain day."),
    S("Follow. I make fitness work in real Tamil Nadu weather."),
    S("Share this with the friend who skips the gym every time it drizzles.")]),
]),
"R28": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Gym pona height valaraadhu."), S("Every relative has said it."), S("Is it true?")]),
  ("5–7s", "MEME", "fast", [D("MEME: relatives giving unsolicited advice at a function.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of lifting, and this myth still follows every teen who joins a gym.")]),
  ("12–48s", "THE EVIDENCE", "", [
    D("CHECK before filming: read the growth-plate section of the position statement and keep the wording within it."),
    S("An international consensus of sports medicine and paediatric experts supports resistance training for kids and teens, when it's supervised and planned for their age."),
    D("ON-SCREEN: Lloyd et al., Br J Sports Med 2014 (International Consensus)"),
    S("The old fear was growth-plate injuries. Newer research has challenged that fear."),
    S("So teens can max out deadlifts? No."),
    S("Supervision. Technique first. Sensible weights. Progress slowly.")]),
  ("48–64s", "CLOSE + SHARE", "fast", [
    S("Follow. I bust the myths your relatives forward."),
    S("Share this with your parents, so your younger brother or sister can start the right way.")]),
]),
"R16": dict(sections=[
  ("0–5s", "HOOK STACK", "fast", [D("Rising SFX."),
    S("Diet perfect."), S("Gym perfect."), S("Sleeping five hours? Your fat loss is losing.")]),
  ("5–7s", "MEME", "fast", [D("MEME: sleepy office worker nodding off, comedy.")]),
  ("7–12s", "AUTHORITY", "fast", [S("Eight years of training, and the most underrated tool is free.")]),
  ("12–48s", "THE STUDY", "", [
    S("In a study, dieters ate the same calories for 14 days, once sleeping 8.5 hours, once sleeping 5.5."),
    D("ON-SCREEN: Nedeltcheva et al., Annals of Internal Medicine 2010"),
    S("With good sleep they lost 1.4 kg of fat. With short sleep, just 0.6. Same diet."),
    S("So one bad night ruins everything? No. It was two weeks of short sleep, in a small study of ten people."),
    S("The fix: a fixed wake-up time, phone away 30 minutes before bed, and no caffeine late in the day.")]),
  ("48–64s", "CLOSE + SHARE", "fast", [
    S("Follow for the boring stuff that actually works."),
    S("Share this with the friend who replies to your messages at 2 am.")]),
]),
}

if __name__ == "__main__":
    json.dump(SCRIPTS, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(SCRIPTS), "scripts")
