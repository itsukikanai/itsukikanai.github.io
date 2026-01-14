from app.ui import create_ui

import os

if __name__ == "__main__":
    demo = create_ui()
    # Ensure we use absolute paths for allowed_paths
    base_path = os.path.abspath(".")
    demo.launch(css="assets/custom.css", allowed_paths=[base_path], inbrowser=True)
