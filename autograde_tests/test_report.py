import os
import re
import pytest

REPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report.md'))

def get_report_content():
    if not os.path.exists(REPORT_PATH):
        raise AssertionError(f"report.md was not found at {REPORT_PATH}")
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def get_section_discussion_answer(question_keyword, content):
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if question_keyword in line and '**' in line:
            answer_lines = []
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith('-') or next_line.startswith('##') or next_line.startswith('---'):
                    break
                if next_line:
                    answer_lines.append(next_line)
            return '\n'.join(answer_lines)
    return None

@pytest.mark.weight(5)
@pytest.mark.number("2.1")
def test_student_information():
    """report.md: Student Information check"""
    content = get_report_content()
    name_match = re.search(r'-\s*\*\*Name:\*\*\s*(.*)', content)
    mmdt_id_match = re.search(r'-\s*\*\*MMDT ID:\*\*\s*(.*)', content)
    
    assert name_match is not None, "Name field not found under Student Information"
    assert mmdt_id_match is not None, "MMDT ID field not found under Student Information"
    
    name = name_match.group(1).strip()
    mmdt_id = mmdt_id_match.group(1).strip()
    
    assert name and name != "[Write your Name here]", "Student Name must be filled out"
    assert not (name.startswith("[") and name.endswith("]")), "Student Name cannot contain placeholder text"
    
    assert mmdt_id and mmdt_id != "[Write your MMDT ID here]", "MMDT ID must be filled out"
    assert not (mmdt_id.startswith("[") and mmdt_id.endswith("]")), "MMDT ID cannot contain placeholder text"

@pytest.mark.weight(5)
@pytest.mark.number("2.2")
def test_test_suite_configuration():
    """report.md: Test Suite Configuration check"""
    content = get_report_content()
    fw_match = re.search(r'-\s*\*\*Pytest Version & Framework:\*\*\s*(.*)', content)
    count_match = re.search(r'-\s*\*\*Total Test Cases Written:\*\*\s*(.*)', content)
    cov_match = re.search(r'-\s*\*\*Measured Code Coverage \(%\):\*\*\s*(.*)', content)
    fix_match = re.search(r'-\s*\*\*Key Fixtures Implemented:\*\*\s*(.*)', content)

    assert fw_match is not None, "Pytest Version & Framework field not found"
    assert count_match is not None, "Total Test Cases Written field not found"
    assert cov_match is not None, "Measured Code Coverage (%) field not found"
    assert fix_match is not None, "Key Fixtures Implemented field not found"

    fw = fw_match.group(1).strip()
    count = count_match.group(1).strip()
    cov = cov_match.group(1).strip()
    fix = fix_match.group(1).strip()

    assert fw and not fw.startswith("["), "Pytest Version & Framework must be filled out"
    assert count and not count.startswith("["), "Total Test Cases Written must be filled out"
    assert cov and not cov.startswith("["), "Measured Code Coverage (%) must be filled out"
    assert fix and not fix.startswith("["), "Key Fixtures Implemented must be filled out"

@pytest.mark.weight(5)
@pytest.mark.number("2.3")
def test_test_design_and_boundaries():
    """report.md: Test Case Design & Boundary Analysis check"""
    content = get_report_content()
    calc_match = re.search(r'-\s*\*\*Calculator Boundary & Edge Cases:\*\*\s*(.*)', content)
    val_match = re.search(r'-\s*\*\*Validator Exception Scenarios:\*\*\s*(.*)', content)
    sm_match = re.search(r'-\s*\*\*Student Manager State Transitions:\*\*\s*(.*)', content)

    assert calc_match is not None, "Calculator Boundary & Edge Cases field not found"
    assert val_match is not None, "Validator Exception Scenarios field not found"
    assert sm_match is not None, "Student Manager State Transitions field not found"

    calc_raw = calc_match.group(1).strip()
    val_raw = val_match.group(1).strip()
    sm_raw = sm_match.group(1).strip()

    assert calc_raw and not calc_raw.startswith("["), "Calculator Boundary & Edge Cases must be filled out"
    assert val_raw and not val_raw.startswith("["), "Validator Exception Scenarios must be filled out"
    assert sm_raw and not sm_raw.startswith("["), "Student Manager State Transitions must be filled out"

@pytest.mark.weight(5)
@pytest.mark.number("2.4")
def test_local_verification_checked():
    """report.md: Verification checklist check"""
    content = get_report_content()
    checked_items = re.findall(r'-\s*\[[xX]\]\s*(.*)', content)
    assert len(checked_items) >= 4, "At least 4 features/test areas must be marked verified with [x]"

@pytest.mark.weight(5)
@pytest.mark.number("2.5")
def test_deployed_and_presentation():
    """report.md: Presentation & Repository Information check"""
    content = get_report_content()
    repo_match = re.search(r'-\s*\*\*GitHub Repository URL:\*\*\s*(.*)', content)
    video_match = re.search(r'-\s*\*\*Video Presentation Link:\*\*\s*(.*)', content)

    assert repo_match is not None, "GitHub Repository URL field not found"
    assert video_match is not None, "Video Presentation Link field not found"

    repo = repo_match.group(1).strip()
    video = video_match.group(1).strip()

    assert repo and not repo.startswith("["), "GitHub Repository URL must be filled out"
    assert video and not video.startswith("["), "Video Presentation Link must be filled out"

@pytest.mark.weight(5)
@pytest.mark.number("2.6")
def test_discussion_answers():
    """report.md: Discussion answers check"""
    content = get_report_content()
    ans1 = get_section_discussion_answer("mutation testing", content) or get_section_discussion_answer("coverage", content)
    ans2 = get_section_discussion_answer("AI engineering", content) or get_section_discussion_answer("Generative AI", content)

    assert ans1 is not None and len(ans1.split()) >= 15, "Discussion Question 1 answer must be completed (at least 15 words)"
    assert ans2 is not None and len(ans2.split()) >= 15, "Discussion Question 2 answer must be completed (at least 15 words)"
