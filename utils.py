import os
import datetime

def format_results(paths):
    """
    Format and display file metadata results.
    
    Args:
        paths (list): List of file paths from search results
    Returns:
        str: Formatted display string
    """
    if not paths:
        return "❌ No matching documents found."

    lines = ["\n📄 Top Matching Files:"]
    count = 0

    for path in paths:
        if not os.path.exists(path):
            continue  # Skip if file doesn't exist

        count += 1
        name = os.path.basename(path)
        filetype = os.path.splitext(path)[1][1:].title() or "Unknown"

        try:
            modified_ts = os.path.getmtime(path)
            modified_date = datetime.datetime.fromtimestamp(modified_ts).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            modified_date = "N/A"

        lines.append(
            f"\n🔹 File {count}:\n"
            f"   📄 Name     : {name}\n"
            f"   📁 Path     : {path}\n"
            f"   🕒 Modified : {modified_date}\n"
            f"   📦 Type     : {filetype}"
        )

        if count == 5:
            break  # Limit to top 5 results

    if count == 0:
        return "❌ No valid (existing) files found."

    return "\n".join(lines)
