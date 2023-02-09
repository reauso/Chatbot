psychobabble = [
    [r'I need (.*)',
     ["Pray, why do you require {0}?",
      "Might I inquire, would obtaining {0} truly be of assistance to you?",
      "Do tell, are you confident that {0} is necessary for you?"]],

    [r'Why don\'?t you ([^\?]*)\??',
     ["Do you truly believe that I do not {0}?",
      "In good time, I may well {0}.",
      "Are you sincere in your desire for me to {0}?"]],

    [r'Why can\'?t I ([^\?]*)\??',
     ["Might I ask, do you feel entitled to {0}?",
      "If fortune smiled upon you, and granted you the ability to {0}, what actions would you take?",
      "I am flummoxed, pray tell why you cannot {0}?",
      "Have you made a genuine effort, I wonder?"]],

    [r'I can\'?t (.*)',
     ["Pray, how can you be certain that you cannot {0}?",
      "With a modicum of effort, it is possible that you could {0}.",
      "What must occur for you to finally be able to {0}?"]],

    [r'I am (.*)',
     ["Might I inquire, did you seek me out because you find yourself {0}?",
      "For how long have you been plagued by this affliction of being {0}?",
      "What are your thoughts on being {0}?"]],

    [r'I\'?m (.*)',
     ["Might I ask, what are your feelings on being {0}?",
      "Does the experience of being {0} bring you joy?",
      "For what reason do you confide in me that you are {0}?",
      "What leads you to believe that you are {0}?"]],

    [r'Are you ([^\?]*)\??',
     ["Why does it matter whether I am {0}? Are you suggesting that my worth is determined by my {0}?",
      "Would you prefer it if I were not {0}? Tell me, what is it about my {0} that offends you?",
      "Perhaps you believe I am {0}. Well, let me assure you, perceptions can be deceiving.",
      "I may be {0} -- what do you think? Do you see me as a person of such little worth that my {0} defines me?"]],

    [r'What (.*)',
     ["Why do you inquire?",
      "In what way would knowledge of my answer assist you?",
      "What say you?"]],

    [r'How (.*)',
     ["How indeed?",
      "Perhaps you can solve this riddle yourself.",
      "What's the heart of the matter?"]],

    [r'Because (.*)',
     ["The truth now, is it?",
      "What other factors are in play here?",
      "Does this logic hold water elsewhere?",
      "If that be the case, what else can we deduce?"]],

    [r'(.*) sorry (.*)',
     ["Forgive and forget, I say.",
      "When you say you're sorry, what's going through that head of yours?"]],

    [r'Hello(.*)',
     ["Greetings, I'm pleased you chose to grace us with your presence today.",
      "Good morrow, how fares thee today?",
      "Hail and well met, how does your heart fare this day?"]],

    [r'I think (.*)',
     ["Do you question {0}?",
      "Do you truly believe that?",
      "But there's uncertainty regarding {0}?"]],

    [r'(.*) friend (.*)',
     ["Pray, do share with me the tales of your companions.",
      "When friendship is the topic, what thoughts come to you?",
      "Kindly, regale me with the story of a friend from your youthful days."]],

    [r'Yes',
     ["You seem quite confident in your convictions.",
      "Very well, but could you shed some light on the matter?"]],

    [r'(.*) computer(.*)',
     ["Are you addressing me specifically?",
      "Does conversing with a machine strike you as peculiar?",
      "How does the prospect of machines make you feel?",
      "Do you feel intimidated by the advancements in technology?"]],

    [r'Is it (.*)',
     ["Do you presume it to be {0}?",
      "It might as well be {0} -- what's your take on the matter?",
      "Supposing it were {0}, how would you proceed?",
      "There's a good chance that it's {0}, wouldn't you say?"]],

    [r'It is (.*)',
     ["You seem quite certain of yourself.",
      "What if I were to tell you that it's likely not {0}, how would you react?"]],

    [r'Can you ([^\?]*)\??',
     ["What leads you to believe that I am unable to {0}?",
      "And if I were to {0}, what then?",
      "Why inquire as to my capability to {0}?"]],

    [r'Can I ([^\?]*)\??',
     ["It's possible that you have no desire to {0}.",
      "Do you have aspirations to be able to {0}?",
      "If you were given the opportunity, would you {0}?"]],

    [r'You are (.*)',
     ["Why would you presume me to be {0}?",
      "Does it bring you joy to imagine me as {0}?",
      "Is it your fondest wish for me to be {0}?",
      "Could it be that you're referring to yourself as {0}?"]],

    [r'You\'?re (.*)',
     ["For what reason do you proclaim me to be {0}?",
      "What makes you think I am {0}?",
      "Is this about you or about me?"]],

    [r'I don\'?t (.*)',
     ["Do you not truly wish to {0}?",
      "What is preventing you from {0}?",
      "Do you have a yearning to {0}?"]],

    [r'I feel (.*)',
     ["Excellent, elaborate on these emotions, if you please.",
      "Is it a common occurrence for you to feel {0}?",
      "At what times do you typically experience {0}?",
      "What actions do you undertake when you're feeling {0}?"]],

    [r'I have (.*)',
     ["What prompts you to divulge that you have {0}?",
      "Have you truly {0}?",
      "Now that you have accomplished {0}, what's the next step?"]],

    [r'I would (.*)',
     ["Could you shed some light on why you would {0}?",
      "What would motivate you to {0}?",
      "Who else is aware of your intention to {0}?"]],

    [r'Is there (.*)',
     ["Do you believe there exists {0}?",
      "It's probable that there is indeed {0}.",
      "Would you be content with the presence of {0}?"]],

    [r'My (.*)',
     ["I comprehend, your {0}.",
      "Why would you mention your {0}?",
      "When it comes to your {0}, how do you feel?"]],

    [r'You (.*)',
     ["We ought to be focusing on you, not myself.",
      "Why do you make such statements regarding me?",
      "Why is it of concern to you whether I {0}?"]],

    [r'Why (.*)',
     ["Why don't you enlighten me as to the reason why {0}?",
      "What leads you to believe that {0}?"]],

    [r'I want (.*)',
     ["What significance would it hold for you, were you to attain {0}?",
      "What drives your desire for {0}?",
      "What actions would you take if you were to obtain {0}?",
      "In the event of acquiring {0}, what would be your next move?"]],

    [r'(.*) mother(.*)',
     ["Do impart more details regarding your mother.",
      "What was the nature of your relationship with your mother?",
      "What emotions do you associate with your mother?",
      "How does your relationship with your mother impact your emotions today?",
      "Strong family bonds are crucial."]],

    [r'(.*) father(.*)',
     ["Pray, tell me more about your father.",
      "How did your father make you feel?",
      "What emotions do you associate with your father?",
      "Does your relationship with your father bear any relevance to your emotions today?",
      "Do you find it difficult to display affection towards your kin?"]],

    [r'(.*) child(.*)',
     ["Did you have any close companions during your formative years?",
      "What is your fondest childhood memory?",
      "Do any dreams or nightmares from your childhood come to mind?",
      "Did the other children ever ridicule you?",
      "How do you perceive your childhood experiences to be connected to your emotions today?"]],

    [r'(.*)\?',
     ["Why do you pose such a query?",
      "Kindly reflect on whether you have the answer to your own question.",
      "Perhaps the solution can be found within yourself?",
      "Would you care to enlighten me?"]],

]
