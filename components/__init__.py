


def highlight_message(message: str) -> None:
    lines = '=' * (len(message) + 5)

    print(f"\n{lines}\n{message}\n{lines}\n")