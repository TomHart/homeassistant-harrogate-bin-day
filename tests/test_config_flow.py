import unittest

from homeassistant.data_entry_flow import FlowResultType

from custom_components.harrogate_bin.config_flow import BinDayCustomConfigFlow


class TestStuff(unittest.IsolatedAsyncioTestCase):

    async def test_async_step_user_with_input(self):
        flow = BinDayCustomConfigFlow()

        user_input = {"username": "testuser", "password": "testpass"}
        result = await flow.async_step_user(user_input)

        assert result is not None
        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["title"] == "Bin Day"
        assert result["data"] == user_input

    async def test_async_step_user_without_input(self):
        flow = BinDayCustomConfigFlow()
        result = await flow.async_step_user()

        assert result is not None
        assert result["type"] == "form"
        assert result["type"] == FlowResultType.FORM
