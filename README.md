![blenderaddon_badge](https://img.shields.io/badge/-Blender%20Addon-%23eb7700)
![size_badge](https://img.shields.io/github/repo-size/daveiator/shutdown-after-render?label=Size)
![licence_badge](https://img.shields.io/github/license/daveiator/shutdown-after-render)

# Shutdown after Render

A addon for Blender which shuts down your PC after your render finishes.



## Panel location:
The Panel is located in the __Output Properties__ _(Properties > Output > Shutdown after Render)_:


![panel location](https://user-images.githubusercontent.com/43887102/175784792-e523f098-4051-45ff-9f80-ed10acca620d.png)

## Usage:

To activate the shutdown after render function, simply press the __Power-Icon__ at the top of the panel:

![panel activate](https://user-images.githubusercontent.com/43887102/175784819-ba01a5c6-93b9-4930-b8a8-cc21ac4cb6db.png)

### Shutdown-Type
After that you will have acces to the Dropdown-List which lets you specify the exact shutdown type.
The options are:
* Shutdown (DEFAULT)
  - Shuts down your PC completely.

* Hibernate
  - Shuts down your PC, but puts remembers the state of all open applications, and reopens them once you start your PC again.
  
* Quit
  - This just quits Blender.

### Extras
Also included in this plugin is this extra section:

![extra_section](https://user-images.githubusercontent.com/43887102/175785330-ff3d725c-6594-4cdb-8488-21d1e19e1c09.png)

For some reason Blender doesn't safe rendered stills automatically to the output-folder, like with animations. This is not optimal, especially when you want to shutdown your PC.

* __"Render Image to Output Folder"__  does exactly that and should be used if you want to render stills with __"Shutdown after Render"__ enabled.  _(The __"File Output"__ node in the compositor is also a great alternative.)_

* __"Render Animation to Output Folder"__ works exactly like the default __"Render Animation"__ button and is only here for completeness.

## Support

There are currently no new features planned for this project . However, Issue reports, contributions or ideas are welcome! :)

## License

MIT License Please see LICENSE for details.

## ⚠️
The shutdown commands are only guarranteed to work on Windows. Linux and MacOS have not been tested! Maybe it works, maybe not. I only plan on using this addon on Windows, but if you have another OS and it doesn't work, please file an Issue! 
