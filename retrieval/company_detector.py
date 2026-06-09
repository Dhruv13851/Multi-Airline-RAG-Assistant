COMPANIES = [
    "Air India",
    "Emirates",
    "Spicejet",
    "Gofirst"
]


def detect_company(query: str) -> str | None:

    query_lower = query.lower()

    for company in COMPANIES:
        if company.lower() in query_lower:
            return company

    return None