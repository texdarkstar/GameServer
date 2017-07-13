from django.conf import settings
from collections import defaultdict
from evennia.utils.utils import fill, dedent
from command import Command
from evennia.help.models import HelpEntry
from evennia.utils import create, evmore
from evennia.utils.eveditor import EvEditor
from evennia.utils.utils import string_suggestions, class_from_module

COMMAND_DEFAULT_CLASS = class_from_module(settings.COMMAND_DEFAULT_CLASS)

# limit symbol import for API
__all__ = ("CmdHelp", "CmdSetHelp")
_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH
_SEP = "|C" + "-" * _DEFAULT_WIDTH + "|n"



class CmdHelp(Command):
    """
    View help or a list of topics

    Usage:
      help <topic or command>
      help list
      help all

    This will search for help on commands and other
    topics related to the game.
    """
    key = "help"
    aliases = ['?']
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    # this is a special cmdhandler flag that makes the cmdhandler also pack
    # the current cmdset with the call to self.func().
    return_cmdset = True

    # Help messages are wrapped in an EvMore call (unless using the webclient
    # with separate help popups) If you want to avoid this, simply set the
    # 'help_more' flag to False.
    help_more = True

    def msg_help(self, text):
        """
        messages text to the caller, adding an extra oob argument to indicate
        that this is a help command result and could be rendered in a separate
        help window
        """
        if type(self).help_more:
            usemore = True

            if self.session.protocol_key in ("websocket", "ajax/comet"):
                try:
                    options = self.player.db._saved_webclient_options
                    if options and options["helppopup"]:
                        usemore = False
                except KeyError:
                    pass

            if usemore:
                evmore.msg(self.caller, text)
                return

        self.msg((text, {"type": "help"}))

    @staticmethod
    def format_help_entry(title, help_text, aliases=None, suggested=None):
        """
        This visually formats the help entry.
        This method can be overriden to customize the way a help
        entry is displayed.

        Args:
            title (str): the title of the help entry.
            help_text (str): the text of the help entry.
            aliases (list of str or None): the list of aliases.
            suggested (list of str or None): suggested reading.

        Returns the formatted string, ready to be sent.

        """
        string = _SEP + "\n"
        if title:
            string += "|CHelp for |w%s|n" % title
        if aliases:
            string += " |C(aliases: %s|C)|n" % ("|C,|n ".join("|w%s|n" % ali for ali in aliases))
        if help_text:
            string += "\n%s" % dedent(help_text.rstrip())
        if suggested:
            string += "\n\n|CSuggested:|n "
            string += "%s" % fill("|C,|n ".join("|w%s|n" % sug for sug in suggested))
        string.strip()
        string += "\n" + _SEP
        return string

    @staticmethod
    def format_help_list(hdict_cmds, hdict_db):
        """
        Output a category-ordered list. The input are the
        pre-loaded help files for commands and database-helpfiles
        respectively.  You can override this method to return a
        custom display of the list of commands and topics.
        """
        string = ""
        if hdict_cmds and any(hdict_cmds.values()):
            string += "\n" + _SEP + "\n   |CCommand help entries|n\n" + _SEP
            for category in sorted(hdict_cmds.keys()):
                string += "\n  |w%s|n:\n" % (str(category).title())
                string += "|G" + fill("|C, |G".join(sorted(hdict_cmds[category]))) + "|n"
        if hdict_db and any(hdict_db.values()):
            string += "\n\n" + _SEP + "\n\r  |COther help entries|n\n" + _SEP
            for category in sorted(hdict_db.keys()):
                string += "\n\r  |w%s|n:\n" % (str(category).title())
                string += "|G" + fill(", ".join(sorted([str(topic) for topic in hdict_db[category]]))) + "|n"
        return string

    def check_show_help(self, cmd, caller):
        """
        Helper method. If this return True, the given cmd
        auto-help will be viewable in the help listing.
        Override this to easily select what is shown to
        the player. Note that only commands available
        in the caller's merged cmdset are available.

        Args:
            cmd (Command): Command class from the merged cmdset
            caller (Character, Player or Session): The current caller
                executing the help command.

        """
        # return only those with auto_help set and passing the cmd: lock
        return cmd.auto_help and cmd.access(caller)

    def should_list_cmd(self, cmd, caller):
        """
        Should the specified command appear in the help table?

        This method only checks whether a specified command should
        appear in the table of topics/commands.  The command can be
        used by the caller (see the 'check_show_help' method) and
        the command will still be available, for instance, if a
        character type 'help name of the command'.  However, if
        you return False, the specified command will not appear in
        the table.  This is sometimes useful to "hide" commands in
        the table, but still access them through the help system.

        Args:
            cmd: the command to be tested.
            caller: the caller of the help system.

        Return:
            True: the command should appear in the table.
            False: the command shouldn't appear in the table.

        """
        return True

    def parse(self):
        """
        input is a string containing the command or topic to match.
        """
        self.original_args = self.args.strip()
        self.args = self.args.strip().lower()

    def func(self):
        """
        Run the dynamic help entry creator.
        """
        query, cmdset = self.args, self.cmdset
        caller = self.caller

        suggestion_cutoff = 0.6
        suggestion_maxnum = 5

        if not query:
            query = "all"

        # removing doublets in cmdset, caused by cmdhandler
        # having to allow doublet commands to manage exits etc.
        cmdset.make_unique(caller)

        # retrieve all available commands and database topics
        all_cmds = [cmd for cmd in cmdset if self.check_show_help(cmd, caller)]
        all_topics = [topic for topic in HelpEntry.objects.all() if topic.access(caller, 'view', default=True)]
        all_categories = list(set([cmd.help_category.lower() for cmd in all_cmds] + [topic.help_category.lower() for topic in all_topics]))

        if query in ("list", "all"):
            # we want to list all available help entries, grouped by category
            hdict_cmd = defaultdict(list)
            hdict_topic = defaultdict(list)
            # create the dictionaries {category:[topic, topic ...]} required by format_help_list
            # Filter commands that should be reached by the help
            # system, but not be displayed in the table.
            for cmd in all_cmds:
                if self.should_list_cmd(cmd, caller):
                    hdict_cmd[cmd.help_category].append(cmd.key)
            [hdict_topic[topic.help_category].append(topic.key) for topic in all_topics]
            # report back
            self.msg_help(self.format_help_list(hdict_cmd, hdict_topic))
            return

        # Try to access a particular command

        # build vocabulary of suggestions and rate them by string similarity.
        vocabulary = [cmd.key for cmd in all_cmds if cmd] + [topic.key for topic in all_topics] + all_categories
        [vocabulary.extend(cmd.aliases) for cmd in all_cmds]
        suggestions = [sugg for sugg in string_suggestions(query, set(vocabulary), cutoff=suggestion_cutoff, maxnum=suggestion_maxnum)
                       if sugg != query]
        if not suggestions:
            suggestions = [sugg for sugg in vocabulary if sugg != query and sugg.startswith(query)]

        # try an exact command auto-help match
        match = [cmd for cmd in all_cmds if cmd == query]
        if len(match) == 1:
            formatted = self.format_help_entry(match[0].key,
                     match[0].get_help(caller, cmdset),
                     aliases=match[0].aliases,
                     suggested=suggestions)
            self.msg_help(formatted)
            return

        # try an exact database help entry match
        match = list(HelpEntry.objects.find_topicmatch(query, exact=True))
        if len(match) == 1:
            formatted = self.format_help_entry(match[0].key,
                     match[0].entrytext,
                     aliases=match[0].aliases.all(),
                     suggested=suggestions)
            self.msg_help(formatted)
            return

        # try to see if a category name was entered
        if query in all_categories:
            self.msg_help(self.format_help_list({query:[cmd.key for cmd in all_cmds if cmd.help_category==query]},
                                                {query:[topic.key for topic in all_topics if topic.help_category==query]}))
            return

        # no exact matches found. Just give suggestions.
        self.msg(self.format_help_entry("", "No help entry found for '%s'" % query, None, suggested=suggestions))

