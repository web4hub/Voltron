import re
from typing import Any

class Tokenizer:
    pattern=re.compile(r"[A-Za-z0-9_]+|[^\sA-Za-z0-9_]", re.UNICODE)

    def encode(self, value: Any) -> list[str]:
        return [t.lower() for t in self.pattern.findall(str(value))]

    def decode(self, tokens: list[str]) -> str:
        return " ".join(tokens)
