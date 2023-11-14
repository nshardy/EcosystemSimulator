# Changelog

commit 8fbf30b8cf5c522bed6cae0c81e33f9c5d333b26 (HEAD -> master, origin/master)
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Wed Oct 11 17:27:43 2023 -0700

    Version 0.1.5.alpha
    
     - Updated CHANGELOG.md
        - added Version 0.1.4
     - Updated main.py
        - added comments
     - Updated hunter.py
        - currently adding basic ai funcionality
        - added sorting lists by distance to entity
     - Updated simulation.py
        - updated import stuff to reduce length of lines
        - updated entity update() function
     - Updated tester_entity.py
        - added base functions

commit 172e363a69826cd92956928fdf49471dc5228801 (HEAD -> master, origin/master)
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Mon Oct 9 10:21:33 2023 -0700

    Version 0.1.4
    Added hunters and updated the supporting code to account for it
    
     - Updated CHANGELOG.md
        - added Version 0.1.3
     - Updated main.py
        - added dt (Delta Time), the time inbetween frames
        - added a way to make a new simulation. KeyCode R
     - Updated entity.py
        - self.pos changed to random ranges in window_dimensions
     - Added hunter.py
        - updated update method to contain settings information
     - Updated settings.py
        - updated version
        - added hunter_color
        - added hunter_size
        - added testing_entity_color
        - added testing_entity_size
     - Updated simulation.py
        - made test_entities and hunters statically typed
        - added self.all_entities
        - updated entities.update
     - Updated tester_entity.py
        - removed self.pos change
        - updated update method to contain settings information

commit 8a00ec868dc9960c9d6e3cb61d0be20f804628bf (HEAD -> master, origin/master)
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Sat Oct 7 12:00:52 2023 -0700

    Version 0.1.3

    Added testing entites and updated the rest of the code to account for it

     - Updated .gitignore
        - deleted __pycache__/
        - deleted *.pyc
        - deleted *.pyo
     - Updated CHANGELOG.md
        - added Version 0.1.3-alpha.2
     - Added entity.py
        - added __init__() def
        - added self.window
        - added self.pos
        - added self.window
        - added update() def
     - Updated simulation.py
        - added entities list
        - added updating entities in entity list in update def
     - Updated tester_entity.py
        - added TestingEntity class which derives from entity

commit 6ab11b1b4105f1c9c6b2434fbb64736c80d8bc41 (HEAD -> master)
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Sat Oct 7 11:39:07 2023 -0700

    Version 0.1.3-alpha.2
    
     - Updated CHANGELOG.md
        - added Version 0.1.3-alpha.1
     - Updated simulation.py
        - removed the print method to make sure it was working

commit c293a5aa4c06975486575b691f11d12187f99149 (HEAD -> master)
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Wed Oct 4 08:22:23 2023 -0700

    Version 0.1.3-alpha.1
    
     - Updated CHANGELOG.md
        - added Version 0.1.3-alpha
     - Updated simulation.py
        - added 'self' parameter to update function

commit 8e3b24a4c38379157e0badaa54b6c7e71ba2cfde
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Wed Oct 4 08:17:07 2023 -0700

    Version 0.1.3-alpha
    
    - Updated CHANGELOG.md
       - added Version 0.1.2
    - Updated main.py
       - added update function from simulation
    - Updated README.md
       - added more information in terms of nonrunnable file
    - Updated simulation.py
       - added print line to debug

commit ad22243fa68bdf9cd0f4b614a660a22d9631007c (origin/master)
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Tue Oct 3 19:48:39 2023 -0700

    Version 0.1.2
    
     - Updated .gitignore
        - added .git/
        - added __pycache__/
        - added *.pyc
        - added *.pyo
     - Updated CHANGELOG.md
        - added version 0.1.1
     - Updated main.py
        - uses variables from settings.py
        - added documentation
        - creates simulation
     - Added settings.py
        - added version
        - added window_dimensions
        - added fps
     - Added simulation.py
        - added class Simulation
        - added def __init__
        - added def update
        - added docstrings to defining functions

commit fe803c066848d3cd133fe86809bcc366a589ade9
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Tue Oct 3 14:26:41 2023 -0700

    Version 0.1.1
    
     - Updated `CHANGELOG.md`
     - Added `main.py`

commit cf08653eb77e235eecd9e5f6a0ee31c48f59fb4d
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Tue Oct 3 14:15:12 2023 -0700

    Version 0.1.0
    
     - Added.gitignore
     - Added CHANGELOG.md
     - Added README.md

commit 3fa578cd2bd1cc42760ef373e546f70823d3fcf8
Author: Noah Hardy <hardysnoah@icloud.com>
Date:   Mon Oct 2 08:42:46 2023 -0700

    Initial commit
