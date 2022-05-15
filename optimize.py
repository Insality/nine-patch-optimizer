import os
import sys
from wand.image import Image

THRESHOLD_COLOR = 0.05 # Threshold in per pixel compare (Disabled in is_row_similar function)
THRESHOLD_COUNT = 8 # Minimum length of reduce
OFFSET = 2 # In pixels of every chopped side, this is the half size of resulting stretchable side
PATCH_OFFSET = 1 # Offset for Nine patch image settings. Usually OFFSET / 2
THRESHOLD_PERCENT = 0.2 # Don't replace image, if we optimize it less than this percent

def is_row_similar(row1, row2):
    if row1 == row2:
        return True

    # for index in range(len(row1)):
    #     if (abs(row1[index].red - row2[index].red) < THRESHOLD_COLOR and
    #         abs(row1[index].blue - row2[index].blue) < THRESHOLD_COLOR and
    #         abs(row1[index].green - row2[index].green) < THRESHOLD_COLOR and
    #         abs(row1[index].alpha - row2[index].alpha) < THRESHOLD_COLOR):
    #         return True

    return False


def optimize(input_path, output_path):
    image_info = {
        "in_row": [],
        "in_col": [],
    }

    image = Image(filename = input_path)
    original_width = image.width
    original_height = image.height

    # Process image by height
    is_similar_counter = 0
    current_info = { "start": 0, "end": 0 }
    for row in range(len(image)):
        if len(image) > (row + 1) and is_row_similar(image[row], image[row + 1]):
            if is_similar_counter == 0:
                current_info["start"] = row
            is_similar_counter += 1
        else:
            if is_similar_counter > 0:
                current_info["end"] = row
                current_info["length"] = current_info["end"] - current_info["start"]
                if current_info["length"] >= THRESHOLD_COUNT:
                    image_info["in_row"].append(current_info)
                current_info = {}
                is_similar_counter = 0

    # Process image by width
    transposed = list(zip(*image))
    is_similar_counter = 0
    current_info = { "start": 0, "end": 0 }
    for col in range(len(transposed)):
        if (len(transposed) > (col + 1)) and is_row_similar(transposed[col], transposed[col + 1]):
            if is_similar_counter == 0:
                current_info["start"] = col
            is_similar_counter += 1
        else:
            if is_similar_counter > 0:
                current_info["end"] = col
                current_info["length"] = current_info["end"] - current_info["start"]
                if current_info["length"] >= THRESHOLD_COUNT:
                    image_info["in_col"].append(current_info)
                current_info = {}
                is_similar_counter = 0

    x, y, width, height = 0, 0, 0, 0 # Similar image areas
    cx, cy, cwidth, cheight = 0, 0, 0, 0 # Actual chop side

    if len(image_info["in_col"]) > 0:
        image_info["in_col"] = sorted(image_info["in_col"], key=lambda d: d['length'])
        info_col = image_info["in_col"][0]
        x = info_col["start"]
        cx = x + OFFSET
        width = info_col["length"] + PATCH_OFFSET
        cwidth = width - OFFSET * 2

    if len(image_info["in_row"]) > 0:
        image_info["in_row"] = sorted(image_info["in_row"], key=lambda d: d['length'])
        info_row = image_info["in_row"][0]
        y = info_row["start"]
        cy = y + OFFSET
        height = info_row["length"] + PATCH_OFFSET
        cheight = height - OFFSET * 2

    image.chop(x = cx, y = cy, width = cwidth, height = cheight)

    # Check on optimize threshold
    saved_percents = 1 - (image.width * image.height) / (original_width * original_height)
    if saved_percents >= THRESHOLD_PERCENT:
        # Check output directory
        directory_path = os.path.dirname(output_path)
        is_exist_directory = os.path.exists(directory_path)
        if not is_exist_directory:
            os.makedirs(directory_path)

        # Save new image && print info
        image.save(filename = output_path)
        nine_patch_info = "[{0}, {1}, {2}, {3}]".format(
            x + PATCH_OFFSET if cx > 0 else 0,
            y + PATCH_OFFSET if cy > 0 else 0,
            original_width - (x + width) + PATCH_OFFSET if width > 0 else 0,
            original_height - (y + height) + PATCH_OFFSET if height > 0 else 0
        )

        info_string = "Image: {input_path} Output: {output_path} Origin Size: {origin_size} New Size: {new_size} 9Patch side: {nine_patch_info} Saved: {saved_percents:.2%}".format(
            input_path = input_path,
            output_path = output_path,
            origin_size = "{0}x{1}".format(original_width, original_height),
            new_size = "{0}x{1}".format(image.width, image.height),
            nine_patch_info = nine_patch_info,
            saved_percents = saved_percents
        )
        print(info_string)
