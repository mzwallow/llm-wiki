import sys
import tiktoken

def count_tokens(file_path: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return len(encoding.encode(content))
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tokenize.py <file_path>", file=sys.stderr)
        sys.exit(1)
    
    file_path = sys.argv[1]
    tokens = count_tokens(file_path)
    print(tokens)
