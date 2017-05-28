from django.http import Http404
from django.shortcuts import render
from evennia.help.models import HelpEntry

from typeclasses.characters import Character
from world.cull_colors import cull_colors as cull


def index(request):
    """The 'index' view."""
    user = request.user

    if not user.is_anonymous() and user.character:
        character = user.character
    else:
        try:
            character = Character.objects.get(id=user.id)
        except:
            character = Character.objects.get(db_key="anonymous")

    # Get the categories and topics accessible to this character
    categories, topics = _get_topics(character)

    # If we have the 'name' in our GET variable
    topic = request.GET.get("name")
    if topic:
        if topic not in topics:
            raise Http404("This help topic doesn't exist.")

        topic = topics[topic]
        topic['content'] = cull(topic['content'])
        context = {
                "character": character,
                "topic": topic,
        }
        return render(request, "help_system/detail.html", context)
    else:
        context = {
                "character": character,
                "categories": categories,
        }
        return render(request, "help_system/index.html", context)

def _get_topics(character):
    """Return the categories and topics for this character."""
    cmdset = character.cmdset.all()[0]
    commands = cmdset.commands
    entries = [entry for entry in HelpEntry.objects.all()]
    categories = {}
    topics = {}

    # Browse commands
    for command in commands:
        if not command.auto_help or not command.access(character):
            continue

        # Create the template for a command
        template = {
                "name": command.key,
                "category": command.help_category,
                "content": command.get_help(character, cmdset),
        }

        category = command.help_category
        if category not in categories:
            categories[category] = []
        categories[category].append(template)
        topics[command.key] = template

    # Browse through the help entries
    for entry in entries:
        if not entry.access(character, 'view', default=True):
            continue

        # Create the template for an entry
        template = {
                "name": entry.key,
                "category": entry.help_category,
                "content": entry.entrytext,
        }

        category = entry.help_category
        if category not in categories:
            categories[category] = []
        categories[category].append(template)
        topics[entry.key] = template

    # Sort categories
    for entries in categories.values():
        entries.sort(key=lambda c: c["name"])

    categories = sorted(categories.items())
    return categories, topics