import os
import sys
import time

def safe_save(prs, path):
    try:
        prs.save(path)
        print(f"Successfully saved: {path}")
        return path
    except PermissionError:
        print(f"Warning: {path} is currently locked by PowerPoint. Trying fallback filenames...")
        base, ext = os.path.splitext(path)
        candidates = [
            f"{base}_教材对齐版{ext}",
            f"{base}_最新{ext}",
            f"{base}_v{int(time.time())}{ext}"
        ]
        for fallback_path in candidates:
            try:
                prs.save(fallback_path)
                print(f"Successfully saved to fallback: {fallback_path}")
                return fallback_path
            except Exception:
                continue
        print(f"Failed to save to any fallback path for {path}")
    except Exception as e:
        print(f"Error saving {path}: {e}")
    return None
