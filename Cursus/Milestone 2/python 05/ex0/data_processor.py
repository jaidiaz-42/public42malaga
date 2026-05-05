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


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")
    print("Testing Numeric Processor...")
    num_processor = NumericProcessor()
    print(f"Trying to validate input '42': {num_processor.validate(42)}")
    print(f"Trying to validate input 'Hello': "
          f"{num_processor.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_processor.ingest('foo')
    except ValueError as e:
        print(f"Got exception: {e}")
    num_data = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_data}")
    num_processor.ingest(num_data)
    print("Extracting 3 values...")
    for i in range(3):
        rank, value = num_processor.output()
        print(f"Numeric value {i}: {value}")

    print("\nTesting Text Processor...")
    text_processor = TextProcessor()
    print(f"Trying to validate input '42': {text_processor.validate(42)}")
    text_data = ["Hello", "Nexus", "World"]
    print(f"Processing data: {text_data}")
    text_processor.ingest(text_data)
    print("Extracting 1 value...")
    rank, value = text_processor.output()
    print(f"Text value 0: {value}")

    print("\nTesting Log Processor...")
    log_processor = LogProcessor()
    print(f"Trying to validate input 'Hello': "
          f"{log_processor.validate('Hello')}")
    log_data = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {log_data}")
    print("Extracting 2 values...")
    log_processor.ingest(log_data)
    for i in range(2):
        rank, value = log_processor.output()
        print(f"Log value {i}: {value}")
