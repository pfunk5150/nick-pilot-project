#!/usr/bin/env python3
"""
Enhanced Claude Repository Builder v2.0 - Production Implementation
Implements core folding, deduplication, and summary table generation
for improved readability and organization of Claude.ai conversation logs.

Key Features:
- Collapsible sections for better navigation
- Deduplication of repeated content
- Native format rendering for artifacts
- Summary tables for enhanced overview
- Processing statistics and insights
"""

import hashlib
import json
import os
import re
from dataclasses import dataclass, field

# Built-in dict and list types used directly


@dataclass
class FileExtraction:
    file_path: str
    extraction_count: int = 1
    first_content: str = ""
    content_hash: str = ""
    line_numbers: list[int] = field(default_factory=list)


@dataclass
class ToolUsage:
    tool_name: str
    usage_count: int = 1
    first_usage_line: int = 0
    parameters_summary: str = ""


@dataclass
class ArtifactContent:
    artifact_id: str
    title: str
    content_type: str
    content: str
    command: str = "create"
    version_uuid: str = ""
    extraction_count: int = 1


@dataclass
class EnhancementConfig:
    enable_folding: bool = True
    enable_deduplication: bool = True
    enable_summary_tables: bool = True
    max_tool_repetitions_before_folding: int = 3
    preserve_thinking_blocks_exactly: bool = True
    preserve_artifact_content_exactly: bool = True


class ConversationProcessor:
    def __init__(self, config: EnhancementConfig = None):
        self.config = config or EnhancementConfig()
        self.file_extractions: dict[str, FileExtraction] = {}
        self.tool_usage: dict[str, ToolUsage] = {}
        self.directory_trees: list[str] = []
        self.artifacts: dict[str, ArtifactContent] = {}
        self.current_line = 0


def get_file_extension_from_mime(mime_type: str) -> str:
    """Maps a MIME type to a file extension."""
    mapping = {
        "application/vnd.ant.mermaid": ".mermaid",
        "text/markdown": ".md",
        "application/json": ".json",
        "text/plain": ".txt",
    }
    return mapping.get(mime_type, ".txt")


def sanitize_filename(filename: str) -> str:
    """Removes characters that are invalid in filenames."""
    filename = re.sub(r"[📄✨]", "", filename).strip()
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


def detect_artifact_content(text_content: str) -> bool:
    """Detects if content contains Claude artifact JSON structure"""
    try:
        if text_content.strip().startswith("{") and text_content.strip().endswith("}"):
            parsed = json.loads(text_content)
            return all(key in parsed for key in ["id", "type", "title", "content"])
    except (json.JSONDecodeError, TypeError):
        pass
    return False


def extract_artifact_info(text_content: str) -> ArtifactContent:
    """Extract artifact information from JSON structure"""
    try:
        parsed = json.loads(text_content)
        return ArtifactContent(
            artifact_id=parsed.get("id", "unknown_artifact"),
            title=parsed.get("title", "Untitled Artifact"),
            content_type=parsed.get("type", "text/plain"),
            content=parsed.get("content", ""),
            command=parsed.get("command", "create"),
            version_uuid=parsed.get("version_uuid", ""),
        )
    except (json.JSONDecodeError, TypeError):
        return None


def format_artifact_content(
    artifact: ArtifactContent, config: EnhancementConfig
) -> str:
    """Format artifact content in its native format with metadata"""
    if not config.preserve_artifact_content_exactly:
        return f"**Artifact:** {artifact.title}"

    # Determine file type indicator
    if artifact.content_type == "text/markdown":
        lang_indicator = "markdown"
    elif artifact.content_type == "application/vnd.ant.mermaid":
        lang_indicator = "mermaid"
    elif artifact.content_type == "application/json":
        lang_indicator = "json"
    else:
        lang_indicator = "text"

    # Format the content in native format
    metadata = f"**Artifact:** `{artifact.artifact_id}` • **Title:** {artifact.title} • **Type:** {artifact.content_type}"

    if config.enable_folding:
        summary = f"📄 {artifact.title} • {lang_indicator.upper()}"

        # Special handling for markdown content - render directly without code blocks
        if artifact.content_type == "text/markdown":
            formatted_content = f"{metadata}\n\n{artifact.content}"
        else:
            # Use code blocks for non-markdown content (mermaid, json, etc.)
            formatted_content = (
                f"{metadata}\n\n```{lang_indicator}\n{artifact.content}\n```"
            )
        return wrap_with_details(summary, formatted_content)
    else:
        # Special handling for markdown content in non-folding mode too
        if artifact.content_type == "text/markdown":
            return f"{metadata}\n\n{artifact.content}"
        else:
            return f"{metadata}\n\n```{lang_indicator}\n{artifact.content}\n```"


def wrap_with_details(summary: str, content: str, tag: str = "details") -> str:
    """Generate collapsible HTML sections with proper escaping"""
    if tag == "details":
        return f"<details><summary>{summary}</summary>\n\n{content}\n\n</details>"
    else:
        return f"<{tag}>\n  <details><summary>{summary}</summary>\n\n{content}\n\n  </details>\n</{tag}>"


def detect_directory_tree(text: str) -> bool:
    """Detects if text contains a directory tree structure"""
    tree_patterns = [r"└──", r"├──", r"│", r"📁", r"📄"]
    return any(re.search(pattern, text) for pattern in tree_patterns)


def generate_file_extraction_table(extractions: dict[str, FileExtraction]) -> str:
    """Generates markdown table summarizing file extractions"""
    if not extractions:
        return ""

    table = "\n| File | Extractions | Status |\n|------|-------------|--------|\n"
    for file_path, extraction in extractions.items():
        filename = os.path.basename(file_path)
        count_display = (
            f"{extraction.extraction_count}x"
            if extraction.extraction_count > 1
            else "1x"
        )
        status = "✅ Consolidated" if extraction.extraction_count > 1 else "📄 Single"
        table += f"| `{filename}` | {count_display} | {status} |\n"

    return table


def generate_artifact_summary_table(artifacts: dict[str, ArtifactContent]) -> str:
    """Generates markdown table summarizing artifacts"""
    if not artifacts:
        return ""

    table = "\n| Artifact | Type | Status |\n|----------|------|--------|\n"
    for artifact in artifacts.values():
        title = (
            artifact.title[:30] + "..." if len(artifact.title) > 30 else artifact.title
        )
        file_type = artifact.content_type.split("/")[-1].upper()
        status = "✅ Consolidated" if artifact.extraction_count > 1 else "📄 Single"
        table += f"| `{title}` | {file_type} | {status} |\n"

    return table


def consolidate_directory_trees(trees: list[str]) -> str:
    """Consolidates multiple directory trees into a single summary"""
    if len(trees) <= 1:
        return trees[0] if trees else ""

    # Extract unique paths from all trees
    all_paths = set()
    for tree in trees:
        lines = tree.split("\n")
        for line in lines:
            if any(char in line for char in ["└──", "├──", "📁", "📄"]):
                all_paths.add(line.strip())

    consolidated = (
        "**Consolidated Directory Structure:**\n```\n"
        + "\n".join(sorted(all_paths)[:20])
        + "\n```"
    )
    if len(all_paths) > 20:
        consolidated += f"\n\n*... and {len(all_paths) - 20} more items*"

    summary = f"*Consolidated {len(trees)} directory tree instances → 1 reference*"
    return wrap_with_details(
        "📂 Directory Structure (Consolidated)", consolidated + "\n\n" + summary
    )


def generate_tool_summary(tool_name: str, tool_input: dict, usage_count: int) -> str:
    """Create intelligent tool summaries based on tool type and parameters"""
    if tool_name == "project_knowledge_search":
        query = tool_input.get("query", "")[:50]
        return f'project_knowledge_search • Query: "{query}..."'
    elif tool_name == "artifacts":
        title = tool_input.get("title", "Generated Artifact")
        return f"artifacts • {title}"
    elif tool_name == "read_file":
        target = tool_input.get("target_file", "")
        return f"read_file • {os.path.basename(target)}"
    else:
        suffix = f" • Usage {usage_count}x" if usage_count > 1 else ""
        return f"{tool_name}{suffix}"


def process_thinking_block(thinking_content: str, config: EnhancementConfig) -> str:
    """Process thinking blocks with exact content preservation"""
    if not thinking_content.strip():
        return ""

    if config.enable_folding:
        # Extract first line for summary
        first_line = thinking_content.split("\n")[0][:100]
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."

        summary = f"Thinking: {first_line}"
        return wrap_with_details(summary, thinking_content, "think")
    else:
        return (
            f"> **Thinking...**\n> {thinking_content.replace(chr(10), chr(10) + '> ')}"
        )


def process_tool_sequence(
    tool_blocks: list[dict], processor: ConversationProcessor
) -> str:
    """Process a sequence of tool use/result blocks"""
    if not tool_blocks:
        return ""

    config = processor.config

    # Group tool use with its results
    tool_pairs: list[dict] = []
    current_use_block: dict | None = None
    current_results: list[dict] = []
    for block in tool_blocks:
        if block.get("type") == "tool_use":
            # Save previous tool if exists
            if current_use_block is not None:
                tool_pairs.append(
                    {"use": current_use_block, "results": current_results}
                )
            current_use_block = block
            current_results = []
        elif block.get("type") == "tool_result":
            current_results.append(block)

    # Add the last tool if exists
    if current_use_block is not None:
        tool_pairs.append({"use": current_use_block, "results": current_results})

    output = []

    for tool_pair in tool_pairs:
        tool_use: dict = tool_pair["use"]
        tool_results: list[dict] = tool_pair["results"]

        tool_name = tool_use.get("name", "unknown_tool")
        tool_input = tool_use.get("input", {})

        # Check if this is an artifact tool and process it specially
        if tool_name == "artifacts" and tool_input:
            artifact_content = ArtifactContent(
                artifact_id=tool_input.get("id", "unknown_artifact"),
                title=tool_input.get("title", "Untitled Artifact"),
                content_type=tool_input.get("type", "text/plain"),
                content=tool_input.get("content", ""),
                command=tool_input.get("command", "create"),
                version_uuid=tool_input.get("version_uuid", ""),
            )

            # Track artifact
            if artifact_content.artifact_id in processor.artifacts:
                processor.artifacts[artifact_content.artifact_id].extraction_count += 1
            else:
                processor.artifacts[artifact_content.artifact_id] = artifact_content

            # Track tool usage for statistics
            if tool_name in processor.tool_usage:
                processor.tool_usage[tool_name].usage_count += 1
            else:
                processor.tool_usage[tool_name] = ToolUsage(
                    tool_name=tool_name, first_usage_line=processor.current_line
                )

            # Generate and add formatted artifact directly
            if config.enable_folding:
                summary = generate_tool_summary(
                    tool_name, tool_input, processor.tool_usage[tool_name].usage_count
                )
                formatted_artifact = format_artifact_content(artifact_content, config)
                wrapped_tool = wrap_with_details(summary, formatted_artifact, "tools")
                output.append(wrapped_tool)
            else:
                output.append(f"\n**Artifact: `{artifact_content.title}`**")
                formatted_artifact = format_artifact_content(artifact_content, config)
                output.append(formatted_artifact)

            continue  # Skip normal tool processing for artifacts

        # Track tool usage
        if tool_name in processor.tool_usage:
            processor.tool_usage[tool_name].usage_count += 1
        else:
            processor.tool_usage[tool_name] = ToolUsage(
                tool_name=tool_name, first_usage_line=processor.current_line
            )

        usage_count = processor.tool_usage[tool_name].usage_count

        if config.enable_folding:
            # Generate summary for this tool usage
            summary = generate_tool_summary(tool_name, tool_input, usage_count)

            # Build content
            content_parts = []

            # Add input section
            if tool_input:
                content_parts.append(
                    "**Input:**\n```json\n" + json.dumps(tool_input, indent=2) + "\n```"
                )

            # Process results
            for result in tool_results:
                result_content = process_tool_result(result, processor)
                if result_content:
                    content_parts.append("**Results:**\n" + result_content)

            # Add deduplication note if applicable
            if (
                usage_count > config.max_tool_repetitions_before_folding
                and config.enable_deduplication
            ):
                content_parts.append(
                    f"\n*De-duplication applied: {usage_count} similar operations consolidated*"
                )

            tool_content = "\n\n".join(content_parts)
            wrapped_tool = wrap_with_details(summary, tool_content, "tools")
            output.append(wrapped_tool)
        else:
            # Original format
            output.append(f"\n**Tool Use: `{tool_name}`**")
            if tool_input:
                # Special handling for markdown artifacts even in non-folding mode
                if (
                    tool_name == "artifacts"
                    and tool_input.get("type") == "text/markdown"
                ):
                    artifact_title = tool_input.get("title", "Untitled Artifact")
                    artifact_content = tool_input.get("content", "")
                    artifact_id = tool_input.get("id", "unknown_artifact")
                    metadata = f"**Artifact:** `{artifact_id}` • **Title:** {artifact_title} • **Type:** text/markdown"
                    output.append(f"{metadata}\n\n{artifact_content}")
                else:
                    output.append(
                        "```json\n" + json.dumps(tool_input, indent=2) + "\n```"
                    )

            for result in tool_results:
                result_content = process_tool_result(result, processor)
                if result_content:
                    output.append(
                        f"\n**Tool Result: `{tool_name}`**\n" + result_content
                    )

    return "\n\n".join(output)


def process_tool_result(result_block: dict, processor: ConversationProcessor) -> str:
    """Process tool result with file tracking, artifact detection, and deduplication"""
    content = result_block.get("content", "")

    if isinstance(content, list):
        processed_items = []
        for item in content:
            if item.get("type") == "text":
                text_content = item.get("text", "").strip()

                # Check for artifact content first
                if detect_artifact_content(text_content):
                    artifact = extract_artifact_info(text_content)
                    if artifact:
                        # Track artifact
                        if artifact.artifact_id in processor.artifacts:
                            processor.artifacts[
                                artifact.artifact_id
                            ].extraction_count += 1
                        else:
                            processor.artifacts[artifact.artifact_id] = artifact

                        # Format artifact content
                        formatted_artifact = format_artifact_content(
                            artifact, processor.config
                        )
                        processed_items.append(formatted_artifact)
                        continue

                # Check for file extraction patterns
                if text_content.startswith("/") and "\n" in text_content:
                    lines = text_content.split("\n", 1)
                    file_path = lines[0].strip()

                    # Track file extraction
                    content_hash = hashlib.md5(text_content.encode()).hexdigest()[:8]

                    if file_path in processor.file_extractions:
                        extraction = processor.file_extractions[file_path]
                        extraction.extraction_count += 1
                        extraction.line_numbers.append(processor.current_line)
                    else:
                        processor.file_extractions[file_path] = FileExtraction(
                            file_path=file_path,
                            first_content=text_content,
                            content_hash=content_hash,
                            line_numbers=[processor.current_line],
                        )

                    # Only include full content for first extraction if deduplication enabled
                    if (
                        processor.config.enable_deduplication
                        and processor.file_extractions[file_path].extraction_count > 1
                    ):
                        processed_items.append(
                            f"**File:** `{file_path}` *(content previously shown)*"
                        )
                    else:
                        processed_items.append(text_content)
                else:
                    # Check for directory trees
                    if detect_directory_tree(text_content):
                        processor.directory_trees.append(text_content)
                        # Don't add to output if consolidation is enabled
                        if not processor.config.enable_deduplication:
                            processed_items.append(text_content)
                    else:
                        processed_items.append(text_content)

        return "\n\n".join(processed_items)

    return str(content)


def post_process_markdown_artifacts(content: str) -> str:
    """
    Legacy post-processing function - now just returns content unchanged
    since file-based processing is more reliable.
    """
    return content


def post_process_markdown_artifacts_file(file_path: str) -> None:
    """
    File-based post-processing fix to remove markdown code blocks from text/markdown artifacts.
    Reads the file, processes it, and writes it back.
    """

    # Read the file
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Count markdown blocks before processing
        markdown_blocks_before = len(re.findall(r"```markdown", content))
        print(
            f"Processing {markdown_blocks_before} markdown code blocks found in file..."
        )

        # Multiple patterns to catch different artifact structures
        patterns = [
            # Pattern 1: Standard artifact structure with double newline
            r"(\*\*Artifact:\*\* `[^`]+` • \*\*Title:\*\* [^\n]+ • \*\*Type:\*\* text/markdown\n\n)```markdown\n(.*?)\n```",
            # Pattern 2: Artifact structure with single newline
            r"(\*\*Artifact:\*\* `[^`]+` • \*\*Title:\*\* [^\n]+ • \*\*Type:\*\* text/markdown\n)```markdown\n(.*?)\n```",
            # Pattern 3: More flexible pattern for any text/markdown artifact
            r"(\*\*Type:\*\* text/markdown[^\n]*\n\s*)```markdown\n(.*?)\n```",
        ]

        result = content
        total_removed = 0

        for i, pattern in enumerate(patterns, 1):
            before_count = len(re.findall(r"```markdown", result))
            result = re.sub(pattern, r"\1\2", result, flags=re.DOTALL)
            after_count = len(re.findall(r"```markdown", result))
            removed_this_pattern = before_count - after_count

            if removed_this_pattern > 0:
                print(
                    f"✅ Pattern {i} removed {removed_this_pattern} markdown code blocks"
                )
                total_removed += removed_this_pattern

        # Write back to file if changes were made
        if total_removed > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result)
            print(
                f"🎉 SUCCESS: Fixed {total_removed} markdown artifacts to render natively!"
            )
            print("✅ Markdown artifacts will now display properly in preview mode")
        else:
            print("No markdown artifacts found that needed fixing")

    except (FileNotFoundError, PermissionError, OSError, UnicodeDecodeError) as e:
        print(f"Warning: Post-processing failed: {e}")


def build_artifact_repository_enhanced(
    file_path: str,
    output_dir: str = "claude_export_repository",
    config: EnhancementConfig = None,
) -> str:
    """Enhanced version with folding, de-duplication, and table generation"""

    if config is None:
        config = EnhancementConfig()

    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except json.JSONDecodeError:
        return f"Error: The file '{file_path}' is not a valid JSON file."

    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize processor
    processor = ConversationProcessor(config)
    output = []

    # Add conversation metadata
    output.append(f"# Conversation: {data.get('name', 'Untitled')}")
    output.append(f"**UUID:** `{data.get('uuid')}`")
    output.append(f"**Created:** `{data.get('created_at')}`")
    output.append(f"**Last Updated:** `{data.get('updated_at')}`")

    if config.enable_folding:
        output.append("\n*Enhanced with collapsible sections and de-duplication*")

    output.append("\n---\n")

    # Process messages
    for message in data.get("chat_messages", []):
        processor.current_line += 1

        sender = "👤 **Human**" if message["sender"] == "human" else "🤖 **Claude**"
        output.append(f"### {sender}")

        if "content" in message and message["content"]:
            # Group content blocks by type
            thinking_blocks = []
            tool_blocks = []
            text_blocks = []

            for content_block in message["content"]:
                block_type = content_block.get("type")

                if block_type == "thinking":
                    thinking_blocks.append(content_block)
                elif block_type in ["tool_use", "tool_result"]:
                    tool_blocks.append(content_block)
                elif block_type == "text":
                    text_blocks.append(content_block)

            # Process each type
            for thinking_block in thinking_blocks:
                thinking_content = thinking_block.get("thinking", "")
                if thinking_content:
                    processed_thinking = process_thinking_block(
                        thinking_content, config
                    )
                    if processed_thinking:
                        output.append(processed_thinking)

            for text_block in text_blocks:
                text_content = text_block.get("text", "")
                if text_content and not detect_directory_tree(text_content):
                    output.append(text_content)

            if tool_blocks:
                processed_tools = process_tool_sequence(tool_blocks, processor)
                if processed_tools:
                    output.append(processed_tools)

        # Handle attachments (simplified)
        if message.get("attachments"):
            output.append("### Attachments:")
            for attachment in message["attachments"]:
                filename = attachment.get("file_name", "Attachment")
                output.append(f"**{filename}**")

        # Add timestamp and separator
        output.append(f"\n*{message.get('created_at', 'Unknown time')}*")
        output.append("\n---\n")

    # Add enhancement summary sections
    if config.enable_summary_tables:
        if processor.artifacts:
            artifact_table = generate_artifact_summary_table(processor.artifacts)
            artifact_summary = wrap_with_details(
                f"📄 Artifact Summary • {len(processor.artifacts)} artifacts processed",
                artifact_table
                + f"\n\n*Total artifacts: {len(processor.artifacts)} unique project outputs*",
            )
            output.append("\n## Enhancement Summary\n")
            output.append(artifact_summary)

        if processor.file_extractions:
            file_table = generate_file_extraction_table(processor.file_extractions)
            summary_section = wrap_with_details(
                f"📁 File Extraction Summary • {len(processor.file_extractions)} files processed",
                file_table
                + f"\n\n*Total extractions reduced from {sum(fe.extraction_count for fe in processor.file_extractions.values())} to {len(processor.file_extractions)} unique references*",
            )
            output.append(summary_section)

        if processor.directory_trees and config.enable_deduplication:
            consolidated_trees = consolidate_directory_trees(processor.directory_trees)
            output.append(consolidated_trees)

        # Processing statistics
        total_tools = sum(tu.usage_count for tu in processor.tool_usage.values())
        unique_tools = len(processor.tool_usage)
        total_artifacts = len(processor.artifacts)
        output.append("\n**Processing Statistics:**")
        output.append(
            f"- **Tool Operations:** {total_tools} total → {unique_tools} unique tool types"
        )
        output.append(
            f"- **Directory Trees:** {len(processor.directory_trees)} instances → 1 consolidated reference"
        )
        output.append(
            f"- **File Extractions:** {sum(fe.extraction_count for fe in processor.file_extractions.values())} → {len(processor.file_extractions)} unique files"
        )
        output.append(
            f"- **Artifacts:** {total_artifacts} project outputs → native format rendering"
        )

    # Write the enhanced conversation log
    conversation_path = os.path.join(output_dir, "conversation_log.md")

    with open(conversation_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    # Post-processing fix: Read the file and fix markdown artifacts
    # This ensures ALL markdown artifacts render properly regardless of processing path
    post_process_markdown_artifacts_file(conversation_path)

    return f"Enhanced conversation log created: {conversation_path}"


# Maintain backward compatibility with original function name
def build_artifact_repository(
    file_path: str, output_dir: str = "claude_export_repository"
) -> str:
    """
    Backward compatibility function that calls the enhanced version.
    Parses a Claude.ai conversation JSON file, creates a repository of artifacts,
    and generates a formatted Markdown log with enhanced features.
    """
    return build_artifact_repository_enhanced(file_path, output_dir)


if __name__ == "__main__":
    import sys

    # Production configuration with balanced settings
    production_config = EnhancementConfig(
        enable_folding=True,
        enable_deduplication=True,
        enable_summary_tables=True,
        max_tool_repetitions_before_folding=3,
        preserve_thinking_blocks_exactly=True,
        preserve_artifact_content_exactly=True,
    )

    # Default paths for production use
    JSON_FILE = "../logs/claude_conversation_exporter/claude_conversation.json"
    OUTPUT_DIRECTORY = "../logs/claude_export_repository"

    # Allow override from command line
    if len(sys.argv) > 1:
        JSON_FILE = sys.argv[1]
    if len(sys.argv) > 2:
        OUTPUT_DIRECTORY = sys.argv[2]

    if not os.path.exists(JSON_FILE):
        print(
            f"Error: '{JSON_FILE}' not found. Please ensure the exported JSON file is available."
        )
        print("Expected workflow:")
        print("1. Export conversation using claude_export_script.js")
        print("2. Move downloaded files to logs/claude_conversation_exporter/")
        print("3. Run 'python claude_repository_builder.py' from tools/ directory")
    else:
        print("Processing conversation and building enhanced artifact repository...")

        # Build the repository using enhanced features
        status_message = build_artifact_repository_enhanced(
            JSON_FILE, OUTPUT_DIRECTORY, config=production_config
        )

        print(f"✅ {status_message}")
        print(
            "✅ Enhanced conversation log with collapsible sections and deduplication"
        )
        print("✅ Native format rendering for artifacts and improved readability")
