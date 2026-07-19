"""Simple starter bot for the Kir.ROBLOX_bot repository."""


def build_message(name: str) -> str:
    """Return a friendly greeting for the provided Roblox bot name."""
    return f"Hello, {name}! Your Roblox bot is ready."


def main() -> None:
    """Run a simple demo message in the terminal."""
    print(build_message("Kir"))


if __name__ == "__main__":
    main()
