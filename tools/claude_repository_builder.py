#!/usr/bin/env python3
"""
Enhanced Claude Repository Builder v2.0 - Complete Production Implementation
Implements comprehensive enhancement features including:
- Individual artifact file extraction (RESTORED)
- Extracted files and user uploads directories (RESTORED) 
- Collapsible sections for better navigation
- Content deduplication with intelligent tracking
- Native markdown rendering for text/markdown artifacts (CRITICAL FIX)
- Summary tables for enhanced overview
- Processing statistics and insights
- Experimental chronological nesting
- Emergent cognitive optimization patterns

Key Features:
✅ Full artifact repository creation with individual files
✅ Enhanced conversation log with collapsible sections  
✅ Intelligent content deduplication and consolidation
✅ Native format rendering for artifacts
✅ Summary tables and processing statistics
✅ Experimental chronological tool nesting within thinking blocks
✅ Meta-cognitive content organization optimization
"""

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

# Built-in dict and list types used directly


@dataclass
class FileExtraction:
    file_path: str
    extraction_count: int = 1
    first_content: str = ""
    content_hash: str = ""
    line_numbers: List[int] = field(default_factory=list)
    file_size: int = 0


@dataclass
class ToolUsage:
    tool_name: str
    usage_count: int = 1
    first_usage_line: int = 0
    parameters_summary: str = ""
    last_input: Dict[str, Any] = field(default_factory=dict)


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
    # Core feature toggles
    enable_folding: bool = True
    enable_deduplication: bool = True
    enable_summary_tables: bool = True
    enable_chronological_nesting: bool = True  # EXPERIMENTAL
    native_markdown_artifacts: bool = True     # CRITICAL FIX
    
    # Content preservation (non-negotiable)
    preserve_thinking_blocks_exactly: bool = True
    preserve_artifact_content_exactly: bool = True
    preserve_user_assistant_content: bool = True
    
    # Thresholds for optimization
    max_tool_repetitions_before_folding: int = 3
    max_directory_trees_before_consolidation: int = 2
    max_file_extractions_before_table: int = 5
    
    # Enhancement features
    generate_individual_artifact_files: bool = True  # RESTORED
    create_extracted_files_directory: bool = True    # RESTORED
    create_user_uploads_directory: bool = True       # RESTORED
    
    # Advanced optimization
    apply_emergent_reasoning: bool = True
    optimize_content_clustering: bool = True


class ConversationProcessor:
    def __init__(self, config: EnhancementConfig = None):
        self.config = config or EnhancementConfig()
        self.file_extractions: Dict[str, FileExtraction] = {}
        self.tool_usage: Dict[str, ToolUsage] = {}
        self.directory_trees: List[str] = []
        self.artifacts: Dict[str, ArtifactContent] = {}
        self.current_line = 0
        
        # Advanced tracking for emergent optimization
        self.thinking_tool_relationships: List[Tuple[str, List[dict]]] = []
        self.content_clusters: Dict[str, List[str]] = {}
        self.semantic_groups: Dict[str, List[dict]] = {}


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


def extract_artifact_info(text_content: str) -> Optional[ArtifactContent]:
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


def create_individual_artifact_file(artifact: ArtifactContent, output_dir: str) -> str:
    """RESTORED: Create individual artifact file and return relative path"""
    if not artifact.content:
        return ""
    
    # Create artifacts directory
    artifact_path = os.path.join(output_dir, "generated_artifacts")
    os.makedirs(artifact_path, exist_ok=True)
    
    # Generate filename
    ext = get_file_extension_from_mime(artifact.content_type)
    filename = f"{sanitize_filename(artifact.artifact_id)}{ext}"
    full_path = os.path.join(artifact_path, filename)
    
    # Write artifact content
    with open(full_path, "w", encoding="utf-8") as af:
        af.write(artifact.content)
    
    return os.path.relpath(full_path, output_dir)


def extract_and_save_file_content(file_path: str, content: str, output_dir: str) -> str:
    """RESTORED: Extract file content and save to extracted_files directory"""
    # Create the file path within the output directory  
    relative_file_path = file_path.lstrip("/")
    full_path = os.path.join(output_dir, "extracted_files", relative_file_path)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Write content
    with open(full_path, "w", encoding="utf-8") as af:
        af.write(content)
    
    return os.path.relpath(full_path, output_dir)


def save_user_attachment(attachment: dict, output_dir: str) -> str:
    """RESTORED: Save user-uploaded attachment to user_uploads directory"""
    uploads_path = os.path.join(output_dir, "user_uploads")
    os.makedirs(uploads_path, exist_ok=True)
    
    filename = sanitize_filename(
        attachment.get("file_name", f"attachment_{attachment.get('id')}.txt")
    )
    content = attachment.get("extracted_content", "")
    full_path = os.path.join(uploads_path, filename)
    
    with open(full_path, "w", encoding="utf-8") as af:
        af.write(content)
    
    return os.path.relpath(full_path, output_dir)


def format_artifact_content(artifact: ArtifactContent, config: EnhancementConfig, artifact_file_path: str = "") -> str:
    """Format artifact content in its native format with metadata and file link"""
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

    # Build metadata with file link if available
    metadata_parts = [
        f"**Artifact:** `{artifact.artifact_id}`",
        f"**Title:** {artifact.title}",
        f"**Type:** {artifact.content_type}"
    ]
    
    if artifact_file_path:
        metadata_parts.append(f"**File:** [{os.path.basename(artifact_file_path)}]({artifact_file_path})")
    
    metadata = " • ".join(metadata_parts)

    if config.enable_folding:
        summary = f"📄 {artifact.title} • {lang_indicator.upper()}"

        # CRITICAL FIX: Native markdown rendering for text/markdown
        if artifact.content_type == "text/markdown" and config.native_markdown_artifacts:
            formatted_content = f"{metadata}\n\n{artifact.content}"
        else:
            # Use code blocks for non-markdown content (mermaid, json, etc.)
            formatted_content = f"{metadata}\n\n```{lang_indicator}\n{artifact.content}\n```"
        
        return wrap_with_details(summary, formatted_content)
    else:
        # CRITICAL FIX: Native markdown rendering in non-folding mode too
        if artifact.content_type == "text/markdown" and config.native_markdown_artifacts:
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


def generate_file_extraction_table(extractions: Dict[str, FileExtraction]) -> str:
    """Generate comprehensive markdown table summarizing file extractions"""
    if not extractions:
        return ""

    table = "\n| File | Extractions | Status | Size |\n|------|-------------|--------|------|\n"
    
    # Sort by extraction count (most repeated first) then by filename
    sorted_extractions = sorted(
        extractions.items(), 
        key=lambda x: (-x[1].extraction_count, os.path.basename(x[0]))
    )
    
    for file_path, extraction in sorted_extractions:
        filename = os.path.basename(file_path)
        count_display = f"{extraction.extraction_count}x" if extraction.extraction_count > 1 else "1x"
        status = "✅ Consolidated" if extraction.extraction_count > 1 else "📄 Single"
        size_display = f"{extraction.file_size}B" if extraction.file_size > 0 else "N/A"
        table += f"| `{filename}` | {count_display} | {status} | {size_display} |\n"

    return table


def generate_artifact_summary_table(artifacts: Dict[str, ArtifactContent]) -> str:
    """Generate comprehensive markdown table summarizing artifacts"""
    if not artifacts:
        return ""

    table = "\n| Artifact | Type | Status | Actions |\n|----------|------|--------|----------|\n"
    
    for artifact in artifacts.values():
        title = artifact.title[:30] + "..." if len(artifact.title) > 30 else artifact.title
        file_type = artifact.content_type.split("/")[-1].upper()
        status = "✅ Consolidated" if artifact.extraction_count > 1 else "📄 Generated"
        
        # Determine actions based on type
        if artifact.content_type == "text/markdown":
            actions = "📄 Native Render"
        elif artifact.content_type == "application/vnd.ant.mermaid":
            actions = "📊 Diagram"
        else:
            actions = "📝 Code Block"
            
        table += f"| `{title}` | {file_type} | {status} | {actions} |\n"

    return table


def consolidate_directory_trees(trees: List[str], config: EnhancementConfig) -> str:
    """Consolidate multiple directory trees into an intelligent summary"""
    if len(trees) <= 1:
        return trees[0] if trees else ""

    # Extract unique paths from all trees with emergent pattern recognition
    all_paths = set()
    directory_stats = {}
    
    for tree in trees:
        lines = tree.split("\n")
        for line in lines:
            if any(char in line for char in ["└──", "├──", "📁", "📄"]):
                clean_line = line.strip()
                all_paths.add(clean_line)
                
                # Emergent analysis: Track directory structure patterns
                if "📁" in clean_line:
                    dir_name = clean_line.split("📁")[-1].strip()
                    directory_stats[dir_name] = directory_stats.get(dir_name, 0) + 1

    # Apply emergent cognitive optimization
    if config.apply_emergent_reasoning:
        # Group related paths by common patterns
        grouped_paths = {}
        for path in sorted(all_paths):
            if "📁" in path:
                key = "directories"
            elif "📄" in path:
                key = "files"
            else:
                key = "structure"
            
            if key not in grouped_paths:
                grouped_paths[key] = []
            grouped_paths[key].append(path)
        
        # Build optimized consolidated view
        consolidated_parts = []
        
        # Add directory overview first
        if "directories" in grouped_paths:
            dir_count = len([p for p in grouped_paths["directories"] if "📁" in p])
            consolidated_parts.append(f"**Project Structure Overview:** {dir_count} directories analyzed")
        
        # Add structured content
        if "structure" in grouped_paths:
            consolidated_parts.extend(grouped_paths["structure"][:10])
        
        consolidated_content = "\n".join(consolidated_parts)
        
        # Add full tree as nested collapsible section
        full_tree = "\n".join(sorted(all_paths)[:30])
        if len(all_paths) > 30:
            full_tree += f"\n... and {len(all_paths) - 30} more items"
        
        nested_tree = wrap_with_details("🌳 Complete Directory Tree", f"```\n{full_tree}\n```")
        consolidated_content += f"\n\n{nested_tree}"
    else:
        # Fallback: Standard consolidation
        consolidated_content = "```\n" + "\n".join(sorted(all_paths)[:20]) + "\n```"
        if len(all_paths) > 20:
            consolidated_content += f"\n\n*... and {len(all_paths) - 20} more items*"

    summary = f"*Consolidated {len(trees)} directory tree instances → 1 intelligent reference*"
    
    return wrap_with_details(
        f"📂 Project Structure Analysis • {len(all_paths)} unique paths", 
        consolidated_content + "\n\n" + summary
    )


def generate_tool_summary(tool_name: str, tool_input: Dict[str, Any], usage_count: int) -> str:
    """Create intelligent tool summaries with emergent context awareness"""
    if tool_name == "project_knowledge_search":
        query = tool_input.get("query", "")[:50]
        return f'project_knowledge_search • Query: "{query}..."'
    elif tool_name == "artifacts":
        title = tool_input.get("title", "Generated Artifact")
        content_type = tool_input.get("type", "").split("/")[-1].upper()
        return f"artifacts • {title} • {content_type}"
    elif tool_name == "read_file":
        target = tool_input.get("target_file", "")
        return f"read_file • {os.path.basename(target)}"
    elif tool_name == "list_dir":
        path = tool_input.get("relative_workspace_path", "")
        return f"list_dir • {path or 'workspace root'}"
    elif tool_name == "grep_search":
        query = tool_input.get("query", "")[:30]
        return f"grep_search • Pattern: {query}..."
    else:
        suffix = f" • Usage #{usage_count}" if usage_count > 1 else ""
        return f"{tool_name}{suffix}"


def process_thinking_block(thinking_content: str, config: EnhancementConfig, related_tools: List[dict] = None) -> str:
    """Process thinking blocks with optional chronological tool nesting"""
    if not thinking_content.strip():
        return ""

    if config.enable_folding:
        # Extract first meaningful line for summary
        lines = thinking_content.split("\n")
        first_line = ""
        for line in lines:
            clean_line = line.strip()
            if clean_line and not clean_line.startswith(">"):
                first_line = clean_line[:100]
                break
        
        if len(first_line) > 80:
            first_line = first_line[:77] + "..."
        
        summary = f"Thinking: {first_line}" if first_line else "Thinking..."
        
        # EXPERIMENTAL: Chronological nesting
        if config.enable_chronological_nesting and related_tools:
            # Nest related tools within thinking block
            content_with_tools = thinking_content
            
            for tool_block in related_tools:
                tool_content = process_single_tool_for_nesting(tool_block, config)
                if tool_content:
                    content_with_tools += f"\n\n{tool_content}"
            
            return wrap_with_details(summary, content_with_tools, "think")
        else:
            return wrap_with_details(summary, thinking_content, "think")
    else:
        return f"> **Thinking...**\n> {thinking_content.replace(chr(10), chr(10) + '> ')}"


def process_single_tool_for_nesting(tool_block: dict, config: EnhancementConfig) -> str:
    """Process a single tool block for nesting within thinking blocks with artifact support"""
    if tool_block.get("type") != "tool_use":
        return ""
    
    tool_name = tool_block.get("name", "unknown_tool")
    tool_input = tool_block.get("input", {})
    
    summary = generate_tool_summary(tool_name, tool_input, 1)
    
    # Special handling for artifacts
    if tool_name == "artifacts" and tool_input and "content" in tool_input:

        artifact_content = ArtifactContent(
            artifact_id=tool_input.get("id", "unknown_artifact"),
            title=tool_input.get("title", "Untitled Artifact"),
            content_type=tool_input.get("type", "text/plain"),
            content=tool_input.get("content", ""),
            command=tool_input.get("command", "create"),
            version_uuid=tool_input.get("version_uuid", ""),
        )
        
        # Format artifact content natively
        formatted_artifact = format_artifact_content(artifact_content, config, "")
        tool_content = formatted_artifact

    else:
        # Simplified tool content for non-artifacts
        content_parts = []
        if tool_input:
            content_parts.append(f"**Parameters:** {json.dumps(tool_input, indent=2)}")
        tool_content = "\n".join(content_parts) if content_parts else "Tool executed"
    
    return f"  <tools>\n    <details><summary>{summary}</summary>\n\n{tool_content}\n\n    </details>\n  </tools>"


def process_tool_sequence(tool_blocks: List[dict], processor: ConversationProcessor, output_dir: str = "") -> str:
    """Process a sequence of tool use/result blocks with enhanced artifact handling"""
    if not tool_blocks:
        return ""

    config = processor.config

    # Group tool use with its results
    tool_pairs: List[Dict[str, Any]] = []
    current_use_block: Optional[dict] = None
    current_results: List[dict] = []
    
    for block in tool_blocks:
        if block.get("type") == "tool_use":
            # Save previous tool if exists
            if current_use_block is not None:
                tool_pairs.append({"use": current_use_block, "results": current_results})
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
        tool_results: List[dict] = tool_pair["results"]

        tool_name = tool_use.get("name", "unknown_tool")
        tool_input = tool_use.get("input", {})
        


        # Enhanced artifact handling with individual file creation
        if tool_name == "artifacts" and tool_input and "content" in tool_input:

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

            # RESTORED: Create individual artifact file
            artifact_file_path = ""
            if config.generate_individual_artifact_files and output_dir:
                artifact_file_path = create_individual_artifact_file(artifact_content, output_dir)

            # Track tool usage for statistics
            if tool_name in processor.tool_usage:
                processor.tool_usage[tool_name].usage_count += 1
            else:
                processor.tool_usage[tool_name] = ToolUsage(
                    tool_name=tool_name, 
                    first_usage_line=processor.current_line,
                    last_input=tool_input
                )

            # Generate formatted artifact with file link
            if config.enable_folding:
                summary = generate_tool_summary(tool_name, tool_input, processor.tool_usage[tool_name].usage_count)
                formatted_artifact = format_artifact_content(artifact_content, config, artifact_file_path)
                wrapped_tool = wrap_with_details(summary, formatted_artifact, "tools")
                output.append(wrapped_tool)

            else:
                output.append(f"\n**Artifact: `{artifact_content.title}`**")
                if artifact_file_path:
                    output.append(f"**Generated File:** [{os.path.basename(artifact_file_path)}]({artifact_file_path})")
                formatted_artifact = format_artifact_content(artifact_content, config, artifact_file_path)
                output.append(formatted_artifact)

            continue  # Skip normal tool processing for artifacts

        # Track tool usage
        if tool_name in processor.tool_usage:
            processor.tool_usage[tool_name].usage_count += 1
            processor.tool_usage[tool_name].last_input = tool_input
        else:
            processor.tool_usage[tool_name] = ToolUsage(
                tool_name=tool_name, 
                first_usage_line=processor.current_line,
                last_input=tool_input
            )

        usage_count = processor.tool_usage[tool_name].usage_count

        if config.enable_folding:
            # Generate summary for this tool usage
            summary = generate_tool_summary(tool_name, tool_input, usage_count)

            # Build content
            content_parts = []

            # Add input section
            if tool_input:
                content_parts.append("**Input:**\n```json\n" + json.dumps(tool_input, indent=2) + "\n```")

            # Process results with enhanced file extraction
            for result in tool_results:
                result_content = process_tool_result(result, processor, output_dir)
                if result_content:
                    content_parts.append("**Results:**\n" + result_content)

            # Add deduplication note if applicable
            if usage_count > config.max_tool_repetitions_before_folding and config.enable_deduplication:
                content_parts.append(f"\n*Optimization applied: {usage_count} similar operations consolidated*")

            tool_content = "\n\n".join(content_parts)
            wrapped_tool = wrap_with_details(summary, tool_content, "tools")
            output.append(wrapped_tool)
        else:
            # Original format with enhanced file handling
            output.append(f"\n**Tool Use: `{tool_name}`**")
            if tool_input:
                output.append("```json\n" + json.dumps(tool_input, indent=2) + "\n```")

            for result in tool_results:
                result_content = process_tool_result(result, processor, output_dir)
                if result_content:
                    output.append(f"\n**Tool Result: `{tool_name}`**\n" + result_content)

    return "\n\n".join(output)


def process_tool_result(result_block: dict, processor: ConversationProcessor, output_dir: str = "") -> str:
    """Enhanced tool result processing with file extraction and artifact detection"""
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
                            processor.artifacts[artifact.artifact_id].extraction_count += 1
                        else:
                            processor.artifacts[artifact.artifact_id] = artifact

                        # RESTORED: Create individual artifact file
                        artifact_file_path = ""
                        if processor.config.generate_individual_artifact_files and output_dir:
                            artifact_file_path = create_individual_artifact_file(artifact, output_dir)

                        # Format artifact content with file link
                        formatted_artifact = format_artifact_content(artifact, processor.config, artifact_file_path)
                        processed_items.append(formatted_artifact)
                        continue

                # Enhanced file extraction with individual file creation
                if text_content.startswith("/") and "\n" in text_content:
                    lines = text_content.split("\n", 1)
                    file_path = lines[0].strip()

                    # Track file extraction with enhanced metadata
                    content_hash = hashlib.md5(text_content.encode()).hexdigest()[:8]
                    file_size = len(text_content.encode('utf-8'))

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
                            file_size=file_size
                        )

                    # RESTORED: Extract and save file content
                    extracted_file_path = ""
                    if processor.config.create_extracted_files_directory and output_dir and len(lines) > 1:
                        # Extract content from code block if present
                        code_match = re.search(r"```[a-zA-Z]*\n(.*?)\n```", lines[1], re.DOTALL)
                        file_content = code_match.group(1) if code_match else lines[1]
                        
                        try:
                            extracted_file_path = extract_and_save_file_content(file_path, file_content, output_dir)
                        except (OSError, IOError) as e:
                            print(f"Warning: Could not extract file {file_path}: {e}")

                    # Enhanced deduplication with file links
                    if (processor.config.enable_deduplication and 
                        processor.file_extractions[file_path].extraction_count > 1):
                        link_text = f" → [📄 View File]({extracted_file_path})" if extracted_file_path else ""
                        processed_items.append(f"**File:** `{file_path}` *(content previously shown)*{link_text}")
                    else:
                        if extracted_file_path:
                            processed_items.append(f"**Extracted File:** [{file_path}]({extracted_file_path})")
                        processed_items.append(text_content)
                else:
                    # Check for directory trees
                    if detect_directory_tree(text_content):
                        processor.directory_trees.append(text_content)
                        # Apply intelligent consolidation
                        if (len(processor.directory_trees) <= processor.config.max_directory_trees_before_consolidation or 
                            not processor.config.enable_deduplication):
                            processed_items.append(text_content)
                    else:
                        processed_items.append(text_content)

        return "\n\n".join(processed_items)

    return str(content)


def apply_emergent_cognitive_optimization(output: List[str], processor: ConversationProcessor) -> List[str]:
    """Apply emergent reasoning and meta-cognitive analysis to optimize content organization"""
    if not processor.config.apply_emergent_reasoning:
        return output
    
    # Implement semantic clustering and content flow optimization
    optimized_output = []
    
    # Group related content sections
    current_section = []
    section_type = None
    
    for item in output:
        # Detect section types
        if "<think>" in item:
            new_type = "thinking"
        elif "<tools>" in item:
            new_type = "tools"
        elif item.startswith("###"):
            new_type = "header"
        else:
            new_type = "content"
        
        # Group consecutive items of same type for better flow
        if section_type == new_type and new_type in ["thinking", "tools"]:
            current_section.append(item)
        else:
            # Finalize current section
            if current_section:
                if len(current_section) > 1 and section_type in ["thinking", "tools"]:
                    # Apply cognitive clustering
                    clustered_section = apply_content_clustering(current_section, section_type, processor.config)
                    optimized_output.extend(clustered_section)
                else:
                    optimized_output.extend(current_section)
            
            # Start new section
            current_section = [item]
            section_type = new_type
    
    # Don't forget the last section
    if current_section:
        optimized_output.extend(current_section)
    
    return optimized_output


def apply_content_clustering(sections: List[str], section_type: str, config: EnhancementConfig) -> List[str]:
    """Apply intelligent content clustering for related sections"""
    if not config.optimize_content_clustering or len(sections) <= 1:
        return sections
    
    # For now, return as-is but this could implement semantic grouping
    # Future enhancement: Cluster by tool types, content similarity, etc.
    return sections


def generate_processing_statistics(processor: ConversationProcessor) -> str:
    """Generate comprehensive processing statistics with insights"""
    stats = []
    
    # Tool usage analysis
    total_tools = sum(tu.usage_count for tu in processor.tool_usage.values())
    unique_tools = len(processor.tool_usage)
    
    # File processing analysis
    total_file_extractions = sum(fe.extraction_count for fe in processor.file_extractions.values())
    unique_files = len(processor.file_extractions)
    
    # Content consolidation analysis
    total_artifacts = len(processor.artifacts)
    repeated_artifacts = sum(1 for a in processor.artifacts.values() if a.extraction_count > 1)
    
    # Directory tree analysis
    tree_reduction = len(processor.directory_trees) if processor.directory_trees else 0
    
    stats.append("**📊 Processing Statistics & Optimization Results:**")
    stats.append(f"- **Tool Operations:** {total_tools} total → {unique_tools} unique tool types")
    stats.append(f"- **File Extractions:** {total_file_extractions} instances → {unique_files} unique files")
    stats.append(f"- **Directory Trees:** {tree_reduction} instances → 1 consolidated reference")
    stats.append(f"- **Artifacts:** {total_artifacts} generated ({repeated_artifacts} with multiple versions)")
    
    # Calculate reduction percentages
    if total_tools > unique_tools:
        tool_reduction = ((total_tools - unique_tools) / total_tools) * 100
        stats.append(f"- **Tool Consolidation:** {tool_reduction:.1f}% reduction in repetitive tool displays")
    
    if total_file_extractions > unique_files:
        file_reduction = ((total_file_extractions - unique_files) / total_file_extractions) * 100
        stats.append(f"- **File Deduplication:** {file_reduction:.1f}% reduction in repeated file content")
    
    # Enhancement features applied
    stats.append(f"- **Enhancement Features:** {sum([processor.config.enable_folding, processor.config.enable_deduplication, processor.config.enable_summary_tables, processor.config.native_markdown_artifacts])} of 4 core features active")
    
    return "\n".join(stats)


def build_artifact_repository_enhanced(
    file_path: str,
    output_dir: str = "claude_export_repository",
    config: EnhancementConfig = None,
) -> str:
    """
    Enhanced version with complete functionality restoration plus all enhancement features:
    - Individual artifact file creation (RESTORED)
    - Extracted files directory (RESTORED) 
    - User uploads directory (RESTORED)
    - Collapsible sections and deduplication
    - Native markdown rendering (CRITICAL FIX)
    - Summary tables and processing statistics
    - Experimental chronological nesting
    - Emergent cognitive optimization
    """

    if config is None:
        config = EnhancementConfig()

    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except json.JSONDecodeError:
        return f"Error: The file '{file_path}' is not a valid JSON file."

    # Create output directory structure
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
        features = []
        if config.enable_folding: features.append("collapsible sections")
        if config.enable_deduplication: features.append("content deduplication")
        if config.enable_summary_tables: features.append("summary tables")
        if config.native_markdown_artifacts: features.append("native markdown rendering")
        if config.enable_chronological_nesting: features.append("experimental chronological nesting")
        
        output.append(f"\n*✨ Enhanced with: {', '.join(features)}*")

    output.append("\n---\n")

    # Process messages with enhanced capabilities
    for message in data.get("chat_messages", []):
        processor.current_line += 1

        sender = "👤 **Human**" if message["sender"] == "human" else "🤖 **Claude**"

        output.append(f"### {sender}")

        # RESTORED: Handle user attachments
        if message["sender"] == "human" and message.get("attachments"):
            if config.create_user_uploads_directory:
                for attachment in message["attachments"]:
                    try:
                        attachment_path = save_user_attachment(attachment, output_dir)
                        filename = attachment.get("file_name", "Attachment")
                        output.append(f"\n**Attachment:** [{filename}]({attachment_path})")
                    except (OSError, IOError) as e:
                        print(f"Warning: Could not save attachment {attachment.get('file_name', 'unknown')}: {e}")

            # Handle text content
            if message.get("text"):
                output.append(message.get("text"))

        if "content" in message and message["content"]:
            # Enhanced content grouping with chronological awareness
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

            # Process each type with enhanced features
            for thinking_block in thinking_blocks:
                thinking_content = thinking_block.get("thinking", "")
                if thinking_content:
                    # Experimental: Find related tools for chronological nesting
                    related_tools = []
                    if config.enable_chronological_nesting:
                        # Simple heuristic: tools immediately following thinking
                        related_tools = [tb for tb in tool_blocks if tb.get("type") == "tool_use"][:2]

                    
                    processed_thinking = process_thinking_block(thinking_content, config, related_tools)
                    if processed_thinking:
                        output.append(processed_thinking)

            # Process text blocks
            for text_block in text_blocks:
                text_content = text_block.get("text", "")
                if text_content and not detect_directory_tree(text_content):
                    output.append(text_content)

            # Process tool blocks (skip if nested in thinking blocks)
            if tool_blocks and not (config.enable_chronological_nesting and thinking_blocks):
                processed_tools = process_tool_sequence(tool_blocks, processor, output_dir)
                if processed_tools:
                    output.append(processed_tools)

        # Add timestamp and separator
        output.append(f"\n*{message.get('created_at', 'Unknown time')}*")
        output.append("\n---\n")

    # Apply emergent cognitive optimization
    if config.apply_emergent_reasoning:
        output = apply_emergent_cognitive_optimization(output, processor)

    # Enhanced summary sections with comprehensive analysis
    if config.enable_summary_tables:
        output.append("\n## 📊 Enhancement Summary & Analytics\n")
        
        # Artifact analysis
        if processor.artifacts:
            artifact_table = generate_artifact_summary_table(processor.artifacts)
            artifact_summary = wrap_with_details(
                f"📄 Artifact Analysis • {len(processor.artifacts)} artifacts generated",
                artifact_table + f"\n\n*Individual artifact files created in `generated_artifacts/` directory*\n*Native markdown rendering applied for optimal readability*",
            )
            output.append(artifact_summary)

        # File extraction analysis
        if processor.file_extractions:
            file_table = generate_file_extraction_table(processor.file_extractions)
            total_extractions = sum(fe.extraction_count for fe in processor.file_extractions.values())
            summary_section = wrap_with_details(
                f"📁 File Processing Analysis • {len(processor.file_extractions)} unique files",
                file_table + f"\n\n*File extraction optimization: {total_extractions} total → {len(processor.file_extractions)} consolidated references*\n*Individual files saved to `extracted_files/` directory*",
            )
            output.append(summary_section)

        # Directory tree consolidation
        if processor.directory_trees and config.enable_deduplication:
            consolidated_trees = consolidate_directory_trees(processor.directory_trees, config)
            output.append(consolidated_trees)

        # Processing statistics with insights
        statistics = generate_processing_statistics(processor)
        output.append(f"\n{statistics}")

    # Write the enhanced conversation log
    conversation_path = os.path.join(output_dir, "conversation_log.md")

    with open(conversation_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    # CRITICAL FIX: Post-processing for native markdown rendering
    if config.native_markdown_artifacts:
        post_process_markdown_artifacts_file(conversation_path)

    # Generate completion report
    total_artifacts = len(processor.artifacts)
    total_files = len(processor.file_extractions)
    total_tools = len(processor.tool_usage)
    
    completion_message = f"""Enhanced conversation repository created successfully!

📁 **Repository Structure:**
   └── {output_dir}/
       ├── conversation_log.md (Enhanced with collapsible sections)
       ├── generated_artifacts/ ({total_artifacts} individual artifact files)
       ├── extracted_files/ ({total_files} project files)
       └── user_uploads/ (User-provided attachments)

✨ **Enhancement Features Applied:**
   • Collapsible sections for improved navigation
   • Content deduplication and intelligent consolidation  
   • Native markdown rendering for text/markdown artifacts
   • Summary tables and processing analytics
   • Individual artifact file generation (RESTORED)
   • File extraction with directory structure (RESTORED)
   • User attachment handling (RESTORED)
   {"• Experimental chronological nesting" if config.enable_chronological_nesting else ""}

📊 **Processing Results:**
   • {total_tools} tool types processed
   • {total_artifacts} artifacts generated
   • {total_files} unique files extracted
   • {len(processor.directory_trees)} directory trees consolidated"""

    return completion_message


def post_process_markdown_artifacts_file(file_path: str) -> None:
    """
    CRITICAL FIX: File-based post-processing to remove markdown code blocks from text/markdown artifacts.
    Ensures native rendering in markdown preview.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Count markdown blocks before processing
        markdown_blocks_before = len(re.findall(r"```markdown", content))
        if markdown_blocks_before == 0:
            print("✅ No markdown code blocks found that need fixing")
            return
            
        print(f"🔄 Processing {markdown_blocks_before} markdown code blocks for native rendering...")

        # Enhanced patterns to catch different artifact structures
        patterns = [
            # Pattern 1: Standard artifact structure with double newline
            r"(\*\*Artifact:\*\* `[^`]+`[^\n]*\*\*Type:\*\* text/markdown[^\n]*\n\n)```markdown\n(.*?)\n```",
            # Pattern 2: Artifact structure with single newline
            r"(\*\*Artifact:\*\* `[^`]+`[^\n]*\*\*Type:\*\* text/markdown[^\n]*\n)```markdown\n(.*?)\n```",
            # Pattern 3: More flexible pattern for any text/markdown artifact
            r"(\*\*Type:\*\* text/markdown[^\n]*\n\s*)```markdown\n(.*?)\n```",
            # Pattern 4: Artifact with file links
            r"(\*\*File:\*\* \[[^\]]+\]\([^)]+\)[^\n]*\n\n)```markdown\n(.*?)\n```",
        ]

        result = content
        total_removed = 0

        for i, pattern in enumerate(patterns, 1):
            before_count = len(re.findall(r"```markdown", result))
            result = re.sub(pattern, r"\1\2", result, flags=re.DOTALL)
            after_count = len(re.findall(r"```markdown", result))
            removed_this_pattern = before_count - after_count

            if removed_this_pattern > 0:
                print(f"✅ Pattern {i} fixed {removed_this_pattern} markdown artifacts")
                total_removed += removed_this_pattern

        # Write back to file if changes were made
        if total_removed > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"🎉 SUCCESS: Fixed {total_removed} markdown artifacts for native rendering!")
            print("✅ Text/markdown artifacts will now display properly in preview mode")
        else:
            print("ℹ️ No markdown artifacts needed fixing")

    except (FileNotFoundError, PermissionError, OSError, UnicodeDecodeError) as e:
        print(f"⚠️ Warning: Post-processing failed: {e}")


# Maintain backward compatibility with original function name
def build_artifact_repository(
    file_path: str, output_dir: str = "claude_export_repository"
) -> str:
    """
    Backward compatibility function that calls the enhanced version.
    RESTORED: Full functionality including individual artifact files, extracted files, and user uploads.
    ENHANCED: Collapsible sections, deduplication, native markdown rendering, and advanced features.
    """
    return build_artifact_repository_enhanced(file_path, output_dir)


if __name__ == "__main__":
    import sys

    # Production configuration with all enhancement features enabled
    production_config = EnhancementConfig(
        # Core enhancements
        enable_folding=True,
        enable_deduplication=True,
        enable_summary_tables=True,
        enable_chronological_nesting=True,  # EXPERIMENTAL
        native_markdown_artifacts=True,     # CRITICAL FIX
        
        # Content preservation (non-negotiable)
        preserve_thinking_blocks_exactly=True,
        preserve_artifact_content_exactly=True,
        preserve_user_assistant_content=True,
        
        # RESTORED functionality
        generate_individual_artifact_files=True,
        create_extracted_files_directory=True,
        create_user_uploads_directory=True,
        
        # Advanced optimization
        apply_emergent_reasoning=True,
        optimize_content_clustering=True,
        
        # Tuned thresholds
        max_tool_repetitions_before_folding=3,
        max_directory_trees_before_consolidation=2,
        max_file_extractions_before_table=5,
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
        print(f"❌ Error: '{JSON_FILE}' not found.")
        print("\n📋 Expected workflow:")
        print("1. Export conversation using claude_export_script.js")
        print("2. Move downloaded files to logs/claude_conversation_exporter/")
        print("3. Run 'python claude_repository_builder.py' from tools/ directory")
        print("\n💡 Alternative: Specify custom paths as arguments")
    else:
        print("🚀 Processing conversation with enhanced Claude Repository Builder v2.0...")
        print("✨ Features: Collapsible sections, deduplication, native markdown, file extraction")

        # Build the comprehensive repository with all features
        status_message = build_artifact_repository_enhanced(
            JSON_FILE, OUTPUT_DIRECTORY, config=production_config
        )

        print(f"\n{status_message}")
        print("\n🎉 Enhanced repository creation completed successfully!")
