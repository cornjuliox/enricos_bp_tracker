from pathlib import Path

import arrow
from jinja2 import (
    Environment,
    PackageLoader,
    Template,
    select_autoescape,
)

class ReportGenerator():
    def __init__(self):
        # NOTE: should package name be hardcoded?
        # NOTE: I don't see why not, at least not for now.
        self.env = Environment(
            loader=PackageLoader("bp_tracker"),
            autoescape=select_autoescape()
        )

    def generate_report(
        self,
        ready_rows: list[dict],
        template_name: str = "report.html",
        output_name: str = None
    ) -> str:
        template: Template = self.env.get_template(template_name)
        if not output_name:
            today: str = arrow.now().format("YYYY_MM_DD_HH_MM")
            output_name = "{}.html".format(today)

        hydrated_template: str = template.render(rows=ready_rows)
        return hydrated_template
