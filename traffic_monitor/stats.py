from traffic_monitor.log_collection import LogCollection
from typing import Dict

class Stats:
    """Stats for a list of logs"""

    def __init__(self, logs: LogCollection = None):
        """ Initialize stats """
        self.sections: Dict[str, int] = {}
        self.request_types: Dict[str, int] = {}
        self.total_requests: int = 0
        self.total_bytes: int = 0
        self.first_timestamp: int = 0
        self.last_timestamp: int = 0

        if logs:
            self.compute(logs)

    def sort_sections(self):
        """Sort sections by hits"""
        self.sections = {k: v for k, v in sorted(self.sections.items(), key=lambda item: item[1], reverse=True)}

    def sort_request_types(self):
        """Sort request types by hits"""
        self.request_types = {k: v for k, v in sorted(self.request_types.items(), key=lambda item: item[1], reverse=True)}

    def compute(self, logs: LogCollection):
        """Compute stats for a list of logs"""

        for log in logs:
            # Count hits per section
            if log.section in self.sections:
                self.sections[log.section] += 1
            else:
                self.sections[log.section] = 1

            # Count requests per type
            rtype = log.request.split()[0]
            if rtype in self.request_types:
                self.request_types[rtype] += 1
            else:
                self.request_types[rtype] = 1

            self.total_bytes += log.bytes
            self.total_requests += 1

        # Sort sections by hits
        self.sort_sections()

        # Sort request types by hits
        self.sort_request_types()

        self.first_timestamp = logs.get_oldest().timestamp
        self.last_timestamp = logs.get_newest().timestamp

    def __str__(self) -> str:
        if not self.total_requests:
            return ""

        return f"Stats from seconds {self.first_timestamp} to {self.last_timestamp} ({self.last_timestamp - self.first_timestamp} seconds)\n" + \
            f"Total requests: {self.total_requests}\n" + \
            f"Total bytes: {self.total_bytes}\n" + \
            "Section hits:\n" + \
            "\n".join([f"   {section}: {hits} hits, {hits/self.total_requests*100:.2f}%" for section, hits in self.sections.items()]) + \
            "\nRequest types:\n" + \
            "\n".join([f"   {rtype}: {hits} hits, {hits/self.total_requests*100:.2f}%" for rtype, hits in self.request_types.items()]) + \
            "\n"
    
    def print(self):
        """Print stats"""
        print(self.__str__())
