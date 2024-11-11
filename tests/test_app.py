from kivy.lang import Builder
from kivy.tests.common import GraphicUnitTest

from pdf_img_converter_gui.app import MyApp
from pdf_img_converter_gui.app import MyWidget


class TestApp(GraphicUnitTest):
    def test_get_widget(self) -> None:
        app = MyApp()

        assert isinstance(app.build(), MyWidget)

    def test_selected_files_is_empty(self) -> None:
        app = MyApp()

        assert app.selected_files == []

    def test_app_rendering(self) -> None:
        app = MyApp()
        Builder.load_file('pdf_img_converter_gui/myapp.kv')
        app.run()
        widget = app.root
        assert (
            widget.ids.conversion_mode.current_active_segment
            == widget.ids.conversion_mode.children[0]
        )
