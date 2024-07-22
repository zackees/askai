from dataclasses import dataclass
from typing import Optional

from advanced_askai.streaming_console import StreamingConsole


@dataclass
class FileOutputStream:
    outfile: Optional[str] = None

    def write(self, text: str) -> None:
        if self.outfile:
            with open(self.outfile, "a") as f:
                f.write(text)


class OutStream:
    def __init__(self, outfile: Optional[str], force_color: bool = False) -> None:
        self.outfile = FileOutputStream(outfile)
        self.color_term = StreamingConsole()
        if force_color:
            self.color_term.force_color()

    def write(self, text: str) -> None:
        self.outfile.write(text)
        self.color_term.update(text)

    def close(self) -> None:
        pass


class NullOutStream(OutStream):
    def __init__(self):
        super().__init__(outfile=None, force_color=False)

    def write(self, text: str) -> None:
        pass

    def close(self) -> None:
        pass
