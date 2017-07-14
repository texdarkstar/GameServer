from evennia.utils import inherits_from


def format_prompt(string, obj):
    prompt_vars = {}

    if inherits_from(obj, "typeclasses.players.Player"):
        prompt_vars["$P"] = obj.key
        try:
            prompt_vars["$p"] = obj.puppet[0].key,
        except IndexError:
            prompt_vars["$p"] = "None"

    elif inherits_from(obj, "typeclasses.characters.Character"):
        prompt_vars = {
            "$P": obj.player.key,
            "$p": obj.key,
            }

    for key in prompt_vars:
        try:
            string = string.replace(key, prompt_vars[key])
        except TypeError:
            pass

    return string
