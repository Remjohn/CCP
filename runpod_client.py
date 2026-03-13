"""
CMF RunPod ComfyUI API Client
Sends workflows directly to your serverless endpoint and retrieves results.
"""

import requests
import json
import time
import base64
from pathlib import Path

# ============ CONFIGURATION ============
RUNPOD_API_KEY = ""  # Your RunPod API key (get from RunPod settings)
ENDPOINT_ID = ""     # Your serverless endpoint ID (after deployment)

# API URLs
BASE_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"
HEADERS = {
    "Authorization": f"Bearer {RUNPOD_API_KEY}",
    "Content-Type": "application/json"
}


def load_workflow(workflow_path: str) -> dict:
    """Load a ComfyUI workflow JSON file."""
    with open(workflow_path, 'r') as f:
        return json.load(f)


def submit_job(workflow: dict, images: list = None) -> str:
    """Submit a workflow to RunPod and return the job ID."""
    payload = {
        "input": {
            "workflow": workflow
        }
    }
    
    if images:
        payload["input"]["images"] = images
    
    response = requests.post(f"{BASE_URL}/run", headers=HEADERS, json=payload)
    response.raise_for_status()
    
    result = response.json()
    job_id = result.get("id")
    print(f"✅ Job submitted: {job_id}")
    return job_id


def check_status(job_id: str) -> dict:
    """Check the status of a job."""
    response = requests.get(f"{BASE_URL}/status/{job_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()


def wait_for_completion(job_id: str, max_wait: int = 600, poll_interval: int = 5) -> dict:
    """Wait for a job to complete, polling periodically."""
    print(f"⏳ Waiting for job {job_id}...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        status = check_status(job_id)
        state = status.get("status")
        
        if state == "COMPLETED":
            print("✅ Job completed!")
            return status
        elif state == "FAILED":
            print(f"❌ Job failed: {status.get('error')}")
            return status
        elif state == "IN_PROGRESS":
            print(f"  ... still processing ({int(time.time() - start_time)}s)")
        
        time.sleep(poll_interval)
    
    print("⚠️ Timeout waiting for job")
    return {"status": "TIMEOUT"}


def save_output(result: dict, output_dir: str = "outputs"):
    """Save output images/videos from the result."""
    Path(output_dir).mkdir(exist_ok=True)
    
    output = result.get("output", {})
    
    # Handle different output formats
    if "message" in output:
        # Base64 encoded output
        for filename, b64_data in output.get("message", {}).items():
            if isinstance(b64_data, str):
                # Decode and save
                file_path = Path(output_dir) / filename
                file_data = base64.b64decode(b64_data)
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                print(f"💾 Saved: {file_path}")
    
    elif "images" in output:
        for i, img_data in enumerate(output["images"]):
            file_path = Path(output_dir) / f"output_{i}.png"
            file_data = base64.b64decode(img_data)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            print(f"💾 Saved: {file_path}")
    
    return output


def generate(workflow_path: str, output_dir: str = "outputs"):
    """Main function: load workflow, submit, wait, save."""
    print(f"📂 Loading workflow: {workflow_path}")
    workflow = load_workflow(workflow_path)
    
    job_id = submit_job(workflow)
    result = wait_for_completion(job_id)
    
    if result.get("status") == "COMPLETED":
        save_output(result, output_dir)
        return result
    else:
        return result


# ============ EXAMPLE USAGE ============
if __name__ == "__main__":
    # Update these before running!
    RUNPOD_API_KEY = "YOUR_RUNPOD_API_KEY"  # Get from RunPod settings
    ENDPOINT_ID = "YOUR_ENDPOINT_ID"        # Get after deploying serverless
    
    # Rebuild headers with actual keys
    HEADERS["Authorization"] = f"Bearer {RUNPOD_API_KEY}"
    BASE_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"
    
    # Run generation
    result = generate(
        workflow_path="serverless_pro_workflow.json",
        output_dir="outputs"
    )
    print(f"\n📊 Result: {json.dumps(result, indent=2)[:500]}...")
