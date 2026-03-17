"""Domain definitions for AI capabilities and human edges."""

from typing import Dict, List, NamedTuple


class DomainCapability(NamedTuple):
    """Represents a capability domain with strength rating."""
    name: str
    strength: int  # 0-10 scale
    description: str
    examples: List[str]


# AI capability domains with strength ratings (0-10)
AI_CAPABILITIES: Dict[str, DomainCapability] = {
    "coding": DomainCapability(
        name="Coding & Programming",
        strength=9,
        description="Writing code, debugging, refactoring across multiple languages",
        examples=["Python scripts", "API development", "Algorithm implementation"]
    ),
    "translation": DomainCapability(
        name="Language Translation",
        strength=8,
        description="Translating between languages with high accuracy",
        examples=["Document translation", "Multilingual content", "Localization"]
    ),
    "summarization": DomainCapability(
        name="Text Summarization",
        strength=9,
        description="Condensing long-form content into concise summaries",
        examples=["Article summaries", "Meeting notes", "Research abstracts"]
    ),
    "math": DomainCapability(
        name="Mathematical Computation",
        strength=10,
        description="Solving mathematical problems and performing calculations",
        examples=["Calculus", "Linear algebra", "Statistical analysis"]
    ),
    "data_analysis": DomainCapability(
        name="Data Analysis",
        strength=8,
        description="Analyzing structured data and identifying patterns",
        examples=["CSV analysis", "Statistical insights", "Trend detection"]
    ),
    "image_recognition": DomainCapability(
        name="Image Recognition",
        strength=9,
        description="Identifying objects, scenes, and patterns in images",
        examples=["Object detection", "Scene classification", "OCR"]
    ),
    "writing": DomainCapability(
        name="Content Writing",
        strength=7,
        description="Generating various forms of written content",
        examples=["Blog posts", "Technical documentation", "Marketing copy"]
    ),
    "information_retrieval": DomainCapability(
        name="Information Retrieval",
        strength=8,
        description="Finding and organizing information from large datasets",
        examples=["Research", "Fact-checking", "Knowledge synthesis"]
    ),
    "pattern_recognition": DomainCapability(
        name="Pattern Recognition",
        strength=9,
        description="Identifying patterns in data and text",
        examples=["Anomaly detection", "Trend analysis", "Classification"]
    ),
    "grammar_correction": DomainCapability(
        name="Grammar & Spelling",
        strength=10,
        description="Correcting grammar, spelling, and syntax errors",
        examples=["Proofreading", "Style consistency", "Language rules"]
    ),
}


# Human edge domains where humans typically excel
HUMAN_EDGE_DOMAINS: Dict[str, DomainCapability] = {
    "physical_experience": DomainCapability(
        name="Physical World Experience",
        strength=10,
        description="Understanding gained from direct physical interaction with the world",
        examples=["Craftsmanship", "Sports coaching", "Hands-on repair work"]
    ),
    "emotional_intelligence": DomainCapability(
        name="Emotional Intelligence",
        strength=10,
        description="Understanding and responding to human emotions authentically",
        examples=["Counseling", "Conflict resolution", "Empathetic communication"]
    ),
    "cultural_context": DomainCapability(
        name="Deep Cultural Context",
        strength=9,
        description="Understanding nuanced cultural contexts from lived experience",
        examples=["Local customs", "Unwritten social rules", "Cultural storytelling"]
    ),
    "tacit_knowledge": DomainCapability(
        name="Tacit Knowledge",
        strength=10,
        description="Knowledge that's difficult to transfer through words alone",
        examples=["Expert intuition", "Apprenticeship skills", "Professional judgment"]
    ),
    "ethical_judgment": DomainCapability(
        name="Ethical Judgment",
        strength=9,
        description="Making complex ethical decisions with moral responsibility",
        examples=["Medical ethics", "Legal judgment", "Moral philosophy"]
    ),
    "creative_intuition": DomainCapability(
        name="Creative Intuition",
        strength=8,
        description="Original creative thinking based on unique experiences",
        examples=["Artistic vision", "Novel problem-solving", "Innovative design"]
    ),
    "real_time_adaptation": DomainCapability(
        name="Real-Time Adaptation",
        strength=9,
        description="Adapting to rapidly changing physical situations",
        examples=["Emergency response", "Live performance", "Crisis management"]
    ),
    "relationship_building": DomainCapability(
        name="Relationship Building",
        strength=10,
        description="Forming and maintaining authentic human connections",
        examples=["Networking", "Mentorship", "Community building"]
    ),
    "sensory_experience": DomainCapability(
        name="Sensory Experience",
        strength=10,
        description="Knowledge from taste, touch, smell, and physical sensation",
        examples=["Culinary arts", "Perfumery", "Textile design"]
    ),
    "contextual_memory": DomainCapability(
        name="Contextual Memory",
        strength=9,
        description="Rich memories tied to personal experiences and emotions",
        examples=["Historical witness", "Personal narrative", "Oral history"]
    ),
    "improvisation": DomainCapability(
        name="Improvisation",
        strength=8,
        description="Creative adaptation in unpredictable situations",
        examples=["Comedy improvisation", "Jazz performance", "Field problem-solving"]
    ),
    "personal_authenticity": DomainCapability(
        name="Personal Authenticity",
        strength=10,
        description="Expressing genuine personal voice and perspective",
        examples=["Memoir writing", "Personal branding", "Unique artistic style"]
    ),
}


# Hybrid domains where both AI and humans have significant capabilities
HYBRID_DOMAINS: Dict[str, Dict[str, int]] = {
    "research": {"ai_strength": 7, "human_strength": 8},
    "teaching": {"ai_strength": 6, "human_strength": 9},
    "customer_service": {"ai_strength": 6, "human_strength": 8},
    "content_creation": {"ai_strength": 7, "human_strength": 8},
    "strategic_planning": {"ai_strength": 5, "human_strength": 9},
    "diagnosis": {"ai_strength": 7, "human_strength": 8},
    "design": {"ai_strength": 6, "human_strength": 9},
    "music_composition": {"ai_strength": 6, "human_strength": 8},
}


def get_ai_capability(skill: str) -> int:
    """
    Estimate AI capability for a given skill.

    Args:
        skill: The skill to evaluate

    Returns:
        AI strength rating (0-10)
    """
    skill_lower = skill.lower()

    # Check exact matches first
    for key, capability in AI_CAPABILITIES.items():
        if key in skill_lower or skill_lower in capability.name.lower():
            return capability.strength

    # Check for keywords in examples
    for capability in AI_CAPABILITIES.values():
        for example in capability.examples:
            if example.lower() in skill_lower or skill_lower in example.lower():
                return capability.strength

    # Check hybrid domains
    for domain, strengths in HYBRID_DOMAINS.items():
        if domain in skill_lower:
            return strengths["ai_strength"]

    # Default: moderate AI capability
    return 5


def get_human_edge_score(skill: str) -> int:
    """
    Estimate human edge for a given skill.

    Args:
        skill: The skill to evaluate

    Returns:
        Human edge strength rating (0-10)
    """
    skill_lower = skill.lower()

    # Check exact matches first
    for key, capability in HUMAN_EDGE_DOMAINS.items():
        if key in skill_lower or skill_lower in capability.name.lower():
            return capability.strength

    # Check for keywords in examples
    for capability in HUMAN_EDGE_DOMAINS.values():
        for example in capability.examples:
            if example.lower() in skill_lower or skill_lower in example.lower():
                return capability.strength

    # Check hybrid domains
    for domain, strengths in HYBRID_DOMAINS.items():
        if domain in skill_lower:
            return strengths["human_strength"]

    # Default: moderate human edge
    return 6
