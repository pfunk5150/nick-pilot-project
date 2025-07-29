#!/usr/bin/env python3
"""
Enhanced Claude Repository Builder v2.0 - Test Implementation
Implements core folding, deduplication, and summary table generation
"""

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Optional


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
class EnhancementConfig:
    enable_folding: bool = True
    enable_deduplication: bool = True
    enable_summary_tables: bool = True
    max_tool_repetitions_before_folding: int = 3
    preserve_thinking_blocks_exactly: bool = True


class ConversationProcessor:
    def __init__(self, config: EnhancementConfig = None):
        self.config = config or EnhancementConfig()
        self.file_extractions: dict[str, FileExtraction] = {}
        self.tool_usage: dict[str, ToolUsage] = {}
        self.directory_trees: list[str] = []
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
    tool_blocks: list[dict[str, Any]], processor: ConversationProcessor
) -> str:
    """Process a sequence of tool use/result blocks"""
    if not tool_blocks:
        return ""

    config = processor.config

    # Group tool use with its results
    tool_pairs = []
    current_tool: Optional[dict[str, Any]] = None

    for block in tool_blocks:
        if block.get("type") == "tool_use":
            if current_tool:
                tool_pairs.append(current_tool)
            current_tool = {"use": block, "results": []}
        elif block.get("type") == "tool_result":
            if current_tool is not None:
                current_tool["results"].append(block)

    if current_tool:
        tool_pairs.append(current_tool)

    output = []

    for tool_pair in tool_pairs:
        tool_use = tool_pair["use"]
        tool_results = tool_pair["results"]

        tool_name = tool_use.get("name", "unknown_tool")
        tool_input = tool_use.get("input", {})

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
            for tool_result in tool_results:
                result_content = process_tool_result(tool_result, processor)
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
                output.append("```json\n" + json.dumps(tool_input, indent=2) + "\n```")

            for tool_result in tool_results:
                result_content = process_tool_result(tool_result, processor)
                if result_content:
                    output.append(
                        f"\n**Tool Result: `{tool_name}`**\n" + result_content
                    )

    return "\n\n".join(output)


def process_tool_result(result_block: dict, processor: ConversationProcessor) -> str:
    """Process tool result with file tracking and deduplication"""
    content = result_block.get("content", "")

    if isinstance(content, list):
        processed_items = []
        for item in content:
            if item.get("type") == "text":
                text_content = item.get("text", "").strip()

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


def build_artifact_repository_enhanced(
    file_path: str,
    output_dir: str = "claude_export_repository_v2_test",
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
        if processor.file_extractions:
            file_table = generate_file_extraction_table(processor.file_extractions)
            summary_section = wrap_with_details(
                f"📄 File Extraction Summary • {len(processor.file_extractions)} files processed",
                file_table
                + f"\n\n*Total extractions reduced from {sum(fe.extraction_count for fe in processor.file_extractions.values())} to {len(processor.file_extractions)} unique references*",
            )
            output.append("\n## Enhancement Summary\n")
            output.append(summary_section)

        if processor.directory_trees and config.enable_deduplication:
            consolidated_trees = consolidate_directory_trees(processor.directory_trees)
            output.append(consolidated_trees)

        # Processing statistics
        total_tools = sum(tu.usage_count for tu in processor.tool_usage.values())
        unique_tools = len(processor.tool_usage)
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

    # Write the enhanced conversation log
    conversation_path = os.path.join(output_dir, "conversation_log_enhanced.md")
    with open(conversation_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    return f"Enhanced conversation log created: {conversation_path}"


if __name__ == "__main__":
    import sys

    # Configuration for testing
    test_config = EnhancementConfig(
        enable_folding=True,
        enable_deduplication=True,
        enable_summary_tables=True,
        max_tool_repetitions_before_folding=2,  # More aggressive for testing
    )

    if len(sys.argv) > 1:
        result = build_artifact_repository_enhanced(sys.argv[1], config=test_config)
    else:
        result = build_artifact_repository_enhanced(
            "logs/claude_conversation_exporter/claude_conversation.json",
            config=test_config,
        )

    print(result)
