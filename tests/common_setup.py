import subprocess
import requests
import json
import socket
import os

def check_internet_connection():
    """Check if there is an active internet connection."""
    try:
        # Try to connect to a known server (Google's public DNS server)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def run_program(commands):
    process = subprocess.Popen(
        ['python', 'db_module.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=commands)
    
    return stdout, stderr

def logic_delRecord():
    commands = "delRecord\n"
    stdout, stderr = run_program(commands)
    return stdout

def logic_updateRec():
    commands = "updateRec\n"
    stdout, stderr = run_program(commands)
    return stdout

def pre_test_setup(test_name=None):
    test_outputs = {}
    test_points_awarded = {}
    test_feedback = None
    test_response_data = None

    # Resolve the base directory path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_module_path = os.path.join(base_dir, '..', 'db_module.py')
    autograding_config_path = os.path.join(base_dir, '..', '.github', 'classroom', 'autograding.json')
    pytest_code_path = os.path.join(base_dir, 'test_db_module.py')

    if test_name:
        if test_name == "delRecord":
            test_outputs["delRecord"] = logic_delRecord()
        elif test_name == "updateRec":
            test_outputs["updateRec"] = logic_updateRec()
    else:
        test_outputs = {
            "delRecord": logic_delRecord(),
            "updateRec": logic_updateRec()
        }

    if check_internet_connection():
        try:
            # Debug: Print resolved paths
            print(f"Resolved path to db_module.py: {db_module_path}")
            print(f"Resolved path to autograding.json: {autograding_config_path}")

            # Read the contents of the files
            with open(db_module_path, 'r') as f:
                student_code = f.read()
            with open(pytest_code_path, 'r') as f:
                pytest_code = f.read()
            with open(autograding_config_path, 'r') as f:
                autograding_config = json.load(f)

            # Determine which test is being run
            if test_name:
                print(f"Running test: {test_name}")
                # Filter the autograding config to include only the relevant section
                relevant_tests = [test for test in autograding_config["tests"] if test["run"].endswith(f"/{test_name}.py")]
                autograding_config["tests"] = relevant_tests

            # Prepare the data for the POST request
            data = {
                "studentCode": student_code,
                "pytestCode": pytest_code,
                "autogradingConfig": json.dumps(autograding_config),
                "terminalOutputs": list(test_outputs.values()),
                "studentRepositoryName": os.path.basename(os.getcwd())

            }

            # Send the POST request
            response = requests.post('https://autograding-api-next.vercel.app/api/autograde', json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the response
            test_response_data = response.json()

            # Store the points awarded for each test
            test_points_awarded.update({test['name']: test['pointsAwarded'] for test in test_response_data["tests"]})

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"API call failed: {e}")
            print("Proceeding without API response. Run the test again with a working API to receive more user-friendly feedback.")

    if check_internet_connection() and test_response_data:
        # Print the results in a well-formatted manner
        test_feedback = (
            "\nTest Results:\n"
            + "\n".join(
                [
                    f"Test Name: {test['name']}\nPoints Awarded: {test['pointsAwarded']}\nFeedback: {test['feedback']}\n"
                    for test in test_response_data["tests"]
                ]
            )
            + f"\nTotal Points Awarded: {test_response_data['totalPointsAwarded']}\n"
            + f"Total Points Possible: {test_response_data['totalPointsPossible']}\n"
            + "\nSpecific Code Feedback:\n"
            + "\n".join(
                [
                    f"{feedback['feedback']}\nRecommendation: {feedback['recommendation']}\n"
                    for feedback in test_response_data["specificCodeFeedback"]["code"]
                ]
            )
            + "\nGeneral Feedback:\n"
            + test_response_data["specificCodeFeedback"]["general"]
        )

    else:
        print("No active internet connection or API response. Run the test again with an active internet connection and a working API to receive more user-friendly feedback.")

    return test_outputs, test_points_awarded, test_feedback, test_response_data
