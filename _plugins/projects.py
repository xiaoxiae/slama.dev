#!/usr/bin/env python3

import os
import requests

try:
    from github import Github

    from secrets import github_token

    g = Github(github_token)

    # (GitHub name, override display name, override language)
    projects = [
        ("climber-apps", "Clis", None, "Fusion 360, Python"),
        ("climber-apps", "Cled", None, "C# (Unity)"),
        (None, "Florodoro", None, "Python (PyQt5)"),
        (None, "Donjun", None, None),
        (None, "Grafatko", "Grafátko", "Python (PyQt5)"),
        (None, "Voronoi", None, None),
        (None, "CV", "CV generator", "Python, LaTeX"),
        (None, "Smichoff-Trophy", "Smíchoff Trophy", "Fusion 360"),
    ]

    result = ""
    i = 0
    for owner, project, name, language in projects:
        repo = g.get_repo(f"{owner or 'xiaoxiae'}/{project}")

        result += f"""<table class="gh{'Right' if i % 2 == 1 else 'Left'}">
        <thead>
          <tr>
            <th class="ghName" colspan="2"><a href="{repo.html_url}">{name or repo.name}</a></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="ghDescription" colspan="2">{repo.description}</td>
          </tr>
          <tr>
            <td class="ghStars"></td>
            <td class="ghLang">{language or repo.language}</td>
          </tr>
        </tbody>
        </table>"""

        i += 1

    base = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(base, "../_includes/projects.md"), "w") as f:
        f.write(result)

    print("generated.", flush=True)
except requests.exceptions.ConnectionError:
    print("network could not be reached, projects not generated.", flush=True)
