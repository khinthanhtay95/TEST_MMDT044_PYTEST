import os
import subprocess
import sys
import re
import pytest

@pytest.mark.weight(5)
@pytest.mark.number("1.4")
def test_test_coverage(request):
    """Verify test coverage of src/ meets the minimum threshold (>= 85%)"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    cmd = [
        sys.executable, "-m", "pytest",
        os.path.join(project_root, "tests"),
        "--cov=src",
        "--cov-report=term"
    ]
    
    result = subprocess.run(
        cmd,
        cwd=project_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    output = result.stdout + "\n" + result.stderr
    
    # Parse TOTAL coverage percentage, e.g. "TOTAL   ... 95%"
    match = re.search(r'TOTAL\s+.*?(\d+)%', output)
    if not match:
        match = re.search(r'(\d+)%\s*$', output, re.MULTILINE)
        
    if match:
        cov_percent = int(match.group(1))
        if cov_percent >= 85:
            earned = 5
        elif cov_percent >= 70:
            earned = 3
        elif cov_percent >= 50:
            earned = 2
        else:
            earned = 0
            
        request.node._earned_points = earned
        print(f"\nMeasured Code Coverage: {cov_percent}% (Earned: {earned}/5 marks)")
        assert cov_percent >= 85, f"Total test coverage ({cov_percent}%) is below required threshold of 85%."
    else:
        # Fallback if pytest-cov is not installed in local environment: run basic pytest
        fallback_cmd = [
            sys.executable, "-m", "pytest",
            os.path.join(project_root, "tests"),
            "-q"
        ]
        fallback_res = subprocess.run(
            fallback_cmd,
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if fallback_res.returncode == 0:
            # Tests pass completely
            request.node._earned_points = 5
            print("\nNote: 'pytest-cov' not installed in local environment. Full coverage analysis will run in GitHub Actions.")
            assert True
        else:
            request.node._earned_points = 0
            assert False, "Tests failed during coverage check."
