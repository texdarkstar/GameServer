from command import Command


class CmdSkill(Command):
    """Syntax: @skill <add/rem> <rank> <skillname> <target>
        Adds or removes a skill from/to a target at a specific rank.
        Example:
            @skill add 2 broker bob

        This will give bob rank 2 broker.
        Calling |w@skill|n multiple times is cumulative, meaning that if you add 2 broker to bob,
        calling the same command with the same arguments will make bob have broker at rank 4 (!).

        Skills are removed totally if the rank goes below zero (meaning unskilled), and there
        is a cap of rank five, mostly because anything above is ridiculous (even rank five is ridiculous).
        A rank of zero is allowed, representing minimial training in it (he avoids an unskilled penalty).

    """
    key = "@skill"
    aliases = ["skill"]
    locks = "cmd:perm(Wizards) or attr(GM, True)"
    help_category = "Gaming"


    def func(self):
        args = self.args.strip().lower().split()
        try:
            action, rank, skillname, who = args
            rank = int(rank)
            if rank < 0:
                self.caller.msg("Rank must be a postive integer.")
                return

        except (IndexError, ValueError):
            self.caller.msg("Syntax: @skill <add/rem> <rank> <skillname> <target>")
            return

        target = self.caller.search(who, global_search=True)

        if target and target.player:
            if action == "add":
                if skillname not in target.db.skills.keys():
                    target.db.skills[str(skillname)] = rank

                elif skillname in target.db.skills.keys():
                    target.db.skills[str(skillname)] += rank

                self.caller.msg("Okay, gave %d ranks of %s to %s." % (rank, skillname, target.name))


            elif action == "rem":
                if skillname in target.db.skills.keys():
                    target.db.skills[str(skillname)] -= rank

                    if target.db.skills[str(skillname)] < 0:
                        del target.db.skills[str(skillname)]

                self.caller.msg("Okay, removed %d ranks of %s from %s." % (rank, skillname, target.name))

            return


        elif not target:
            self.caller.msg("No such connected player.")
            return

