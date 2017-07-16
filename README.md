# Spritesheet Capture
Captures anything on screen and saves them into a sprite sheet

## Getting Started
### Prerequisites
* PyQt5 - this is kinda a pain to set up. But if you're using [Anaconda](https://www.continuum.io/downloads) you can just use *conda*
```
conda install qtpy 
```
* [PIL](http://www.pythonware.com/products/pil/) - image processing library

### Using it
Can be used through command line
```
python cap.py -f 0.1 -d 5 -c 3 -o "output_path/output_file.png"
```
* **-f**:  time between each capture in seconds (default 0.05)
* **-d**:  total duration of capture in seconds (default 60)
* **-c**:  number of columns in the output sprite sheet, number of rows is dependent on total images and number of columns (default 10)
* **-o**:  output file path **AND** name (default "images/image.png")

## THANKS
Jack
