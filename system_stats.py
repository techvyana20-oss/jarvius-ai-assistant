import psutil

def get_cpu():
    return f"CPU: {psutil.cpu_percent()}%"

def get_ram():
    mem = psutil.virtual_memory()
    return f"RAM: {mem.percent}%"

