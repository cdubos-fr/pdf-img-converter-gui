import pytest
from kivy.tests.common import GraphicUnitTest


@pytest.mark.skip(reason='Current CI does not support GUI testing')
class TestApp(GraphicUnitTest):
    def setUp(self) -> None:
        from kivy.lang import Builder

        from pdf_img_converter_gui.app import MyApp

        Builder.load_file('pdf_img_converter_gui/myapp.kv')
        self.app = MyApp()
        return super().setUp()

    def test_app_rendering(self) -> None:
        self.app.run()
        widget = self.app.root
        assert (
            widget.ids.conversion_mode.current_active_segment
            == widget.ids.conversion_mode.children[0]
        )

    def test_get_widget(self) -> None:
        from pdf_img_converter_gui.app import MyWidget

        assert isinstance(self.app.build(), MyWidget)

    def test_selected_files_is_empty(self) -> None:
        assert self.app.selected_files == []
