"""
Runs testing for the register option on the CLI.
Tests for success and for multiple failure states.
"""

from os import popen
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


# read expected in/out
expected_in = open(current_folder.joinpath(
    'test_register.in'))
expected_out = open(current_folder.joinpath(
    'test_register.out')).read()

print(expected_out)


def test_register():
    """capsys -- object created by pytest to 
    capture stdout and stderr

    Uses test_register.in and test_register.out to determine, through
    black-box testing, whether the register option on the command line was
    properly implemented.
    Has no parameters
    Returns None
    Has one assert
    """

    # pip the input
    output = subprocess.run(
        ['python', '-m', 'qbay'],
        stdin=expected_in,
        capture_output=True,
    ).stdout.decode()
    output = output.replace('\r', '')
    # command line uses \r\n, file uses \n
    print('outputs', output)
    assert output.strip() == expected_out.strip()
