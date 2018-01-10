' Reminders
---
These are just some things to remind me when I am adding new features to the project.

Jinja macros do not automatically get the context from the page that they are imported into.
To pass the context amend the line that reads {% import [macro_file_here] as x %} to read
{% import [macro_file_here] as x with context %}
