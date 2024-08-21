from functions import extract_github_details, read_text_file
import pytest

test1 = 'https://github.com/BiggestChris/CS50P-Final-Project-V1'
test2 = 'https://github.com/JoshuaHardyAquinas/InversityCrownEstate'
test3 = 'https://github.com/BiggestChris/Companies-House-Unlock/blob/main/functions.py'
test4 = 'https://github.com/BiggestChris/Companies-House-Unlock.git'

def test_extract_github_details():
    assert extract_github_details(test1) == ('BiggestChris', 'CS50P-Final-Project-V1')
    assert extract_github_details(test2) == ('JoshuaHardyAquinas', 'InversityCrownEstate')
    assert extract_github_details(test4) == ('BiggestChris', 'Companies-House-Unlock')


# TODO: Tests to check when errors are raised