#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define 
  Created: 06/01/17
"""

import inspect

########################################################################
class FSMError(Exception):
    """"""
    pass

########################################################################
class FSM(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, start_state=None, end_state=None, states=[]):
        """Constructor"""
        self._start_state = start_state
        self._end_state = end_state
    
        self._STATE = self._start_state
        self._states = states
        
        #
        # private fields
        #
        self._action_table = {}
    
    #----------------------------------------------------------------------
    def transfer(self, orig, dest):
        """"""
        def _transfer_action(func):
            def _execute_transfer(*args, **kwargs):
                if self.state == orig:
                    self.state = dest
                    return func(*args, **kwargs)
                else:
                    raise FSMError('not a valid action in shift: {}->{}, current: {}'\
                                   .format(orig, dest, self.state))
            return _execute_transfer
        return _transfer_action
    
    #----------------------------------------------------------------------
    def onstate(self, *states):
        """"""
        def _onstate_check(func):
            def _execute_onstate(*args, **kw):
                if self.state in states:
                    return func(*args, **kw)
                else:
                    raise FSMError('not a valid method on state: {}'.format(self.state))
            return _execute_onstate
        return _onstate_check
    
    @property
    def state(self):
        """"""
        return self._STATE
    
    @state.setter
    def state(self, value):
        """"""
        assert value in self._states
        self._STATE = value
    
    #----------------------------------------------------------------------
    def preset_all_states(self, *args):
        """"""
        self._states = list(args)
    
    #----------------------------------------------------------------------
    def set_start(self, state):
        """"""
        assert state in self._states
        self._start_state = state
        self._STATE = self._start_state
    
    #----------------------------------------------------------------------
    def set_end(self, state):
        """"""
        assert state in self._states
        self._end_state = state
    
    #----------------------------------------------------------------------
    def create_action(self, action_name, orig, dest):
        """"""
        assert orig in self._states, 'not a valid state'
        assert dest in self._states, 'not a valid state'
        
        assert not self._action_table.has_key(action_name), 'repeat action name'
        self._action_table[action_name] = {}
        self._action_table[action_name]['orig'] = orig
        self._action_table[action_name]['dest'] = dest
    
    #----------------------------------------------------------------------
    def action(self, action_name):
        """"""
        assert action_name in self._action_table, 'not a valid action'
        orig = self._action_table[action_name]['orig']
        dest = self._action_table[action_name]['dest']
        
        assert self.state == orig, 'current state is not {}, cannot shift to {}'.format(orig, dest)
        
        self.state = dest
        


class FSMBase(object):
    
    _fsm = FSM()
    
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        self.config()
    
    #----------------------------------------------------------------------
    def config(self):
        """"""
        #self._fsm.preset_all_states(state_END, state_RUNNING, state_START)
        #self._fsm.set_start(state_START)
        #self._fsm.set_end(state_END)
    
    @property
    def state(self):
        """"""
        return self._fsm.state
    
    