from functools import partial
from importlib import import_module

from mpf.core.case_insensitive_dict import CaseInsensitiveDict
from mpf.core.utility_functions import Util
from mpfmc.core.config_collection import ConfigCollection
from mpfmc.uix.widget import magic_events


class Widget(ConfigCollection):

    config_section = 'widgets'
    collection = 'widgets'
    class_label = 'WidgetConfig'

    type_map = CaseInsensitiveDict()

    def _initialize(self):
        for cls_name, module in self.mc.machine_config['mpf-mc']['widgets'].items():
            for widget_cls in import_module(module).widget_classes:
                self.type_map[cls_name] = widget_cls

    def process_config(self, config):
        # config is localized to a specific widget section
        if isinstance(config, dict):
            config = [config]

        widget_list = list()

        for widget in config:
            widget_list.append(self.process_widget(widget))

        return widget_list

    def process_widget(self, config):
        # config is localized widget settings
        try:
            widget_cls = Widget.type_map[config['type']]
        except (KeyError, TypeError):
            try:
                raise ValueError(
                    '"{}" is not a valid MPF display widget type. Did you '
                    'misspell it, or forget to enable it in the "mpf-mc: '
                    'widgets" section of your machine config?'.format(
                        config['type']))
            except (KeyError, TypeError):
                raise ValueError("Invalid widget config: {}".format(config))

        config['_default_settings'] = list()

        for default_setting_name in widget_cls.merge_settings:
            if default_setting_name in config:
                config['_default_settings'].append(default_setting_name)

        self.mc.config_validator.validate_config('widgets:{}'.format(
            config['type']).lower(), config, base_spec='widgets:common')

        if 'animations' in config:
            config['animations'] = (
                self.process_animations(config['animations']))

        else:
            config['animations'] = None

        if 'reset_animations_events' in config:
            for event_name in config['reset_animations_events']:
                if event_name not in magic_events:
                    self.mc.events.add_handler("client_connected", partial(self._register_trigger, event_name))

        if config.get('z', 0) < 0:
            raise ValueError(
                "\nWidget with negative z value in config: {}.\n\nAs of MPF "
                "v0.30.3, negative z: "
                "values are no longer used to put widgets in 'parent' frames. "
                "Instead add a 'target:' setting to the 'widget_player:' entry"
                " and set that to the name of the display target (display or "
                "slide_frame) you want to add this widget to. Note that "
                "'target: default' is valid and will add the widget to the "
                "default display on top of any slides.\n".format(config))

        return config

    def _register_trigger(self, event_name, **kwargs):
        del kwargs
        self.mc.bcp_processor.register_trigger(event=event_name)

    def process_animations(self, config):
        # config is localized to the slide's 'animations' section

        for event_name, event_settings in config.items():

            # make sure the event_name is registered as a trigger event so MPF
            # will send those events as triggers via BCP. But we don't want
            # to register magic events since those aren't real MPF events.
            if event_name not in magic_events:
                self.mc.events.add_handler("client_connected", partial(self._register_trigger, event_name))

            # str means it's a list of named animations
            if isinstance(event_settings, str):
                event_settings = Util.string_to_list(event_settings)

            # dict means it's a single set of settings for one animation step
            elif isinstance(event_settings, dict):
                event_settings = [event_settings]

            # ultimately we're producing a list of dicts, so build that list
            # as we iterate
            new_list = list()
            for settings in event_settings:
                new_list.append(self.mc.animations.process_animation(settings))

            config[event_name] = new_list

        return config



collection_cls = Widget
