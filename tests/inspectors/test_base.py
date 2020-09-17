import logging
import pytest

from concurrent.futures import ProcessPoolExecutor

from must_triage.inspectors.base import Inspector


@pytest.fixture
def inspector(request):
    obj = Inspector(root='/tmp/must_triage_tests', progress=False)
    return obj


class TestInspector:
    def test_init(self, inspector):
        assert inspector.root == '/tmp/must_triage_tests'
        assert inspector.progress is False
        assert isinstance(inspector.log, logging.Logger)

    @staticmethod
    def _dummy_inspector(path):
        return {path: [f"inspected {path}"]}

    @pytest.mark.asyncio
    async def test_inspector_helper(self, inspector):
        paths = ['/foo', '/bar']

        with ProcessPoolExecutor() as executor:
            result = await inspector._inspect_helper(
                executor, paths, self._dummy_inspector, "description")

        for key, value in result.items():
            assert len(value) == 1
            assert value[0] == f"inspected {key}"
