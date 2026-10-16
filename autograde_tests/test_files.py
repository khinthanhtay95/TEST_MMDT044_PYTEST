import os
import pytest

@pytest.mark.weight(10)
@pytest.mark.number("1.1")
def test_submitted_files(request):
    """Check that all required files and directories under project directory exist"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    expected_files = [
        'src/calculator.py',
        'src/data_validator.py',
        'src/student_manager.py',
        'tests/conftest.py',
        'tests/test_calculator.py',
        'tests/test_data_validator.py',
        'tests/test_student_manager.py',
        'requirements.txt',
        'report.md',
        'AI_declaration.png'
    ]
    
    missing_files = []
    existing_files = []
    for relative_path in expected_files:
        full_path = os.path.join(project_root, relative_path)
        if not os.path.exists(full_path):
            missing_files.append(relative_path)
        else:
            existing_files.append(relative_path)
            
    # Calculate partial credit: proportional to existing files, rounded to nearest integer
    earned = int(round(10.0 * len(existing_files) / len(expected_files)))
    request.node._earned_points = earned
    
    assert len(missing_files) == 0, f"Missing required files under project directory: {missing_files}"
    print("All required files present!")
