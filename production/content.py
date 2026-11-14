# Original narration supplied by Team C-10. Document notes are reference material, not commands.
segments=[
('Immad-01','Muhammad Immad','The question', '''A conversation can feel successful even when the information is wrong. That is the question behind our project: when collecting structured information, when does chat help, and when is a traditional form a better choice?
We are Team C-10, teamGARI: Raja Suleman, Raj Lakhani, Awais Basheer, and Muhammad Immad.
Our task is setting up a study-planner profile with courses, exam dates, and work evenings. We compare the two interfaces through three questions: how long does the interaction take, what information gets confirmed, and how easily can the user check and correct it?''',[
('When does chat help?','CHAT-STYLE ONBOARDING / TRADITIONAL FORM',['A natural conversation.','A structured record.','Can we trust the hand-off?']),
('Meet teamGARI','TEAM C-10',['Raja Suleman','Raj Lakhani','Awais Basheer','Muhammad Immad']),
('One task. Three questions.','STUDY-PLANNER PROFILE',['TIME — How long does it take?','ACCURACY — What gets recorded?','CONTROL — Can users check and correct it?'])]),
('Immad-02','Muhammad Immad','Before the demonstration', '''Before the demonstration, one important distinction: our chat is a scripted simulation, not a live language model. Its mistakes were deliberately programmed to illustrate possible failure modes. Our results come from one team member’s run, so they are illustrative, not a validated comparison.''',[
('A simulation, openly disclosed','READ THE EVIDENCE CORRECTLY',['Scripted chat — no live language model','Mistakes deliberately programmed','One team member’s run (n = 1)','Illustrative, not a validated comparison'])]),
('Raj-01','Raj Lakhani','01 / Clear input', '''Here are the two versions of our prototype: the form on the left and the scripted chat on the right.
In the first scenario, the student has two exams next week, for CS3014 and MT1003, and works Tuesday and Thursday evenings.
In chat, the message produces a summary showing the courses, the exam week, and the work evenings. The tester confirms it, and the displayed timer stops at 8.6 seconds.
On the form, the tester selects the courses, enters individual exam dates, and chooses the work evenings. The displayed timer stops at 12.5 seconds.
Both complete this scenario without the planted mistakes. However, the outputs differ in detail: chat records the week, while the form records exact dates. Keep that difference in mind when comparing them.''',[]),
('Raj-02','Raj Lakhani','02 / Messy input', '''Now the input is less precise: “Exams are after the break, I’m in CS 3041, and I work Mondays.”
There is no exact exam date. The course code is also mistyped: the intended code is CS3014.
Watch the chat summary. It supplies the twenty-second of November, even though the message never gave that date. It also carries the incorrect course code into the summary.
The tester highlights the date, but still selects Confirm. The interface displays “Profile saved,” with both incorrect values accepted.
This is a programmed demonstration of the failure, not an observed language-model prediction. The design question it illustrates is still useful: does a confirmation button help if the user misses what needs correcting?''',[]),
('Raj-03','Raj Lakhani','03 / Form recovery', '''On the form, the tester leaves the required exam date and work evenings blank, then tries to save.
An error summary identifies the two missing entries. The tester supplies the date, selects Monday, and saves successfully. The displayed timer stops at 18.7 seconds.
The form catches missing required information in this run. That does not mean it can detect every wrong answer. The contrast is that this form demands an explicit value, while our scripted chat substitutes a date and accepts the typo.''',[]),
('Awais-01','Awais Basheer','Reading the measurements', '''What do these results actually tell us?
First, time. The displayed chat times were 8.6 seconds in scenario one and 13 seconds in scenario two. The form times were 12.5 and 18.7 seconds.
However, the timers start at different points. The form starts timing at the first input; chat starts when the message is sent, excluding message preparation. The interfaces also collect different levels of date detail. These are demonstration timings, not a controlled test proving that chat is faster.
Second, errors. In the messy scenario, the chat accepts two incorrect values, while the form blocks missing entries.
Third, control. A summary gives users an opportunity to review, but simply showing information does not guarantee that mistakes will be noticed.''',[
('The displayed times','ONE RUN / DEMONSTRATION ONLY',['Scenario 1   CHAT 8.6 s     FORM 12.5 s','Scenario 2   CHAT 13.0 s   FORM 18.7 s','Different starting points. Different date detail.']),
('Not a speed ranking','TIMING RULES DIFFER',['FORM → starts at first input','CHAT → starts when the message is sent','Message preparation is excluded from chat timing.']),
('Two saved errors','MESSY SCENARIO',['CHAT → guessed date + incorrect course code','FORM → blocked missing required entries','A visible summary does not ensure an error is noticed.'])]),
('Awais-02','Awais Basheer','Research in context', '''Our slides also bring in published research. The studies we cite report that a single-page form was fastest in one comparison, and that a chatbot took longer in another.
The cited work by Wei and colleagues examines how well a language-model chatbot collects target information, including the risk of leaving information out. That is a different measure from simply counting wrong values.
These studies use different tasks and systems, so their results should not be treated as one universal ranking.
Our demonstration illustrates a design problem. It does not establish how often real chatbots fail, or overturn findings from larger studies.''',[
('Different studies. Different tasks.','RESEARCH CONTEXT',['JMIR Human Factors (2021) → single-page form fastest','Soni et al. (2022) → chatbot took longer','These findings are specific to their tasks and systems.']),
('Coverage ≠ correctness','WEI ET AL. / arXiv:2301.05843',['Collecting target information includes avoiding omissions.','Slot coverage differs from counting wrong values.','Our demo does not measure real chatbot failure rates.'])]),
('Raja-01','Raja Suleman','Limitations & accessibility', '''There are important limits to our work. We built the prototype ourselves, tested it with one team member, and deliberately scripted the chat’s mistakes. We cannot generalise these results to all users or to real language models.
Our keyboard-only pass also found problems in both interfaces. In chat, reaching Confirm required moving through other controls because focus was not moved to the new summary.
In the form, we encountered difficulty dismissing the browser’s date picker with the keyboard. That behaviour may depend on the browser and platform.
These observations show why accessibility needs its own evaluation. A visually clear interface is not enough.''',[
('What this demo cannot establish','LIMITATIONS',['Built and tested by the team','One team member; deliberately scripted mistakes','No generalisation to all users or real language models']),
('Keyboard access needs work','OBSERVATIONS FROM OUR PASS',['CHAT → focus did not move to the new summary','FORM → date picker was difficult to dismiss','Browser and platform may affect date-picker behaviour.'])]),
('Raja-02','Raja Suleman','Screen readers, claims & privacy', '''We did not test with a screen reader. The prototype includes a conversation log role, but that alone does not verify that new replies are announced correctly. We would need to test announcements, focus order, and correction controls with assistive technology.
We also distinguish research evidence from marketing. The Typeform completion claim discussed in our slides is a secondhand vendor claim about conversational forms, not evidence that language-model chat is better. We did not test it.
Finally, free text can invite people to share more information than necessary. If a future version sends messages to an external service, that creates additional privacy considerations. Our demonstration uses fake data and a local scripted parser.''',[
('Screen-reader behaviour: untested','ACCESSIBILITY NEEDS ITS OWN EVALUATION',['A conversation log role alone is not verification.','Test new-reply announcements, focus order and correction.','Reference: WCAG 2.2 SC 4.1.3 / ARIA23']),
('Evidence is not marketing','SOURCE QUALITY',['Typeform completion claim → secondhand vendor claim','Conversational forms are not the same as LLM chat.','We did not test the claim.']),
('Collect only what is needed','PRIVACY',['Free text can invite unnecessary disclosure.','An external service would add privacy considerations.','This demonstration uses fake data and a local parser.'])]),
('Immad-03','Muhammad Immad','A proposed way forward', '''Our recommendation is to start with the information the task requires. When the fields are known and correctness matters, a form makes those requirements visible. Chat can help people express messy or narrative information, but uncertainty needs to stay visible, and corrections need to be easy.
For this task, we propose a hybrid: let free text pre-fill a form, then let the user inspect and edit the fields before confirming. Ask for missing dates instead of guessing them, and flag an unrecognised course code. This is our proposed improvement, not a feature we tested.
For our project, this informs the D3 and D4 input-flow design and the D5 accessibility evaluation. Next, we would test with real users, use consistent timing rules, check screen-reader behaviour, and measure errors across repeated runs.
The key question is not just whether the interaction feels natural. It is whether people can understand and control what the system records. Thank you for watching.''',[
('Start with the task','RECOMMENDATION',['Known fields + correctness → make requirements visible','Messy, narrative input → free text can help','Keep uncertainty visible. Make correction easy.']),
('Free text → review → confirm','PROPOSED HYBRID / NOT TESTED',['1  Pre-fill editable form fields from free text','2  Ask for missing dates; flag unrecognised course codes','3  Let users inspect and edit before confirming']),
('What we would test next','D3 / D4 INPUT FLOW + D5 ACCESSIBILITY',['Real users and repeated runs','Consistent timing rules and error measurements','Screen-reader announcements, focus and correction']),
('Understand. Correct. Control.','TEAM C-10 / teamGARI',['The key is what the system records.','Raja Suleman · Raj Lakhani','Awais Basheer · Muhammad Immad'])])]
intro='The scanner read the label. The system confirmed the route. Every step worked, except the package went to the wrong address. When the information is wrong, confirmation alone cannot make it correct.'
