# Sincrest

Music notation and composition software, built by Sseruwagi Sinclaire Sebastian.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

Sincrest is an open source and free music notation software. Fork and make pull requests!

## Features

- WYSIWYG design, notes are entered on a "virtual notepaper"
- TrueType font(s) for printing & display allows for high quality scaling to all sizes
- Easy & fast note entry
- Many editing functions
- MusicXML import/export
- MIDI (SMF) import/export
- MEI import/export
- MuseData import
- MIDI input for note entry
- Integrated sequencer and software synthesizer to play the score
- Print or create PDF files

## License

Sincrest is licensed under GPL version 3.0. See [license file](LICENSE.txt) in the same directory.

## Building

### Getting sources

If using git to download repo of entire code history, type:

    git clone --recurse-submodules https://github.com/CCRI-TCRI/Sincrest.git
    cd Sincrest

(The `--recurse-submodules` ensures that the `muse_framework` git submodule is checked out into the `muse/` subdirectory.)

### Release Build

To compile Sincrest for release, type:

    cmake -P build.cmake -DCMAKE_BUILD_TYPE=Release

On MacOS, append `-G Ninja` in order to use the `ninja` build tool (which you may need to install), since this
is required to compile Swift components.

If something goes wrong, append the word "clean" to the above command to delete the build subdirectory:

    cmake -P build.cmake -DCMAKE_BUILD_TYPE=Release clean

Then try running the first command again.

### Running

To start Sincrest, type:

    cmake -P build.cmake -DCMAKE_BUILD_TYPE=Release run

Or run the compiled executable directly.

### Debug Build

A debug version can be built and run by replacing `-DCMAKE_BUILD_TYPE=Release`
with `-DCMAKE_BUILD_TYPE=Debug` in the above commands.

If you omit the `-DCMAKE_BUILD_TYPE` option entirely then `RelWithDebInfo` is
used by default, as it provides a useful compromise between Release and Debug.

### Testing

Run the test suite via CTest after building.

### Code Formatting

Run `./hooks/install.sh` to install a pre-commit hook that will format your staged files. Requires that you install `uncrustify`.

If you have problems, please report them. To uninstall, run `./hooks/uninstall.sh`.
