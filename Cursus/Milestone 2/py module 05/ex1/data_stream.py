from abc import ABC, abstractmethod
from typing import Any, Union, List, Dict


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[str] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("Storage not found")
        first = self._storage.pop(0)
        listRange = self._rank - len(self._storage) - 1
        return (listRange, first)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        return isinstance(data, list) and all(isinstance(x, (int, float))
                                              for x in data)

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append(str(item))
            self._rank += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        return isinstance(data, list) and all(isinstance(x, str) for x in data)

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append(item)
            self._rank += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_valid_log(d: Any) -> bool:
            return (isinstance(d, dict) and
                    all(isinstance(log_key, str) and
                        isinstance(log_value, str)
                        for log_key, log_value in d.items()))

        if is_valid_log(data):
            return True
        if isinstance(data, list) and all(is_valid_log(x) for x in data):
            return True
        return False

    def ingest(self, data: Union[Dict[str, str],
                                 List[Dict[str, str]]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        def format_funct(d: Dict[str, str]) -> str:
            return f"{d.get('log_level', '')}: {d.get('log_message', '')}"

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._storage.append(format_funct(item))
            self._rank += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            processed = False
            for proc in self._processors:
                if proc.validate(item):
                    proc.ingest(item)
                    processed = True
                    break
            if not processed:
                print(f"DataStream error - "
                      f"Can't process element in stream: {item}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return

        for proc in self._processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            print(f"{name}: total {proc._rank} items processed, "
                  f"remaining {len(proc._storage)} on processor")


# Note: Terminal output might differ slightly from the subject
# examples for readability purposes.
if __name__ == "__main__":
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...\n")
    data_stream = DataStream()
    data_stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    numeric_processor = NumericProcessor()
    data_stream.register_processor(numeric_processor)

    print("\nSend first batch of data on stream: "
          "['Hello world', [3.14, -1, 2.71], [{'log_level': "
          "'WARNING',\n    'log_message': 'Telnet access! Use ssh instead'}"
          ", {'log_level': 'INFO',\n    "
          "'log_message': 'User wil is connected'}]"
          ", 42, ['Hi', 'five']]\n")
    batch = [
        'Hello world', [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING',
             'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
            ], 42, ['Hi', 'five']
          ]
    data_stream.process_stream(batch)
    print()
    data_stream.print_processors_stats()

    print("\nRegistering other data processors")
    text_processor = TextProcessor()
    log_processor = LogProcessor()
    data_stream.register_processor(text_processor)
    data_stream.register_processor(log_processor)

    print("\nSend the same batch again\n")
    data_stream.process_stream(batch)
    data_stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        numeric_processor.output()
    for _ in range(2):
        text_processor.output()
    log_processor.output()
    data_stream.print_processors_stats()
