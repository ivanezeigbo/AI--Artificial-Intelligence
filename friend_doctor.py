'''
This is the algorithm for my Friend Doctor, your favorite chatbot and medical non-expert.
Be advised though that this bot does not render any medical advise, but gives probabilistic prognosis on information you provide.
This bot would be developed to something a bit different and much better, but for the finals - here you go!
Reference: Www2.hawaii.edu. (n.d.). [online] Available at: http://www2.hawaii.edu/~nreed/ics361/assignments/prolog/birdKB.pro [Accessed 18 Apr. 2018].
'''

import random as ran
import random
import re
import time
from pyswip.prolog import Prolog
from pyswip.easy import *



KB ="""
%KB

suggestion('see a dermatologist.') :- gender(A), member(A, [male, female]), above_45_years(L), member(L, [yes, no]), feel_discomfort(yes), feel_discomfort_where(F), member(F, [arm, stomach, back, leg, thigh, chest, foot, other]), is_bleeding(no), is_sore(N), member(N, [yes, no]), it_aches(no), discomfort_internal(no), excess_physical_activity(no), had_bad_food(S), member(S, [no, unsure]).
suggestion('see a cardiologist.') :- gender(A), member(A, [male, female]), above_45_years(L), member(L, [yes, no]), feel_discomfort(yes), feel_discomfort_where(chest), is_bleeding(no), is_sore(no), it_aches(yes), discomfort_internal(yes), eat_meat_often(J), member(J, [yes, unsure]), excess_physical_activity(yes), had_bad_food(B), member(B, [yes, no, unsure]).
suggestion('see a gynecologist'):- gender(female), above_45_years(no), feel_discomfort(yes), feel_discomfort_where(private_part), is_bleeding(yes), discomfort_internal(yes), excess_physical_activity(Z), member(Z, [no, maybe]), had_period_before(yes), way_out_of_period_cycle(yes).
suggestion("look up a dermatologist if it's a skin problem") :- gender(A), member(A, [male, female]), above_45_years(L), member(L, [yes, no]), feel_discomfort(no), disturbance_where(R), member(R, [arm, back, chest, stomach, leg, thigh, foot, private_part, other]), discomfort_internal(no), had_bad_food(I), member(I, [no, unsure]).
suggestion('see a dentist, dude'):- gender(A), member(A, [male, female]), above_45_years(L), member(L, [yes, no]), feel_discomfort(yes), feel_discomfort_where(tooth), is_bleeding(yes), discomfort_internal(no), excess_physical_activity(V), member(V, [yes, maybe, no]), had_bad_food(S), member(S, [no, unsure]), too_much_sweets(G), member(G, [yes, no, unsure]).
suggestion('get a massage!!'):- gender(A), member(A, [male, female]), above_45_years(no), feel_discomfort(yes), is_bleeding(no), is_sore(no), it_aches(yes), discomfort_internal(yes), feel_discomfort_where(D), member(D, [arm, back, leg, thigh, foot, other]), excess_physical_activity(Q), member(Q, [yes, maybe]), had_bad_food(no).
suggestion('see a nutritionist, man'):- gender(A), member(A, [male, female]), above_45_years(U), member(U, [yes, no]), feel_discomfort(yes), feel_discomfort_where(S), member(S, [arm, back, stomach, leg, thigh, foot, other]), is_bleeding(no), is_sore(J), member(J, [yes, no]), it_aches(C), member(C, [yes, no]), discomfort_internal(yes), excess_physical_activity(P), member(P, [yes, no, maybe]), had_bad_food(yes).
suggestion('see a pharmacist, my friend.') :- gender(P), member(P, [male, female]), above_45_years(J), member(J, [yes, no]), excess_physical_activity(N), member(N, [yes, maybe]), feel_discomfort(yes), is_bleeding(yes), discomfort_internal(no), feel_discomfort_where(R), member(R, [arm, back, chest, leg, thigh, foot, other]), had_bad_food(no).
suggestion('relax!') :- gender(P), member(P, [male, female]), above_45_years(yes), feel_discomfort(yes), feel_discomfort_where(E), member(E, [arm, back, stomach, leg, thigh, foot, other]), is_bleeding(no), it_aches(yes), is_sore(K), member(K, [yes, no]), discomfort_internal(yes), excess_physical_activity(M), member(M, [yes, maybe]), had_bad_food(no).
suggestion('check out a urologist, perhaps?') :- gender(male), above_45_years(G), member(G, [yes, no]), feel_discomfort(yes), feel_discomfort_where(private_part), discomfort_internal(T), member(T, [yes, no]), is_bleeding(no), is_sore(yes), it_aches(L), member(L, [yes, no]), excess_physical_activity(O), member(O, [yes, maybe, no]), had_bad_food(no). 

diagnosis('it might just be your period coming') :- gender(female), above_45_years(no), feel_discomfort(yes), discomfort_internal(yes), feel_discomfort_where(private_part), is_bleeding(yes), excess_physical_activity(J), member(J, [no, maybe], had_period_before(no).
diagnosis('it might be your period.. :)') :- gender(female), above_45_years(no), feel_discomfort(yes), discomfort_internal(yes), feel_discomfort_where(private_part), is_bleeding(yes), excess_physical_activity(J), member(J, [no, maybe]), had_period_before(yes), way_out_of_period_cycle(no), slightly_out_of_cycle(yes).
diagnosis('it might be due to the stressful physical activity, in my opinion.') :- gender(female), above_45_years(no), feel_discomfort(yes), discomfort_internal(yes), feel_discomfort_where(private_part), is_bleeding(yes), excess_physical_activity(yes), had_period_before(yes), way_out_of_period(yes).
diagnosis('keep those sweets away!') :- suggestion('see a dentist').
diagnosis('go to the hospital soon. Might be a heart problem!!') :- suggestion('see a cardiologist.'), how_painful(very).
diagnosis('ask for some medicine from the pharmacist.') :- suggestion('see a pharmacist, my friend.'), how_painful(Y), member(Y, [very, slightly]).
diagnosis("if you don't get better, visit a general physician immediately!") :- suggestion('relax'), how_painful(very).
diagnosis('you must go immediately to a gynecologist; it is critical!') :- suggestion('see a gynecologist'), how_painful(very).
diagnosis('visit the dentist soon, I guess...') :- suggestion('see a dentist.'), how_painful(very).
diagnosis('check out your physician!') :- how_painful(K), member(K, [very, slightly]).


gender(X) :- menuask(gender, X, [male, female]).
above_45_years(X) :- menuask(above_45_years, X, [yes, no]).
feel_discomfort(X) :- menuask(feel_discomfort, X, [yes, no]).
feel_discomfort_where(X) :- feel_discomfort(yes), menuask(feel_discomfort_where, X, [arm, back, tooth, chest, stomach, leg, thigh, foot, private_part, other]).
disturbance_where(X):- feel_discomfort(no), menuask(disturbance_where, X, [arm, back, chest, stomach, leg, thigh, foot, tooth, private_part, other]).
is_bleeding(X) :- feel_discomfort(yes), feel_discomfort_where(B), member(B, [arm, tooth, back, chest, leg, thigh, foot, private_part, other]), menuask(is_bleeding, X, [yes, no]).
is_sore(X) :- is_bleeding(no), menuask(is_sore, X, [yes, no]).
it_aches(X) :- is_sore(D), member(D, [yes, no]), menuask(it_aches, X, [yes, no]).
discomfort_internal(X) :- menuask(discomfort_internal, X, [yes, no]).
eat_meat_often(X) :- feel_discomfort_where(F), member(F, [tooth, chest]), discomfort_internal(yes), menuask(eat_meat_often, X, [no, yes, unsure]).
too_much_sweets(X) :- feel_discomfort_where(tooth), menuask(too_much_sweets, X, [yes, no, unsure]).
excess_physical_activity(X) :- feel_discomfort_where(C), member(C, [arm, tooth, stomach, back, leg, thigh, foot, private_part]), discomfort_internal(yes), menuask(excess_physical_activity, X, [yes, no, maybe]).
had_bad_food(X) :- feel_discomfort_where(C), member(C, [arm, tooth, stomach, back, leg, thigh, foot, other]), menuask(had_bad_food, X, [yes, no, unsure]).
how_painful(X) :- menuask(how_painful, X, [very, slightly]).
had_period_before(X) :- discomfort_internal(yes), is_bleeding(yes), gender(female), above_45_years(no), feel_discomfort(yes), feel_discomfort_where(private_part), menuask(had_period_before, X, [yes, no]).
way_out_of_period_cycle(X) :- had_period_before(yes), menuask(way_out_of_period_cycle, X, [yes, no, unsure]).
slightly_out_of_cycle(X) :- way_out_of_period_cycle(no), menuask(slightly_out_of_cycle, X, [yes, no]).





% The menuask would give you a menu to choose from

menuask(Attribute,Value,_) :-
  known(yes,Attribute,Value),       % succeed if we know
  !.
  
menuask(Attribute,_,_) :-
  known(yes,Attribute,_),           % fail if its some other value
  !, fail.

menuask(A, V, _):-
known(_, A, V),
!, fail.

menuask(Attribute,AskValue,Menu):-
  menuread(Attribute, Y, Menu),
  asserta(known(yes,Attribute,Y)),
  AskValue = AnswerValue.           % succeed or fail based on answer


"""

def delay():
    time.sleep(ran.randint(3,6)) #make it natural that it appears an actual person is reading and typing instead of answering from already prepared responses
    return
greetings = ['Hi', 'Hi there!', "Hi!!", "Hello", "Greetings.", "Heyy", "Hiii", "Nice to meet you!", "Welcome!", "Hey there!", "What's up?!"]
names = ['Felicity', 'Angela', 'Pablo', 'Chloe', 'Ferdinand', 'Jevie', 'Kato', 'Jake', 'Raymond', 'Reuben', 'Kingsley', 'Joshua', 'Deborah', 'Matthew', "Sarah"]
bot_name = names[ran.randint(0, len(names) - 1)]
print bot_name.upper()+':', greetings[ran.randint(0, len(greetings) - 1)]
delay()
print bot_name.upper()+':','My name is', bot_name, 'and I am your Friend Doctor!'
delay()
print bot_name.upper()+':','Would you like a diagnosis of an ailment you may have or would you like to just have a nice chat with your friend?'
delay()
print bot_name.upper()+':','Or both...if you like'
just_chat = True
chat_starter = ['Okay, I suppose we just have a chat then!', "Perfect option for the day; let's chat!! :D", "Alright then, let's chat!!", "Yayy, I'll make a friend today...let's chat.", "Awesome, I would love to know you more - let's chat then!"]
diagnosis_starter = ['Aiit...diagnosis then!', 'Alright, putting on my medical cap. Gimme a sec.', "Diagnosis it is! Lemme put on my medical cap", "Okay, I would give you a diagnosis to the best of my ability - but this is not a medical advise, dude", "Medical diagnosis it is! See a doctor later if you want", "You want a diagnosis -- you've got a diagnosis!!"]
confirm_user_ans = False
misunderstand = ["Sorry, didn't quite understand. A diagnosis or no?", "Umm...I don't understand your response. Here, let's try again."+ '\n' + bot_name.upper()+': ' +"Would you like a diagnosis or you just wanna chat?", "I don't really understand. Do you want a diagnosis or you wanna make a cool friend? :)", "Hmm...hard to follow what you mean" +"\n" + bot_name.upper()+':' +" Sorry, but I gotta get that response again. A diagnosis or a chat?", "Sorry man, but I did not really get your last repsonse. So what did you say you want?"+"\n"+bot_name.upper()+':'+" ...a diagnosis or a chat?", "heeyy, so sorry..but I am lost here :((" + "\n" + bot_name.upper()+':'+" did not understand you" + "\n" + bot_name.upper()+':'+" so, do you want to chat or not?"]
doc_quit = False
while not confirm_user_ans:
    print ""
    user_first_ans = (raw_input('>> ')).lower()
    print ""
    delay()
    if 'diagnosis' in user_first_ans:
        if "don't" in user_first_ans or "not" in user_first_ans or "no " in user_first_ans:
            print bot_name.upper()+':',"Am I right that you don't want a diagnosis from me?"
            print ""
            confirm = (raw_input('>> ')).lower()
            print ""
            delay()
            if 'yes' in confirm or 'yup' in confirm or 'yep' in confirm or 'right' in confirm or 'yea' in confirm or 'correct' in confirm or 'true' in confirm:
                print bot_name.upper()+':',chat_starter[ran.randint(0, len(chat_starter)-1)]
                confirm_user_ans = True
            else:
                print bot_name.upper()+':',diagnosis_starter[ran.randint(0, len(diagnosis_starter)-1)]
                just_chat = False
                confirm_user_ans = True
        else:
            print bot_name.upper()+':',"Am I right that you want a diagnosis? Yes?"
            print ""
            confirm = raw_input('>> ').lower()
            print ""
            delay()
            if 'yes' in confirm or 'yup' in confirm or 'yep' in confirm or 'right' in confirm or 'yea' in confirm or 'correct' in confirm or 'true' in confirm:
                print bot_name.upper()+':',diagnosis_starter[ran.randint(0, len(diagnosis_starter)-1)]
                just_chat = False
                confirm_user_ans = True
            else:
                print bot_name.upper()+':',chat_starter[ran.randint(0, len(chat_starter)-1)]
                confirm_user_ans = True
    elif 'chat' in user_first_ans:
        if "don't" in user_first_ans or "not" in user_first_ans or "no " in user_first_ans:
            print bot_name.upper()+':',"Am I right that you don't want a chat with me? Yes?"
            print ""
            confirm = (raw_input('>> ')).lower()
            print ""
            delay()
            if 'yes' in confirm or 'yup' in confirm or  'yep' in confirm or 'right' in confirm or 'yea' in confirm or 'correct' in confirm or 'true' in confirm:
                print bot_name.upper()+':',diagnosis_starter[ran.randint(0, len(diagnosis_starter)-1)]
                confirm_user_ans = True
                just_chat = False
            else:
                print bot_name.upper()+':',chat_starter[ran.randint(0, len(chat_starter)-1)]
                confirm_user_ans = True
        else:
            print bot_name.upper()+':',"You want to chat?"
            print ""
            confirm = raw_input('>> ').lower()
            print ""
            delay()
            if 'yes' in confirm or 'yup' in confirm or 'yep' in confirm or 'right' in confirm or 'yea' in confirm or 'correct' in confirm or 'true' in confirm:
                print bot_name.upper()+':',chat_starter[ran.randint(0, len(chat_starter)-1)]
                confirm_user_ans = True
            else:
                print bot_name.upper()+':',diagnosis_starter[ran.randint(0, len(diagnosis_starter)-1)]
                just_chat = False
                confirm_user_ans = True
    elif 'both' in user_first_ans or 'all' in user_first_ans:
        print bot_name.upper()+':',"Umm..both? Haha. Alright. We would start with one first, and then you decide if you want the other..okay?"
        delay()
        print bot_name.upper()+':',"Hmmm...which should we go with first?"
        choice = ran.choice(['chat', 'diagnosis'])
        delay()
        if choice == 'chat':
            print bot_name.upper()+':',chat_starter[ran.randint(0, len(chat_starter)-1)]
            confirm_user_ans = True
        else:
            print bot_name.upper()+':',diagnosis_starter[ran.randint(0, len(diagnosis_starter) - 1)]
            confirm_user_ans = True
            just_chat = False
    elif 'none' in user_first_ans:
        print bot_name.upper()+':',"None? You want to go? Alright. :( "
        delay()
        print bot_name.upper()+':',"Hope you come back next time"
        delay()
        print bot_name.upper()+':',":))"
        doc_quit = True
        confirm_user_ans = True
    else:
        print bot_name.upper()+':',misunderstand[ran.randint(0, len(misunderstand) - 1)]

delay()


def diagnose_client():
    global just_chat, doc_quit
    with open("KB_B.pl", "w") as text_file:
        text_file.write(KB)
    # The code here will ask the user for input based on the askables
    # It will check if the answer is known first
    prolog = Prolog() # Global handle to interpreter

    retractall = Functor("retractall")
    known = Functor("known",3)

    # Define foreign functions for getting user input and writing to the screen
    def menuread(A, Y, Menu):
        Y.unify(raw_input(str(A) + " is " + str([str(i) for i in Menu]) + "? "))
        return True

    menuread.arity = 3
    registerForeign(menuread)

    prolog.consult("KB_B.pl") # open the KB
    call(retractall(known))
    count = 0
    print bot_name.upper()+':',"Okay...let's backtrack for a bit. Whatever I suggest here is not medical advice!"
    delay()
    print bot_name.upper()+':', "you shouldn't take medical advices from anyone other than a doctor - you know"
    delay()
    print bot_name.upper()+':', "I am only here to narrow down your choices and suggest a doctor you might be interested in going to. No more!"
    delay()
    print bot_name.upper()+ ":", "lol...so that being said, my friend. I would begin to ask you a few questions. Please answer to the best of your knowledge from the options I provide you."
    delay()
    for soln in prolog.query("suggestion(X).", maxresult = 1):
        result = soln['X'].split('_')
        result= ' '.join(result).title()
        print bot_name.upper()+':', "Your best bet is to " + result.lower()
        delay()
        count +=1
    if count ==0:
        print bot_name.upper()+':',"Hmmm..."
        delay()
        print bot_name.upper()+':', "i really can't make a sound judgement based on the symptoms you have shown"
        delay()
        print bot_name.upper()+':', "I'll suggest you see a general physician"
        delay()
    for solved in prolog.query("diagnosis(X).", maxresult = 1):
        result = solved['X'].split('_')
        result = ' '.join(result).title()
        print bot_name.upper()+':', "My take is this..." + result.lower()
        delay()
    print bot_name.upper()+':', "do you still wanna chat now or do you want to quit? yeah?"
    understand = False
    while not understand:
        print ""
        confirm = (raw_input('>> ')).lower()
        print ""
        delay()
        if 'yes' in confirm or 'right' in confirm or 'yea' in confirm or 'correct' in confirm or 'true' in confirm or 'i want to chat' in confirm or confirm[0:4] == 'chat':
            print bot_name.upper()+':',chat_starter[ran.randint(0, len(chat_starter)-1)]
            just_chat = True
            understand = True
            break
        elif 'no' in confirm or 'quit' in confirm or 'leave' in confirm or 'go' in confirm or 'none' in confirm or 'neither' in confirm or 'not' in confirm:
            print bot_name.upper()+':',"No? You want to go? Alright. :( "
            delay()
            goodbye = ['It was a pleasure meeting you', 'dude, hope you feel better', 'see the doctor as suggested', 'Alright, take it easy there!', 'Be carful' + '\n' + bot_name.upper()+': '+ 'sorry, careful* lol', 'I wish you well!' + '\n'+ bot_name.upper()+' Take care my frend' + '\n' + bot_name.upper()+' friend*']
            print bot_name.upper() + ': '+ goodbye[ran.randint(0, len(goodbye)-1)]
            doc_quit = True
            understand = True
            break
        else:
            print bot_name.upper()+':',misunderstand[ran.randint(0, len(misunderstand) - 1)]
    return

def chat_client():
    global doc_quit, just_chat
    
    reflections = {
        "am": "are",
        "was": "were",
        "i": "you",
        "i'd": "you would",
        "i've": "you have",
        "i'll": "you will",
        "my": "your",
        "are": "am",
        "you've": "I have",
        "you'll": "I will",
        "your": "my",
        "yours": "mine",
        "you": "me",
        "me": "you"
    }
     
    psychobabble = [

        [r'(.*)What is your name(.*)',
         ["Told you already. My name is " + bot_name,
          "Dude, I already said my name is " + bot_name +'.',
          "Again? I said before already...I am " + bot_name]],

        [r'(.*)what is your name(.*)',
         ["Told you already. My name is " + bot_name,
          "I said my name was " + bot_name + ", my friend. Were you not listening?",
          "Dude, I already said my name is " + bot_name +'.',
          "Again? I said before already...I am " + bot_name]],

        [r'(.*)sorry(.*)',
         ["don't worry about apologies. Tell me something interesting!",
          "don't mind apologies. Tell me more about yourself",
          "It's okay...what interests you most?!",
          "haha, no worries. Okay, so tell me something new."]],


        [r'(.*)you?',
         ["Haha me? lol, i don't know. I'm more curious about you. Why are you asking about me? lol",
          "Umm... let's just focus on you for a while longer. Forget me haha. k? :) Tell me more about yourself",
          "Lol I'll dodge that one thrown to me. Cos I don't like talking about myself. Let's change the topic a bit - what do you care most about?"]],

        [r'(.*)yours?',
         ["Haha mine? lol, i don't know. I'm more curious about you. Why are you asking about me? lol",
          "Umm... let's focus on you for a while longer. k? :) Tell me more about yourself",
          "Lol I'll doge that question thrown to me. Cos I don't like talking about myself. Let's change the topic a bit - what do you care most about?"]],

        [r'my name is (.*)',
         ["Well, hi {0}, thanks for telling me your name...but tell me something deeper about you though.",
          "hey, {0}! {0} is a cool name to be honest. ;) Tell me something else about yourself.",
          "Again, great to meet you, {0}, like I said, I am " + bot_name + " but I really want to know more about you. Sorry. carry on :) "]],

            
        [r'My name is (.*)',
         ["Well, hi {0}, thanks for telling me your name...but tell me something deeper about you though.",
          "hey, {0}! {0} is a cool name tbh. Tell me something else about yourself.",
          "Again, great to meet you, {0}, like I said, I am " + bot_name + " but I really want to know more about you. Sorry. carry on :) "]],

        [r'no',
         ["Why the negative response?",
          "Hmmm, no? Why so?",
          "That's quite affirmatively negative - quite strongly. Are you sure?"]],
     
     
        [r'I need (.*)',
         ["Why do you need {0}?",
          "Would it really help you to get {0}?",
          "Are you sure you need {0}?"]],
     
        [r'Why don\'?t you ([^\?]*)\??',
         ["Do you really think I don't {0}?",
          "Perhaps eventually I will {0}.",
          "Do you really want me to {0}?"]],
     
        [r'Why can\'?t I ([^\?]*)\??',
         ["Do you think you should be able to {0}?",
          "If you could {0}, what would you do?",
          "I don't know -- why can't you {0}?",
          "Have you really tried?"]],
     
        [r'I can\'?t (.*)',
         ["How do you know you can't {0}?",
          "Perhaps you could {0} if you tried.",
          "What would it take for you to {0}?"]],
     
        [r'I am (.*)',
         ["Did you come to me because you are {0}?",
          "Tell me something about being {0}?",
          "How do you feel about being {0}?"]],
     
        [r'I\'?m (.*)',
         ["How does being {0} make you feel?",
          "Do you enjoy being {0}?",
          "Why do you tell me you're {0}?",
          "Why do you think you're {0}?"]],
     
        [r'Are you ([^\?]*)\??',
         ["Why does it matter whether I am {0}?",
          "Would you prefer it if I were not {0}?",
          "Perhaps you believe I am {0}.",
          "I may be {0} -- what do you think?"]],
     
        [r'What (.*)',
         ["Why do you ask?",
          "How would an answer to that help you?",
          "What do you think?"]],
     
        [r'How (.*)',
         ["How do you suppose?",
          "Perhaps you can answer your own question.",
          "What is it you're really asking?"]],
     
        [r'Because (.*)',
         ["Is that the real reason?",
          "What other reasons come to mind?",
          "Does that reason apply to anything else?",
          "If {0}, what else must be true?"]],
     
        [r'(.*) sorry (.*)',
         ["There are many times when no apology is needed.",
          "What feelings do you have when you apologize?"]],
     
        [r'Hello(.*)',
         ["Hello... I'm glad you could drop by today.",
          "Hi there... how are you today?",
          "Hello, how are you feeling today?"]],
     
        [r'I think (.*)',
         ["Do you doubt {0}?",
          "Do you really think so?",
          "But you're not sure {0}?"]],
     
        [r'(.*) friend (.*)',
         ["Tell me more about your friends.",
          "When you think of a friend, what comes to mind?",
          "Why don't you tell me about a childhood friend?"]],
     
        [r'Yes',
         ["You seem quite sure.",
          "OK, but can you elaborate a bit?"]],
     
        [r'(.*) computer(.*)',
         ["Are you really talking about me?",
          "Does it seem strange to talk to a computer?",
          "How do computers make you feel?",
          "Do you feel threatened by computers?"]],
     
        [r'Is it (.*)',
         ["Do you think it is {0}?",
          "Perhaps it's {0} -- what do you think?",
          "If it were {0}, what would you do?",
          "It could well be that {0}."]],
     
        [r'It is (.*)',
         ["You seem very certain.",
          "If I told you that it probably isn't {0}, what would you feel?"]],
     
        [r'Can you ([^\?]*)\??',
         ["What makes you think I can't {0}?",
          "If I could {0}, then what?",
          "Why do you ask if I can {0}?"]],
     
        [r'Can I ([^\?]*)\??',
         ["Perhaps you don't want to {0}.",
          "Do you want to be able to {0}?",
          "If you could {0}, would you?"]],
     
        [r'You are (.*)',
         ["Why do you think I am {0}?",
          "Does it please you to think that I'm {0}?",
          "Perhaps you would like me to be {0}.",
          "Perhaps you're really talking about yourself?"]],
     
        [r'You\'?re (.*)',
         ["Why do you say I am {0}?",
          "Why do you think I am {0}?",
          "Are we talking about you, or me?"]],
     
        [r'I don\'?t (.*)',
         ["Don't you really {0}?",
          "Why don't you {0}?",
          "Do you want to {0}?"]],
     
        [r'I feel (.*)',
         ["Good, tell me more about these feelings.",
          "Do you often feel {0}?",
          "When do you usually feel {0}?",
          "When you feel {0}, what do you do?"]],
     
        [r'I have (.*)',
         ["Why do you tell me that you've {0}?",
          "Have you really {0}?",
          "Now that you have {0}, what will you do next?"]],
     
        [r'I would (.*)',
         ["Could you explain why you would {0}?",
          "Why would you {0}?",
          "Who else knows that you would {0}?"]],
     
        [r'Is there (.*)',
         ["Do you think there is {0}?",
          "It's likely that there is {0}.",
          "Would you like there to be {0}?"]],
     
        [r'My (.*)',
         ["I see, your {0}.",
          "Why do you say that your {0}?",
          "When your {0}, how do you feel?"]],
     
        [r'You (.*)',
         ["We should be discussing you, not me.",
          "Why do you say that about me?",
          "Why do you care whether I {0}?"]],
     
        [r'Why (.*)',
         ["Why don't you tell me the reason why {0}?",
          "Why do you think {0}?"]],
     
        [r'I want (.*)',
         ["What would it mean to you if you got {0}?",
          "Why do you want {0}?",
          "What would you do if you got {0}?",
          "If you got {0}, then what would you do?"]],
     
        [r'(.*) mother(.*)',
         ["Tell me more about your mother.",
          "What was your relationship with your mother like?",
          "How do you feel about your mother?",
          "How does this relate to your feelings today?",
          "Good family relations are important."]],
     
        [r'(.*) father(.*)',
         ["Tell me more about your father.",
          "How did your father make you feel?",
          "How do you feel about your father?",
          "Does your relationship with your father relate to your feelings today?",
          "Do you have trouble showing affection with your family?"]],
     
        [r'(.*) child(.*)',
         ["Did you have close friends as a child?",
          "What is your favorite childhood memory?",
          "Do you remember any dreams or nightmares from childhood?",
          "Did the other children sometimes tease you?",
          "How do you think your childhood experiences relate to your feelings today?"]],
     
        [r'(.*)\?',
         ["Why do you ask that?",
          "Please consider whether you can answer your own question.",
          "Perhaps the answer lies within yourself?",
          "Why don't you tell me?",
          "{0} what?"]],
     
        [r'quit',
         ["Thank you for talking with me.",
          "It was a nice chat.",
          "Thank you.  I enjoyed our conversation!",
          "You seem like a pretty cool person to me. Thanks for dropping by :)"]],

        [r'(.*)quit(.*)',
         ["Thank you for talking with me.",
          "It was a nice chat.",
          "Thank you.  I enjoyed our conversation!",
          "You seem like a pretty cool person to me. Thanks for dropping by :)"]],


        [r'(.*)bye(.*)',
         ["Thank you for talking with me.",
          "It was a nice chat.",
          "Thank you.  I enjoyed our conversation!",
          "Cheers, mate. Nice convo my man"]],
        
        [r'(.*)go(.*)',
         ["Go? You want to chat or you want to quit?",
          "It was a nice chat. you want to talk more or quit?",
          "you want to talk or quit?",
          "dude, do want to chill here or quit? :)"]],
        
        [r'(.*)go(.*)',
         ["Go? You want to chat or you want to quit?",
          "It was a nice chat. you want to talk more or quit?",
          "you want to talk or quit?",
          "dude, do want to chill here or quit? :)"]],
        
        [r'(.*)',
         ["Please tell me more.",
          "Let's change focus a bit... Tell me about your family.",
          "Can you elaborate on that?",
          "Why do you say that {0}?",
          "I see. Tell me more!",
          "Very interesting. Go on.",
          "{0}.",
          "I see.  And what does that tell you?",
          "How does that make you feel?",
          "How do you feel when you say that?"]]
    ]
     
     
    def reflect(fragment):
        tokens = fragment.lower().split()
        for i, token in enumerate(tokens):
            if token in reflections:
                tokens[i] = reflections[token]
        return ' '.join(tokens)
     
     
    def analyze(statement):
        for pattern, responses in psychobabble:
            match = re.match(pattern, statement.rstrip(".!"))
            if match:
                response = random.choice(responses)
                return response.format(*[reflect(g) for g in match.groups()])
     
     
    def main():
        global doc_quit, just_chat
        print bot_name.upper()+': ' + "How are you feeling, my friend?"
     
        while True:
            print ""
            statement = raw_input(">> ")
            print ""
            delay()
            print bot_name.upper()+': '+ analyze(statement)
     
            if statement == "quit" or statement == "leave" or statement == "gotta run" or 'quit' in statement:
                delay()
                print bot_name.upper()+':', "okay, :( do you want a diagnosis now or you just want to go? yeah?"
                understand = False
                while not understand:
                    print ""
                    confirm = (raw_input('>> ')).lower()
                    print ""
                    delay()
                    if 'yes' in confirm or 'right' in confirm or 'yea' in confirm or 'correct' in confirm or 'true' in confirm or 'i want to diagnosis' in confirm or 'diagnosis' in confirm:
                        print bot_name.upper()+':',diagnosis_starter[ran.randint(0, len(diagnosis_starter)-1)]
                        just_chat = False
                        understand = True
                        break
                    elif 'no' in confirm or 'quit' in confirm or 'leave' in confirm or 'go' in confirm or 'none' in confirm or 'neither' in confirm or 'not' in confirm:
                        print bot_name.upper()+':',"No? You want to go? Alright. :( "
                        delay()
                        goodbye = ['It was a pleasure meeting you', 'dude, hope you feel better', 'see the doctor as suggested', 'Alright, take it easy there!', 'Be carful' + '\n' + bot_name.upper()+': '+ 'sorry, careful* lol', 'I wish you well!' + '\n'+ bot_name.upper()+' Take care my frend' + '\n' + bot_name.upper()+' friend*']
                        print bot_name.upper() + ': '+ goodbye[ran.randint(0, len(goodbye)-1)]
                        doc_quit = True
                        understand = True
                        break
                    else:
                        print bot_name.upper()+':',misunderstand[ran.randint(0, len(misunderstand) - 1)]
                
                break
        return
     
     
    if __name__ == "__main__":
        main()

while not doc_quit:
    if just_chat:
        chat_client()
    else:
        diagnose_client()

    


