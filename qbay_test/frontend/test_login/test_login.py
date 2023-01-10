from os import popen
import os
from pathlib import Path
import subprocess

# get expected input/output file
current_folder = Path(__file__).parent


# read expected in/out
# expected_in tests the intended inputs for the login function
expected_in = open(current_folder.joinpath(
    'test_login.in'))
# expected_out tests the intended outputs for the login function
expected_out = open(current_folder.joinpath(
    'test_login.out')).read()


def test_login():
    """capsys -- object created by pytest to 
    capture stdout and stderr

    This section tests the functionality  of the login function
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
