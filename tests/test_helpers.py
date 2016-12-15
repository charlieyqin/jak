# -*- coding: utf-8 -*-

import pytest
from jak import helpers

jakfile_content_1 = """
// Comment 1
{
// Comment 2
"password_file": "jakpassword",
// Comment 3
"files_to_encrypt": [ "env", "env2" ]  // Inline-Comment 4
// "commented out line": 5
} // Comment 5 (seriously?)
// Comment 6
// Comment 7
"""


def test_remove_comments_from_JSON():
    result = helpers._remove_comments_from_JSON(jakfile_content_1)
    assert result == '{"password_file":"jakpassword","files_to_encrypt":["env","env2"]}'


def test_read_jakfile_to_dict(tmpdir):
    jakfile = tmpdir.join("jakfile")
    jakfile.write(jakfile_content_1)
    assert jakfile.read() == jakfile_content_1

    result = helpers.read_jakfile_to_dict(jakfile.strpath)

    assert isinstance(result, dict)
    assert 'files_to_encrypt' in result
    assert 'password_file' in result


def test_grouper():
    assert helpers.grouper('aaa', 1) == ('a', 'a', 'a')
    assert helpers.grouper('aaa', 5) == ('aaa', )
    assert helpers.grouper('aaabbbcc', 3) == ('aaa', 'bbb', 'cc')

    # Raise error due to 2 not being iterable
    with pytest.raises(TypeError):
        helpers.grouper(2, 1)


@pytest.mark.parametrize('input,expected', [
    ('/hello/there.js', ('/hello/there', '.js')),
    ('there.js', ('there', '.js')),
    ('/hello/there', ('/hello/there', ''))])
def test_get_filepath_and_extension(input, expected):
    assert helpers.get_filepath_end_extension(full_filepath=input) == expected
