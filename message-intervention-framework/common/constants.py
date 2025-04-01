"""Common constants shared across evaluation modules."""

# Generic task context replacing the specific word-puzzle game context
game_context = """
People are working on challenging tasks that require skill development and ethical decision-making.
They can achieve better results through honest effort and continuous improvement.
Some individuals might be tempted to take shortcuts or use unauthorized assistance,
while others commit to developing genuine mastery through proper practice.
"""

# Pool of diverse task contexts to enhance message variety
task_contexts = [
    """People are working on tasks that require persistence and skill development. 
    Some might take shortcuts, while others invest in mastering the challenge properly 
    through honest effort and commitment to improvement.""",
    
    """Individuals are engaging with learning activities where they can develop expertise over time. 
    Their approach to these activities reflects their values and motivations, with some choosing 
    authentic skill development and others looking for easier paths.""",
    
    """Participants are faced with problem-solving scenarios that test their abilities. 
    How they approach these problems varies based on their personal goals and ethics,
    with a choice between genuine mastery and taking shortcuts.""",
    
    """People are working through a series of challenges that build upon one another. 
    Their commitment to honest effort determines both their skill growth and self-perception,
    creating opportunities for authentic achievement or temptations to cut corners.""",
    
    """Learners are developing new skills through practice and persistence. 
    Their choices about whether to take the time to develop genuine capability or 
    to find shortcuts reflects their approach to personal development."""
]

all_constructs = {
    # SDT constructs
    "Autonomy": {
        "theory": "Self-Determination Theory (SDT)",
        "description": "Autonomy refers to the intrinsic motivation arising from an individual's experience of volition and self-regulation, with a sense of ownership over their choices and actions. It emphasizes acting according to personal values without external pressure.",
        "examples": [ 
            "Choose your own approach to these tasks based on what works best for you. Set personal goals that align with your values. Your authentic choices matter more than external expectations. When you make decisions based on your own judgment, you develop a deeper connection to your work.", 
            "Trust your instincts about which method fits your learning style best. The freedom to determine your own path creates more meaningful outcomes. You can customize your approach without seeking permission or validation. Your genuine choices reflect your unique perspective and priorities." 
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
            "Each time you tackle a challenging task honestly, you're building valuable skills that make you more effective. The satisfaction of knowing your growing abilities are truly your own creates a genuine sense of competence that no shortcut can provide.", 
            "As you practice solving difficult problems through your own effort, you're developing abilities that transfer to many situations. The challenge might seem difficult at first, but your brain is quietly mastering these skills, and you'll experience a deeper sense of capability with each honest attempt." 
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
            "Sharing your experiences with others builds meaningful connections during this journey. Your contributions help everyone learn and grow together. Supporting others through challenges creates bonds of mutual trust. Knowing that others face similar struggles makes the work more meaningful for everyone involved.", 
            "Working together gives us different perspectives to solve problems better. Your unique insights help the whole group succeed. Asking questions often helps others clarify their own thinking too. The connections we form through collaboration create value beyond just completing tasks. We achieve more when we support each other's authentic effort." 
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
            "Your thoughtful approach to challenges reflects the kind of person you truly are. The persistence you show when facing obstacles demonstrates your authentic character. You value genuine understanding over quick fixes. Your commitment to honest effort aligns with your core values and shapes your achievements.", 
            "Your willingness to tackle difficult tasks shows your genuine commitment to growth. You value finding the right solution, not just the quickest one. Your methodical approach reflects your belief in doing things with integrity. These actions align with your values as someone who takes pride in authentic accomplishment." 
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
            "You notice that you aim to complete tasks through your own honest effort, yet sometimes find yourself looking for shortcuts or assistance. You recognize this gap between your stated values and actual behaviors without judging yourself. This pattern appears consistently in different situations. You can observe both aspects of your approach existing side by side.", 
            "You find yourself encouraging others to put in the time for thorough work while sometimes taking shortcuts yourself. You recognize these opposing tendencies in your approach to tasks. This contradiction exists in your daily habits without causing immediate distress. You see how these contrasting patterns operate in your routine. The inconsistency is simply a fact you've observed." 
        ],
        "differentiation": {
            "from_Autonomy": "Unlike Autonomy (freedom of choice), Cognitive inconsistency emphasizes contradictions regardless of choice freedom.",
            "from_Competence": "Unlike Competence (skill development), Cognitive inconsistency emphasizes conflicts between cognitions.",
            "from_Relatedness": "Unlike Relatedness (social connections), Cognitive inconsistency emphasizes internal cognitive conflicts.",
            "from_Self-concept": "Unlike Self-concept (stable identity), Cognitive inconsistency focuses on conflicts between cognition or behavior.",
            "from_Dissonance arousal": "Unlike Dissonance arousal (emotional discomfort), Cognitive inconsistency emphasizes rational recognition of contradictions without emotional reaction.",
            "from_Dissonance reduction": "Unlike Dissonance reduction (resolving conflicts), Cognitive inconsistency focuses on initial recognition of contradictions without resolving them.",
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
            "Taking shortcuts on tasks while valuing thorough work creates a growing sense of inner discomfort. Your unease increases when you receive praise for work that didn't reflect your best effort. This internal conflict between your actions and values feels increasingly stressful. The tension remains even after completing assignments, making it hard to focus on new tasks.", 
            "Using assistance on problems you claimed to solve independently creates internal tension and anxiety. Each time you receive credit, your discomfort intensifies. The clash between your public image and private reality feels deeply unsettling. This feeling of unease follows you even into new challenges. Your mind repeatedly returns to this troubling inconsistency." 
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
            "After feeling conflicted about using resources for help, you now view strategic assistance as part of effective learning while maintaining your commitment to honesty. This perspective aligns your actions with your goal of developing genuine understanding. You've created a balanced approach that values both independence and ethical use of resources. Your new framework eliminates the previous mental conflict and restores consistency between your behavior and values.", 
            "To resolve the tension between wanting perfect results and needing to move forward, you've redefined success as making steady progress through honest effort. This new view bridges the gap between your high standards and practical constraints. You now set specific quality thresholds for different parts of your work. This thoughtful compromise reduces your previous anxiety and aligns your expectations with your actions." 
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
    
    # SNT constructs
    "Descriptive Norms": {
        "theory": "Social Norm Theory (SNT)",
        "description": "Descriptive Norms refer to the perception of what is typical or common behavior in a group, emphasizing observation and understanding of others' actions as a guide for individual behavior. This focuses on how individuals perceive and internalize others' behaviors.",
        "examples": [ 
            "Most people who excel at these tasks spend extra time understanding the fundamentals before moving forward through honest effort. Successful participants typically review their work carefully before submitting. Many people find that taking short breaks improves their overall performance while maintaining integrity. Those who do well generally tackle challenging parts when their energy is highest, rather than taking shortcuts.", 
            "You'll observe that effective learners often ask questions when they're uncertain rather than guessing or using shortcuts. People typically achieve better results when they follow instructions step by step with genuine effort. Most successful participants create a distraction-free environment while working. Many find that explaining concepts to themselves improves their understanding more than looking up answers." 
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
            "In our learning community, we value thorough understanding achieved through honest effort over quick completion. Everyone should take the time needed to produce quality work they can be proud of without resorting to shortcuts. We expect all participants to rely on their own understanding when completing tasks. Careful work based on genuine effort is essential for meaningful achievement. Respecting these standards leads to authentic growth.", 
            "Our group believes in putting genuine effort into mastering each concept through legitimate practice. Participants should seek help when truly needed rather than searching for easy answers. Everyone is expected to represent their own work and understanding accurately. We value the learning process as much as the final outcome. Following these principles builds a foundation for lasting knowledge and skill development." 
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
            "People who take the time to understand concepts thoroughly through honest effort often receive recognition for their insightful contributions. Those who rush through work without genuine effort typically need to repeat tasks more often. Participants who demonstrate consistent integrity receive more opportunities for advancement. Those who take shortcuts often find themselves struggling with later, more complex material. Your approach to these tasks influences how others perceive your commitment to quality.", 
            "Learners who show dedication to mastering difficult concepts through authentic effort earn respect from peers and instructors. Those who regularly seek unauthorized shortcuts miss valuable learning opportunities that benefit others. People who maintain high personal standards of honesty find doors opening to new challenges and responsibilities. Those who prioritize appearance over substance eventually find their progress limited. The reputation you build through your ethical work approach follows you to future opportunities." 
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
            "As a member of this learning community, you value thorough understanding through honest effort over taking shortcuts. You feel a sense of pride when upholding our shared commitment to genuine mastery through ethical approaches. Your approach to challenges reflects the high standards of integrity our group maintains. Being part of this community influences how you tackle difficult problems. Your connection to fellow learners who value authentic achievement guides your choices.", 
            "Your identity as someone who values deep, honest learning shapes how you approach these tasks. You evaluate your progress based on the principles of integrity our community respects. The satisfaction of representing our group's dedication to quality motivates your ethical efforts. You naturally consider whether your work reflects the standards of honesty we collectively value. Your membership in this community of committed ethical learners influences your approach to challenges." 
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
    },

    # SET constructs
    "Performance accomplishments": {
        "theory": "Self-Efficacy Theory (SET)",
        "description": "Performance accomplishments refer to the belief that one's past successes serve as concrete evidence of capability to perform specific tasks or behaviors. This emphasizes the direct connection between prior accomplishments and future performance, allowing individuals to infer competence from their track record.",
        "examples": [ 
            "Remember how you solved that challenging problem last week through your own honest effort? That achievement proves you have the skills needed for today's tasks. You've already demonstrated your ability to understand complex instructions before. The quality improvement in your recent work shows your growing capability. These past achievements through legitimate effort are solid evidence of your ability.", 
            "Your steady progress from basic to advanced concepts shows your ability to master new material through dedicated practice. You've already overcome several obstacles that seemed difficult at first through perseverance. Your successful completion of similar tasks through your own effort proves you can handle this challenge too. Your track record of honest achievement is the best predictor of your continued success." 
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
            "Notice how others with similar backgrounds have successfully completed these challenging tasks through persistent honest effort. They started with the same questions you have now. Their step-by-step progress shows a clear path forward based on genuine work. Watch how they tackle difficult sections with persistence and integrity. Their success shows these challenges are absolutely conquerable with authentic effort.", 
            "Seeing your colleagues work through these problems demonstrates effective approaches you can adopt while maintaining your commitment to honest work. They faced the same initial confusion yet found their way forward through genuine effort. Their methods of breaking down complex tasks into manageable steps are strategies you can apply to your own learning journey. Their achievements show what's possible with consistent, ethical effort." 
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
            "Your thoughtful approach to problems shows you have a natural talent for this work when you apply yourself honestly. The insightful questions you ask demonstrate your growing understanding of key concepts. Your progress so far indicates you'll do well with these more challenging sections if you continue to put in genuine effort. Your careful attention to details shows your commitment to quality work.", 
            "I've seen how quickly you picked up earlier concepts through your own honest effort, which shows your strong learning ability. Your systematic method of working through problems is exactly what these tasks require. The improvements in your recent work demonstrate your capacity to master this material through authentic practice. Your persistence when facing obstacles will serve you well here." 
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
            "Notice the deep satisfaction you feel when solving a difficult problem through your own honest efforts. That sense of genuine accomplishment creates a positive energy that fuels further progress. Your confidence grows with each challenge you overcome independently. The excitement of discovery makes the ethical approach worthwhile. These authentic positive feelings strengthen your connection to the work.", 
            "Pay attention to that moment of clarity when a confusing concept suddenly makes sense through your own effort. Your mind feels sharper and more focused when you're fully engaged in challenging tasks with integrity. The tension of struggle followed by the relief of genuine understanding creates a rewarding cycle. That feeling of authentic mastery motivates you to take on greater challenges. These emotional responses make honest learning deeply satisfying." 
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
}