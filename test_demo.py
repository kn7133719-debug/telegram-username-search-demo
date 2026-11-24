import unittest

from demo import Preview, load_screens


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.preview = Preview()

    def test_start_and_links_are_valid(self):
        screens = load_screens()
        self.assertIn("start", screens)
        self.assertGreater(len(screens), 1)
        for screen in screens.values():
            self.assertTrue(screen.title)
            self.assertTrue(screen.body)
            for button in screen.buttons:
                self.assertIn(button.target, screens)

    def test_valid_navigation(self):
        first = self.preview.screen.buttons[0]
        self.assertTrue(self.preview.select(1))
        self.assertEqual(self.preview.current, first.target)

    def test_invalid_choice_does_not_change_screen(self):
        self.assertFalse(self.preview.select(0))
        self.assertFalse(self.preview.select(999))
        self.assertEqual(self.preview.current, "start")

    def test_reset(self):
        self.preview.select(1)
        self.preview.reset()
        self.assertEqual(self.preview.current, "start")


if __name__ == "__main__":
    unittest.main()
