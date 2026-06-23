class MultiReviewAgent:

    def __init__(
        self,
        architecture_agent,
        dependency_agent,
        impact_agent,
        repository_review_agent
    ):

        self.architecture_agent = (
            architecture_agent
        )

        self.dependency_agent = (
            dependency_agent
        )

        self.impact_agent = (
            impact_agent
        )

        self.repository_review_agent = (
            repository_review_agent
        )

    def review(
        self,
        symbol_name,
        file_content
    ):

        architecture = (
            self.architecture_agent.explain(
                symbol_name,
                file_content
            )
        )

        dependencies = (
            self.dependency_agent.analyze(
                symbol_name
            )
        )

        impact = (
            self.impact_agent.analyze(
                symbol_name
            )
        )

        review = (
            self.repository_review_agent.review(
                symbol_name,
                file_content
            )
        )

        combined = f"""
REPOSITORY REVIEW REPORT

================================================

TARGET

{symbol_name}

================================================

ARCHITECTURE

{architecture}

================================================

DEPENDENCIES

{dependencies}

================================================

IMPACT ANALYSIS

{impact}

================================================

CODE REVIEW

{review}
"""

        return combined