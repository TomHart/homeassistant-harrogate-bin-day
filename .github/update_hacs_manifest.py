"""Update the manifest file."""
import json
import os
import sys


def update_manifest():
    """Update the manifest file."""
    version = "0.0.0"
    for index, value in enumerate(sys.argv):
        if value in ["--version", "-V"]:
            version = sys.argv[index + 1]

    with open(
        f"{os.getcwd()}/custom_components/harrogate_bin/manifest.json"
    ) as manifest_file:
        manifest = json.load(manifest_file)

    manifest["version"] = version

    with open(
        f"{os.getcwd()}/custom_components/harrogate_bin/manifest.json", "w"
    ) as manifest_file:
        manifest_file.write(json.dumps(manifest, indent=4, sort_keys=True))


update_manifest()
