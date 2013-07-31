import re

import sublime
import sublime_plugin


SETTINGS_FILE = "TextReplacement.sublime-settings"


class TextReplacementCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # Store the edit
        self._edit = edit

        # Read the settings.
        self._settings = sublime.load_settings(SETTINGS_FILE)

        # Read the replacement fields.
        self._fields = self._get_fields()

        # Create a regex pattern from the field keys.
        escaped = [re.escape(key) for key in self._fields.keys()]
        self._pattern = re.compile('|'.join(escaped))

        # Replace the text in each selection.
        for selection in self._get_selections():
            self._replace_text(selection)

    def _get_selections(self):
        """Return a list or Regions for the selection(s)."""

        sels = self.view.sel()
        if len(sels) == 1 and sels[0].empty():
            return [sublime.Region(0, self.view.size())]
        else:
            return sels

    def _get_fields(self):
        """Build a flat list of fields for the current configuration"""

        configuration = self._settings.get("configuration")
        fields = self._settings.get("fields", {})
        resolved = {}

        for key, value in fields.items():
            if isinstance(value, dict):
                if configuration in value:
                    resolved[key] = value[configuration]
            else:
                resolved[key] = value

        return resolved

    def _replace_text(self, selection, template=None, iteration=0):
        """Merge the fields into the template, recursively if needed"""

        # Read the content of the selection, if no template was passed.
        if template is None:
            template = self.view.substr(selection)

        # Merge the fields into the template.
        result = self._pattern.sub(lambda x: self._fields[x.group()], template)

        if result != template \
                and self._settings.get("recursive") \
                and iteration < self._settings.get("max_iterations"):
            self._replace_text(selection, result, iteration + 1)
        else:
            self.view.replace(self._edit, selection, result)
