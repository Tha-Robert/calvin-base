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

class FakeButton(Actor):

    """
    Fake button presses, simulate edge fall and pull up on pin
    Defaults to repeat sequence
    Outputs:
      state: button state
    """

    @manage(exclude=['timer'])
    def init(self, seq, sleep=2.0, repeat=True, void1=None, void2=None, void3=None):
        self.step = 0
        self.seq = seq
        self.repeat = repeat
        self.length = len(seq)
        self.sleep = sleep
        self.use("calvinsys.events.timer", shorthand="timer")
        if seq:
            self.timer = self['timer'].repeat(self.sleep)
        else:
            # If seq empty we do nothing
            self.timer = None

    @condition([], ['state'])
    @guard(lambda self: self.timer and self.timer.triggered and self.seq[self.step]==1)
    def pressed(self):
        """ Button pressed"""
        self.timer.ack()
        self.step += 1
        if self.step == self.length:
            self.step = 0
            if not self.repeat:
                self.timer.cancel()

        return ActionResult(production=(1,))

    @condition([], [])
    @guard(lambda self: self.timer and  self.timer.triggered and self.seq[self.step]==0)
    def no_action(self):
        """ Button no action"""
        self.timer.ack()
        self.step += 1
        if self.step == self.length:
            self.step = 0
            if not self.repeat:
                self.timer.cancel()
        return ActionResult()


    action_priority = (pressed, no_action)
    requires =  ['calvinsys.events.timer']
