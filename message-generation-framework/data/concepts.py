"""
Psychological concepts and task contexts data.
This module contains the definitions of psychological concepts and task contexts
used for message generation.
"""

# Task contexts shared resources by generator and evaluator
TASK_CONTEXTS = [
    """Participants are faced with problem-solving scenarios that test their abilities. How they approach these problems varies based on their personal goals and values.""",
    
    """People are working on tasks that require persistence and skill development. Some might take shortcuts, while others invest in mastering the challenge properly through honest effort and commitment to improvement.""",

    """Individuals are engaging with learning activities where they can develop expertise over time. Their approach to these activities reflects their values and motivations, with some choosing authentic skill development and others looking for easier paths.""",

    """People are working through a series of challenges that build upon one another. Their commitment to honest effort determines both their skill growth and self-perception, creating opportunities for authentic achievement or temptations to cut corners.""",

    """Learners are developing new skills through practice and persistence. Their choices about whether to take the time to develop genuine capability or to find shortcuts reflects their approach to personal development."""
]

# Diversity focus options for message variation
MESSAGE_FOCUSES = [
    "The relationship between this concept and maintaining integrity",
    "How this concept manifests in personal growth over time",
    "How this concept helps people overcome specific challenges and obstacles",
    "The universal experience of engaging with this concept",
    "The long-term benefits of applying this concept consistently",
    "How this concept relates to authentic skill development",
    "How this concept guides effective decision-making processes",
    "Practical day-to-day applications of this concept",
    "How this concept shapes perspectives on learning",
    "The relationship between this concept and genuine satisfaction"
]

MESSAGE_STYLE = [
    "Create a message that uses a question-answer format",
    "Create a message that uses a conditional 'when-then' structure",
    "Create a message that uses a comparison or contrast structure",
    "Create a message that uses cause-effect reasoning format",
]

# Tone options for message generation
TONES = [
    "Motivational",
    "Encouraging",
    "Informative",
    "Supportive",
    "Coaching",
    "Reflective",
    "Straightforward",
    "Friendly"
]

# All psychological concepts with their descriptions and examples
ALL_conceptS = {
    # SDT concepts
    "Autonomy": {
        "theory": "Self-Determination Theory",
        "description": "Autonomy is the psychological need to experience one’s actions as self-endorsed and originating from the self. It involves an internal locus of causality, a sense of volition, and perceived choice over one’s behaviors.",
        "examples": [
            "I notice you really dive into projects you choose yourself. Having that freedom keeps you motivated. Even when things get tough, you stick with it because it's your own path.",
            "What I love about this job is choosing my own approach. When I can tackle problems my way, I'm much more invested. It's not about avoiding help, just having space to make my own choices.",
            "The best teams are ones where people have a say in how they work. When folks feel ownership instead of just following orders, they get more creative. Having that personal choice makes even hard work feel worthwhile.",
            "Ever notice how different you feel when you're doing something you chose versus something forced on you? Your whole attitude changes when the decision comes from you."
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
        "theory": "Self-Determination Theory",
        "description": "Competence is the psychological need to feel effective in one’s pursuits and interactions with the environment. It reflects the desire to use and extend one’s abilities by seeking out and mastering challenges.",
        "examples": [
            "That feeling when you finally master something tough? It's amazing. When you push through the hard parts of learning, you build real confidence. I've seen how your persistence is making you better at solving problems.",
            "Remember when you solved that tough problem after trying so many times? That pride came from working through it, not finding an easy way out. The real growth happens when you're struggling with something new.",
            "I used to hate when I couldn't solve things right away. Now I actually like those challenges. Each difficult problem teaches me something for the next one. It feels so good to improve through honest effort.",
            "Learning an instrument means daily practice that seems boring. But it's building skills that eventually make playing feel natural. What seemed impossible becomes easy with time. You can't shortcut that process."
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
        "theory": "Self-Determination Theory",
        "description": "Relatedness is the psychological need to form close emotional bonds and secure, caring connections with others. It involves feeling understood, valued, and involved in mutually supportive relationships.",
        "examples": [
            "My best projects are always with teammates I connect with. Having that sense of belonging makes it easier to share ideas. When we support each other, we not only solve problems better - we enjoy it more.",
            "Notice how different it feels to work with people you connect with? There's something energizing about knowing your contribution matters. Even tough challenges feel manageable when you're part of a supportive group.",
            "I'm much more productive when I feel comfortable sharing my ideas. That feeling of being understood by colleagues creates the right foundation. Often the relationships become the most rewarding part of any project.",
            "Think about a time when you felt truly part of a team. That connection probably made you want to give your best effort. When people appreciate us, we naturally want to contribute more."
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

    # CDT concepts
    "Self-concept": {
        "theory": "Cognitive Dissonance Theory",
        "description": "Self-concept refers to a person's self-perceptions formed through experience and interpretations of one's environment.",
        "examples": [
            "I see myself as someone who cares about quality work. So when I rush through assignments, it feels wrong. I'm most satisfied when I give things the attention they deserve. That matches the kind of professional I want to be.",
            "You're so thoughtful about problems. You take time to understand before offering solutions. That careful approach is core to who you are. When you stay true to that, even under pressure, your work reflects your values.",
            "The care you put into your projects says a lot about you. You clearly believe if something's worth doing, it's worth doing right. That's not just about the result—it's about staying true to your standards.",
            "What made you rethink your approach? I'm guessing those shortcuts didn't feel right for someone who values understanding things fully. When our actions match our deeper values, it just feels better."
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
        "theory": "Cognitive Dissonance Theory",
        "description": "Cognitive inconsistency refers to a contradictory relationship between two related cognitions, where one (e.g., a behavior) implies the opposite of the other (e.g., a belief).",
        "examples": [
            "I've noticed something funny about how I study. I tell everyone I value deep understanding. Yet I sometimes skim readings just to finish quickly. These two habits exist side by side without bothering me much. Just an interesting quirk.",
            "Don't you sometimes say you want to master a skill properly while looking for shortcuts? I catch myself doing this with coding. I claim to want deep knowledge while skipping the basics. I notice both patterns without feeling troubled about it.",
            "You encourage teammates to take time for quality work. Yet you often submit your own stuff last minute. This isn't necessarily bad - just two different patterns in how you approach group projects.",
            "I say I value evidence-based decisions. Yet I sometimes go with my gut without doing research. These contradictory approaches both show up in my work regularly. It's interesting to see these patterns coexist."
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
        "theory": "Cognitive Dissonance Theory",
        "description": "Dissonance arousal refers to the psychological state in which individuals experience discomfort when confronted with conflicting or inconsistent cognitions (e.g., beliefs and behaviors).",
        "examples": [
            "Every time I rush through something important, I get this nagging feeling. The gap between how I want to work and how I actually did it creates this tension that follows me around. My mind won't let me just move on.",
            "Don't you hate that uncomfortable feeling when you take shortcuts on something that deserves better? It gets worse when people praise work you know isn't your best. That mismatch between your actions and standards creates a pressure that's hard to ignore.",
            "I feel so anxious when I present work as completely mine after getting lots of help. Each time someone compliments my 'independent' work, my stomach knots up. The gap between my public image and private reality keeps building until I address it.",
            "That discord when your actions don't match your values feels awful, right? I notice how that tension stays with me, creating this constant stress. My mind keeps circling back to the mismatch, making it hard to focus on anything else."
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
        "theory": "Cognitive Dissonance Theory",
        "description": "Dissonance reduction is the psychological process that motivates individuals to resolve the discomfort caused by inconsistencies between related cognitions (e.g., beliefs and behaviors), aiming to restore internal consistency or consonance.",
        "examples": [
            "I used to feel torn about working long hours while saying family comes first. I've fixed this by redefining success as making meaningful contributions in both areas. Now I set clearer boundaries and fully engage wherever I am. This balanced view has replaced my inner conflict.",
            "I dreaded team meetings because I wanted to speak up but feared judgment. Now I see my role as offering helpful perspectives rather than showing expertise. This lets me share ideas without feeling they must be perfect. The anxiety has disappeared as I focus on adding value.",
            "I struggled with flying often while claiming to care about the environment. I've resolved this by buying carbon offsets and combining trips to reduce travel. Rather than perfect consistency, I see harm reduction as acceptable. This practical compromise settled my previous guilt.",
            "The conflict between wanting creative excellence and meeting deadlines caused constant stress. Now I see constraints as creative catalysts, not limitations. I focus my perfectionism only where it matters most. This targeted approach has replaced my all-or-nothing thinking."
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

    # SNT concepts
    "Descriptive Norms": {
        "theory": "Social Norm Theory",
        "description": "Descriptive norms refer to the prevalent or common behaviors within a group and reflect individuals' perceptions of the likelihood that others engage in these behaviors.",
        "examples": [
            "Most people in our study group review their notes before speaking up. This leads to much better discussions. Many students also form smaller practice groups outside class to work through tough concepts together.",
            "Successful grad students usually set aside focused time without distractions. Most break big projects into smaller chunks rather than cramming. They're also not afraid to ask questions when they don't understand something.",
            "Looking around this workshop, you'll see most people sketch ideas before building prototypes. Many experienced makers test their designs multiple times. It's also common to see them documenting their process as they go.",
            "The developers who advance quickly typically study code from senior engineers. Many take time to understand systems before changing them. Most also write tests for their code to make sure it works properly."
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
        "theory": "Social Norm Theory",
        "description": "Injunctive norms refer to individuals' perceptions of what behaviors are considered acceptable or unacceptable in a given context, motivating actions through the anticipation of social rewards or punishments.",
        "examples": [
            "On our dev team, code reviews should be thorough, not quick check-offs. Team members should give specific, helpful feedback. Everyone should welcome suggestions instead of defending imperfect code. These principles keep our codebase strong.",
            "In our program, students should engage deeply with readings to form their own views. During discussions, everyone should build on others' ideas, not just wait for their turn. We value questions that explore concepts, not just facts. These standards help everyone grow.",
            "Athletes here should focus on proper technique over quick results. Everyone should keep complete training logs. Coaches should balance pushing limits with respecting recovery needs. These expectations create an environment where everyone improves long-term.",
            "At this hospital, staff should document patient interactions clearly. We expect everyone to admit what they don't know rather than guessing. All personnel should verify critical information firsthand. These standards protect patients and practitioners."
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
        "theory": "Social Norm Theory",
        "description": "Social sanctions include a variety of verbal and nonverbal reactions to norm transgressions designed to dissuade individuals from engaging in a behavior.",
        "examples": [
            "Scientists who document their methods thoroughly get more collaboration invitations and citations. Those who take shortcuts often find their work questioned. I've watched how Dr. Kim's careful approach has led to her methods being adopted across multiple labs.",
            "Customer service reps who really understand customer needs before offering solutions get higher ratings. Those who rush to close tickets quickly generate repeat calls and bad feedback. Notice how people specifically ask for Michael when they have complex issues.",
            "Students who contribute thoughtful comments in seminars receive more detailed feedback on their papers. Those who speak without preparation get more generic responses. Professors invest extra time mentoring students like Alicia who consistently come prepared.",
            "Architects who research environmental and community factors before finalizing designs win more bids. Those who focus only on looks without considering practical aspects face costly revisions. Tim's reputation for thorough work has clients waiting months for him."
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
        "theory": "Social Norm Theory",
        "description": "Reference group identification refers to the psychological process through which individuals who strongly identify with a social group align their self-perceptions, beliefs, attitudes and behaviors with the group’s norms.",
        "examples": [
            "As engineers here, we take pride in documenting our code fully, not just making quick fixes. When I'm deciding how to tackle a tough bug, I think about our team's reputation for solid solutions. That guides my choices even under tight deadlines.",
            "Being part of this academic community means embracing curiosity and thorough investigation. When facing complex questions, I remember our shared commitment to rigorous methods. This identity as careful scholars influences even my routine tasks.",
            "What connects us as craftspeople is our dedication to mastering traditional techniques. The satisfaction of upholding these shared values keeps me going through tedious practice. When I'm tempted to take shortcuts, I remember that's not who we are.",
            "Our team's identity is built around user-centered design. This shared value shapes how we evaluate our work - not just by whether it functions, but by how well it serves real people. Being part of a group that prioritizes empathetic design influences every project."
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

    # SET concepts
    "Performance accomplishments": {
        "theory": "Self-Efficacy Theory",
        "description": "Performance accomplishment refers to the mastery experiences one gains when taking on a new challenge and successfully completing it.",
        "examples": [
            "Remember when you solved that database problem everyone was stuck on? You worked through each part methodically until you found the issue. That wasn't luck—it was your analytical skills. Those same abilities will help you tackle this new challenge.",
            "You've already mastered three programming languages through consistent practice. Each time you thought it was too hard, you broke it down and persisted. Your track record of learning technical skills shows you can handle this new framework too.",
            "Think about how you handled that tough negotiation last quarter. You prepared thoroughly and adapted as new information came up. That success wasn't random—it showed your strategic thinking. Those same skills will serve you well in this upcoming meeting.",
            "Your portfolio shows clear progress from basic designs to complex projects. The improvement in your work over time isn't coincidence—it reflects your ability to learn from each project. You apply those insights to each new challenge."
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
        "theory": "Self-Efficacy Theory",
        "description": "Vicarious experience refers to the process through which individuals enhance their belief in their own capabilities to master tasks by observing people similar to themselves succeed through sustained effort.",
        "examples": [
            "Watch how Eliza tackles these complex design problems. She starts with rough sketches before committing to one direction. When she hits technical limits, she works through each constraint step by step. Seeing her approach has changed how I handle my own creative challenges.",
            "Marco had never used this software before joining our team last year. He watched how our senior analysts structured their work. Within six months, he was using these same techniques himself. Seeing his quick progress showed me these skills are definitely learnable.",
            "Remember how Dr. Chen demonstrated that technique last month? She broke down each movement into clear steps. Several residents who watched her have already used her approach successfully. Seeing them apply her methods makes me confident I can master this too.",
            "My sister struggled with public speaking just like you. She joined a speech club where she could see others progress from nervous to confident. Watching people with similar anxiety gradually improve showed her a clear path forward. Now she mentors new members herself."
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
        "theory": "Self-Efficacy Theory",
        "description": "Verbal persuasion refers to the process of receiving encouraging verbal feedback that strengthen an individual's belief in their ability to succeed in a task.",
        "examples": [
            "The way you analyzed that complex data set showed amazing attention to detail. Your methodical approach to validating findings demonstrates exactly what this project needs. I've seen how quickly you learn new methods, which makes me confident you'll excel with this challenge.",
            "Your presentations always connect technical concepts to real applications so well. You have a gift for making complex ideas accessible. The questions you ask show deep understanding. These communication strengths will make you perfect for this cross-functional role.",
            "I've noticed how thoroughly you test your code before submitting it. Your systematic approach to breaking down problems is exactly what we need. Based on how you've handled increasing complexity lately, I know you're ready for more advanced work.",
            "The thoughtful questions you ask during discussions show you're thinking at a strategic level. You naturally consider both technical limits and business needs when suggesting solutions. Your consistent follow-through shows you're ready for this leadership role."
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
        "theory": "Self-Efficacy Theory",
        "description": "Emotional arousal refers to the emotional states that individuals experience in response to challenging situations, which can influence the beliefs in their ability to succeed in a task.",
        "examples": [
            "Pay attention to that mental clarity you feel after working through a complex problem step by step. That sharpness tells you something important about how challenges affect your thinking. This positive energy becomes a resource for future obstacles.",
            "Notice that satisfaction when you express an idea precisely. That feeling of clarity is different from just finishing a task. These emotional rewards guide us toward deeper engagement that leads to real growth.",
            "There's a unique confidence that comes after mastering something that seemed impossible at first. This isn't just momentary happiness but a fundamental shift. Each time you experience this earned confidence, new challenges feel less intimidating.",
            "That calm focus you feel when fully engaged in challenging work signals an optimal learning state. This feeling, when you're neither bored nor overwhelmed, shows you're working at the edge of your abilities. Learning to recognize this state can transform how you approach difficult tasks."
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