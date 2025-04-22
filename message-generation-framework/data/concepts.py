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
            "I've noticed you seem most engaged when working on projects you've chosen yourself. Having the freedom to direct your own learning journey tends to keep that motivation going strong. Even when faced with challenges, you stick with it because it feels like your own path, not something imposed on you.",
            "What I find most fulfilling about this type of work is being able to chart my own course. When I can approach challenges in my own way, I feel much more invested in finding solutions. It's not about avoiding guidance, but rather having space to make meaningful choices about how to proceed.",
            "The teams that consistently deliver exceptional results are those where members have a real say in how they approach problems. When people feel ownership over their process rather than just following orders, their creativity and dedication naturally increase. This sense of personal agency makes even difficult tasks feel worthwhile.",
            "Have you noticed how your motivation changes when you're working on something you genuinely chose versus something that feels forced upon you? The quality of your engagement is completely different when the decision to pursue something comes from within."
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
            "The satisfaction you get from mastering something difficult is unlike anything else. When you persist through the challenging parts of learning a new skill, you build both capability and confidence. I've seen how your persistence with that difficult project has sharpened your problem-solving abilities in ways that quick fixes never could.",
            "Remember that feeling when you finally solved that tricky problem after multiple attempts? That sense of accomplishment came from working through the difficulty, not from finding an easy way around it. The growth happens in those moments of struggle when you're pushing beyond what you already know.",
            "I used to get frustrated when I couldn't solve something right away, but now I appreciate those challenges. Each time I work through a difficult problem, I develop tools that help me tackle the next one more effectively. The feeling of becoming more capable through honest effort is incredibly rewarding.",
            "When you're learning a musical instrument, the daily practice might seem tedious, but it's building neural pathways that eventually make playing feel natural. What seemed impossible becomes possible through consistent effort. That gradual mastery process can't be shortcut, but it creates abilities that stay with you."
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
            "The most rewarding projects I've worked on have always been those where I felt truly connected to my teammates. Having that sense of belonging makes it easier to share ideas, ask questions, and take creative risks. When we support each other through challenges, we not only solve problems better but also enjoy the process more.",
            "Have you noticed how different it feels to work on a task when you feel connected to the people around you? There's something energizing about knowing others value your contribution. Even difficult challenges become more manageable when you feel like you're part of a supportive community that recognizes your efforts.",
            "My productivity always increases when I work in an environment where I feel comfortable expressing my ideas and asking for input. That sense of being understood and valued by colleagues creates a foundation that makes creative work possible. The relationships we build through collaboration often become the most meaningful part of any project.",
            "Think about a time when you felt truly part of a team working toward a shared goal. That feeling of connection probably gave you extra motivation to contribute your best work. When we feel understood and appreciated by others, we naturally want to invest more of ourselves in the collective effort."
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
            "I've always seen myself as someone who values quality work, so when I rush through assignments just to get them done, it doesn't sit right with me. The times I feel most satisfied with my contributions are when I've given them the attention they deserve, in line with the kind of professional I aim to be.",
            "You approach problems so thoughtfully, taking time to understand them deeply before offering solutions. That careful consideration is such a core part of who you are. When you stay true to that thoughtful approach, even under pressure, your work reflects the values you hold most important.",
            "The craftsmanship you put into your projects speaks volumes about what matters to you. You're clearly someone who believes that if something's worth doing, it's worth doing thoroughly. That commitment to quality work isn't just about the outcome—it's about staying aligned with your personal standards.",
            "What made you reconsider your approach to the project? I'm guessing it might be because taking shortcuts didn't align with your values as someone who takes pride in understanding things thoroughly. When our actions match our deeper principles, there's a certain harmony that feels right."
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
            "I've noticed something interesting about my study habits lately. I tell myself and others that I value thorough understanding, yet I sometimes rush through readings just to finish them. These two approaches exist side by side in my routine without really bothering me much. It's just an observation about how I operate.",
            "Have you ever found yourself saying you want to master a skill properly, while simultaneously looking for shortcuts? I've caught myself doing this with learning programming—claiming I want deep knowledge while skipping foundational concepts. I can see both patterns in my behavior without feeling particularly troubled by it.",
            "You might notice that you encourage teammates to take time for quality work, yet you often submit your own contributions at the last minute. This isn't necessarily a problem—just an observation about two different patterns that exist in your approach to collaborative projects.",
            "I realize that I claim to value evidence-based decision-making, yet I sometimes go with my initial instinct without researching thoroughly. These contradictory approaches both show up in my work regularly. It's interesting to observe these different tendencies coexisting in my daily routine."
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
        "description": "Dissonance arousal refers to the psychological state in which individuals experience discomfort when confronted with conflicting or inconsistent cognitions (e.g. beliefs and behaviors).",
        "examples": [
            "Every time I rush through an assignment I claimed was important to me, I feel this growing sense of unease that's hard to shake. The gap between how I want to approach my work and how I actually handled it creates this uncomfortable tension that follows me even after I've submitted it. It's like my mind won't let me simply move on.",
            "Have you experienced that nagging discomfort when you take a shortcut on something you believe should be done thoroughly? That feeling intensifies when others praise work that you know doesn't reflect your best effort. The clash between your actions and your standards creates a persistent internal pressure that's difficult to ignore.",
            "I feel increasingly anxious when I present work as entirely my own after receiving substantial help. Each time someone compliments my 'independent' achievement, that knot in my stomach tightens. The disconnect between my public image and private reality creates a tension that keeps building until I address it somehow.",
            "That feeling of discord when your actions don't align with your values can be really unsettling, can't it? I notice how that tension stays with me, creating a persistent undercurrent of stress that affects my focus on new tasks. My mind keeps circling back to the mismatch, making it difficult to fully engage elsewhere."
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
            "I used to feel conflicted about spending so much time on work projects while claiming family was my priority. I've resolved this by redefining success as making meaningful contributions in both areas, rather than maximizing either one. Now I set clearer boundaries and fully engage wherever I am without the gnawing sense of neglecting something important. This balanced perspective has replaced my previous inner conflict.",
            "The tension between wanting to speak up in meetings and fearing judgment was making me dread team discussions. I've reframed my participation as offering potentially helpful perspectives rather than demonstrating expertise. This shift allows me to contribute ideas without feeling they must be perfectly formulated. The mental conflict has dissolved as I focus on adding value rather than proving worth.",
            "I struggled with the contradiction between valuing environmental sustainability and my frequent air travel for work. I've reconciled this by committing to carbon offsets and maximizing impact during each trip to reduce overall travel needs. Rather than seeing perfect consistency as the goal, I now view effective harm reduction as an acceptable approach. This pragmatic compromise has resolved my previous discomfort.",
            "The conflict between my desire for creative excellence and meeting deadlines was causing constant stress. I've developed a new framework that treats constraints as creative catalysts rather than limitations. By establishing clear quality thresholds for different project components, I can focus perfectionism where it matters most. This selective approach has resolved my previous all-or-nothing thinking."
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
            "I've noticed that most people in our study group spend time reviewing their notes before sharing their thoughts. This approach seems to lead to more insightful discussions. Many students also form smaller practice groups outside class to work through difficult concepts together.",
            "In my experience, successful graduate students typically set aside dedicated time for deep work without distractions. Most of them break large projects into manageable chunks rather than cramming at the deadline. I've also observed that they're not afraid to ask questions when they're unsure about something.",
            "Looking around the workshop, you'll see that most participants sketch out their ideas before building prototypes. Many experienced makers test their designs multiple times and refine them based on what they learn. It's also common to see people documenting their process as they go.",
            "The developers I've worked with who advance quickly in their careers tend to study code written by more experienced engineers. Many spend time understanding existing systems before making changes. It's also pretty standard to see them writing tests for their code to ensure it works as expected."
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
            "On our software development team, we believe that code reviews should be thorough rather than cursory. Team members should provide specific, constructive feedback rather than simply approving changes. We expect everyone to welcome code improvement suggestions rather than defending imperfect solutions. Following these principles ensures our codebase remains maintainable and robust.",
            "In our graduate program, students should engage with assigned readings deeply enough to form their own perspectives. During discussions, everyone is expected to build on others' contributions rather than just waiting to speak. We value questions that explore conceptual boundaries over those with simple factual answers. These standards foster the intellectual growth that defines our academic community.",
            "Athletes in our training program should prioritize proper technique over immediate performance gains. Everyone is expected to maintain complete training logs rather than relying on memory. Coaches and experienced athletes should model a balance between pushing limits and respecting recovery needs. These expectations create an environment where sustainable excellence can flourish.",
            "At this hospital, staff should document patient interactions clearly enough that any team member can understand the situation. We expect everyone to acknowledge knowledge gaps rather than making assumptions. All personnel should verify critical information directly rather than relying on secondhand reports. These standards protect both patients and practitioners while fostering a culture of continuous improvement."
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
            "Research scientists who thoroughly document their methodologies tend to receive more collaboration invitations and citation mentions. Those who take shortcuts in their protocols or documentation often find their work questioned or overlooked in literature reviews. I've watched how Dr. Kim's meticulous attention to reproducibility has led to her methods being adopted across multiple laboratories.",
            "Customer service representatives who take time to truly understand customer needs before suggesting solutions receive significantly higher satisfaction ratings and more personal requests from returning customers. Those who rush to close tickets quickly often generate repeat calls and declining feedback scores. Notice how clients specifically ask for Michael when they have complex issues because of his thorough approach.",
            "Students who consistently contribute thoughtful, well-prepared comments in seminars receive more detailed feedback on their written work from professors. Those who speak without clear preparation tend to get more generalized responses. I've observed how professors invest extra time mentoring students like Alicia who demonstrate consistent intellectual engagement through careful preparation.",
            "Architects who thoroughly research environmental and community factors before finalizing designs tend to win more competitive bids and referrals. Those who prioritize aesthetic appeal without considering practical implementation often face costly revisions and damaged relationships with contractors. The reputation Tim has built through his comprehensive approach has clients waiting months for his availability."
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
            "As engineers in this company, we take pride in documenting our code thoroughly rather than just making quick fixes. When I'm deciding how to approach a challenging bug, I think about our team's reputation for maintainable solutions, and that guides my choices even when deadlines are tight.",
            "Being part of this academic community means embracing intellectual curiosity and methodical investigation. When faced with complex research questions, I remember our shared commitment to rigorous methods over expedient conclusions. This identity as careful scholars influences how I approach even routine tasks.",
            "What connects us as craftspeople in this workshop is our dedication to mastering traditional techniques while finding our personal expression. The satisfaction of upholding these shared values motivates me through tedious practice sessions. When I'm tempted to take shortcuts, I remember that's not who we are as a guild.",
            "Our team's identity is built around our commitment to user-centered design processes. This shared value shapes how we evaluate our work—not just by whether it functions correctly, but by how well it serves real people's needs. Being part of a group that prioritizes empathetic design influences my approach to every project."
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
            "Remember last month when you solved that database optimization problem everyone was stuck on? You worked through each component methodically until you found the bottleneck. That success wasn't luck—it was evidence of your analytical skills. Those same abilities will help you tackle this new challenge.",
            "You've already mastered three programming languages through consistent practice and application. Each time you thought the learning curve was too steep, you broke it down into manageable parts and persisted. Your track record of learning technical skills through dedication is concrete evidence you can handle this new framework too.",
            "Think about how you navigated that complex negotiation last quarter. You prepared thoroughly, anticipated objections, and adapted your approach as new information emerged. That successful outcome wasn't random—it demonstrated your strategic thinking. Those same capabilities will serve you well in this upcoming client meeting.",
            "Your portfolio shows a clear progression from basic designs to increasingly complex projects, each building on skills you developed through deliberate practice. The quality improvement in your work over time isn't coincidental—it reflects your ability to learn from each project and apply those insights to new challenges."
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
            "Watch how Eliza approaches these complex design problems. She starts by sketching multiple rough concepts before committing to one direction. Even when she encounters technical limitations, she systematically works through each constraint rather than abandoning her vision. Seeing her methodical process has completely changed how I approach my own creative challenges.",
            "My colleague Marco had never used this statistical software before joining our team last year. He spent time observing how our senior analysts structured their queries and organized their data pipelines. Within six months, he was implementing these same techniques in his own analyses. Watching his rapid progress showed me that these skills are definitely learnable with the right approach.",
            "Remember how Dr. Chen demonstrated that surgical technique last month? She broke down each movement into clear steps, explaining her decision-making throughout. Several residents who observed her have already successfully incorporated her approach into their procedures. Seeing their successful application of her methods makes me confident I can master this technique too.",
            "My sister struggled with public speaking just like you do, but she found a way through it. She joined a speech club where she could watch others progress from nervous beginners to confident presenters. Seeing people with similar anxiety gradually build their skills through regular practice showed her a clear pathway to improvement. Now she mentors new members using the same step-by-step approach that worked for her."
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
            "The way you analyzed that complex data set showed remarkable attention to detail and pattern recognition. Your methodical approach to validating findings before drawing conclusions demonstrates exactly the kind of careful thinking this project needs. I've seen how quickly you pick up new analytical methods, which makes me confident you'll excel with this new visualization challenge.",
            "Your presentations always connect technical concepts to practical applications so effectively. You have a gift for making complex ideas accessible without oversimplifying them. The questions you ask reveal deep understanding of underlying principles. These communication strengths will make you particularly effective in the cross-functional role we discussed.",
            "I've noticed how thoroughly you test your code before submitting it for review, which shows real commitment to quality. Your systematic approach to breaking down problems reflects the kind of thinking needed for architecture-level work. Based on how you've handled increasing complexity in recent projects, I believe you're ready for more advanced responsibilities.",
            "The thoughtful questions you ask during discussions show you're already thinking at a strategic level. You have a natural ability to consider both technical constraints and business needs when proposing solutions. Your consistent follow-through on commitments demonstrates the reliability this leadership position requires."
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
            "Pay attention to that feeling of mental clarity you experience after working through a complex problem step by step. That sense of intellectual sharpness is telling you something important about how meaningful challenges affect your cognitive state. This positive mental energy becomes a resource you can draw on when facing future obstacles.",
            "Notice the distinctive satisfaction that comes after expressing an idea precisely, especially when you've taken time to refine your thinking. That internal sense of clarity feels qualitatively different from the temporary relief of just completing a task. These emotional rewards guide us toward the kinds of deep engagement that foster genuine growth.",
            "There's a unique feeling of confidence that emerges when you've mastered something that initially seemed beyond your capabilities. This isn't just momentary happiness but a fundamental shift in how you perceive challenges. Each time you experience this earned confidence, it becomes easier to approach new difficult situations with optimism.",
            "The calm centeredness you feel when fully engaged in challenging work—what some call 'flow'—signals an optimal learning state. This feeling of absorbed focus, when you're neither bored nor overwhelmed, indicates you're working at the edge of your capabilities where the most growth happens. Learning to recognize and cultivate this state can transform how you approach complex tasks."
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