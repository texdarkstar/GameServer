from builtins import range

import time
from django.conf import settings
from evennia.server.sessionhandler import SESSIONS
from evennia.utils import utils, create, search, evtable


COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)

_MAX_NR_CHARACTERS = settings.MAX_NR_CHARACTERS
_MULTISESSION_MODE = settings.MULTISESSION_MODE


class CmdWho(COMMAND_DEFAULT_CLASS):
    """
    list who is currently online

    Usage:
      who
      doing

    Shows who is currently online. Doing is an alias that limits info
    also for those with all permissions.
    """

    key = "who"
    aliases = "doing"
    locks = "cmd:all()"

    # this is used by the parent
    player_caller = True

    def func(self):
        """
        Get all connected players by polling session.
        """

        player = self.player
        session_list = SESSIONS.get_sessions()

        session_list = sorted(session_list, key=lambda o: o.player.key)

        if self.cmdstring == "doing":
            show_session_data = False
        else:
            show_session_data = player.check_permstring("Immortals") or player.check_permstring("Wizards")

        nplayers = (SESSIONS.player_count())
        if show_session_data:
            # privileged info
            table = evtable.EvTable("|wPlayer Name",
                                    "|wOn for",
                                    "|wIdle",
                                    "|wPuppeting",
                                    "|wRoom",
                                    "|wCmds",
                                    "|wProtocol",
                                    "|wHost")
            for session in session_list:
                if not session.logged_in:
                    continue
                delta_cmd = time.time() - session.cmd_last_visible
                delta_conn = time.time() - session.conn_time
                player = session.get_player()
                puppet = session.get_puppet()
                location = puppet.location.key if puppet and puppet.location else "None"
                table.add_row(utils.crop(player.name, width=25),
                              utils.time_format(delta_conn, 0),
                              utils.time_format(delta_cmd, 1),
                              utils.crop(puppet.key if puppet else "None", width=25),
                              utils.crop(location, width=25),
                              session.cmd_total,
                              session.protocol_key,
                              isinstance(session.address, tuple) and session.address[0] or session.address)
        else:
            # unprivileged
            table = evtable.EvTable("|wPlayer name", "|wOn for", "|wIdle")
            for session in session_list:
                if not session.logged_in:
                    continue
                puppet = session.get_puppet()
                if puppet.db.invisible:
                    continue

                delta_cmd = time.time() - session.cmd_last_visible
                delta_conn = time.time() - session.conn_time
                player = session.get_player()
                table.add_row(utils.crop(player.key, width=25),
                              utils.time_format(delta_conn, 0),
                              utils.time_format(delta_cmd, 1))
        is_one = nplayers == 1
        self.msg("|wPlayers:|n\n%s\n%s unique account%s logged in."
                 % (table, "One" if is_one else nplayers, "" if is_one else "s"))

