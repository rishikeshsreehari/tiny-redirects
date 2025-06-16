import os
import yaml
import re
import glob

# Paths
REDIRECTS_FOLDER = "./redirects"
OUTPUT_FILE = "./_redirects"

def read_redirects(folder_path):
    """
    Read all YAML files in the folder and collect redirects.
    Supports both plain list and dict with 'redirects' key.
    """
    redirects = []
    redirect_file_count = 0
    for file_path in glob.glob(os.path.join(folder_path, "*.yaml")):
        redirect_file_count += 1
        file_redirects = 0
        with open(file_path, "r") as file:
            try:
                data = yaml.safe_load(file)
                if data is None:
                    print(f"Warning: {file_path} is empty or invalid, skipping.")
                    continue

                # Support both list of redirects or dict with key 'redirects'
                if isinstance(data, dict) and "redirects" in data:
                    entries = data["redirects"]
                elif isinstance(data, list):
                    entries = data
                else:
                    print(f"Warning: Unrecognized format in {file_path}, skipping.")
                    continue

                for entry in entries:
                    short_url = entry.get("short_url")
                    target_url = entry.get("target_url")
                    status_code = entry.get("status_code", 301)  # Default to 301
                    if short_url and target_url:
                        redirects.append((short_url, target_url, status_code))
                        file_redirects += 1
            except yaml.YAMLError as e:
                print(f"Error parsing {file_path}: {e}")

        print(f"Found {file_redirects} redirects in {os.path.basename(file_path)}")

    print(f"Total {redirect_file_count} redirect files found.")
    return redirects

def validate_redirects(redirects):
    """
    Validate the redirects:
    - No duplicate short URLs.
    - Valid URL format for target URLs.
    - Valid status codes (301 or 302).
    """
    seen = set()
    url_pattern = re.compile(r'^(http|https)://[a-zA-Z0-9.-]+(:[0-9]+)?(/.*)?$')

    for short_url, target_url, status_code in redirects:
        if short_url in seen:
            raise ValueError(f"Duplicate short URL detected: {short_url}")
        seen.add(short_url)

        if not short_url.startswith("/"):
            raise ValueError(f"Invalid short URL (must start with '/'): {short_url}")

        if not url_pattern.match(target_url):
            raise ValueError(f"Invalid target URL format: {target_url}")

        if status_code not in [301, 302]:
            raise ValueError(f"Invalid status code (must be 301 or 302): {status_code}")

def write_redirects(redirects, output_file):
    """
    Write the combined redirects to the _redirects file.
    """
    with open(output_file, "w") as file:
        for short_url, target_url, status_code in redirects:
            file.write(f"{short_url} {target_url} {status_code}\n")
    print(f"Total {len(redirects)} redirects added to {output_file}")

if __name__ == "__main__":
    try:
        redirects = read_redirects(REDIRECTS_FOLDER)
        validate_redirects(redirects)
        print("Validation passed. No issues detected.")
        write_redirects(redirects, OUTPUT_FILE)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
