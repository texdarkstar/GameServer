from command import Command


class CmdInflict(Command):
    """Syntax: @inflict <damage> <target>
        This command will inflict damage to a target, by id or name.
        It is the opposite of |w@uninflict|n, and deals damage in the order of:
        1. endurance
        2. strength
        3. dexterity

        If a single call will bring endurance from its maximum to zero, the target will be rendered unconcious.
        If all physical characteristics are brought to zero, the target will be rendered dead.

        Damage sucks, hope you brought a decent surgeon!  (And a merciful gamemaster, that always helps...)
    """
    locks = 'cmd:perm(Wizards) or attr(GM, True)'

    key = "@inflict"
    aliases = ["inflict", "inf"]

    help_category = "Gaming"

    def func(self):
        args = self.args.strip().split()
        try:
            damage, who = args
        except ValueError:
            self.caller.msg("Syntax: @inflict <damage> <target>")
            return

        try:
            damage = int(damage)
            _damage = damage
        except ValueError:
            self.caller.msg("Damage must be an integer.")
            return

        target = self.caller.search(who)  # global_search=True

        if target and target.player:
            attrs = target.db.attrs
            cstr = attrs['str']['current']
            cend = attrs['end']['current']
            cdex = attrs['dex']['current']

            bstr = attrs['str']['base']
            bend = attrs['end']['base']
            bdex = attrs['dex']['base']

            if damage > 0:
                if cend == bend and damage == cend:
                    cend = 0
                    damage = 0
                    # he is now unconcious

                elif (cend - damage) > 0:
                    cend -= damage
                    damage = 0
                    # endurance soaked it all up

                elif (cend - damage) < 0:
                    damage -= cend
                    cend = 0

            if damage > 0:
                if cstr == bstr and damage == cstr:
                    cstr = 0
                    damage = 0
                    # he is now unconcious

                elif (cstr - damage) > 0:
                    cstr -= damage
                    damage = 0
                    # strength soaked it all up

                elif (cstr - damage) < 0:
                    damage -= cstr
                    cstr = 0

            if damage > 0:
                if cdex == bdex and damage == cdex:
                    cend = 0
                    damage = 0
                    # he is now unconcious

                elif (cdex - damage) > 0:
                    cdex -= damage
                    # dexterity soaked it all up

                elif (cdex - damage) < 0:
                    damage -= cdex
                    cdex = 0

            target.db.attrs['str']['current'] = cstr
            target.db.attrs['end']['current'] = cend
            target.db.attrs['dex']['current'] = cdex

            self.caller.msg("Okay, inflicted %d damage to %s." % (_damage, target.name))
            target.msg("%s inflicted %d damage to you." % (self.caller.name, _damage))
            return

        elif target and not target.player:
            self.caller.msg("{target} isn't online.".format(target=target.name))
            return
            
        elif not target:
            self.caller.msg("{target} doesn't exist.".format(target=who))
            return


class CmdUninflict(Command):
    """Syntax: @uninflict <damage> <target>
        This command will heal damage taken to a target, by id or name, providing it was injured in the first place.
        It is the opposite of |w@inflict|n, and heals damage in the order of:
        1. endurance
        2. strength
        3. dexterity

        Those silly players...
        """
    locks = 'cmd:perm(Wizards) or attr(GM, True)'

    key = "@uninflict"
    aliases = ["uninflict", "uninf"]

    help_category = "Gaming"


    def func(self):
        args = self.args.strip().split()
        try:
            damage, who = args
        except ValueError:
            self.caller.msg("Syntax: @uninflict <damage> <target>")
            return

        try:
            damage = int(damage)
            _damage = damage
        except ValueError:
            self.caller.msg("Damage must be an integer.")
            return

        target = self.caller.search(who)  # global_search=True

        if target and target.player:
            attrs = target.db.attrs
            cstr = attrs['str']['current']
            cend = attrs['end']['current']
            cdex = attrs['dex']['current']

            bstr = attrs['str']['base']
            bend = attrs['end']['base']
            bdex = attrs['dex']['base']


            if damage > 0 and cend < bend:
                if damage >= (bend - cend):
                    damage -= (bend - cend)
                    cend = bend

                elif damage < (bend - cend):
                    cend += damage
                    damage = 0

            if damage > 0 and cstr < bstr:
                if damage >= (bstr - cstr):
                    damage -= (bstr - cstr)
                    cstr = bstr

                elif damage < (bstr - cstr):
                    cstr += damage
                    damage = 0

            if damage > 0 and cdex < bdex:
                if damage >= (bdex - cdex):
                    damage -= (bdex - cdex)
                    cdex = bdex

                elif damage < (bdex - cdex):
                    cdex += damage
                    damage = 0

            target.db.attrs['str']['current'] = cstr
            target.db.attrs['end']['current'] = cend
            target.db.attrs['dex']['current'] = cdex

            self.caller.msg("Okay, healed %d damage from %s." % (_damage, target.name))
            target.msg("%s healed %d damage from you." % (self.caller.name, _damage))
            return

        elif target and not target.player:
            self.caller.msg("{target} isn't online.".format(target=target.name))
            return
            
        elif not target:
            self.caller.msg("{target} doesn't exist.".format(target=who))
            return
