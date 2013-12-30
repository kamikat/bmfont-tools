bmfont tools
============

CLI utility helps crack raw bitmap font.

Usage
-----

* entropy.py

  Apply entropy analysis to help figure out proper bitmap dimension. It may
  take a loooooong time calculating the whole result and it is recommended
  to get the output csv file visualized to pick up a proper width/height of
  the file.

  Typically, the dimension with lower entropy is more likely to be the one.

  Output csv file is in "horizontial_tiles, entropy" format, to calculate
  vertical_tiles, divide total tile count by horizontial tiles. And to get
  width and height in pixel, multiply dimension of a single tile.

License
-------

(The MIT License)

