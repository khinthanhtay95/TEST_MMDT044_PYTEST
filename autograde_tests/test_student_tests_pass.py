import os
import subprocess
import sys
import pytest

@pytest.mark.weight(10)
@pytest.mark.number("1.2")
def test_student_tests_pass_on_correct_code(request):
    """Verify that student test suite passes 100% on reference implementation"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Run pytest directly on the student's tests directory
    cmd = [
        sys.executable, "-m", "pytest",
        os.path.join(project_root, "tests"),
        "-q", "--no-header"
    ]
    
    result = subprocess.run(
        cmd,
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # pytest returns exit code 0 if all tests passed
    if result.returncode == 0:
        request.node._earned_points = 10
        assert True
    else:
        request.node._earned_points = 0
        error_output = result.stdout + "\n" + result.stderr
        assert False, f"Student test suite failed against reference implementation:\n{error_output}"
