import os

from claude_repository_builder import build_artifact_repository


def main() -> bool:
    """
    Main entry point for the Claude conversation repository builder.
    Processes exported Claude conversation files and creates structured repository.
    """
    print("🚀 Claude Repository Builder - Starting...")

    # File paths (relative to tools/ directory)
    json_file = "../logs/claude_conversation_exporter/claude_conversation.json"
    output_directory = "../logs/claude_export_repository"

    if not os.path.exists(json_file):
        print(f"❌ Error: '{json_file}' not found.")
        print("📋 Expected workflow:")
        print("   1. Export conversation using claude_export_script.js")
        print("   2. Move downloaded files to logs/claude_conversation_exporter/")
        print("   3. Run 'python main.py' from tools/ directory")
        return False

    try:
        print("📊 Processing conversation and building artifact repository...")
        # Build the repository and get the formatted log content
        formatted_text = build_artifact_repository(json_file, output_directory)

        # Save the main Markdown log file inside the repository directory
        print("💾 Saving conversation log...")
        output_filename = os.path.join(output_directory, "conversation_log.md")
        with open(output_filename, "w", encoding="utf-8") as output_file:
            output_file.write(formatted_text)

        print(
            f"✅ Conversation repository successfully created in '{output_directory}'"
        )
        print(f"✅ Main log file saved as '{output_filename}'")
        return True

    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"❌ Error during processing: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 Repository building completed successfully!")
    else:
        print("💥 Repository building failed. Please check the error messages above.")
