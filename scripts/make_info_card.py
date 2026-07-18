import json
from pathlib import Path

# Read profile.json
with open("data/profile.json", "r") as f:
    profile = json.load(f)

svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="520" height="250">

<rect width="520" height="250" fill="#0d1117"/>

<text x="20" y="35"
font-size="22"
font-family="monospace"
fill="#39d353">

$ whoami

</text>

<text x="20" y="75"
font-size="16"
font-family="monospace"
fill="#c9d1d9">

Name       : {profile["name"]}

</text>

<text x="20" y="100"
font-size="16"
font-family="monospace"
fill="#c9d1d9">

Role       : {profile["role"]}

</text>

<text x="20" y="125"
font-size="16"
font-family="monospace"
fill="#c9d1d9">

College    : {profile["college"]}

</text>

<text x="20" y="150"
font-size="16"
font-family="monospace"
fill="#c9d1d9">

Focus      : {profile["focus"]}

</text>

<text x="20" y="175"
font-size="16"
font-family="monospace"
fill="#c9d1d9">

Learning   : {profile["learning"]}

</text>

<text x="20" y="200"
font-size="16"
font-family="monospace"
fill="#39d353">

Status     : {profile["status"]}

</text>

</svg>
"""

Path("assets").mkdir(exist_ok=True)

with open("assets/info-card.svg", "w") as f:
    f.write(svg)

print("Generated assets/info-card.svg")