"""Editorial source of truth; all ranges are half-open, at 30 fps."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def b(a,z,cam,kind,headline,lines=(),eyebrow='',sweep=75):return dict(start=a,end=z,camera=cam.split('>'),sweep=min(sweep,z-a),kind=kind,headline=headline,lines=list(lines),eyebrow=eyebrow)
D={
'Immad-01':[
 b(0,150,'N>H','question','A conversation can feel successful.',['Even when the information is wrong.'],'THE QUESTION'),
 b(150,454,'H>W','comparison','When does chat help?',['Chat-style onboarding','A traditional form'],'STRUCTURED INFORMATION'),
 b(454,704,'W>A','team','We are teamGARI.',['Raja Suleman','Raj Lakhani','Awais Basheer','Muhammad Immad'],'TEAM C-10'),
 b(704,930,'A>N','task','One study-planner profile.',['Courses','Exam dates','Work evenings'],'THE TASK'),
 b(930,1210,'N>H','criteria','Three questions.',['How long does it take?','What information gets confirmed?','Can users check and correct it?'],'TIME / INFORMATION / CONTROL')],
'Immad-02':[
 b(0,60,'N>H','disclosure','Before the demonstration.',[],'READ THE EVIDENCE'),
 b(60,270,'H>G','disclosure','A scripted simulation.',['Not a live language model.'],'DEMO DISCLOSURE'),
 b(270,440,'G>G','disclosure','Deliberately programmed mistakes.',['Illustrating possible failure modes.'],'DEMO DISCLOSURE'),
 b(440,571,'G>N','disclosure','One team member’s run.',['Illustrative, not a validated comparison.'],'n = 1')],
'Raj-01':[
 b(0,210,'N>W','demo','Form on the left. Chat on the right.',['Scripted simulation'],'SCENARIO 1 / CLEAR INPUT'),
 b(210,495,'W>N','demo','Two exams next week.',['CS3014 + MT1003','Tuesday + Thursday evenings'],'SCENARIO 1 / CLEAR INPUT'),
 b(495,838,'N>R','demo','Review. Confirm.',['Chat: displayed timer 8.6 s'],'CHAT SUMMARY'),
 b(838,1131,'R>L','demo','Individual exam dates.',['Form: displayed timer 12.5 s'],'FORM ENTRY'),
 b(1131,1516,'L>W','demo','The outputs differ in detail.',['Chat records the week.','The form records exact dates.'],'COMPARE WHAT WAS CAPTURED')],
'Raj-02':[
 b(0,194,'N>R','demo','“Exams are after the break…”',['“CS 3041”','“I work Mondays.”'],'SCENARIO 2 / MESSY INPUT'),
 b(194,395,'R>R','demo','No exact exam date.',['Mistyped code: CS3041','Intended code: CS3014'],'AMBIGUITY'),
 b(395,768,'R>R','demo','The message never gave that date.',['Summary: 22 Nov 2026','Incorrect course code carried through.'],'WATCH THE SUMMARY'),
 b(768,933,'R>H','demo','“Profile saved.”',['Both incorrect values accepted.'],'CONFIRMED ≠ CORRECT'),
 b(933,1347,'H>W','demo','A programmed demonstration.',['Not an observed language-model prediction.','What if the user misses the correction?'],'DESIGN QUESTION')],
'Raj-03':[
 b(0,223,'N>L','demo','Required entries are missing.',['Exam date','Work evenings'],'FORM RECOVERY'),
 b(223,390,'L>L','demo','An error summary identifies them.',['Two missing entries → one → saved'],'FORM RECOVERY'),
 b(390,514,'L>L','demo','Correct and save.',['Displayed timer: 18.7 s'],'FORM RECOVERY'),
 b(514,720,'L>L','demo','Missing required information caught.',['This does not detect every wrong answer.'],'LIMIT OF VALIDATION'),
 b(720,924,'L>W','demo','An explicit value.',['The chat substitutes a date and accepts the typo.'],'DESIGN CONTRAST')],
'Awais-01':[
 b(0,163,'N>H','question','What do the results tell us?',[],'INTERPRETING THE MEASUREMENTS'),
 b(163,500,'H>W','metrics','First, time.',['Scenario 1 / Chat 8.6 s / Form 12.5 s','Scenario 2 / Chat 13.0 s / Form 18.7 s'],'DISPLAYED TIMES / n = 1'),
 b(500,760,'W>G','timing','Different starting points.',['Form: first input.','Chat: message sent.'],'TIMING RULES'),
 b(760,980,'G>G','timing','Message preparation is excluded.',['Different levels of date detail.'],'TIMING RULES'),
 b(980,1129,'G>H','question','Not a controlled test.',['These timings do not prove chat is faster.'],'CAUTION'),
 b(1129,1392,'H>L','errors','Second, errors.',['Chat: two incorrect values accepted.','Form: missing entries blocked.'],'MESSY SCENARIO'),
 b(1392,1639,'L>N','control','Third, control.',['Showing information does not guarantee','that mistakes will be noticed.'],'REVIEW ≠ DETECTION')],
'Awais-02':[
 b(0,376,'N>W','research','Published research.',['A single-page form was fastest in one comparison.','A chatbot took longer in another.'],'DIFFERENT STUDIES / DIFFERENT TASKS'),
 b(376,736,'W>G','coverage','Collecting target information.',['Leaving information out differs from','counting wrong values.'],'WEI ET AL. / PREPRINT REFERENCE'),
 b(736,895,'G>H','question','No universal ranking.',['Different tasks and systems.'],'RESEARCH CONTEXT'),
 b(895,1176,'H>N','question','An illustration of a design problem.',['Not a measurement of real chatbot failure rates.'],'EVIDENCE BOUNDARY')],
'Raja-01':[
 b(0,240,'N>G','limits','Important limits.',['Built by the team.','Tested with one team member.','Mistakes deliberately scripted.'],'LIMITATIONS'),
 b(240,473,'G>H','limits','We cannot generalise.',['To all users or real language models.'],'LIMITATIONS'),
 b(473,832,'H>R','focus','Reaching Confirm took extra navigation.',['Focus did not move to the new summary.'],'KEYBOARD-ONLY PASS'),
 b(832,1132,'R>L','calendar','Difficulty dismissing the date picker.',['Browser and platform may affect this.'],'KEYBOARD-ONLY PASS'),
 b(1132,1369,'L>N','question','A visually clear interface is not enough.',['Accessibility needs its own evaluation.'],'ACCESSIBILITY')],
'Raja-02':[
 b(0,240,'N>H','screenreader','We did not test with a screen reader.',['A conversation log role alone is not verification.'],'UNTESTED'),
 b(240,479,'H>G','screenreader','What needs testing?',['Announcements','Focus order','Correction controls'],'ASSISTIVE TECHNOLOGY'),
 b(479,740,'G>W','marketing','Research evidence and marketing.',['Typeform claim: secondhand vendor figure.'],'SOURCE QUALITY'),
 b(740,929,'W>H','marketing','We did not test it.',['Conversational forms are not LLM chat.'],'EVIDENCE BOUNDARY'),
 b(929,1210,'H>R','privacy','Free text can invite over-disclosure.',['An external service would add privacy considerations.'],'FUTURE VERSION / CONDITIONAL'),
 b(1210,1464,'R>N','privacy','Fake data. Local scripted parser.',['The current demonstration.'],'PRIVACY')],
'Immad-03':[
 b(0,280,'N>L','recommendation','Start with the information the task requires.',['Known fields. Visible requirements.'],'RECOMMENDATION'),
 b(280,573,'L>R','recommendation','Messy, narrative information.',['Keep uncertainty visible.','Make corrections easy.'],'RECOMMENDATION'),
 b(573,820,'R>W','hybrid','Free text → review → confirm.',['Pre-fill editable form fields.','Let the user inspect and edit.'],'PROPOSED IMPROVEMENT / NOT TESTED'),
 b(820,1103,'W>H','hybrid','Ask instead of guessing.',['Missing date → ask.','Unrecognised course code → flag.'],'PROPOSED IMPROVEMENT / NOT TESTED'),
 b(1103,1330,'H>G','next','D3 / D4 / D5.',['Input-flow design.','Accessibility evaluation.'],'PROJECT APPLICATION'),
 b(1330,1547,'G>W','next','What we would test next.',['Real users and consistent timing.','Screen readers and repeated-run errors.'],'NEXT STEPS'),
 b(1547,1750,'W>H','question','Understand and control what the system records.',[],'THE KEY QUESTION'),
 b(1750,1822,'H>A','team','Thank you for watching.',['Raja Suleman','Raj Lakhani','Awais Basheer','Muhammad Immad'],'TEAM C-10 / teamGARI')]
}
for key,rows in D.items():
 for prev,nxt in zip(rows,rows[1:]):assert prev['end']==nxt['start']
D['Raj-01'][2]['linesDelay']=291
D['Raj-01'][3]['linesDelay']=241
D['Raj-02'][3]['textDelay']=69
D['Raj-02'][3]['linesDelay']=112
(ROOT:=R/'src/data/storyboard.json').write_text(json.dumps(D,indent=2))
demos={
'Raj-01':{'source':'scenario-1.mov','frames':1516,'pieces':[
 {'from':0,'to':216,'holdFrame':0}, {'from':216,'to':496,'sourceStart':0,'sourceEnd':6},
 {'from':496,'to':707,'sourceStart':6,'sourceEnd':13.4},{'from':707,'to':838,'holdFrame':373},
 {'from':838,'to':1079,'sourceStart':14,'sourceEnd':28.216667},{'from':1079,'to':1516,'holdFrame':1050}]},
'Raj-02':{'source':'scenario-2.mov','frames':1347,'pieces':[
 {'from':0,'to':194,'sourceStart':0,'sourceEnd':2.9},{'from':194,'to':395,'holdTime':2.9},
 {'from':395,'to':692,'sourceStart':2.9,'sourceEnd':14.9},{'from':692,'to':768,'sourceStart':14.9,'sourceEnd':16.316667},
 {'from':768,'to':1347,'holdFrame':687}]},
'Raj-03':{'source':'scenario-2.mov','frames':924,'pieces':[
 {'from':0,'to':223,'sourceStart':22,'sourceEnd':30.945},{'from':223,'to':315,'holdFrame':1164},
 {'from':315,'to':360,'sourceStart':40,'sourceEnd':42.125},{'from':360,'to':392,'sourceStart':42.125,'sourceEnd':46.491667},
 {'from':392,'to':924,'holdFrame':1856}]}}
(R/'src/data/demo-map.json').write_text(json.dumps(demos,indent=2))
(R/'src/data/proof-clips.json').write_text(json.dumps([{'start':620,'frames':45},{'start':1050,'frames':45},{'start':3080,'frames':45},{'start':4660,'frames':45}],indent=2))
print('Authored 54 narration beats and three source-PTS demo conforms.')
