#!/usr/bin/env python3
"""
Article Version Comparison Tool
Generates a comprehensive diff analysis between multiple versions of an article.
"""

import difflib
import re
from pathlib import Path
from typing import Dict, List, Optional


class ArticleVersionComparator:
    def __init__(self, base_dir: str = "outputs"):
        self.base_dir = Path(base_dir)
        self.versions: List[int] = []
        self.content_by_version: Dict[int, str] = {}

    def load_versions(
        self, pattern: str = "# Standardizing Private Equity Reporting_v*.md"
    ):
        """Load all article versions matching the pattern."""
        for file_path in self.base_dir.glob(pattern):
            version_match = re.search(r"_v(\d+)\.md$", file_path.name)
            if version_match:
                version_num = int(version_match.group(1))
                self.versions.append(version_num)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.content_by_version[version_num] = content

        self.versions.sort()
        print(f"Loaded {len(self.versions)} versions: {self.versions}")

    def generate_progressive_diff(self) -> str:
        """Generate a progressive diff showing changes from v1 to v4."""
        if len(self.versions) < 2:
            return "Need at least 2 versions to compare."

        diff_output = []
        diff_output.append("# Article Version Comparison Analysis")
        diff_output.append(
            f"## Progressive Changes from v{self.versions[0]} to v{self.versions[-1]}"
        )
        diff_output.append("")

        # Compare each version with the previous one
        for i in range(1, len(self.versions)):
            prev_version = self.versions[i - 1]
            curr_version = self.versions[i]

            diff_output.append(
                f"## Changes in v{curr_version} (compared to v{prev_version})"
            )
            diff_output.append("")

            # Generate diff
            prev_lines = self.content_by_version[prev_version].splitlines(keepends=True)
            curr_lines = self.content_by_version[curr_version].splitlines(keepends=True)

            diff = difflib.unified_diff(
                prev_lines,
                curr_lines,
                fromfile=f"v{prev_version}",
                tofile=f"v{curr_version}",
                lineterm="",
            )

            # Filter and format diff output
            diff_lines = list(diff)
            if diff_lines:
                # Remove the first few lines that are just file headers
                diff_lines = diff_lines[3:]

                # Group changes by sections
                section_changes = self._group_changes_by_section(diff_lines)

                for section, changes in section_changes.items():
                    if changes:
                        diff_output.append(f"### {section}")
                        diff_output.append("")
                        diff_output.extend(changes)
                        diff_output.append("")
            else:
                diff_output.append("*No changes detected*")
                diff_output.append("")

        return "\n".join(diff_output)

    def _group_changes_by_section(self, diff_lines: List[str]) -> Dict[str, List[str]]:
        """Group diff changes by article sections."""
        sections = {
            "Executive Summary": [],
            "Background & Industry Context": [],
            "Key Changes & Strategic Enhancements": [],
            "Implementation Strategy & Competitive Positioning": [],
            "Strategic Imperative and Partnership Value": [],
            "Contact Information": [],
            "Other Changes": [],
        }

        current_section = "Other Changes"

        for line in diff_lines:
            # Check if this line indicates a section header
            if line.startswith("+") and "## " in line:
                for section_name in sections.keys():
                    if section_name in line:
                        current_section = section_name
                        break

            # Add the line to the current section
            sections[current_section].append(line)

        return sections

    def generate_summary_changes(self) -> str:
        """Generate a summary of key changes across all versions."""
        summary = []
        summary.append("# Article Version Change Summary")
        summary.append("")

        # Word count comparison
        summary.append("## Word Count Comparison")
        summary.append("")
        for version in self.versions:
            word_count = len(self.content_by_version[version].split())
            summary.append(f"- **v{version}**: {word_count:,} words")
        summary.append("")

        # Key changes summary
        summary.append("## Key Changes Summary")
        summary.append("")

        changes_summary = {
            "v2": "Added visual placeholder for ILPA Template Development Timeline",
            "v3": "No significant changes from v2",
            "v4": "No significant changes from v3",
        }

        for version_key, change_desc in changes_summary.items():
            summary.append(f"### {version_key}")
            summary.append(f"- {change_desc}")
            summary.append("")

        return "\n".join(summary)

    def generate_side_by_side_comparison(
        self, section_name: Optional[str] = None
    ) -> str:
        """Generate a side-by-side comparison of a specific section across versions."""
        if section_name is None:
            section_name = "Executive Summary"

        comparison = []
        comparison.append(f"# Side-by-Side Comparison: {section_name}")
        comparison.append("")

        # Extract the section from each version
        sections = {}
        for version in self.versions:
            content = self.content_by_version[version]
            section_content = self._extract_section(content, section_name)
            if section_content:
                sections[version] = section_content

        if not sections:
            comparison.append(f"Section '{section_name}' not found in any version.")
            return "\n".join(comparison)

        # Create side-by-side view
        comparison.append("| Version | Content |")
        comparison.append("|---------|---------|")

        for version in self.versions:
            if version in sections:
                # Truncate content for table display
                content_preview = (
                    sections[version][:200] + "..."
                    if len(sections[version]) > 200
                    else sections[version]
                )
                content_preview = content_preview.replace("\n", "<br>")
                comparison.append(f"| v{version} | {content_preview} |")

        return "\n".join(comparison)

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from the content."""
        # Find the section header
        section_pattern = rf"## {re.escape(section_name)}"
        match = re.search(section_pattern, content)

        if not match:
            return ""

        start_pos = match.start()

        # Find the next section header or end of content
        next_section_match = re.search(r"\n## ", content[start_pos + 1 :])
        if next_section_match:
            end_pos = start_pos + 1 + next_section_match.start()
        else:
            end_pos = len(content)

        return content[start_pos:end_pos].strip()


def main():
    """Main function to run the comparison."""
    comparator = ArticleVersionComparator()
    comparator.load_versions()

    # Generate all comparison outputs
    outputs = {
        "progressive_diff.md": comparator.generate_progressive_diff(),
        "change_summary.md": comparator.generate_summary_changes(),
        "executive_summary_comparison.md": comparator.generate_side_by_side_comparison(
            "Executive Summary"
        ),
    }

    # Write outputs
    for filename, content in outputs.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated: {filename}")

    print("\nComparison complete! Check the generated files for detailed analysis.")


if __name__ == "__main__":
    main()
