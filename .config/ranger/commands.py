# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import *

# A simple command for demonstration purposes follows.
#------------------------------------------------------------------------------

# You can import any python module as needed.
import os

# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!
class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.  
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    def tab(self):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()

class setbg(Command):
    """:setbg <image>

    A command to temporarily set the background image of the desktop to the selected image file.
    """ 

    #base command
    def execute(self):
        if self.arg(1):
            bg = self.arg(1)
        else:
            bg = self.fm.thisfile.path
        
        self.fm.run("feh --bg-fill " + bg)

    #tab completion
    def tab(self):
        return self._tab_directory_content()

class setbg_always(Command):
    """:setbg_always <image>

    Permanently set background to desired image. Symlinks image to ~/Pictures/wallpaper.jpg
    """

    def execute(self):
        if self.arg(1):
            bg = str(self.fm.thisdir) + "/" + self.arg(1)
        else:
            bg = self.fm.thisfile.path

        self.fm.run("feh --bg-fill " + bg)
        self.fm.run("ln -sf " + bg + " ~/Pictures/wallpaper.jpg")

    def tab(self):
        return self._tab_directory_content()

#class download(Command):
#    """:download <web link>
#
#    Runs wget on the specified link and saves it to the current directory.
#    """
#
#    def execute(self):
#        if self.arg(1):
#            www = self.arg(1)
#            self.fm.run("wget " + www)
#        else:
#            return "Please enter a valid link to download!"
#
#    def tab(self):
#        return self._tab_directory_content()

