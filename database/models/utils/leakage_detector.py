import re


PATTERNS = {

    "Email Address":
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    "Phone Number":
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",

    "Credit Card-like Number":
        r"\b(?:\d[ -]*?){13,19}\b",

    "API Key":
        r"\b(?:api[_-]?key|secret[_-]?key)\s*[:=]\s*[A-Za-z0-9_\-]{8,}\b",

    "Password":
        r"\b(?:password|passwd|pwd)\s*[:=]\s*\S+\b"
}


def detect_sensitive_data(text):

    detected = []

    for data_type, pattern in PATTERNS.items():

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        if matches:

            detected.append({
                "type": data_type,
                "count": len(matches)
            })

    return detected


def calculate_risk(detected_data):

    total = sum(
        item["count"]
        for item in detected_data
    )

    if total == 0:
        return "LOW"

    if total <= 2:
        return "MEDIUM"

    return "HIGH"


def generate_recommendations(detected_data):

    if not detected_data:

        return [
            "No obvious sensitive information was detected.",
            "Continue following data-minimization practices."
        ]

    recommendations = [

        "Remove sensitive information before sharing the data."

    ]

    for item in detected_data:

        if item["type"] == "Email Address":

            recommendations.append(
                "Avoid exposing personal email addresses."
            )

        elif item["type"] == "Phone Number":

            recommendations.append(
                "Avoid exposing personal phone numbers."
            )

        elif item["type"] == "Credit Card-like Number":

            recommendations.append(
                "Never expose payment-card information."
            )

        elif item["type"] == "API Key":

            recommendations.append(
                "Move API secrets into protected environment variables."
            )

        elif item["type"] == "Password":

            recommendations.append(
                "Never share passwords in plain text."
            )

    return recommendations
