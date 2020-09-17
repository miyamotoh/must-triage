import logging
import pytest

from concurrent.futures import ProcessPoolExecutor
from unittest.mock import patch

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

    def test_gather(self, inspector):
        inspector.gather_types = dict(
            jpg=dict(
                match=None,
                description='desc',
            )
        )
        with patch('must_triage.inspectors.base.fs.find') as m_find:
            m_find.return_value = 'path'
            inspector.gather()
        assert m_find.call_count == len(inspector.gather_types.keys())
        assert len(inspector.gathered.keys()) == m_find.call_count

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
