import os
import subprocess
import sys
import pytest

MUTANT_EVAL_SCRIPTS = [
    (
        "Calc: is_prime treats 1 as prime",
        """
import sys, pytest, autograde_tests.mutants.calc_mutants as cm, src.calculator
src.calculator.is_prime = cm.is_prime_mutant_1
ret = pytest.main(['tests/test_calculator.py', '-k', 'is_prime', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
    (
        "Calc: calculate_average empty list bug",
        """
import sys, pytest, autograde_tests.mutants.calc_mutants as cm, src.calculator
src.calculator.calculate_average = cm.calculate_average_mutant_2
ret = pytest.main(['tests/test_calculator.py', '-k', 'calculate_average', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
    (
        "Calc: find_maximum negative numbers bug",
        """
import sys, pytest, autograde_tests.mutants.calc_mutants as cm, src.calculator
src.calculator.find_maximum = cm.find_maximum_mutant_3
ret = pytest.main(['tests/test_calculator.py', '-k', 'find_maximum', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
    (
        "Validator: email missing TLD bug",
        """
import sys, pytest, autograde_tests.mutants.val_mutants as vm, src.data_validator
src.data_validator.validate_email = vm.validate_email_mutant_1
ret = pytest.main(['tests/test_data_validator.py', '-k', 'validate_email', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
    (
        "Validator: password missing special char check",
        """
import sys, pytest, autograde_tests.mutants.val_mutants as vm, src.data_validator
src.data_validator.validate_password = vm.validate_password_mutant_2
ret = pytest.main(['tests/test_data_validator.py', '-k', 'validate_password', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
    (
        "Validator: registration missing field check",
        """
import sys, pytest, autograde_tests.mutants.val_mutants as vm, src.data_validator
src.data_validator.validate_registration = vm.validate_registration_mutant_3
ret = pytest.main(['tests/test_data_validator.py', '-k', 'validate_registration', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
    (
        "StudentManager: duplicate ID check bug",
        """
import sys, pytest, autograde_tests.mutants.sm_mutants as smm, src.student_manager
src.student_manager.StudentManager = smm.StudentManagerMutant1
ret = pytest.main(['tests/test_student_manager.py', '-k', 'add_student or duplicate', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
    (
        "StudentManager: remove missing student KeyError bug",
        """
import sys, pytest, autograde_tests.mutants.sm_mutants as smm, src.student_manager
src.student_manager.StudentManager = smm.StudentManagerMutant2
ret = pytest.main(['tests/test_student_manager.py', '-k', 'remove_student', '-q', '--no-header'])
sys.exit(0 if ret != 0 else 1)
"""
    ),
]


@pytest.mark.weight(15)
@pytest.mark.number("1.3")
def test_mutation_bug_detection(request):
    """Evaluate student test suite effectiveness against buggy mutant implementations"""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    mutant_results = []
    
    for name, script in MUTANT_EVAL_SCRIPTS:
        cmd = [sys.executable, "-c", script]
        result = subprocess.run(
            cmd,
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Exit code 0 means mutant was killed (tests failed on buggy code)
        killed = (result.returncode == 0)
        mutant_results.append((name, killed))
        
    total_mutants = len(mutant_results)
    caught_count = sum(1 for _, killed in mutant_results if killed)
    earned = int(round(15.0 * caught_count / total_mutants))
    request.node._earned_points = earned

    details = "\n".join([f"  [{'CAUGHT' if c else 'MISSED'}] {name}" for name, c in mutant_results])
    print(f"\nMutant Detection Rate: {caught_count}/{total_mutants} ({earned}/15 marks)\n{details}")

    assert caught_count >= total_mutants * 0.75, (
        f"Test suite caught {caught_count}/{total_mutants} bugs. Must catch at least 75%.\nDetails:\n{details}"
    )
