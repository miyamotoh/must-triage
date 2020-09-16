import pytest

from must_triage.inspectors.ocs import OCS


class TestOCS:
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
        "line,expected",
        [
            (
                'yesterday I Observed a panic: here it is',
                True,
            ),
            (
                'tomorrow there will be no such panic',
                False,
            )
        ]
    )
    def test_panicked(self, line, expected):
        assert OCS.panicked(line) is expected
