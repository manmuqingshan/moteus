#!/usr/bin/python3 -B

# Copyright 2023 mjbots Robotic Systems, LLC.  info@mjbots.com
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


"""
This example shows how to use the diagnostic protocol from python.
The diagnostic protocol should not typically be used during active
control, but can be used for debugging, or during setup or
provisioning.
"""

import asyncio
import moteus


async def main():
    c = moteus.Controller()
    s = moteus.Stream(c)

    # When using the diagnostic protocol, it is important to know that
    # applications like tview may leave the controller "spewing" on
    # the diagnostic channel, i.e. sending unsolicited data.  In order
    # stop that, a client needs to issue a "tel stop" command, and
    # then flush all data that is present.  After that point, normal
    # commands can be issued.
    await s.write_message(b'tel stop')
    await s.flush_read()

    # Stream.command will always return the result.  The `conf get`
    # diagnostic command is unique in that it replies with a single
    # line and no final "OK", so we use `allow_any_response=True`
    # option.
    old_kp = float((await s.command(
        b'conf get servo.pid_position.kp',
        allow_any_response=True)).decode('utf8'))
    new_kp = 4.0

    await s.command(f'conf set servo.pid_position.kp {new_kp}'.encode('utf8'))

    print(f"Changed kp from {old_kp} to {new_kp}")


if __name__ == '__main__':
    asyncio.run(main())
