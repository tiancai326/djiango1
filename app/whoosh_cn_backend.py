import jieba
from haystack.backends.whoosh_backend import WhooshEngine, WhooshSearchBackend
from whoosh.analysis import LowercaseFilter, Token, Tokenizer


class ChineseTokenizer(Tokenizer):
    def __call__(
        self,
        value,
        positions=False,
        chars=False,
        keeporiginal=False,
        removestops=True,
        start_pos=0,
        start_char=0,
        mode="",
        **kwargs,
    ):
        token = Token(
            positions,
            chars,
            removestops=removestops,
            mode=mode,
            **kwargs,
        )
        position = start_pos
        for word, start, end in jieba.tokenize(value or "", mode="search"):
            word = word.strip()
            if not word:
                continue
            token.text = word
            if positions:
                token.pos = position
                position += 1
            if chars:
                token.startchar = start_char + start
                token.endchar = start_char + end
            yield token


def ChineseAnalyzer():
    return ChineseTokenizer() | LowercaseFilter()


class ChineseWhooshSearchBackend(WhooshSearchBackend):
    def build_schema(self, fields):
        analyzer = ChineseAnalyzer()
        for field_class in fields.values():
            if (
                field_class.field_type in ("string", "text")
                and field_class.analyzer is None
            ):
                field_class.analyzer = analyzer
        return super().build_schema(fields)


class ChineseWhooshEngine(WhooshEngine):
    backend = ChineseWhooshSearchBackend
