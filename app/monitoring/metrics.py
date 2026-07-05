from datetime import datetime

metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "errors": 0,
    "latencies": []
}


def register_request():
    metrics["total_requests"] += 1


def register_success():
    metrics["successful_requests"] += 1


def register_error():
    metrics["errors"] += 1


def register_latency(seconds):
    metrics["latencies"].append(seconds)


def get_metrics():
    avg_latency = 0

    if metrics["latencies"]:
        avg_latency = sum(metrics["latencies"]) / len(metrics["latencies"])

    return {
        "total_requests": metrics["total_requests"],
        "successful_requests": metrics["successful_requests"],
        "errors": metrics["errors"],
        "average_latency": round(avg_latency, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }