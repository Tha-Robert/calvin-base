# -*- coding: utf-8 -*-

# Copyright (c) 2015 Ericsson AB
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

import sys
from calvin.actor.actor import Actor, manage, condition, stateguard

class CountTimer(Actor):

    """
    Produce a counter token on the output every period seconds
    and for steps times, using a timer.
    Outputs:
      integer: Integer counter
    """

    @manage(exclude=['timer'])
    def init(self, sleep=0.1, start=1, steps=sys.maxint):
        self.start = start
        self.count = start
        self.sleep = sleep
        self.steps = steps + start
        self.setup()

    def setup(self):
        self.use("calvinsys.events.timer", shorthand="timer")
        if self.count < 3:
            self.timer = self['timer'].once(self.sleep)
        else:
            self.timer = self['timer'].repeat(self.sleep)

    def will_migrate(self):
        self.timer.cancel()

    def did_migrate(self):
        self.setup()

    def will_end(self):
        self.timer.cancel()

    def timer_trigger_stepwise(self):
        return self.timer.triggered and self.count < self.steps and self.count < 3

    def timer_trigger_repeat(self):
        return self.timer.triggered and self.count < self.steps

    def timer_trigger_stopped(self):
        return self.timer.triggered and self.count >= self.steps

    # The counting action, first 3 use non periodic for testing purpose
    # need guard with triggered() since the actor might be fired for other
    # reasons
    @stateguard(timer_trigger_stepwise)
    @condition(action_output=('integer',))
    def step_no_periodic(self):
        self.timer.ack()
        if self.count == 2:
            # now continue with periodic timer events
            self.timer = self['timer'].repeat(self.sleep)
        else:
            self.timer = self['timer'].once(self.sleep)
        self.count += 1
        return (self.count - 1, )

    # The counting action, handle periodic timer events hence no need to setup repeatedly
    # need guard with triggered() since the actor might be fired for other
    # reasons
    @stateguard(timer_trigger_repeat)
    @condition(action_output=('integer',))
    def step_periodic(self):
        self.timer.ack()
        self.count += 1
        return (self.count - 1, )

    # The stopping action, need guard with raised() since the actor might be
    # fired for other reasons
    @stateguard(timer_trigger_stopped)
    @condition()
    def stop(self):
        self.timer.ack()
        self.timer.cancel()
        

    def report(self, **kwargs):
        if kwargs.get("stopped", False):
            self.timer.cancel()
        return self.count - self.start

    action_priority = (step_no_periodic, step_periodic, stop)
    requires = ['calvinsys.events.timer']
