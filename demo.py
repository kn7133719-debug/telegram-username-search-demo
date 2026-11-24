"""Локальный демонстрационный интерфейс; подключения к Telegram нет."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Button:
    label: str
    target: str


@dataclass(frozen=True)
class Screen:
    title: str
    body: str
    buttons: tuple[Button, ...]


def load_screens() -> dict[str, Screen]:
    data = json.loads(Path(__file__).with_name("screens.json").read_text(encoding="utf-8"))
    screens = {
        key: Screen(
            title=value["title"],
            body=value["body"],
            buttons=tuple(Button(**button) for button in value["buttons"]),
        )
        for key, value in data.items()
    }
    if "start" not in screens:
        raise ValueError("В макете отсутствует стартовый экран")
    for screen in screens.values():
        if not screen.title or not screen.body:
            raise ValueError("Заголовок и текст экрана не могут быть пустыми")
        for button in screen.buttons:
            if not button.label or button.target not in screens:
                raise ValueError("Некорректная кнопка или переход")
    return screens


class Preview:
    def __init__(self, screens: dict[str, Screen] | None = None) -> None:
        self.screens = load_screens() if screens is None else screens
        self.current = "start"

    @property
    def screen(self) -> Screen:
        return self.screens[self.current]

    def select(self, number: int) -> bool:
        """Выбрать пункт по номеру. Неверный номер не меняет экран."""
        buttons = self.screen.buttons
        if not 1 <= number <= len(buttons):
            return False
        self.current = buttons[number - 1].target
        return True

    def reset(self) -> None:
        self.current = "start"


def main() -> None:
    preview = Preview()
    print("ДЕМО: локальный макет, без Telegram и сетевых запросов.")
    while True:
        screen = preview.screen
        print(f"\n=== {screen.title} ===\n{screen.body}")
        for number, button in enumerate(screen.buttons, 1):
            print(f"{number}. {button.label}")
        choice = input("Выберите пункт (q — выход): ").strip().lower()
        if choice in {"q", "й"}:
            break
        if not choice.isdigit() or not preview.select(int(choice)):
            print("Такого пункта нет. Выберите номер из меню.")


if __name__ == "__main__":
    main()
