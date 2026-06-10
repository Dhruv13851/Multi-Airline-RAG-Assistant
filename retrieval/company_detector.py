from rapidfuzz import fuzz
from rapidfuzz import process


class CompanyDetector:

    COMPANIES = (
        "Air India",
        "Emirates",
        "Spicejet",
        "Gofirst"
    )

    MIN_CONFIDENCE = 55

    def detect(
        self,
        query: str
    ) -> str | None:
       
        # Fuzzy match
        match = process.extractOne(
            query,
            self.COMPANIES,
            scorer=fuzz.WRatio
        )

        if not match:
            return None

        company, score, _ = match

        if score >= self.MIN_CONFIDENCE:

            print(
                f"\nFuzzy Company Match: "
                f"{company} ({score})"
            )

            return company

        return None