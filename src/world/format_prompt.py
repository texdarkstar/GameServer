from evennia.utils import inherits_from


def format_prompt(string, player):
    prompt_vars = {}
    prompt_vars["$P"] = player.key

    try:
        prompt_vars["$p"] = player.get_puppet(player.sessions.get()[0]).key
    except:
        prompt_vars["$p"] = "None"


    for key in prompt_vars:
        try:
            string = string.replace(key, prompt_vars[key])
        except TypeError:
            pass

    return string
