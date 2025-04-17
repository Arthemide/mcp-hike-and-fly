import argparse

from jiki import create_jiki


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple multi‑turn CLI demonstrating Jiki tool use"
    )
    parser.add_argument(
        "--model",
        "-m",
        default="anthropic/claude-3-7-sonnet-latest",
        help="LLM model to use",
    )
    parser.add_argument(
        "--trace-dir",
        help="Directory where interaction traces will be saved (defaults to interaction_traces/)",
    )
    return parser

def chat_loop(orchestrator):
    """Run an interactive chat loop until the user exits."""
    print("Jiki multi‑turn CLI. Type your message, or 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print()  # newline after ^C/^D
            break

        if not user_input or user_input.lower() == "exit":
            break

        try:
            response = orchestrator.process(user_input)
            print(f"Jiki: {response}\n")
        except Exception as e:
            print(f"[ERROR] {e}")

    # Save traces (if tracing enabled)
    try:
        orchestrator.export_traces(None)  # default path
    except Exception:
        pass


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    orchestrator = create_jiki(
        model=args.model,
        mcp_script_path="src/server.py",
        auto_discover_tools=True,
        trace=True,
        trace_dir=args.trace_dir,
    )

    chat_loop(orchestrator)


if __name__ == "__main__":
    main()
