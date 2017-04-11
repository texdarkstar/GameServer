"""
Channel

The channel class represents the out-of-character chat-room usable by
Players in-game. It is mostly overloaded to change its appearance, but
channels can be used to implement many different forms of message
distribution systems.

Note that sending data to channels are handled via the CMD_CHANNEL
syscommand (see evennia.syscmds). The sending should normally not need
to be modified.

"""

from evennia import DefaultChannel
import time


class Channel(DefaultChannel):
    """
    Working methods:
        at_channel_creation() - called once, when the channel is created
        has_connection(player) - check if the given player listens to this channel
        connect(player) - connect player to this channel
        disconnect(player) - disconnect player from channel
        access(access_obj, access_type='listen', default=False) - check the
                    access on this channel (default access_type is listen)
        delete() - delete this channel
        message_transform(msg, emit=False, prefix=True,
                          sender_strings=None, external=False) - called by
                          the comm system and triggers the hooks below
        msg(msgobj, header=None, senders=None, sender_strings=None,
            persistent=None, online=False, emit=False, external=False) - main
                send method, builds and sends a new message to channel.
        tempmsg(msg, header=None, senders=None) - wrapper for sending non-persistent
                messages.
        distribute_message(msg, online=False) - send a message to all
                connected players on channel, optionally sending only
                to players that are currently online (optimized for very large sends)

    Useful hooks:
        channel_prefix(msg, emit=False) - how the channel should be
                  prefixed when returning to user. Returns a string
        format_senders(senders) - should return how to display multiple
                senders to a channel
        pose_transform(msg, sender_string) - should detect if the
                sender is posing, and if so, modify the string
        format_external(msg, senders, emit=False) - format messages sent
                from outside the game, like from IRC
        format_message(msg, emit=False) - format the message body before
                displaying it to the user. 'emit' generally means that the
                message should not be displayed with the sender's name.

        pre_join_channel(joiner) - if returning False, abort join
        post_join_channel(joiner) - called right after successful join
        pre_leave_channel(leaver) - if returning False, abort leave
        post_leave_channel(leaver) - called right after successful leave
        pre_send_message(msg) - runs just before a message is sent to channel
        post_send_message(msg) - called just after message was sent to channel

    """

    def channel_prefix(self, msg, emit=False):
        return '%s[{key}]|n '.format(key=self.key) % self.db.color


    def at_channel_creation(self):
        if self.key.lower() == 'chat':
            self.db.color = "|y"

        elif self.key.lower() == 'system':
            self.db.color = "|g"

        elif self.key.lower() == 'info':
            self.db.color = "|y"

        else:  # color coding this channel red if no matches
            self.db.color = '|r'


    def pose_transform(self, msgobj, sender_string):
        """transform messages with a named sender (like [Public] Griatch: Hello)"""
        current_time = ""
        pref = ''
        h = time.localtime().tm_hour
        m = time.localtime().tm_min
        s = time.localtime().tm_sec

        if h in range(0, 12):
            pref += 'am'

        elif h in range(12, 24):
            pref += 'pm'

        if h == 0:
            h = 12

        if h > 12:
            h -= 12

        h = str(h)
        m = str(m)
        s = str(s)

        if len(m) == 1:
            m = '0' + m

        if len(s) == 1:
            s = '0' + s

        current_time = '{hour}:{minute}:{second}:{pref}'.format(hour=h, minute=m, second=s, pref=pref)

        msgobj.message = "%s[{time}] {name} : {message}|n".format(time=current_time, name=sender_string, message=msgobj.message) % self.db.color
        # return super(Channel, self).pose_transform(msgobj, sender_string)
        return msgobj.message


