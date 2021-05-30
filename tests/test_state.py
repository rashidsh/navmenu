import pytest

from navmenu.state import MemoryStateHandler


class TestMemoryStateHandler:
    @pytest.fixture
    def state_handler(self):
        return MemoryStateHandler('default')

    def test_get_set(self, state_handler):
        state_handler.set(123, 'new_state')

        assert state_handler.get(123) == 'new_state'

    def test_history(self, state_handler):
        state_handler.set(123, 'new_state')

        assert state_handler.history == {123: ['default']}

    def test_default_state(self, state_handler):
        assert state_handler.get(123) == 'default'

    def test_go_back(self, state_handler):
        state_handler.set(123, 'new_state')
        state_handler.go_back(123)

        assert state_handler.get(123) == 'default'
        assert state_handler.history == {123: []}

    def test_go_back_with_invalid_count(self, state_handler):
        state_handler.set(123, 'new_state')

        with pytest.raises(ValueError):
            state_handler.go_back(123, 0)

    def test_create(self, state_handler):
        is_created = state_handler.create(123)
        assert is_created
        assert 123 in state_handler.state

        is_created = state_handler.create(123)
        assert not is_created
