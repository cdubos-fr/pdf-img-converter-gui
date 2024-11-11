"""GUI for converting PDFs to images and images to PDFs."""

import os
from typing import Any
from typing import cast

from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.segmentedcontrol import MDSegmentedControl
from kivymd.uix.segmentedcontrol import MDSegmentedControlItem
from pdf_converter import convert_imgs_to_pdf
from pdf_converter import convert_pdf_to_img


class MyWidget(BoxLayout):
    """The main widget for the Kivy app."""

    selected_files = ListProperty([])


class MyApp(MDApp):
    """The main Kivy app."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            selector='multi',
            ext=['.png', '.jpg', '.jpeg', '.pdf'],
        )
        self.selected_files: list[str] = []
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'DeepPurple'

    def build(self) -> MyWidget:
        """Create the app layout."""
        widget = MyWidget()
        widget.ids.conversion_mode.current_active_segment = widget.ids.conversion_mode.children[0]
        return widget

    def file_manager_open(self) -> None:
        """Open the file manager."""
        self.file_manager.show(os.environ.get('HOME', '/'))

    def select_path(self, paths: list[str]) -> None:
        """Add the selected files to the selected files list."""
        self.exit_manager()
        self.selected_files.extend(paths)
        self.update_selected_files()

    def exit_manager(self, *args: Any) -> None:
        """Close the file manager."""
        self.file_manager.close()

    def update_selected_files(self) -> None:
        """Update the selected files in the RecycleView."""
        self.root.ids.rv.data = [{'text': path} for path in self.selected_files]

    def remove_file(self, path: str) -> None:
        """Remove a file from the selected files."""
        if path in self.selected_files:
            self.selected_files.remove(path)
            self.update_selected_files()
            toast(f'Removed: {path}')

    def convert_files(self) -> None:
        """Convert the selected files based on the selected conversion mode."""
        mode: MDSegmentedControlItem = cast(
            MDSegmentedControl, self.root.ids.conversion_mode
        ).current_active_segment
        if not self.selected_files:
            toast('No files selected')
            return
        if not mode:
            toast('Select a conversion mode')
            return
        converted_files: list[str]
        if mode.text == 'PDF to Images':
            if any(not file.endswith('.pdf') for file in self.selected_files):
                toast('All selected files must be PDFs for this conversion mode')
                return
            converted_files = [
                path for file in self.selected_files for path in convert_pdf_to_img(file)
            ]
        elif mode.text == 'Images to PDF':
            if any(not file.endswith(('.png', '.jpg', '.jpeg')) for file in self.selected_files):
                toast('All selected files must be images for this conversion mode')
                return
            converted_files = [convert_imgs_to_pdf(self.selected_files)]
        toast(f'Conversion completed {", ".join(converted_files)}')


def run() -> None:
    """Run the Kivy app."""
    MyApp().run()


if __name__ == '__main__':
    run()
