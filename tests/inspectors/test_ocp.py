import pytest

from must_triage.inspectors.ocp import OCP


class TestOCP:
    @pytest.mark.parametrize(
        "obj,expected",
        [
            (
                dict(
                    metadata=dict(name='test_pod'),
                    status=dict(containerStatuses=[
                        dict(
                            name='test_container',
                            ready=False,
                            state=dict(
                                terminated=dict(
                                    reason='garbage',
                                ),
                            ),
                        ),
                    ]),
                ),
                ["Container 'test_container' in pod 'test_pod' is not ready"],
            ),
            (
                dict(
                    metadata=dict(name='test_pod'),
                    status=dict(),
                ),
                [dict(
                    pod_name='test_pod',
                    status=dict(),
                )],
            ),
        ]
    )
    def test_pod_ready(self, obj, expected):
        result = OCP.pod_ready(obj)
        assert result == expected
