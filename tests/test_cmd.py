import argparse
import pytest

from must_triage import cmd


def test_parse_args():
    args = ['.']
    parsed = cmd.parse_args(args)
    assert parsed.quiet is False
    assert parsed.out == 'json'
    assert parsed.path == '.'


def test_parse_args_bad_path():
    args = ['/fake_path_here']
    with pytest.raises((argparse.ArgumentError, SystemExit)):
        cmd.parse_args(args)
