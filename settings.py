import sublime


class SettingsDeclaration(object):
    namespace = "org.rctay.buildview"
    settings_file = "%s.sublime-settings" % namespace
    prefix = "%s." % namespace

    def __init__(self):
        self.dirty = False
        self.value = None

    def set_value(self, value):
        self.dirty = True
        self.value = value

    def get_value(self, view=None):
        if self.dirty:
            return self.value
        value = sublime.load_settings(self.settings_file).get(self.settings_key_stem, self.default)
        if view:
            value = view.settings().get(self.settings_key, value)
        return value

    @property
    def settings_key(self):
        return self.prefix + self.settings_key_stem


class EnumSettingsDeclaration(SettingsDeclaration):
    def set_value(self, value):
        self.dirty = True
        self.value = value if value in self.enum else self.default


class ScrollSetting(EnumSettingsDeclaration):
    settings_key_stem = "scroll"

    enum = ["bottom", "top", "last"]
    default = "bottom"


class BoolSettingsDeclaration(SettingsDeclaration):
    def set_opposite(self):
        if self.dirty:
            self.value = not self.value
        else:
            self.value = not self.get_value()
            self.dirty = True

        return self.value


class EnabledSetting(BoolSettingsDeclaration):
    settings_key_stem = "enabled"

    default = True


class SilenceModifiedWarningSetting(BoolSettingsDeclaration):
    """
    This setting determines if a "Save changes?" dialog is to be launched.

    The default is to not show a "Save changes?" dialog.
    """

    settings_key_stem = "silence_modified_warning"

    default = True


# a hack to allow us to set attributes with less keystrokes - via http://stackoverflow.com/a/2283725
class _Struct(object):
    pass


available = _Struct()
available.SilenceModifiedWarning = SilenceModifiedWarningSetting()
