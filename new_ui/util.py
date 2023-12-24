from PyQt5.QtWidgets import QLayout


class Util:
    @classmethod
    def add_trailing_zero(cls, text: str) -> str:
        return '0' + text if len(text) == 1 else text

    @classmethod
    def remove_widgets(cls, layout: QLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()