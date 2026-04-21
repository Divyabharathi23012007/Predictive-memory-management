import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psutil
from model import predict_memory
from database import (
    initialize_database,
    save_memory_sample,
    get_memory_history,
    get_memory_stats,
    save_alert,
    get_training_data,
    save_process_snapshot,
    get_top_processes,
)

app = FastAPI()

# Initialize database on startup
initialize_database()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Predictive Memory Management Backend Running"}

@app.get("/api/scan")
def scan_system():
    mem = psutil.virtual_memory()

    current_used = mem.used / (1024 ** 2)      # MB
    available = mem.available / (1024 ** 2)    # MB
    percent = mem.percent

    predicted = predict_memory(current_used, percent)

    # OS-style decision logic
    if percent < 60:
        decision = "Memory Stable"
    elif percent < 80:
        decision = "Monitor Memory"
    else:
        decision = "Allocate More Memory"

    # Save to database — capture returned sample id
    sample_id = save_memory_sample(current_used, available, percent, predicted, decision)

    # Collect top 5 processes by memory usage
    top_procs = []
    try:
        proc_list = []
        for proc in psutil.process_iter(["pid", "name", "memory_info", "memory_percent"]):
            try:
                mem_mb = proc.info["memory_info"].rss / (1024 ** 2)
                proc_list.append({
                    "pid": proc.info["pid"],
                    "name": proc.info["name"],
                    "memory_mb": round(mem_mb, 2),
                    "memory_percent": round(proc.info["memory_percent"], 3),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        proc_list.sort(key=lambda x: x["memory_mb"], reverse=True)
        top_procs = [dict(p, rank=i + 1) for i, p in enumerate(proc_list[:5])]

        if sample_id:
            save_process_snapshot(sample_id, top_procs)
    except Exception as e:
        print(f"Error collecting process data: {e}")

    # Trigger alert if memory usage is high
    if percent > 85:
        save_alert("HIGH_MEMORY", f"Memory usage at {percent}%", current_used, "CRITICAL")

    return {
        "current_memory_mb": round(current_used, 2),
        "available_memory_mb": round(available, 2),
        "memory_usage_percent": round(percent, 2),
        "predicted_memory_mb": round(predicted, 2),
        "os_decision": decision,
        "top_processes": top_procs,
    }

@app.get("/api/processes")
def get_processes():
    """Get the top memory-consuming processes from the latest snapshot"""
    procs = get_top_processes(5)
    return {
        "count": len(procs),
        "processes": procs,
    }

@app.get("/api/history")
def get_history(limit: int = 100):
    """Get historical memory readings"""
    history = get_memory_history(limit)
    return {
        "count": len(history),
        "data": history
    }

@app.get("/api/stats")
def get_stats(hours: int = 1):
    """Get memory statistics"""
    stats = get_memory_stats(hours)
    return {
        "hours": hours,
        "statistics": stats
    }

@app.get("/api/training-data")
def get_training():
    """Get data for ML model training"""
    data = get_training_data(500)
    return {
        "samples": len(data),
        "data": data
    }

# For Vercel serverless deployment
handler = app
