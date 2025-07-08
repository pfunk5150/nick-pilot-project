import json
import os
import re


def get_file_extension_from_mime(mime_type):
    """Maps a MIME type to a file extension."""
    mapping = {
        "application/vnd.ant.mermaid": ".mermaid",
        "text/markdown": ".md",
        "application/json": ".json",
        "text/plain": ".txt",
    }
    # Return the specific extension or default to .txt
    return mapping.get(mime_type, ".txt")


def sanitize_filename(filename):
    """Removes characters that are invalid in filenames."""
    # Emojis and other special characters are removed or replaced
    filename = re.sub(r"[📄✨]", "", filename).strip()
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


def build_artifact_repository(file_path, output_dir="claude_export_repository"):
    """
    Parses a Claude.ai conversation JSON file, creates a repository of artifacts,
    and generates a formatted Markdown log with links to these artifacts.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except json.JSONDecodeError:
        return f"Error: The file '{file_path}' is not a valid JSON file."

    # Create the main output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output = []

    # Add conversation metadata to the top of the file
    output.append(f"# Conversation: {data.get('name', 'Untitled')}")
    output.append(f"**UUID:** `{data.get('uuid')}`")
    output.append(f"**Created:** `{data.get('created_at')}`")
    output.append(f"**Last Updated:** `{data.get('updated_at')}`")
    output.append("\n---\n")

    # Process each message in the chat
    for message in data.get("chat_messages", []):
        sender = message.get("sender", "unknown").capitalize()

        # Handle the user's initial prompt and attachments
        if sender == "Human":
            output.append(f"### 👤 {sender}")
            if message.get("text"):
                output.append(message.get("text"))

            # Extract and save any attachments the user uploaded
            if message.get("attachments"):
                uploads_path = os.path.join(output_dir, "user_uploads")
                if not os.path.exists(uploads_path):
                    os.makedirs(uploads_path)

                for attachment in message["attachments"]:
                    filename = sanitize_filename(
                        attachment.get(
                            "file_name", f"attachment_{attachment.get('id')}.txt"
                        )
                    )
                    content = attachment.get("extracted_content", "")
                    full_path = os.path.join(uploads_path, filename)

                    with open(full_path, "w", encoding="utf-8") as af:
                        af.write(content)

                    relative_path = os.path.relpath(full_path, output_dir)
                    output.append(f"\n**Attachment:** [{filename}]({relative_path})")

            output.append("\n---\n")
            continue

        # Handle the assistant's multi-part responses
        if sender == "Assistant":
            output.append(f"### 🤖 {sender}")

            for content_block in message.get("content", []):
                block_type = content_block.get("type")

                if block_type == "text":
                    output.append(content_block.get("text", ""))

                elif block_type == "thinking":
                    output.append("\n> **Thinking...**")
                    output.append(
                        f"> {content_block.get('thinking', '').replace(os.linesep, ' ')}"
                    )

                elif block_type == "tool_use":
                    tool_name = content_block.get("name", "unknown_tool")
                    tool_input = content_block.get("input", {})
                    output.append(f"\n**Tool Use: `{tool_name}`**")

                    # If it's an artifact generation tool, save the file
                    if tool_name == "artifacts" and "content" in tool_input:
                        artifact_id = tool_input.get("id", "unnamed_artifact")
                        artifact_title = tool_input.get("title", artifact_id)
                        artifact_content = tool_input.get("content", "")
                        mime_type = tool_input.get("type", "text/plain")

                        ext = get_file_extension_from_mime(mime_type)
                        filename = f"{sanitize_filename(artifact_id)}{ext}"

                        artifact_path = os.path.join(output_dir, "generated_artifacts")
                        os.makedirs(artifact_path, exist_ok=True)
                        full_path = os.path.join(artifact_path, filename)

                        with open(full_path, "w", encoding="utf-8") as af:
                            af.write(artifact_content)

                        relative_path = os.path.relpath(full_path, output_dir)
                        output.append(
                            f"\n**Generated Artifact:** [{artifact_title}]({relative_path})"
                        )
                    else:
                        output.append("```json")
                        output.append(json.dumps(tool_input, indent=2))
                        output.append("```")

                elif block_type == "tool_result":
                    tool_name = content_block.get("name", "unknown_tool")
                    status = "ERROR" if content_block.get("is_error") else "Result"
                    output.append(f"\n**Tool {status}: `{tool_name}`**")

                    # Handle file content extracted from project knowledge
                    if tool_name == "project_knowledge_search" and isinstance(
                        content_block.get("content"), list
                    ):
                        for item in content_block["content"]:
                            if item.get("type") == "text":
                                text_content = item.get("text", "").strip()
                                lines = text_content.split("\n", 1)

                                # Check for a file path followed by a code block
                                if (
                                    len(lines) > 1
                                    and lines[0].startswith("/")
                                    and "```" in lines[1]
                                ):
                                    file_path_str = lines[0].strip()
                                    code_match = re.search(
                                        r"```[a-zA-Z]*\n(.*?)\n```",
                                        lines[1],
                                        re.DOTALL,
                                    )
                                    file_content = (
                                        code_match.group(1) if code_match else ""
                                    )

                                    # Create the file path within the output directory
                                    relative_file_path = file_path_str.lstrip("/")
                                    full_path = os.path.join(
                                        output_dir,
                                        "extracted_files",
                                        relative_file_path,
                                    )

                                    os.makedirs(
                                        os.path.dirname(full_path), exist_ok=True
                                    )
                                    with open(full_path, "w", encoding="utf-8") as af:
                                        af.write(file_content)

                                    relative_link_path = os.path.relpath(
                                        full_path, output_dir
                                    )
                                    output.append(
                                        f"\n**Extracted File:** [{file_path_str}]({relative_link_path})"
                                    )
                                else:
                                    output.append(f"\n```\n{text_content}\n```")
                    # Fallback for other content types
                    else:
                        output.append(
                            f"```json\n{json.dumps(content_block.get('content'), indent=2)}\n```"
                        )

            output.append("\n---\n")

    return "\n".join(output)


if __name__ == "__main__":
    JSON_FILE = "claude_conversation.json"
    # Define the main directory for the exported repository
    OUTPUT_DIRECTORY = "claude_export_repository"

    if not os.path.exists(JSON_FILE):
        print(
            f"Error: '{JSON_FILE}' not found. Please place the script in the same directory as your JSON file."
        )
    else:
        print("Processing conversation and building artifact repository...")
        # Build the repository and get the formatted log content
        FORMATTED_TEXT = build_artifact_repository(JSON_FILE, OUTPUT_DIRECTORY)

        # Save the main Markdown log file inside the repository directory
        print("Saving conversation log...")
        output_filename = os.path.join(OUTPUT_DIRECTORY, "conversation_log.md")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(FORMATTED_TEXT)
        print(
            f"✅ Conversation repository successfully created in '{OUTPUT_DIRECTORY}'"
        )
        print(f"✅ Main log file saved as '{output_filename}'")
