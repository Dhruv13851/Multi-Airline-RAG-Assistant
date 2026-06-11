from rapidfuzz import fuzz


class CompanyDetector:

    COMPANIES = (
        "Air India",
        "Emirates",
        "Spicejet",
        "Gofirst"
    )

    MIN_CONFIDENCE = 70

    def detect_all(
        self,
        query: str
    ) -> list[str]:

        found = []

        query_lower = query.lower()

        for company in self.COMPANIES:

            score = fuzz.partial_ratio(
                company.lower(),
                query_lower
            )

            if score >= self.MIN_CONFIDENCE:

                found.append(company)

                print(
                    f"\nFuzzy Company Match: "
                    f"{company} ({score})"
                )

        return found