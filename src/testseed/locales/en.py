"""Neutral English base locale."""

from __future__ import annotations

from testseed.locales._base import LocaleData

LOCALE = LocaleData(
    code="en",
    name="English (neutral)",
    first_names=(
        "Olivia", "Emma", "Ava", "Sophia", "Mia", "Amelia", "Harper", "Evelyn",
        "Abigail", "Emily", "Ella", "Grace", "Chloe", "Nora", "Lily", "Zoe",
        "Hannah", "Leah", "Ruby", "Alice", "Liam", "Noah", "Oliver", "James",
        "Elijah", "William", "Henry", "Lucas", "Benjamin", "Theodore", "Jack",
        "Leo", "Samuel", "Daniel", "Owen", "Ethan", "Isaac", "Caleb", "Nathan",
        "Adam",
    ),
    last_names=(
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis",
        "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Martin", "Jackson",
        "Thompson", "White", "Harris", "Clark", "Lewis", "Walker", "Hall",
        "Allen", "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams",
        "Nelson",
    ),
    surnames_per_person=1,
    email_domains=("example.test", "mail.test", "inbox.test"),
)  # fmt: skip
