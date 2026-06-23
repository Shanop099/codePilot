from pathlib import Path


class ReportGenerator:

    @staticmethod
    def export_report(
        title,
        content
    ):

        reports_dir = Path(
            "reports"
        )

        reports_dir.mkdir(
            exist_ok=True
        )

        filename = (
            title.lower()
            .replace(
                " ",
                "_"
            )
            + ".md"
        )

        file_path = (
            reports_dir
            / filename
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return str(
            file_path
        )