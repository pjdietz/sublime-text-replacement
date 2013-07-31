import sublime
import sublime_plugin


SETTINGS_FILE = "TextReplacement.sublime-settings"


class TextReplacementCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self._settings = sublime.load_settings(SETTINGS_FILE)
