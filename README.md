# MaGAI - Manim Gui AI
This project aims to create an GUI application targeted at teachers and students for creating interactive manim animations during classes and studies without focusing too much on coding. The main attraction/ selling point for this app should be its easy to use GUI and a reliable AI to translate user's prompt into animations (current AI's like ChatGPT produce unreliable and imprecise animations)

## Folder Structure
We'll follow the MVC (Model-View-Controller) approach:
Main Directory/
│── main.py             → Entry point, initializes the app.
│── ui_main.py          → Main UI logic (ManimUI class).
│── sidebar.py          → Left Sidebar (Animations, Objects)
│── editor.py           → File Editor, AI Prompt, Terminal
│── right_sidebar.py    → Scrollable "Default Objects" list
│── terminal.py         → Terminal interaction
│── manim_runner.py     → Runs Manim animation
│── Canvas.py           → Manim scene

##
Run main.py for the app to start
