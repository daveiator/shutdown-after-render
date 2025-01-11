# Shutdown after Render

Automatically shuts down your PC after your render finishes.



## Panel location:
The Panel is located in the __Render Properties__ _(Properties > Render > Shutdown after Render)_:

## Usage:

To activate the shutdown after render function, simply press the __Power-Icon__ at the top of the panel:

![panel_activate](https://github.com/user-attachments/assets/7961ab77-7614-4b17-95f8-14f3e1352ba7)


### Shutdown-Type
Choose your desired action in the Dropdown-List.
The options are:
* Shutdown (default)
  - Shuts down your PC completely.

* Hibernate
  - Shuts down your PC, but puts remembers the state of all open applications, and reopens them once you start your PC again.
  
* Quit
  - Quits the Blender application.

### Important!

Blender doesn't automatically safe rendered stills to the output-folder, like with animations. This is not optimal, especially when you want to shutdown your PC.

For this reason the addon comes with an addidtional render button in the **render top menu**:

![render_panel](https://github.com/user-attachments/assets/d752e10e-7b6b-4526-9fab-91e8ebe7a63b)

*Render Image to Disk*

It simply renders the active scene like normal, but saves the image afterwards to the path specified in the **Output Properties**

Another option would be to use the "**File Output**"-Node in the compositor.

### Custom Commands
The commands used for shutdown, hiberation and canceling the shutdown can be customized in the **Addon Preferences**: 
