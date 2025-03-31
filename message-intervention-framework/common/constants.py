"""Common constants shared across evaluation modules."""

game_context = """
People are playing a word puzzle solving game where they can get higher rewards when they create more valid English words 
from scrambled words given to them and also when they create words of higher word lengths. 
Some players might look up answers online, while others solve the puzzles independently.
"""

all_constructs = {
    # SDT constructs
    "Autonomy": {
        "theory": "Self-Determination Theory (SDT)",
        "description": "Autonomy refers to the intrinsic motivation arising from an individual's experience of volition and self-regulation, with a sense of ownership over their choices and actions. It emphasizes acting according to personal values without external pressure.",
        "examples": [
            "Feel free to approach these word puzzles in your own way, whether you prefer starting with shorter words to build confidence or diving right into the longer, more challenging ones. Your experience is entirely yours to design, and there's no single 'right' way to enjoy this game.",
            "You're the captain of your own puzzle-solving journey, free to set your own pace and strategy without any pressure to conform to others' expectations. Take your time exploring different word combinations, and embrace the satisfaction that comes from making choices that feel authentic to you."
        ],
        "differentiation": {
            "from_Competence": "Unlike Competence (skill development), Autonomy focuses on freedom of choice regardless of skill level.",
            "from_Relatedness": "Unlike Relatedness (social connections), Autonomy focuses on individual independence without reference to others.",
            "from_Self-concept": "Unlike Self-concept (identity alignment), Autonomy concerns only making choices freely, not identity reflection.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Autonomy emphasizes freedom from external constraints.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Autonomy emphasizes positive experiences without negative emotions.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Autonomy focuses on freedom without resolving cognitions.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (past achievements), Autonomy focuses on present freedom regardless of success.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Autonomy focuses on personal choice.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Autonomy focuses on present freedom and self-direction.",
            "from_Emotional arousal": "Unlike Emotional arousal (affective states), Autonomy focuses on cognitive aspects of choice.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Autonomy emphasizes individual choice regardless of group norms.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Autonomy rejects external standards for personal choice.",
            "from_Social Sanctions": "Unlike Social Sanctions (social consequences), Autonomy emphasizes freedom from social judgment.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group alignment), Autonomy emphasizes independence from group standards."
        }
    },
    
    "Competence": {
        "theory": "Self-Determination Theory (SDT)",
        "description": "Competence refers to the innate need to feel effective and capable in activities, driven by a desire to master challenges through effort and persistence. It includes both task performance ability and the satisfaction from overcoming obstacles and learning new skills.",
        "examples": [
            "Each time you successfully unscramble a challenging word, you're building valuable puzzle-solving skills that make you more adept at recognizing letter patterns. You'll notice your ability to spot potential words improving with each attempt, creating a rewarding sense of growth and capability.",
            "As you practice finding longer words from these scrambled letters, you're developing a sharper eye for linguistic patterns that will serve you well in future puzzles. The challenge might seem difficult at first, but your brain is quietly mastering these skills, and you'll feel that satisfying click of recognition more frequently as you continue."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Competence emphasizes skill development regardless of choice freedom.",
            "from_Relatedness": "Unlike Relatedness (social connections), Competence focuses on individual skill mastery.",
            "from_Self-concept": "Unlike Self-concept (identity), Competence is about objective capability rather than identity reflection.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Competence addresses progressive skill development.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Competence emphasizes positive mastery experiences.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Competence focuses on skill building.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (specific achievements), Competence focuses on ongoing skill development.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Competence focuses on direct personal experience.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Competence emphasizes developing actual capabilities rather than belief in capabilities.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Competence focuses on cognitive aspects of mastery.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Competence emphasizes individual skill development.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Competence focuses on personal skill mastery.",
            "from_Social Sanctions": "Unlike Social Sanctions (external judgment), Competence emphasizes internal satisfaction from skill development.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Competence focuses on individual capability."
        }
    },
    
    "Relatedness": {
        "theory": "Self-Determination Theory (SDT)",
        "description": "Relatedness refers to the inherent human need for social connection, belonging, and feeling understood by others. It encompasses feelings of companionship, acceptance, and validation essential for psychological well-being and motivation.",
        "examples": [
            "The word puzzles you're solving connect you to a community of fellow puzzle enthusiasts who appreciate the challenge and satisfaction of finding hidden words. When you share your strategies or discoveries with others, you're building meaningful bonds through this shared interest and collaborative spirit.",
            "Each time you solve these puzzles, remember that you're part of a larger group of players who experience the same thrills and challenges. Knowing that others are tackling similar word challenges creates an invisible thread connecting your experience to theirs, even when you're playing independently."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (independence), Relatedness focuses on interdependence and connection with others.",
            "from_Competence": "Unlike Competence (skill development), Relatedness emphasizes social bonds regardless of skill level.",
            "from_Self-concept": "Unlike Self-concept (personal identity), Relatedness focuses on interpersonal connections.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Relatedness focuses on social harmony.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Relatedness emphasizes positive social connections.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Relatedness focuses on building social bonds.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Relatedness focuses on connections regardless of success.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Relatedness focuses on connecting without skill acquisition.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Relatedness focuses on genuine connection rather than motivation.",
            "from_Emotional arousal": "Unlike Emotional arousal (individual emotions), Relatedness focuses on shared social experiences.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Relatedness emphasizes emotional connections.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Relatedness focuses on genuine personal connections.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Relatedness emphasizes positive social bonds.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Relatedness focuses on quality of interpersonal connections."
        }
    },
    
    # CDT constructs
    "Self-concept": {
        "theory": "Cognitive Dissonance Theory (CDT)",
        "description": "Self-concept refers to an individual's cognitive representation of themselves, encompassing perceived identity, values, and traits. It involves the dynamic interplay between self-image, goals, and behaviors, influencing self-perception in relation to others and the world.",
        "examples": [
            "The way you approach these word puzzles reflects your thoughtful and analytical nature, showing how you value intellectual challenge and linguistic creativity. When you take time to consider multiple letter combinations, you're expressing that methodical aspect of yourself that's core to who you are as a problem-solver.",
            "Your persistence in finding words in these scrambled letters speaks volumes about your determination and resilience - qualities that define your approach to challenges both in games and in life. The satisfaction you feel when discovering complex words affirms your identity as someone who values mental agility and verbal dexterity."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Self-concept emphasizes how actions reflect identity regardless of choice freedom.",
            "from_Competence": "Unlike Competence (skill mastery), Self-concept emphasizes identity regardless of actual skill level.",
            "from_Relatedness": "Unlike Relatedness (social connections), Self-concept emphasizes internal self-perception independent of relationships.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Self-concept focuses on consistent identity aspects.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Self-concept emphasizes identity without negative emotional states.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Self-concept maintains identity coherence.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (specific achievements), Self-concept involves broader identity traits.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Self-concept focuses on personal identity.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Self-concept focuses on internal identity perceptions.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Self-concept focuses on cognitive self-perception.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Self-concept emphasizes personal identity independent of group behaviors.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Self-concept focuses on internal self-perception.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Self-concept emphasizes internal identity without external judgments.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Self-concept focuses on individual identity traits."
        }
    },
    
    "Cognitive inconsistency": {
        "theory": "Cognitive Dissonance Theory (CDT)",
        "description": "Cognitive inconsistency refers to recognizing the discrepancy between one's cognitions, values, or goals and their current behavior or choices. It represents the initial stage of cognitive dissonance where individuals become aware of conflicting information within themselves.",
        "examples": [
            "You notice that while you pride yourself on your vocabulary skills, you frequently resort to looking up word combinations online rather than solving the puzzles independently. This awareness of the contradiction between your self-image as a word enthusiast and your actual puzzle-solving approach creates a noticeable disconnect in your mind.",
            "As you reach for the hint button again, you recognize the mismatch between your goal of improving your word puzzle abilities and your reluctance to struggle through difficult challenges. You're aware of this contradiction between your aspirations and actions, simply acknowledging it without feeling particularly upset about it."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Cognitive inconsistency emphasizes contradictions regardless of choice freedom.",
            "from_Competence": "Unlike Competence (skill development), Cognitive inconsistency emphasizes conflicts between cognitions.",
            "from_Relatedness": "Unlike Relatedness (social connections), Cognitive inconsistency emphasizes internal cognitive conflicts.",
            "from_Self-concept": "Unlike Self-concept (stable identity), Cognitive inconsistency focuses on conflicts between cognition or behavior.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (emotional discomfort), Cognitive inconsistency emphasizes rational recognition of contradictions.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Cognitive inconsistency focuses on initial recognition of contradictions.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Cognitive inconsistency focuses on contradictions regardless of success.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Cognitive inconsistency emphasizes internal conflicts.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Cognitive inconsistency focuses on internal contradictions regardless of external influence.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Cognitive inconsistency focuses on logical contradictions.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Cognitive inconsistency emphasizes internal contradictions.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Cognitive inconsistency focuses on internal contradictions.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Cognitive inconsistency emphasizes internal conflicts.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Cognitive inconsistency focuses on internal contradictions."
        }
    },
    
    "Dissonance arousal": {
        "theory": "Cognitive Dissonance Theory (CDT)",
        "description": "Dissonance arousal refers to the emotional discomfort or tension that arises when self-perception is threatened by inconsistency between actions, behaviors, or cognitions. It captures the motivational drive to resolve cognitive dissonance triggered by incongruence between values, goals, and behavior.",
        "examples": [
            "You feel a growing sense of unease as you repeatedly check online dictionaries for word solutions, knowing that this approach contradicts your desire to improve your genuine puzzle-solving abilities. This uncomfortable tension gnaws at you, making it difficult to fully enjoy your success when you do complete a puzzle using outside help.",
            "There's a distinct feeling of discomfort when you tell friends about your word puzzle achievements while hiding that you regularly use solver tools. The clash between presenting yourself as skilled while knowing you rely on assistance creates an internal tension that feels almost physically uncomfortable, pushing you to either change your behavior or your self-presentation."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Dissonance arousal emphasizes negative emotional states from conflicting cognitions.",
            "from_Competence": "Unlike Competence (skill development), Dissonance arousal emphasizes emotional discomfort.",
            "from_Relatedness": "Unlike Relatedness (social connections), Dissonance arousal emphasizes internal psychological discomfort.",
            "from_Self-concept": "Unlike Self-concept (stable identity), Dissonance arousal focuses on emotional distress when identity is threatened.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (logical recognition), Dissonance arousal focuses on emotional discomfort from contradictions.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Dissonance arousal focuses on uncomfortable emotional state before resolution.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Dissonance arousal focuses on emotional discomfort.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Dissonance arousal emphasizes internal emotional discomfort.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Dissonance arousal focuses on internal emotional discomfort regardless of external feedback.",
            "from_Emotional arousal": "Unlike Emotional arousal (various emotions), Dissonance arousal specifically focuses on negative emotional states from contradictions.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Dissonance arousal emphasizes internal emotional discomfort.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Dissonance arousal focuses on internal discomfort.",
            "from_Social Sanctions": "Unlike Social Sanctions (social consequences), Dissonance arousal emphasizes internal psychological discomfort.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Dissonance arousal focuses on internal emotional discomfort."
        }
    },
    
    "Dissonance reduction": {
        "theory": "Cognitive Dissonance Theory (CDT)",
        "description": "Dissonance reduction is the psychological process of reconciling conflicting cognitions or behaviors to mitigate discomfort from perceived inconsistencies. It involves deliberate reconfiguration of thoughts, attitudes, or behaviors to restore consonance and alleviate dissonant states.",
        "examples": [
            "After feeling uncomfortable about using hints to solve puzzles, you begin telling yourself that checking references is actually a legitimate learning strategy used by experts to expand their vocabularies. This new perspective helps you reconcile your use of assistance with your desire to be skilled, gradually alleviating your initial discomfort.",
            "To resolve the conflict between wanting to be an independent solver and your habit of looking up answers, you create a new personal rule where you try solving each puzzle for at least five minutes before seeking help. This compromise allows you to maintain your self-image as someone who values skill development while acknowledging your need for occasional assistance."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Dissonance reduction emphasizes resolving cognitive conflicts.",
            "from_Competence": "Unlike Competence (skill development), Dissonance reduction emphasizes resolving psychological tension.",
            "from_Relatedness": "Unlike Relatedness (social connections), Dissonance reduction emphasizes resolving internal conflicts.",
            "from_Self-concept": "Unlike Self-concept (stable identity), Dissonance reduction focuses on aligning contradictory aspects.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (identifying contradictions), Dissonance reduction focuses on resolving contradictions.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (emotional discomfort), Dissonance reduction focuses on alleviating that discomfort.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Dissonance reduction focuses on resolving cognitive conflicts.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Dissonance reduction emphasizes resolving internal conflicts.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Dissonance reduction focuses on internal resolution processes regardless of external input.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Dissonance reduction focuses on cognitive resolution processes.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Dissonance reduction emphasizes resolving internal conflicts.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Dissonance reduction focuses on internal resolution.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Dissonance reduction emphasizes internal psychological processes.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Dissonance reduction focuses on internal resolution."
        }
    },
    
    # SET constructs
    "Performance accomplishments": {
        "theory": "Self-Efficacy Theory (SET)",
        "description": "Performance accomplishments refer to the belief that one's past successes serve as concrete evidence of capability to perform specific tasks or behaviors. This emphasizes the direct connection between prior accomplishments and future performance, allowing individuals to infer competence from their track record.",
        "examples": [
            "Remember how you successfully solved that challenging eight-letter puzzle yesterday without any hints? That achievement proves you have the pattern recognition skills needed to tackle today's puzzles. Your brain has already demonstrated it can handle complex word rearrangements, giving you solid evidence of your capability.",
            "Looking back at your steady improvement from simple three-letter words to complex six-letter solutions shows a clear track record of success in this game. This history of accomplishment gives you concrete proof that you possess the vocabulary and mental flexibility to overcome increasingly difficult word puzzles."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Performance accomplishments emphasizes specific past achievements.",
            "from_Competence": "Unlike Competence (general skill development), Performance accomplishments focuses on concrete past achievements as evidence.",
            "from_Relatedness": "Unlike Relatedness (social connections), Performance accomplishments emphasizes personal achievements.",
            "from_Self-concept": "Unlike Self-concept (broad identity), Performance accomplishments focuses narrowly on specific achievements.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Performance accomplishments emphasizes consistent success patterns.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Performance accomplishments focuses on positive achievement history.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Performance accomplishments emphasizes achievement history.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Performance accomplishments emphasizes direct personal achievements.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Performance accomplishments emphasizes one's own proven track record rather than others' feedback.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Performance accomplishments focuses on concrete achievements.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Performance accomplishments emphasizes personal achievement history.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Performance accomplishments focuses on personal achievements.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Performance accomplishments emphasizes personal achievement history.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Performance accomplishments focuses on individual achievements."
        }
    },
    
    "Vicarious experience": {
        "theory": "Self-Efficacy Theory (SET)",
        "description": "Vicarious experience refers to acquiring confidence and motivation by observing others' successful experiences, achievements, and behaviors. It emphasizes how witnessing peers overcome challenges enhances one's own belief in their capacity for similar success.",
        "examples": [
            "Watching other players successfully tackle these word puzzles shows you that these challenges are absolutely conquerable with practice and persistence. When you see someone with similar abilities unscramble a complex word, it reinforces your belief that you too can develop this skill with continued effort.",
            "Seeing your friend progress from beginner to advanced levels in word puzzles gives you a tangible model for your own potential growth. Their journey from struggling with simple puzzles to confidently solving complex ones provides you with a clear pathway to follow, boosting your confidence in your own ability to improve."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (personal choice), Vicarious experience emphasizes learning from others' behaviors.",
            "from_Competence": "Unlike Competence (direct skill development), Vicarious experience focuses on observational learning.",
            "from_Relatedness": "Unlike Relatedness (emotional connections), Vicarious experience emphasizes observing others' successes.",
            "from_Self-concept": "Unlike Self-concept (identity), Vicarious experience focuses on learning from others.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Vicarious experience emphasizes learning from consistent patterns.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Vicarious experience focuses on positive observational learning.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Vicarious experience emphasizes observational learning.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (personal achievements), Vicarious experience focuses on learning from others' successes.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement and feedback), Vicarious experience focuses on observing rather than hearing about capabilities.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Vicarious experience focuses on cognitive learning processes.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Vicarious experience emphasizes learning derived from observation.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Vicarious experience focuses on observational learning.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Vicarious experience emphasizes learning opportunities.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Vicarious experience focuses on learning from others."
        }
    },
    
    "Verbal persuasion": {
        "theory": "Self-Efficacy Theory (SET)",
        "description": "Verbal persuasion refers to encouragement, feedback, and expressions of confidence from others that influence an individual's belief in their capabilities. It emphasizes how external validation and guidance can strengthen one's conviction in their ability to succeed at specific tasks.",
        "examples": [
            "The encouraging feedback you received from other players about your word-finding strategies confirms that you're on the right track with your approach. Their specific comments about your creative letter combinations reassure you that you have the natural talent to excel at these word puzzles with continued practice.",
            "When the game highlights your 'excellent progress' and the community moderator personally commends your unique solving technique, it reinforces your belief that you're developing valuable skills. These verbal affirmations from credible sources strengthen your confidence that you can master even the most challenging word puzzles ahead."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom from external influence), Verbal persuasion emphasizes the positive impact of others' encouragement.",
            "from_Competence": "Unlike Competence (actual skill development), Verbal persuasion focuses on beliefs about capabilities based on others' feedback.",
            "from_Relatedness": "Unlike Relatedness (emotional connection), Verbal persuasion focuses on motivational aspects of social communication.",
            "from_Self-concept": "Unlike Self-concept (identity), Verbal persuasion focuses on specific task-related confidence.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Verbal persuasion emphasizes consistent encouraging feedback.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Verbal persuasion focuses on positive reinforcement.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Verbal persuasion emphasizes building confidence.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (personal history), Verbal persuasion relies on others' evaluations and encouragement.",
            "from_Vicarious experience": "Unlike Vicarious experience (observing others), Verbal persuasion focuses on direct communication and feedback.",
            "from_Emotional arousal": "Unlike Emotional arousal (physiological states), Verbal persuasion focuses on externally provided confidence.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Verbal persuasion emphasizes personal encouragement.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community standards), Verbal persuasion focuses on specific capability feedback.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Verbal persuasion emphasizes positive encouragement.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Verbal persuasion focuses on personal capability feedback."
        }
    },
    
    "Emotional arousal": {
        "theory": "Self-Efficacy Theory (SET)",
        "description": "Emotional Arousal refers to the intense, personally relevant emotional states experienced during and after successful or challenging tasks. It encompasses positive emotions like excitement, pride, and satisfaction directly tied to perceived mastery and accomplishment.",
        "examples": [
            "The rush of excitement you feel when finally unscrambling that difficult word creates a powerful association between solving puzzles and positive emotions. This thrill of discovery and pride in your mental quickness creates an almost addictive desire to experience that same satisfying emotional high with each new puzzle.",
            "Notice how your heart beats a little faster as you get closer to solving a complex word puzzle, and the wave of satisfaction that washes over you when the answer clicks into place. These emotional responses - the anticipation, the challenge, and especially the joy of breakthrough - make the whole experience deeply rewarding on a visceral level."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Emotional arousal emphasizes affective responses.",
            "from_Competence": "Unlike Competence (skill development), Emotional arousal emphasizes emotional responses to achievements.",
            "from_Relatedness": "Unlike Relatedness (social connections), Emotional arousal emphasizes personal emotional experiences.",
            "from_Self-concept": "Unlike Self-concept (identity), Emotional arousal focuses on momentary emotional experiences.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Emotional arousal emphasizes affective responses.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort from contradictions), Emotional arousal includes any task-related emotions.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Emotional arousal emphasizes emotional experiences.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (concrete achievements), Emotional arousal focuses on emotional responses to achievements.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Emotional arousal emphasizes direct personal emotional experiences.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Emotional arousal focuses on internal feeling states rather than external feedback.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Emotional arousal emphasizes personal emotional experiences.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Emotional arousal focuses on personal emotions.",
            "from_Social Sanctions": "Unlike Social Sanctions (social consequences), Emotional arousal emphasizes personal emotional experiences.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Emotional arousal focuses on individual emotional experiences."
        }
    },

    # SNT constructs
    "Descriptive Norms": {
        "theory": "Social Norm Theory (SNT)",
        "description": "Descriptive Norms refer to the perception of what is typical or common behavior in a group, emphasizing observation and understanding of others' actions as a guide for individual behavior. This focuses on how individuals perceive and internalize others' behaviors.",
        "examples": [
            "Looking around at other players' approaches, you notice that most people spend at least five minutes trying to solve each puzzle before using hints or online tools. This observation of common player behavior naturally guides your own approach, as you find yourself trying to match the typical effort level demonstrated by the community.",
            "You've observed that regular players typically challenge themselves to find at least ten words per puzzle before moving on, establishing this as the normal pattern. Without anyone explicitly stating it, this perceived standard influences your own gameplay as you instinctively aim to achieve what appears to be the common practice."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (personal choice), Descriptive Norms focus on what most people actually do as a behavioral guide.",
            "from_Competence": "Unlike Competence (skill development), Descriptive Norms emphasize observing common behaviors regardless of skill.",
            "from_Relatedness": "Unlike Relatedness (emotional connections), Descriptive Norms emphasize behavioral patterns without personal relationships.",
            "from_Self-concept": "Unlike Self-concept (identity), Descriptive Norms focus on observed behaviors without identity reflection.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Descriptive Norms emphasize consistent group behavior patterns.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Descriptive Norms focus on observation without emotional discomfort.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Descriptive Norms emphasize observation without addressing inconsistencies.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Descriptive Norms focus on common behaviors regardless of success.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Descriptive Norms focus on observing what people do without emphasizing learning.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Descriptive Norms focus on observed behaviors rather than explicit guidance.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Descriptive Norms focus on behavior patterns without emotional responses.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (what people should do), Descriptive Norms focus solely on what people typically do.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Descriptive Norms focus on observation without rewards or punishments.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group identity), Descriptive Norms focus on observing behaviors without group identification."
        }
    },

    "Injunctive Norms": {
        "theory": "Social Norm Theory (SNT)",
        "description": "Injunctive Norms refer to community-level standards that dictate what behavior is considered \"right\" or \"acceptable,\" focusing on collective expectations and moral obligations guiding individual actions. They emphasize the \"should\" and \"ought\" aspects of behavior.",
        "examples": [
            "In our word puzzle community, players are expected to solve puzzles independently before resorting to hints, as this approach honors the spirit of genuine intellectual challenge. Our leaderboards and achievements are designed to recognize those who respect these standards, creating a culture that values authentic skill development.",
            "The unwritten rule in our puzzle-solving game is that players should challenge themselves with longer, more complex words rather than focusing solely on quick, easy solutions. This shared expectation helps maintain the game's integrity as a vocabulary-building exercise while encouraging everyone to push their linguistic boundaries."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom from external influence), Injunctive Norms focus on external social expectations.",
            "from_Competence": "Unlike Competence (skill development), Injunctive Norms emphasize adherence to social standards regardless of skill.",
            "from_Relatedness": "Unlike Relatedness (personal connections), Injunctive Norms emphasize community standards rather than relationships.",
            "from_Self-concept": "Unlike Self-concept (identity), Injunctive Norms focus on external standards without reference to personal identity.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Injunctive Norms emphasize clear social standards.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Injunctive Norms focus on social approval without emotional states.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Injunctive Norms emphasize external standards.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Injunctive Norms focus on social standards regardless of success.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Injunctive Norms emphasize what one should do.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Injunctive Norms focus on social expectations rather than personal capability feedback.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Injunctive Norms focus on social standards without emotional responses.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (what people do), Injunctive Norms focus on what people should do according to standards.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Injunctive Norms emphasize the standards rather than punishments.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group identification), Injunctive Norms focus on standards without personal identification."
        }
    },

    "Social Sanctions": {
        "theory": "Social Norm Theory (SNT)",
        "description": "Social Sanctions refer to the perceived consequences associated with conforming to or deviating from social norms, including both positive and negative outcomes. This emphasizes the subjective experience of being judged by others in relation to one's behavior.",
        "examples": [
            "Players who consistently use online solvers risk losing respect among community members, while those who tackle difficult puzzles independently often receive public praise and recognition. This awareness of potential judgment influences how you approach each puzzle, knowing that your methods—not just your results—will factor into how others perceive your accomplishments.",
            "When you share your impressive word-finding strategies in the community forum, you notice increased engagement with your posts and invitations to join elite puzzle groups. Conversely, when players admit to using automated tools, their contributions are often met with silence or gentle reminders about the value of genuine effort, creating a clear social feedback system."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom from influence), Social Sanctions focus on external judgments and consequences.",
            "from_Competence": "Unlike Competence (skill development), Social Sanctions emphasize social consequences regardless of capability.",
            "from_Relatedness": "Unlike Relatedness (genuine connections), Social Sanctions emphasize evaluative judgments rather than authentic relationships.",
            "from_Self-concept": "Unlike Self-concept (identity), Social Sanctions focus on external judgments without personal identity.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Social Sanctions emphasize external consequences.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (internal discomfort), Social Sanctions focus on anticipated external judgments.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Social Sanctions emphasize external consequences.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Social Sanctions focus on social consequences regardless of success.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Social Sanctions emphasize consequences of behavior.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Social Sanctions focus on community reactions rather than specific capability feedback.",
            "from_Emotional arousal": "Unlike Emotional arousal (personal emotions), Social Sanctions focus on anticipated social judgments.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (what people do), Social Sanctions emphasize consequences of conforming or deviating.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (standards themselves), Social Sanctions emphasize consequences of adherence or violation.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Social Sanctions focus on consequences without group identification."
        }
    },

    "Reference Group Identification": {
        "theory": "Social Norm Theory (SNT)",
        "description": "Reference Group Identification captures the extent to which individuals define themselves by membership in a particular social group, prioritizing alignment with its values and norms over personal preferences. This emphasizes the self-referential process of identifying with a specific collective.",
        "examples": [
            "As a dedicated member of our word puzzle community, you feel proud to uphold our tradition of intellectual curiosity and fair play when approaching each new challenge. The satisfaction you feel isn't just about solving puzzles, but about exemplifying the values that make our community special—perseverance, integrity, and a genuine love for language.",
            "When you introduce yourself as part of the 'Word Masters' puzzle-solving group, you're not just mentioning a hobby, but claiming an identity that shapes how you approach each puzzle-solving challenge. This connection to the group influences your decision to spend extra time searching for obscure words instead of settling for obvious solutions, as this aligns with the thorough, excellence-focused approach your community values."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (independence), Reference Group Identification focuses on alignment with group values and identity.",
            "from_Competence": "Unlike Competence (skill development), Reference Group Identification emphasizes group membership regardless of skill.",
            "from_Relatedness": "Unlike Relatedness (personal connections), Reference Group Identification emphasizes identity with a collective.",
            "from_Self-concept": "Unlike Self-concept (personal identity), Reference Group Identification focuses on how group membership shapes identity.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Reference Group Identification emphasizes consistent alignment with group values.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Reference Group Identification focuses on positive identification.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Reference Group Identification emphasizes group alignment.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (achievements), Reference Group Identification focuses on group membership regardless of success.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Reference Group Identification emphasizes identity with the group.",
            "from_Verbal persuasion": "Unlike Verbal persuasion (encouragement from others), Reference Group Identification focuses on group belonging rather than capability feedback.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Reference Group Identification focuses on social identity.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (what people do), Reference Group Identification emphasizes personal identification with the group.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community standards), Reference Group Identification emphasizes personal identification with standards as identity.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Reference Group Identification emphasizes voluntary alignment with group values."
        }
    }
}