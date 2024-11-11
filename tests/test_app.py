import pytest
from kivy.lang import Builder
from kivy.tests.common import GraphicUnitTest

from pdf_img_converter_gui.app import MyApp
from pdf_img_converter_gui.app import MyWidget


class TestApp(GraphicUnitTest):
    def setUp(self) -> None:
        Builder.load_file('pdf_img_converter_gui/myapp.kv')
        return super().setUp()

    @pytest.mark.skip(reason='Current CI does not support GUI testing')
    def test_app_rendering(self) -> None:
        app = MyApp()

        app.run()
        widget = app.root
        assert (
            widget.ids.conversion_mode.current_active_segment
            == widget.ids.conversion_mode.children[0]
        )

    @pytest.mark.skip(reason='Current CI does not support GUI testing')
    def test_get_widget(self) -> None:
        app = MyApp()

        assert isinstance(app.build(), MyWidget)

    @pytest.mark.skip(reason='Current CI does not support GUI testing')
    def test_selected_files_is_empty(self) -> None:
        app = MyApp()

        assert app.selected_files == []
