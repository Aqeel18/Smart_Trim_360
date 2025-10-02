import os
import json
import re

GITHUB_REPO = "Aqeel18/Smart_Trim_360"
GITHUB_URL = f"https://github.com/{GITHUB_REPO}"
COLAB_PREFIX = f"https://colab.research.google.com/github/{GITHUB_REPO}/blob/main/"

def update_notebook_metadata(nb_path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    changed = False
    if "colab" in nb.get("metadata", {}):
        nb["metadata"]["colab"]["name"] = os.path.basename(nb_path)
        nb["metadata"]["colab"]["provenance"] = []
        nb["metadata"]["colab"]["private_outputs"] = True
        nb["metadata"]["colab"]["toc_visible"] = True
        nb["metadata"]["colab"]["authorship_tag"] = "github"
        changed = True
    # Add or update colab metadata if missing
    if "colab" not in nb.get("metadata", {}):
        nb.setdefault("metadata", {})["colab"] = {
            "name": os.path.basename(nb_path),
            "provenance": [],
            "private_outputs": True,
            "toc_visible": True,
            "authorship_tag": "github"
        }
        changed = True
    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"Updated Colab metadata in: {nb_path}")

def update_readme_badge(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Regex to find Colab badge and update the link
    new_content = re.sub(
        r'(https://colab\\.research\\.google\\.com/github/)[^/]+/[^/]+/blob/main/([^\)\s]+)',
        rf'\1{GITHUB_REPO}/blob/main/\2',
        content
    )
    if new_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated Colab badge in: {readme_path}")

def main():
    # Update all .ipynb files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".ipynb"):
                update_notebook_metadata(os.path.join(root, file))
    # Update README.md badge
    if os.path.exists("README.md"):
        update_readme_badge("README.md")
    print("All done! Your notebooks and README now point to your GitHub repo.")

if __name__ == "__main__":
    main()
