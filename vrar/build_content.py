# ================= CONTENT =================
def S(x): return x
bl = lambda t, l=None: bullet(t, l)
# ---------- TITLE / ABSTRACT ----------
heading(None, TITLE, page_break=True)
sub('Abstract')
para('Assembly workers on a machine assembly line follow paper manuals or fixed screens, so they must look away from the '
     'part, search for the right page, and cope with the same level of detail whether they are new or highly experienced. '
     'This report describes an Adaptive Augmented Reality (AR) work instruction system for a gearbox assembly line. An AR '
     'device (tablet or head-mounted display) recognises the machine part with the camera and overlays the next step '
     'directly on it: arrows, highlighted bolts, a ghost image of the part to be fitted, the torque value and a short text. '
     'The system adapts to the operator. A skill score calculated from step time and errors decides whether the instruction '
     'is shown in full detail with animation (novice), with key values only (expert), or in between. Sensors and a vision '
     'checker confirm every step, lock the tool when a wrong part is used, and send the data to a supervisor dashboard.')
sub('Objectives')
for t_ in ['To show assembly steps in the worker\'s own view so that the eyes and hands stay on the product.',
           'To adapt the amount of guidance automatically to the skill and the performance of each operator.',
           'To detect wrong parts, wrong torque and skipped steps while they happen and prevent defective units.',
           'To reduce training time, cycle time and assembly errors, and to give the supervisor live data.']: bl(t_)
sub('Tools and technologies')
table(['Component / Tool', 'Specification', 'Purpose'], [
    ['AR device', 'Android tablet / HoloLens 2 class headset', 'Camera, display, voice commands'],
    ['Unity + AR Foundation / Vuforia', 'Unity 2022 LTS, Model Targets from CAD', 'Tracking and 3D overlay'],
    ['Vision checker', 'Lightweight CNN (part, bolt, orientation)', 'Detect wrong or missing parts'],
    ['IoT torque tool', 'MQTT messages over the plant Wi-Fi', 'Confirm tightening torque'],
    ['Grafana dashboard (browser)', 'Time-series database + web dashboard', 'View cycle time, errors and station status'],
    ['MES / PLC', 'Work order and station signals', 'Link the system with the line']],
    [2.1, 2.7, 2.2], size=12)
sub('Key idea in one line')
para('Instruction detail = f (operator skill score, step time, error count, step risk). The more help a worker needs, the more '
     'the AR overlay shows; the more skilled the worker, the more the overlay stays out of the way.', italic=True)

# ---------- 1. INTRODUCTION ----------
heading(1, 'Introduction', page_break=True)
sub('1.1 Background')
para('Machine assembly lines build products such as gearboxes, engines and electrical panels from many parts. Operators '
     'follow work instructions that tell them which part to pick, where to fit it and how tightly to fasten it. Traditional '
     'instructions are printed sheets or a monitor next to the station. The worker has to read, remember, look back at the '
     'product and match what was read with what is seen. This takes time and leads to mistakes, especially when product '
     'variants change often.')
sub('1.2 Problem statement')
para('Design an Adaptive AR Work Instruction system for machine assembly lines that overlays step by step guidance on the '
     'real machine part and automatically adjusts the level of guidance to the skill of the operator.')
sub('1.3 Augmented Reality in manufacturing')
para('Augmented Reality adds computer generated information to the real scene in real time and registers it with real objects. '
     'In assembly, AR can show the exact bolt to tighten, the position of a part that is not yet fitted, and the next tool to '
     'use. Compared with Virtual Reality, the worker still sees the real station, which is essential for safety and quality.')
table(['Feature', 'Paper / screen manual', 'AR work instruction'], [
    ['Where information is shown', 'Separate sheet or monitor', 'On the real part, in the field of view'],
    ['Finding the right step', 'Manual page turning', 'Automatic, step follows the work'],
    ['Part and bolt identification', 'Picture and part number', 'Highlighted part, arrow and ghost image'],
    ['Error detection', 'Final inspection', 'Immediately at the step (vision + sensors)'],
    ['New product variant', 'Reprint and retrain', 'Publish new instructions to devices'],
    ['Matching worker skill', 'Same for everyone', 'Adaptive detail level']],
    [2.1, 2.3, 2.6], size=12)
sub('1.4 Need for adaptive instructions')
para('A new operator needs animations, text and warnings for every step. An expert finds the same content slow and '
     'distracting, and starts to ignore the screen, which also hides important safety messages. An adaptive system gives each '
     'operator the right amount of help and brings the detail back when the operator makes errors.')
sub('1.5 Scope of the project')
for t_ in ['One gearbox assembly station of nine steps with four fastened bolts on the bearing cover.',
           'Three skill levels (novice, skilled, expert) and automatic switching between them.',
           'Authoring in the Unity editor, display on an AR tablet / headset, supervisor dashboard.',
           'The screenshots in this report are simulated screens built to show the design; no factory trial was run.']: bl(t_)
sub('1.6 Benefits expected')
table(['Benefit', 'How it is achieved'], [
    ['Shorter training', 'Full guidance for novices, no classroom for each variant'],
    ['Fewer errors', 'Vision and torque checks at every step with tool lock'],
    ['Faster cycle', 'Hands-free voice control and automatic step advance'],
    ['Safety', 'Warnings shown at the point of risk, in the line of sight'],
    ['Data', 'Step times and errors stored for continuous improvement']],
    [2.0, 5.0], size=12)

sub('1.7 VR, AR and MR compared')
table(['Technology', 'Real world visible?', 'Typical device', 'Use in assembly'], [
    ['Virtual Reality (VR)', 'No, fully virtual', 'Closed headset', 'Training before going to the line, planning'],
    ['Augmented Reality (AR)', 'Yes, with overlays', 'Tablet, smart glasses', 'Live guidance on the real part (this project)'],
    ['Mixed Reality (MR)', 'Yes, virtual objects interact', 'HoloLens 2', 'Guidance with spatial anchors and remote help']],
    [1.7, 1.6, 1.6, 2.1], size=12)
sub('1.8 Challenges of today\'s assembly instructions')
for lead, t_ in [('Information overload: ', 'long manuals hide the few facts that matter for the current step.'),
                 ('Frequent variants: ', 'each change of product needs new printed sheets and retraining.'),
                 ('Skill gap: ', 'new operators and experts are given the same instruction.'),
                 ('Late detection: ', 'a wrong bolt is usually found at the final inspection, after more work is added.')]: bl(t_, lead)
sub('1.9 Applications')
for t_ in ['Automobile and engine assembly lines.', 'Electrical panel and wiring harness assembly.', 'Aircraft and machinery maintenance and repair.',
           'Training of new workers and cross-training between stations.']: bl(t_)

sub('1.10 Existing AR work instruction solutions')
table(['Solution', 'Main idea', 'Gap addressed here'], [
    ['Microsoft Dynamics 365 Guides', 'Step by step holographic guidance on HoloLens', 'Detail level is authored, not tuned to each worker'],
    ['PTC Vuforia work instructions', 'AR authoring from CAD with tracking of the product', 'Limited use of live skill data'],
    ['Connected worker platforms', 'Digital instructions with skills tracking and analytics', 'Guidance not linked to vision and tool checks per step']],
    [2.0, 2.6, 2.4], size=12)
# ---------- 2. DESCRIPTION ----------
heading(2, 'Description', page_break=True)
sub('2.1 System overview')
para('The system has three parts: the shop-floor devices (AR device, torque tool, scanner, PLC), the adaptive work instruction '
     'server, and the Unity editor and web dashboard used by engineers and supervisors. The server holds the instructions, the operator profiles and '
     'the rules. The AR device only has to track the part, render the overlay and send camera frames and sensor events.')
table(['Module', 'Function'], [
    ['Tracking service', 'Recognises the gearbox from its CAD model (Model Target) and keeps the overlay fixed to it; QR marker as fallback'],
    ['Instruction database', 'Stores steps, 3D models, animations, texts, audio and safety notes for each product variant'],
    ['Step manager', 'State machine that moves from step to step only when the completion checks are passed'],
    ['Vision checker', 'CNN that checks part type, bolt length, orientation and presence of grease or gasket'],
    ['Torque tool bridge', 'Receives torque and angle values over MQTT and locks the tool on a wrong step'],
    ['Adaptation engine', 'Calculates the skill score and selects the detail level for every step'],
    ['Operator profile service', 'Keeps skill score, history, language and preferred interaction (voice / touch)'],
    ['Analytics dashboard', 'Shows cycle time, errors by step, first pass yield and station status']],
    [1.9, 5.1], size=12)
sub('2.2 Overlay elements used')
table(['Element', 'Meaning', 'Colour'], [
    ['Numbered ring', 'Fastener or location to work on, number gives the order', 'Green'],
    ['Tick on grey ring', 'Fastener already completed and confirmed', 'Grey'],
    ['Red ring and banner', 'Wrong part or failed check, work is held', 'Red'],
    ['Ghost part', 'Transparent copy of the part that must be fitted', 'Blue'],
    ['Arrow / line', 'Direction of movement or location of the correct bin', 'Blue'],
    ['Instruction card', 'Title, tool, torque, text and buttons', 'Dark blue']],
    [1.8, 3.9, 1.3], size=12)
sub('2.3 Adaptation of the instruction')
para('After every step the adaptation engine updates a skill score between 0 and 1 for the operator. The score rises when '
     'steps are finished within the target time without errors and falls when time is exceeded by more than 20% or errors '
     'occur. The score selects the detail level of the next steps.')
table(['Level', 'Skill score', 'What the operator sees'], [
    ['Novice', 'below 0.40', '3D animation, three text lines, safety warning, voice help, confirmation of each step'],
    ['Skilled', '0.40 to 0.75', 'Highlights, torque value, short text; warnings only for risky steps'],
    ['Expert', '0.75 and above', 'Bolt highlight and torque value only; step advances on the sensor signal']],
    [1.1, 1.3, 4.6], size=12)
sub('2.4 Rules of the adaptation engine')
table(['Condition', 'Action'], [
    ['Step time more than 20% above target', 'Reduce skill score; keep or increase detail'],
    ['Two errors in the last five steps', 'Step down one detail level and notify the supervisor'],
    ['Five consecutive steps on time and without error', 'Step up one detail level'],
    ['Risky step (torque, hot part, moving part)', 'Always show the safety card, even for experts'],
    ['New or changed product variant', 'Show one level more detail for the first three units'],
    ['Operator asks for help by voice', 'Show full detail for this step only']],
    [3.3, 3.7], size=12)
sub('2.5 Information exchanged during one step')
table(['From', 'To', 'Data'], [
    ['Step manager', 'AR device', 'Step id, detail level, 3D assets, torque target'],
    ['AR device camera', 'Vision checker', 'Camera frame (10 per second)'],
    ['Vision checker', 'Step manager', 'Part / bolt result with confidence value'],
    ['Torque tool', 'Torque bridge (MQTT)', 'Torque value, angle, tool id'],
    ['Step manager', 'Adaptation engine', 'Step time and error count'],
    ['Adaptation engine', 'Profile service', 'Updated skill score of the operator'],
    ['Server', 'Dashboard', 'Station, step, cycle time, errors']],
    [1.9, 2.1, 3.0], size=12)
sub('2.6 Safety and ergonomics')
for lead, t_ in [('Safety first: ', 'a safety card is always shown for torque, hot and moving-part steps, at every level.'),
                 ('Clear view: ', 'overlays are semi-transparent and kept away from the area where the hands work.'),
                 ('Short sessions: ', 'tablets on a stand or light glasses are used to avoid fatigue over a full shift.'),
                 ('Fail-safe: ', 'if tracking is lost the overlay freezes and the torque tool is locked.')]: bl(t_, lead)

# ---------- 3. WORKING STEPS ----------
heading(3, 'Working Steps', page_break=True)
sub('3.1 Steps followed')
for i, (lead, txt) in enumerate([
    ('Study the assembly: ', 'list the nine steps of the gearbox GB-220 station, the parts, tools, torque values and risks.'),
    ('Prepare the 3D data: ', 'import the CAD model, reduce it for mobile use and create the Model Target used for tracking.'),
    ('Author the instructions: ', 'in the Unity editor create the step cards with title, tool, torque, completion check and the three detail levels.'),
    ('Define the adaptation rules: ', 'set the skill thresholds (0.40 and 0.75), the 20% time tolerance and the error rules.'),
    ('Build the AR application: ', 'create the Unity scene with the Model Target, instruction cards, highlights, ghost part and arrows.'),
    ('Connect the tools: ', 'link the torque wrench and scanner through MQTT and the vision checker to the camera feed.'),
    ('Start the work order: ', 'the operator scans the order QR code; the profile service returns the skill score.'),
    ('Run the steps: ', 'the overlay shows each step at the selected detail level; the step ends when the sensor and vision checks pass.'),
    ('Handle errors: ', 'a wrong part turns the ring red, locks the tool and informs the supervisor until the check is passed.'),
    ('Adapt and log: ', 'after each step the skill score is updated; times and errors are sent to the dashboard.')], 1):
    step(i, txt, lead)
figure('shots/w1_mtg.png', 'Output 1: Creating the Model Target from the CAD file', 'Fig. 1 - Model Target Generator: guide view, tracking settings, training status and dataset report for the gearbox.', width=6.5, maxh=2.9)
figure('shots/ar1_novice.png', 'Output 2: AR view for a novice operator', 'Fig. 2 - Highlighted bolts 3 and 4, animation button and full text for Step 4 of 9.', width=6.5, maxh=3.0)

# ---------- 3 (continued) ----------
sub('3.2 Operator view at different skill levels')
figure('shots/ar2_expert.png', 'Output 3: AR view for an expert operator', 'Fig. 3 - Only the bolt rings and the torque value are shown; the card is small and Step 4 is ahead of time.', width=6.5, maxh=3.0)
figure('shots/ar3_error.png', 'Output 4: Error detected by the vision checker', 'Fig. 4 - A wrong bolt (M8) is detected at bolt 3; the ring turns red, the tool is locked and the supervisor is notified.', width=6.5, maxh=3.0)
sub('3.3 Handheld (mobile) view')
figure('shots/m1_mobile.png', 'Output 5: Instruction on a mobile phone (screenshot)', 'Fig. 5 - Portrait screenshot with compact card, step progress and Back / Animation / Next buttons.', width=2.0, maxh=3.9)

# ---------- 3.4 table steps ----------
sub('3.4 Gearbox GB-220 assembly steps and checks')
table(['Step', 'Operation', 'Tool / part', 'Check', 'Target (s)'], [
    ['1', 'Pick housing and place on jig', 'Housing H-220', 'Vision: part and position', '8'],
    ['2', 'Insert shaft into housing', 'Shaft S-14', 'Vision: seated', '12'],
    ['3', 'Press bearing on shaft', 'Press, bearing B-6204', 'Press force signal', '15'],
    ['4', 'Fix the bearing cover', 'Torque wrench 12 N·m, M6 x 20 x 4', 'Torque + vision', '25'],
    ['5', 'Fit gear wheel and key', 'Gear G-40, key', 'Vision: key in slot', '18'],
    ['6', 'Apply grease (5 g)', 'Dispenser', 'Dispenser volume', '12'],
    ['7', 'Close side plate', 'Plate P-3, 6 bolts', 'Vision + torque', '20'],
    ['8', 'Final torque check', 'Torque wrench', 'Torque sweep', '10'],
    ['9', 'Scan QR and release', 'Scanner', 'Order match', '5']],
    [0.5, 2.3, 2.0, 1.4, 0.8], size=12)
sub('3.5 Voice commands used')
table(['Command', 'Action'], [
    ['"Next"', 'Go to the next step (when no sensor signal is available)'],
    ['"Back"', 'Return to the previous step'],
    ['"Show animation"', 'Play the 3D animation of the current step'],
    ['"Show details" / "Hide details"', 'Increase or reduce the detail level for this step'],
    ['"Call supervisor"', 'Send an alert to the supervisor dashboard']],
    [2.6, 4.4], size=12)

sub('3.6 Sample session of one operator (simulated)')
table(['Time', 'Event', 'Detail level shown'], [
    ['10:40:55', 'Operator S. Meena scans work order WO-5521', 'Novice (score 0.31)'],
    ['10:41:20', 'Steps 1 and 2 finished within target time', 'Novice'],
    ['10:41:49', 'Step 3 took 21 s against 15 s target', 'Novice (score 0.29)'],
    ['10:42:11', 'Wrong bolt M8 detected at step 4, tool locked', 'Novice, error banner'],
    ['10:42:30', 'Correct bolt fitted, torque 12.1 N\u00b7m accepted', 'Novice'],
    ['11:30:00', 'After 5 correct steps in a row score rises to 0.44', 'Skilled']],
    [1.0, 4.0, 2.0], size=12)
# ---------- 4. DIAGRAMMATIC REPRESENTATION ----------
heading(4, 'Diagrammatic Representation', page_break=True)
figure('shots/d1_arch.png', '4.1 System architecture', 'Fig. 6 - Shop-floor devices, the adaptive instruction server and the analytics dashboard.', width=6.6, maxh=4.1)
figure('shots/d3_levels.png', '4.2 Detail levels of the instruction', 'Fig. 7 - Novice, skilled and expert levels selected from the skill score.', width=6.6, maxh=2.4)
figure('shots/d2_flow.png', '4.3 Flowchart of the adaptive instruction process', 'Fig. 8 - From the work order scan to the release of the unit with adaptation after every step.', width=5.9, maxh=8.9)
sub('4.4 Supervisor dashboard (sample data)', True)
figure('shots/w2_dash.png', None, 'Fig. 9 - Grafana dashboard of Line 2 showing cycle time, errors by step and live station status. The values are sample data of the simulation, not measurements from a factory.', width=6.6, maxh=3.6)
sub('4.5 Development environment')
figure('shots/u1_unity.png', None, 'Fig. 10 - Unity editor (Scene view) with the Model Target, the instruction layer, the Adaptation Engine settings and the console log of one step.', width=6.6, maxh=3.3)
sub('4.6 Game view in Play mode')
figure('shots/u2_play.png', None, 'Fig. 11 - Play mode: the Game view shows the AR overlay for the novice operator while the Console logs the checks.', width=6.6, maxh=3.3)

# ---------- 5. CONCLUSION ----------
heading(5, 'Conclusion', page_break=True)
para('An Adaptive AR work instruction system for a machine assembly line was designed. The instructions are overlaid on the '
     'real gearbox so the operator does not need to look away, and they are checked by sensors and a vision model at every '
     'step. The adaptation engine changes the detail level from the operator skill score, giving animations and warnings to '
     'new workers and a quiet, fast view to experts. The Unity authoring setup, the AR operator views, the error handling, the '
     'dashboard and the Unity setup were presented as simulated screens. A real trial on a line is needed to measure the '
     'actual reduction in training time, cycle time and errors.')
sub('Advantages')
for t_ in ['Guidance is in the line of sight and fixed to the part.', 'Errors are stopped at the moment they happen.',
           'Each operator gets the amount of help that is needed.', 'Instructions for new variants are published digitally in minutes.']: bl(t_)
sub('Limitations')
for t_ in ['Tracking can fail with reflective parts, poor light or when the part is covered by the hands.',
           'A head-mounted display can be tiring for a full shift; tablets or lighter glasses may be preferred.',
           'The skill score depends on enough data; the first units of a new worker use the novice level.']: bl(t_)
sub('Future enhancements')
for t_ in ['Hand tracking to detect which part the worker picks, with pick-to-light bins.', 'Learning the best detail level for each step with machine learning.',
           'Remote expert support with a shared AR view for rare faults.', 'Digital twin of the line to test new variants before release.',
           'Multi-language voice and text for a mixed workforce.']: bl(t_)
sub('References')
table(['S. No.', 'Reference'], [
    ['1', 'Unity Technologies, AR Foundation and Unity 2022 LTS documentation'],
    ['2', 'PTC Vuforia Engine, Model Targets developer guide'],
    ['3', 'Microsoft, HoloLens 2 and Dynamics 365 Guides documentation'],
    ['4', 'ISO 9241-210, Human-centred design for interactive systems'],
    ['5', 'Azuma R., A Survey of Augmented Reality, Presence: Teleoperators and Virtual Environments, 1997']],
    [0.8, 6.2], size=12)
