from evennia.utils import inherits_from


def format_prompt(string, obj):
    if inherits_from(obj, "typeclasses.players.Player"):
        prompt_vars = {
            "$P": obj.key,
            "$p": obj.puppet[0].key,
            }
    elif inherits_from(obj, "typeclasses.characters.Character"):
        prompt_vars = {
            "$P": obj.player.key,
            "$p": obj.key,
            }

    for key in prompt_vars:
        string = string.replace(key, prompt_vars[key])

    return string
