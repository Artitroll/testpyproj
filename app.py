import sys
import time
import random
import traceback
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

"""
$ python3.5 guess.py <token>
Guess a number:
1. Send the bot anything to start a game.
2. The bot randomly picks an integer between 0-99.
3. You make a guess.
4. The bot tells you to go higher or lower.
5. Repeat step 3 and 4, until guess is correct.
"""

class Player(telepot.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self._answer = random.randint(0, 99)
        self._started = False

    def _hint(self, answer, guess):
        if answer > guess:
            return 'more'
        else:
            return 'less'

    #def open(self, initial_msg, seed):
    #    self.sender.sendMessage('Guess a number')
    #    return True  # prevent on_message() from being called on the initial message

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            self.sender.sendMessage('not even a text')
            return

        if msg['text'] == 'start':
            self._started = True
            self.sender.sendMessage('Started')
            return

        if msg['text'] == 'stop':
            self._started = False
            self.sender.sendMessage('Stopped')
            return


        if self._started == True:
            try:
                guess = int(msg['text'])
            except ValueError:
                self.sender.sendMessage('not a number')
                return
            # check the guess against the answer ...
            if guess != self._answer:
                # give a descriptive hint
                hint = self._hint(self._answer, guess)
                self.sender.sendMessage(hint)
            else:
                self.sender.sendMessage('Correct!')
                self._started == False
                self.close()
        else:
            self.sender.sendMessage('Input start to initiate game')

    def on__idle(self, event):
        if self._started == True:
            self.sender.sendMessage('Game expired. The answer is %d' % self._answer)
            self.close()

    def on_close(self, event):
        {}


TOKEN = '320582700:AAFfPITTDl8AOGRNxpTpWk75vTC3pqQmI3I'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=10),
])

MessageLoop(bot).run_forever()
print('Listening ...')

while 1:
    time.sleep(10)
