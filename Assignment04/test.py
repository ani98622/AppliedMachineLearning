import subprocess
import time
import requests

def test_docker():
    print("🚀 Starting Docker test...")

    # Build Docker image
    subprocess.run(["docker", "build", "-t", "flask-score-app", "."], check=True)

    # Run container
    subprocess.run([
        "docker", "run", "-d", "--rm", "-p", "5000:5000", "--name", "test-container", "flask-score-app"
    ], check=True)

    time.sleep(5)

    try:
        sample = {"text": "Todays Vodafone numbers ending with 4882 are selected to a receive a £350 award. If your number matches call 09064019014 to receive your Â£350 award."}
        response = requests.post("http://localhost:5000/score", json=sample)
        assert response.status_code == 200
        json_data = response.json()
        assert "prediction" in json_data
        assert "propensity" in json_data
        print("Test passed ✅")
        print("Prediction:", json_data["prediction"])
        print("Propensity:", json_data["propensity"])        

    finally:
        subprocess.run(["docker", "stop", "test-container"])
