from traffic_monitor.log_collection import LogCollection


def stats(logs: LogCollection):
    """Compute stats for a list of logs"""

    sections = {}
    request_types = {}
    total_requests = len(logs)
    total_bytes = 0

    for log in logs:
        # Count hits per section
        if log.section in sections:
            sections[log.section] += 1
        else:
            sections[log.section] = 1

        # Count requests per type
        rtype = log.request.split()[0]
        if rtype in request_types:
            request_types[rtype] += 1
        else:
            request_types[rtype] = 1

        total_bytes += log.bytes

    # Sort sections by hits
    sections = {k: v for k, v in sorted(sections.items(), key=lambda item: item[1], reverse=True)}

    # Sort request types by hits
    request_types = {k: v for k, v in sorted(request_types.items(), key=lambda item: item[1], reverse=True)}

    first_time = logs.get_oldest().timestamp
    last_time = logs.get_newest().timestamp
    print(f"Stats from seconds {first_time} to {last_time} ({last_time - first_time} seconds)")

    print(f"Total requests: {total_requests}")
    print(f"Total bytes: {total_bytes}")
    
    print("Section hits:")
    for section, hits in sections.items():
        print(f"   {section}: {hits} hits, {hits/total_requests*100:.2f}%")

    print("Request types:")
    for rtype, hits in request_types.items():
        print(f"   {rtype}: {hits} hits, {hits/total_requests*100:.2f}%")

    print()