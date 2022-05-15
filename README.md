# Nine Patch Image Optimiser

The python script to check image to make nine patch image and reduce it size.

![](/nine-patch-example.png)


# Usage

The script using the [imagemagick Wand](https://docs.wand-py.org/en/0.6.7/). To install it use next command:
``` 
$ pip install Wand
```

You can pass folder with images, the output folder will be created nearby with script file

`python parse_directory.py ./path_to_image_folder`

You can pass single image and pass the output name (or it will create the same image nearby script file)

`python parse_file.py ./path_to_image.png ./path_to_output_image.png`


The image output:

![](/tool-example.png)


# Output

For every processed image you will get the next output (I recommend you to store all processed info to single file to check image settings later)

```
Image: button_purple.png Output: button_purple.png Origin Size: 368x128 New Size: 122x128 9Patch side: [60, 0, 60, 0] Saved: 66.85%
```

To use image as before, set in the editor nine patch settings:
`60 (from left) 0 (from top) 60 (from right) 0 (from bottom)`

And set node size to origin size:
`Origin Size: 368x128`


