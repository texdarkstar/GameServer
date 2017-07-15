from command import Command


class CmdPrompt(Command):
    """Syntax @prompt <new prompt>

    This command will change your prompt, and it can be used to display certain information with special variables.
    The prompt saves to your Player object, so it is global across accounts.

    Hint, you can turn your prompt off completely by using |wconfig prompt|n if desired.

    Contact Texdarkstar for custom prompt variables if it isn't in this list.
    Evennia's usual text tags also work, see |bhttps://github.com/evennia/evennia/wiki/TextTags|n.

    Examples:
        @prompt $p > 
        @prompt $P: $p> 
        @prompt -=> 


    Available variables:
        $p - Your current puppet name/key
        $P - Your current player name/key
    """
    key = "@prompt"
    aliases = ["prompt"]
    locks = "cmd:all()"
    help_category = "Gaming"


    def func(self):
        args = self.args

        if args:
            self.caller.player.db.prompt = "|/" + args.strip() + "|/"
            self.caller.msg("Okay, prompt updated.")
            return

        elif not args:  # just a blank string
            self.caller.msg("No prompt provided. If you mean to turn your prompt off, use |wconfig prompt|n.")
            return

