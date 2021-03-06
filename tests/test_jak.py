# -*- coding: utf-8 -*-

import os
import pytest
from click.testing import CliRunner
from jak.app import main as jak
import jak.crypto_services as cs
from jak.compat import b


@pytest.fixture
def runner():
    return CliRunner()


def test_empty(runner):
    result = runner.invoke(jak)
    assert result.exit_code == 0
    assert not result.exception


@pytest.mark.parametrize('version_flag', ['--version', '-v'])
def test_version(runner, version_flag):
    result = runner.invoke(jak, [version_flag])
    assert not result.exception
    assert result.exit_code == 0
    assert '(Troubled Toddler)' in result.output.strip()


@pytest.mark.parametrize('cmd, filepath', [
    ('encrypt', 'filethatdoesnotexist'),
    ('decrypt', 'filethatdoesnotexist2')])
def test_file_not_found(runner, cmd, filepath):
    result = runner.invoke(jak, [cmd, filepath, '-k', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'])
    assert 'find the file:' in result.output


def test_encrypt_smoke(runner):
    """This one has proven to be an absolute godsend for finding
    weirdness, especially between python versions."""
    with runner.isolated_filesystem():
        with open('secret.txt', 'wb') as f:
            f.write(b('secret'))
        runner.invoke(jak,
                      ['encrypt',
                       os.path.abspath('secret.txt'),
                       '--key',
                       'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])

        with open('secret.txt', 'rb') as f:
            result = f.read()
        assert b(cs.ENCRYPTED_BY_HEADER) in result


def test_decrypt_smoke(runner):
    contents = '''- - - Encrypted by jak - - -

SkFLLTAwMHM0jlOUIaTUeVwbfS459sfDJ1SUW9_3wFFcm2rCxTnLvy1N-Ndb
O7t2Vcol566PnyniPGn9IadqwWFNykZdaycRJG7aL8P4pZnb4gnJcp08OLwR
LiFC7wcITbo6l3Q7Lw=='''
    with runner.isolated_filesystem():

        with open('secret.txt', 'w') as f:
            f.write(contents)

        runner.invoke(jak,
                      ['decrypt',
                       os.path.abspath('secret.txt'),
                       '--key',
                       'f40ec5d3ef66166720b24b3f8716c2c31ffc6b45295ff72024a45d90e5fddb56'])

        with open('secret.txt', 'rb') as f:
            result = f.read()
        assert b(cs.ENCRYPTED_BY_HEADER) not in result
        assert result.strip(b('\n')) == b('attack at dawn')
