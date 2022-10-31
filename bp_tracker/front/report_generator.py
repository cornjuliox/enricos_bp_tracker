from pathlib import Path
from jinja2 import (
    Environment,
    PackageLoader,
    Template,
    select_autoescape,
)

env: Environment = Environment(
    loader=PackageLoader("bp_tracker"),
    autoescape=select_autoescape()
)

def generate_report(
    env: Environment,
    ready_rows: list[dict],
    template_name: str="report.html",
    output_name: str="output.html",
):
    # NOTE: Should cwd be passed in or hardcoded? IDK right now.
    cwd: Path = Path().absolute()
    report_template: Template = env.get_template(template_name)
    output: str = report_template.render(rows=ready_rows)

    absolute_path: Path = cwd / output_name

    with absolute_path.open("w") as F:
        F.write(output)
