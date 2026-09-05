def predict_persona(text):

    text_lower = text.lower()

    scores = {
        "Student": 0,
        "Professional": 0,
        "Business User": 0,
        "Technology User": 0,
        "General User": 0
    }

    student_words = [
        "college",
        "university",
        "student",
        "exam",
        "assignment",
        "semester",
        "class",
        "professor",
        "study"
    ]

    professional_words = [
        "office",
        "employee",
        "job",
        "meeting",
        "company",
        "project",
        "manager",
        "work"
    ]

    business_words = [
        "business",
        "customer",
        "sales",
        "marketing",
        "startup",
        "client",
        "product",
        "revenue"
    ]

    technology_words = [
        "python",
        "programming",
        "software",
        "developer",
        "coding",
        "database",
        "github",
        "api",
        "computer"
    ]

    for word in student_words:

        if word in text_lower:
            scores["Student"] += 1

    for word in professional_words:

        if word in text_lower:
            scores["Professional"] += 1

    for word in business_words:

        if word in text_lower:
            scores["Business User"] += 1

    for word in technology_words:

        if word in text_lower:
            scores["Technology User"] += 1

    if max(scores.values()) == 0:

        return "General User"

    return max(scores, key=scores.get)
