import sys
from jiki import create_jiki

def main():
    try:
        mcp_script_path = "src/server.py"
        print(f"[INFO] Using default model and discovering tools from '{mcp_script_path}'...", file=sys.stderr)

        orchestrator = create_jiki(
            mcp_script_path=mcp_script_path,
            auto_discover_tools=True,
            trace=True,
        )

        orchestrator.run_ui(frontend='cli')

    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"[ERROR] Failed to start Jiki: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()