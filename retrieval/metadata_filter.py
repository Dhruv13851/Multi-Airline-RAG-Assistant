def build_filter(company: str | None = None):
    """
    Convert extracted entities into vector DB filters.
    """

    filters = {}

    if company:
        filters["company"] = company

    return filters if filters else None