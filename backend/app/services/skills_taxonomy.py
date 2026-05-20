"""Curated technology and professional skills for extraction and matching."""

# Grouped skills for gap analysis and keyword optimization
SKILL_CATEGORIES: dict[str, list[str]] = {
    "languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
        "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "sql", "html", "css",
    ],
    "frameworks": [
        "react", "angular", "vue", "next.js", "node.js", "express", "django", "flask",
        "fastapi", "spring", "spring boot", ".net", "laravel", "rails", "tensorflow",
        "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform",
        "ansible", "jenkins", "ci/cd", "github actions", "linux", "nginx", "helm",
    ],
    "databases": [
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "dynamodb",
        "sqlite", "oracle", "cassandra", "snowflake", "bigquery",
    ],
    "tools": [
        "git", "jira", "confluence", "figma", "postman", "swagger", "rest api",
        "graphql", "microservices", "agile", "scrum", "kanban",
    ],
    "data_ai": [
        "machine learning", "deep learning", "nlp", "computer vision", "data analysis",
        "data engineering", "etl", "apache spark", "hadoop", "tableau", "power bi",
        "llm", "rag", "generative ai", "bert", "transformers",
    ],
    "soft_skills": [
        "leadership", "communication", "problem solving", "teamwork", "project management",
        "critical thinking", "collaboration", "mentoring", "presentation",
    ],
}

ALL_SKILLS: list[str] = []
for skills in SKILL_CATEGORIES.values():
    ALL_SKILLS.extend(skills)

# Normalized lookup: lowercase -> canonical display form
SKILL_LOOKUP: dict[str, str] = {s.lower(): s for s in ALL_SKILLS}
