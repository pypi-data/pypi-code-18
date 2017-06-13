
from Tkinter import NORMAL, EW
from collections import OrderedDict

from ..widget.switch import Switch
from ..mixin import WidgetMixIn
from ..frame.label import BaseLabelFrame
from stateutil.persist import Persist
from ..frame.introspection import locate_calling_base_frame
from ..helper.arguments import pop_kwarg, pop_mandatory_kwarg, raise_on_positional_args


class SwitchBox(WidgetMixIn):

    SWITCH_WIDGET = Switch
    DEFAULT_SWITCH_STATE = Switch.ON

    def __init__(self,
                 # title,
                 # switches,
                 # frame=None,
                 # switch_states=None,
                 # switch_parameters=None,
                 # link=None,
                 # width=None,
                 # sort=True,
                 # take_focus=None,
                 *args,
                 **kwargs):
        """
        There's small leap to make with labels versus objects.
        Objects can be anything hashable, which the switch is associated with
        and the labels are the strings displayed. If just labels are supplied,
        the labels are used as the associated objects (This is likely to be the
        most common usage).
        
        Getting the state of a switch uses the associated object as a key,
        not the label (unless they're the same)
        
        :param title: Text for the label frame
        :param switches: A list of switch names or, if the switch objects
                         and labels are different, a dictionary:

                                  {"switch label": <switch object>,
                                   ...
                                   "switch label": <switch object>}

        :param switch_states: Dictionary of initial switch states, these values
                              also override persisted states. Not all objets
                              need to be in this list, so if you always want
                              to set a subset of the switches, this is where
                              you do it. Dict looks like this:

                                  {<switch object>: <switch state>,
                                    ...
                                   <switch object>: <switch state>}
                                   
        :param link: A Persist object (or subclass). A dictionary is stored that 
                     uses the labels as keys. This is because they're strings,
                     which are easier to store than objects
                     
        :param switch_parameters: Parameters for the individual switches, e.g.:
        
                                  {<switch object>: {"tooltip", "Switch for the thing"},
                                    ...
                                   <switch object>: {"tooltip", "Switch for another thing"}}
        :param width: 
        :param args: invalid. positional args are poison in BaseWidget!
        :param kwargs:
        """
        raise_on_positional_args(self, args)
        frame = pop_kwarg(kwargs, u'frame', locate_calling_base_frame())
        title = pop_mandatory_kwarg(kwargs, u'title')
        switches = pop_mandatory_kwarg(kwargs, u'switches')
        switch_states = pop_kwarg(kwargs, u'switch_states', {})
        switch_parameters = pop_kwarg(kwargs, u'switch_parameters', {})
        link = pop_kwarg(kwargs, u'link')
        width = pop_kwarg(kwargs, u'width')
        sort = pop_kwarg(kwargs, u'sort', True)
        take_focus = pop_kwarg(kwargs, u'take_focus')

        grid_kwargs = self.grid_kwargs(frame=frame,
                                       **kwargs)

        # All other kwargs are discarded.

        super(SwitchBox, self).__init__(*args, **kwargs)

        # Setup a containing frame
        self.containing_frame = BaseLabelFrame(frame)

        self.containing_frame._set_title(title=title)

        # Set up object to label mapping...

        if not isinstance(switches, dict):
            # Only label labels, so make a dictionary
            # using those labels as the objects
            temp = OrderedDict()

            for switch in switches:
                # key=label: value=label (labels and objects are the same)
                temp[switch] = switch

            switches = temp

        if sort:
            switches = OrderedDict(sorted(switches.items(),
                                          key=lambda t: t[0]))

        self.switch_states = {switches[key]: value for key, value in switch_states.iteritems()}

        self.link = link

        if self.link:
            # Retrieve persisted states (link), but then override with any
            # supplied states, then write these back to the linked store.
            persisted_states = self.link.value
            persisted_states.update(self.switch_states)
            self.switch_states = persisted_states
            self.link.value = self.switch_states

        self.switches = {}

        for switch_label, switch_object in switches.iteritems():

            command = (lambda sw=switch_object: self.state_change(sw))

            # key into self.switch_states is the label, not the object
            switch_link = Persist(persistent_store=self.switch_states,
                                  key=switch_label,
                                  initial_value=self.switch_states.get(switch_label, self.DEFAULT_SWITCH_STATE))

            switch_params = switch_parameters.get(switch_object, {})
            switch_params[u'sticky'] = switch_params.get(u'sticky', EW)

            self.switches[switch_object] = self.SWITCH_WIDGET(frame=self.containing_frame,
                                                              text=switch_label,
                                                              state=NORMAL,
                                                              width=width,
                                                              command=command,
                                                              link=switch_link,
                                                              row=self.containing_frame.row.current,
                                                              column=self.containing_frame.column.start(),
                                                              take_focus=take_focus,
                                                              **switch_params)
            self.containing_frame.row.next()

        self.containing_frame.grid(**grid_kwargs)

    def state_change(self,
                     switch):

        if self.switched_on(switch):
            self.switch_on(switch)

        else:
            self.switch_off(switch)

        if self.link:
            self.link.set(self.switch_states)

    def switch_state(self,
                     switch):
        return self.switches[switch].state

    def switched_on(self,
                    switch):
        return self.switches[switch].switched_on

    def switched_off(self,
                     switch):
        return self.switches[switch].switched_off

    def switch_on(self,
                  switch):

        """
        Override this method to take action when the
        state of a switch changes to on if the actions needs
        to be at the switch array level, otherwise override
        switch_on in the switch_widget
        """

        self.switches[switch].switch_on()

    def switch_off(self,
                   switch):

        """
        Override this method to take action when the
        state of a switch changes to off if the actions needs
        to be at the switch array level, otherwise override
        switch_off in the switch_widget
        """

        self.switches[switch].switch_off()

    @property
    def all_switched_on(self):
        return [switch for switch in self.switches if self.switched_on(switch)]


    @property
    def all_switched_off(self):
        return [switch for switch in self.switches if self.switched_off(switch)]

    @property
    def all_states(self):
        return {switch: self.switch_state(switch) for switch in self.switches}

    def enable_all(self):
        for switch in self.switches.values():
            switch.enable()

    def disable_all(self):
        for switch in self.switches.values():
            switch.disable()
