# -*- coding: utf-8 -*-

# Copyright (c) 2016 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from calvin.actor.actor import Actor, ActionResult, manage, condition, guard

class ButtonLedSelect(Actor):

    """
    Get button activity, order migration, turn on led

    Inputs:
      button: Button pushed True/False
      force_led: force LED on/off True/False
      done: token when task accomplished (push_token, True/False)
    Outputs:
      force_leds: other LEDs on/off True/False
      led: LED on/off True/False
      token: argument passed as token when button pushed
    """

    @manage([])
    def init(self, push_token, default_state=False, bool_out=True):
        self.push_token = push_token
        self.ledstate = default_state
        self.do_default = True
        self.bool_out = bool_out
        self.in_progress = False

    def _out(self, out):
        if self.bool_out:
            return out
        else:
            return 1 if out else 0

    @condition([], ['led'])
    @guard(lambda self: self.do_default)
    def default_led(self):
        """ Set default state """
        self.do_default = False
        return ActionResult(production=(self._out(self.ledstate),))

    @condition(['force_led'], ['led'])
    def force(self, force_led):
        """ If we get a forced state set the led to it """
        self.ledstate = force_led
        return ActionResult(production=(self._out(force_led),))

    @condition(['button'], ['token'])
    @guard(lambda self, button: not self.in_progress)
    def pressed(self, button):
        """ When button is pressed flash the led and push token """
        self.in_progress = True
        return ActionResult(production=(self.push_token,))

    @condition(['button'])
    @guard(lambda self, button: self.in_progress)
    def pressed_during_progress(self, button):
        """ When button is pressed during progress just ignore it """
        return ActionResult()

    @condition(['done'], ['led', 'force_leds'])
    @guard(lambda self, done: done[1] and done[0] == self.push_token)
    def done_success(self, done):
        """ When done succesfully turn on led and force other leds off """
        self.in_progress = False
        self.ledstate = True
        return ActionResult(production=(self._out(True), self._out(False)))

    @condition(['done'], ['led'])
    @guard(lambda self, done: not done[1] and done[0] == self.push_token)
    def done_failed(self, done):
        """ When done failed turn off led and leave other leds alone """
        self.in_progress = False
        self.ledstate = False
        return ActionResult(production=(self._out(False),))

    @condition(['done'])
    @guard(lambda self, done: done[0] != self.push_token)
    def done_other(self, done):
        """ When not our done """
        return ActionResult()

    action_priority = (default_led, force, pressed, done_success, done_failed, done_other, pressed_during_progress)
