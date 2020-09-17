import pytest

from unittest.mock import mock_open, patch

from must_triage.inspectors.ocs import OCS


class TestOCS:
    def teardown(self):
        patch.stopall()

    @pytest.mark.parametrize(
        "obj,expected",
        [
            (
                dict(status='HEALTH_OK'),
                list(),
            ),
            (
                dict(status='something else'),
                [dict(status='something else')],
            ),
        ]
    )
    def test_unhealthy(self, obj, expected):
        result = OCS.unhealthy(obj)
        assert (obj['status'] == 'HEALTH_OK') != (obj in result)

    @pytest.mark.parametrize(
        "lines,panics",
        [
            (
                [
                    'we Observed a panic: here it is',
                ],
                1,
            ),
            (
                [
                    'no panic',
                ],
                0,
            ),
            (
                [
                    'we Observed a panic: here it is',
                    'no panic',
                    'Observed a panic:',
                ],
                2,
            ),
        ]
    )
    def test_inspect_log(self, lines, panics):
        path = '/fake_path'
        m_open = mock_open()
        with patch('must_triage.inspectors.ocs.open', m_open):
            m_open.return_value.readlines.return_value = lines
            result = OCS.inspect_log(path)
        assert len(result[path]) == panics
