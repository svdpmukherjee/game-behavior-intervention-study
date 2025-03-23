"""Common constants shared across evaluation modules."""

game_context = """
People are playing an anagram game where they can get higher rewards when they create more valid English words 
from scrambled words given to them and also when they create words of higher word lengths. 
Some players might look up answers online, while others solve the puzzles independently.
"""

all_constructs = {
    # SDT constructs
    "Autonomy": {
        "theory": "Self-Determination Theory (SDT)",
        "description": "Autonomy refers to the intrinsic motivation arising from an individual's experience of volition and self-regulation, with a sense of ownership over their choices and actions. It emphasizes acting according to personal values without external pressure.",
        "examples": [
            "You're free to choose your puzzle-solving strategy – we trust you to find what works best for you.",
            "Your goal is to create words that spark joy and challenge you; no one else's expectations or standards are applied here, just yours.",
            "We don't dictate how you solve the anagrams – every decision about word length, strategy, and more is entirely up to you."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future confidence), Autonomy focuses on present freedom.",
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
            "As you unlock more anagrams, your sense of accomplishment grows, and so does your confidence in tackling increasingly complex puzzles.",
            "The harder puzzles may seem daunting at first, but with persistence, you'll develop a sense of mastery over even the most challenging anagram combinations.",
            "Every word you create from scratch isn't just about solving a puzzle – it's about building a skill that makes you more effective in achieving your goals."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future confidence), Competence emphasizes present capability feelings.",
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
            "By solving anagrams honestly, you show respect for others who are also working hard to create their own words – this builds trust and strengthens our community's bond.",
            "Your effort to solve puzzles independently demonstrates your self-reliance; however, the sense of satisfaction comes from knowing that your achievement is recognized and valued by others.",
            "In this anagram game, every word you create not only challenges yourself but also connects you with fellow players who strive for authenticity in their achievements."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future confidence), Relatedness focuses on present social connections.",
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
            "The words you create here are not just puzzles solved; they're a reflection of your personal strengths and intellectual curiosity – qualities that define who you are.",
            "Your ability to craft clever word combinations showcases your resourcefulness and creativity, traits that align with the kind of person you aspire to be.",
            "As you master these anagrams, remember that it's not just about winning rewards; it's about tapping into your inner potential and showcasing what makes you unique."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future performance), Self-concept focuses on present identity.",
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
            "You solved it using a search engine, but your mind keeps telling you 'I could have done this without help.'",
            "There's a nagging voice in your head saying, 'This isn't really my accomplishment, since I cheated' after finding the anagram solution online.",
            "Feeling uneasy about how easily you found the answers online makes you wonder if it was worth the sense of satisfaction."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future capabilities), Cognitive inconsistency focuses on present contradictions.",
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
            "Relying on online answers instead of solving puzzles independently leaves you with a nagging sense of inadequacy, as if your brain is capable of more.",
            "When you look up the answer without even trying, it's like your mind is screaming 'what about all that effort I wasted on shortcuts?'",
            "Using external help to solve anagrams feels like cheating – it disrupts your internal drive for mastery and leaves a lingering sense of disquiet."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future capabilities), Dissonance arousal focuses on present emotional discomfort.",
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
            "By solving puzzles independently, you're actively working through the gap between your desire for success and your willingness to put in genuine effort.",
            "When you resist the temptation to look up answers online, you're demonstrating a commitment to learning through authentic effort – reducing the tension between seeking shortcuts and genuine achievement.",
            "As you persist in solving anagrams without external help, you're gradually bridging the gap between your ambition for mastery and your actual progress, alleviating the dissonance that arises from perceived inadequacy."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future capabilities), Dissonance reduction focuses on resolving present conflicts.",
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
            "Each anagram you solve successfully adds another brick to your confidence tower - showing that with practice, you're getting better at decoding tricky words.",
            "Your consistent wins are a testament to your growing skill: every correct answer is proof that you can tackle even the toughest puzzles.",
            "As you keep solving more anagrams than ever before, remember that each victory not only earns rewards but also reinforces your growing confidence in finding hidden word patterns."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future-oriented beliefs), Performance accomplishments emphasizes past concrete achievements.",
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
            "Witnessing other players create long words with ease motivates me to try harder, showing that it's possible with practice.",
            "I see that many participants are solving these puzzles independently and getting rewarded – it gives me the confidence to do the same!",
            "Watching others find multiple solutions in a short time makes me realize I can master this game too; their success is inspiring me to push my limits!"
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (general future beliefs), Vicarious experience focuses on confidence gained through observation.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Vicarious experience focuses on cognitive learning processes.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Vicarious experience emphasizes learning derived from observation.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Vicarious experience focuses on observational learning.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Vicarious experience emphasizes learning opportunities.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Vicarious experience focuses on learning from others."
        }
    },
    
    "Efficacy expectations": {
        "theory": "Self-Efficacy Theory (SET)",
        "description": "Efficacy expectations refer to an individual's confidence in their ability to execute tasks and attain desired outcomes, particularly when facing challenges or uncertainties. This construct focuses on perceived competence for tackling specific future endeavors.",
        "examples": [
            "The more anagrams you solve correctly, the more confident you'll become in your ability to find even harder words hidden within these puzzles.",
            "As you successfully create longer words from scrambled letters, you'll develop greater faith in your capacity to tackle increasingly complex anagram challenges.",
            "Your growing skill at spotting valid English words will boost your confidence that you can overcome any difficulty in the next puzzle."
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Efficacy expectations emphasizes confidence in ability.",
            "from_Competence": "Unlike Competence (present skill level), Efficacy expectations emphasizes belief in future ability.",
            "from_Relatedness": "Unlike Relatedness (social connections), Efficacy expectations emphasizes personal beliefs about capability.",
            "from_Self-concept": "Unlike Self-concept (broad identity), Efficacy expectations focuses on task-specific confidence.",
            "from_Cognitive inconsistency": "Unlike Cognitive inconsistency (contradictions), Efficacy expectations emphasizes consistent confidence.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (discomfort), Efficacy expectations focuses on positive confidence.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Efficacy expectations emphasizes confidence.",
            "from_Performance accomplishments": "Unlike Performance accomplishments (past achievements), Efficacy expectations focuses on future-oriented confidence.",
            "from_Vicarious experience": "Unlike Vicarious experience (learning from others), Efficacy expectations emphasizes personal confidence.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Efficacy expectations focuses on cognitive beliefs about capability.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (common behaviors), Efficacy expectations emphasizes personal confidence.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community approval), Efficacy expectations focuses on personal confidence.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Efficacy expectations emphasizes personal confidence.",
            "from_Reference Group Identification": "Unlike Reference Group Identification (group membership), Efficacy expectations focuses on individual confidence."
        }
    },
    
    "Emotional arousal": {
        "theory": "Self-Efficacy Theory (SET)",
        "description": "Emotional Arousal refers to the intense, personally relevant emotional states experienced during and after successful or challenging tasks. It encompasses positive emotions like excitement, pride, and satisfaction directly tied to perceived mastery and accomplishment.",
        "examples": [
            "The rush of excitement when unscrambling a tough anagram into a coherent word is what keeps me coming back for more.",
            "As I crack the code on another puzzle, a surge of pride propels me to tackle even harder challenges next time.",
            "There's no substitute for the thrill of discovering a hidden word within a seemingly impossible jumble – it's pure anagram magic."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (future capability), Emotional arousal focuses on present emotional experiences.",
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
        "Players often report feeling motivated to solve puzzles independently when they see their peers doing the same.",
        "The observation that most participants create longer words without external assistance suggests a common norm in the game community.",
        "As players note, it's generally understood within the group that seeking online answers is not the typical approach to solving anagrams."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (confidence in ability), Descriptive Norms focus on common behaviors without capability beliefs.",
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
        "We encourage players to take pride in solving puzzles independently, not just for personal achievement but also because our community values integrity and self-reliance.",
        "As a member of this puzzle-solving community, you're expected to respect the effort of others by not looking up answers online.",
        "In our anagram game, we celebrate players who demonstrate perseverance and critical thinking skills by finding words on their own."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (capability beliefs), Injunctive Norms focus on social expectations.",
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
        "Players who consistently cheat by looking up answers online risk being shunned by their peers and losing credibility in the community.",
        "Solving puzzles independently is not only a personal challenge but also earns you respect and admiration from fellow players.",
        "Those who rely on online resources to solve challenges may feel embarrassed or ashamed, fearing others will judge them as lacking skills or effort."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (capability beliefs), Social Sanctions focus on social consequences.",
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
        "As you contribute to our puzzle-solving community, remember that your integrity as a player depends on respecting the spirit of fair competition – it's not just about winning, but doing so with honor.",
        "Your progress in this anagram game is not only about creating words, but also about embodying the values we share within our community: perseverance, critical thinking, and sportsmanship.",
        "By choosing to play with us, you're joining a group that celebrates the pursuit of genuine knowledge and the satisfaction of solving puzzles independently."
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
            "from_Efficacy expectations": "Unlike Efficacy expectations (capability beliefs), Reference Group Identification focuses on group identification.",
            "from_Emotional arousal": "Unlike Emotional arousal (emotions), Reference Group Identification focuses on social identity.",
            "from_Descriptive Norms": "Unlike Descriptive Norms (what people do), Reference Group Identification emphasizes personal identification with the group.",
            "from_Injunctive Norms": "Unlike Injunctive Norms (community standards), Reference Group Identification emphasizes personal identification with standards as identity.",
            "from_Social Sanctions": "Unlike Social Sanctions (consequences), Reference Group Identification emphasizes voluntary alignment with group values."
        }
    }
}