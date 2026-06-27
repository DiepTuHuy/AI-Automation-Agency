import subprocess
import sys
import time
import os

def run_service(name, cmd, port):
    print(f"[INFRA] Starting {name} on port {port}...")
    # Add PYTHONPATH so imports resolve correctly if started from base folder
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    # Run uvicorn process
    proc = subprocess.Popen(cmd, shell=True, env=env)
    return proc

if __name__ == "__main__":
    processes = []
    try:
        # Start Content Service (8001)
        content_proc = run_service(
            "Content Service",
            "uvicorn content-service.main:app --host 127.0.0.1 --port 8001 --reload",
            8001
        )
        processes.append(content_proc)
        
        # Start Quiz Service (8002)
        quiz_proc = run_service(
            "Quiz Service",
            "uvicorn quiz-service.main:app --host 127.0.0.1 --port 8002 --reload",
            8002
        )
        processes.append(quiz_proc)
        
        # Give services a second to spin up
        time.sleep(1.5)
        
        # Start API Gateway (8000)
        gateway_proc = run_service(
            "API Gateway",
            "uvicorn gateway.main:app --host 127.0.0.1 --port 8000 --reload",
            8000
        )
        processes.append(gateway_proc)
        
        print("\n[INFRA] Playbook platform is fully running at: http://127.0.0.1:8000")
        print("[INFRA] Press Ctrl+C to terminate all services.\n")
        
        # Keep launcher alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[INFRA] Stopping all microservices...")
        for proc in processes:
            proc.terminate()
            proc.wait()
        print("[INFRA] All services terminated successfully.")
        sys.exit(0)
