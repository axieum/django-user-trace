from __future__ import annotations

import re
from datetime import date

import mkdocs_gen_files

# A mapping of commit section titles to their new titles
RENAME_SCOPE_HEADINGS: dict[str, str] = {
    # "⚠ BREAKING CHANGES": ":octicons-alert-fill-24: BREAKING CHANGES",
    "Bug Fixes": ":octicons-bug-24: Bug Fixes",
    "Build System": ":octicons-tools-24: Build System",
    "Code Refactoring": ":octicons-iterations-24: Code Refactoring",
    "Continuous Integration": ":octicons-gear-24: Continuous Integration",
    "Dependencies": ":octicons-package-24: Dependencies",
    "Documentation": ":octicons-repo-24: Documentation",
    "Features": ":octicons-rocket-24: Features",
    "Miscellaneous Chores": ":octicons-checklist-24: Miscellaneous Chores",
    "Performance Improvements": ":octicons-zap-24: Performance Improvements",
    "Reverts": ":octicons-history-24: Reverts",
    "Styles": ":octicons-flame-24: Styles",
    "Tests": ":octicons-beaker-24: Tests",
}

# Open the destination markdown file, and read each line of the original `CHANGELOG.md` file
with mkdocs_gen_files.open("changelog/index.md", "a") as md, open("CHANGELOG.md", encoding="utf8") as file:
    admonition_active: bool = False
    for line in file.readlines():
        # Format H2 versions, e.g. ## [1.0.0](...) (2023-02-19)
        if match := re.match(r"## \[(?P<version>.+?)]\((?P<url>.+?)\) \((?P<date>[\d-]+?)\)", line):
            version: str = match.group("version")
            url: str = match.group("url")
            dt = date.fromisoformat(match.group("date")).strftime("%B %d, %Y")
            line = f'## [{version}]({url}) <small>{dt}</small> {{ #{version} data-toc-label="{version}" }}\n'

        # Format H3 commit sections, e.g. ### Features
        elif match := re.match(r"### (?P<scope>[^\n]+)", line):
            scope: str = RENAME_SCOPE_HEADINGS.get(match.group("scope"), match.group("scope"))
            line = f"**{scope}**\n"

        # Format breaking changes
        if "BREAKING CHANGES" in line.upper():
            md.write('!!! danger "Breaking Changes"\n')
            admonition_active = True
            continue

        # Apply admonition indentation
        if admonition_active and not line.startswith("**") and not line.startswith("#"):
            md.write("\t")
        else:
            admonition_active = False

        # Finally, write the line
        md.write(line)
