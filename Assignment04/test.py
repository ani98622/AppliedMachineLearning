import subprocess
import time
import requests

def test_docker():
    print("🚀 Starting Docker test...")

    # Build Docker image
    build = subprocess.run(["docker", "build", "-t", "flask-score-app", "."], capture_output=True, text=True)
    print("📦 Build output:\n", build.stdout)
    assert build.returncode == 0, "❌ Docker build failed"

    # Run container
    run = subprocess.run([
        "docker", "run", "-d", "--rm", "-p", "5000:5000", "--name", "test-container", "flask-score-app"
    ], capture_output=True, text=True)
    print("🚢 Container ID:", run.stdout.strip())
    assert run.returncode == 0, "❌ Docker container failed to run"

    time.sleep(5)  # Wait for Flask app to start

    try:
        # Valid input test
        sample = {
            "text": "Todays Vodafone numbers ending with 4882 are selected to a receive a £350 award. "
                    "If your number matches call 09064019014 to receive your Â£350 award."
        }

        print("📨 Sending request to /score...")
        response = requests.post("http://localhost:5000/score", json=sample, timeout=10)
        print("📥 Status Code:", response.status_code)
        print("📥 Response JSON:", response.text)

        assert response.status_code == 200
        json_data = response.json()

        assert "prediction" in json_data
        assert "propensity" in json_data
        assert isinstance(json_data["prediction"], (int, bool))
        assert isinstance(json_data["propensity"], float)
        assert 0 <= json_data["propensity"] <= 1

        print("✅ Prediction:", json_data["prediction"])
        print("✅ Propensity:", json_data["propensity"])

        # Invalid input test
        bad_sample = {"badkey": "This is invalid"}
        bad_resp = requests.post("http://localhost:5000/score", json=bad_sample)
        assert bad_resp.status_code in [400, 422]

    finally:
        subprocess.run(["docker", "stop", "test-container"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
