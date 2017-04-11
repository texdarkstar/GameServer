from command import Command


class CmdForce(Command):
    """Syntax: @force <player> <action>
        Forces the player to do 'action'.
    """
    locks = 'cmd:perm(Immortal)'

    key = "@force"
    aliases = ["force"]

    help_category = "Admin"


    def func(self):
        try:
            args = self.args.strip().split()
            who = args.pop(0)
            action = ' '.join(args).strip()

        except ValueError:
            self.caller.msg("Syntax: @force <player> <action>")
            return

        target = self.caller.search(who, global_search=True)

        if target and target.player:
            self.caller.msg("You force {name} to '{action}'.".format(name=target.name, action=action))
            target.msg("{name} forces you to '{action}'.".format(name=self.caller.name, action=action))
            target.execute_cmd(action, session=target.player.sessions.get()[0])
            return


        else:
            self.caller.msg("No such player connected.")
            return

