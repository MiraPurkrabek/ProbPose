import cv2
import numpy as np
import os

def concat_images(directory):
    # Get all image files in the directory
    image_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and (f.endswith('.jpg') or f.endswith('.png'))]

    # Group images by prefix
    image_groups = {}
    for image_file in image_files:
        prefix = image_file.split('_')[0]
        if prefix not in image_groups:
            image_groups[prefix] = []
        image_groups[prefix].append(image_file)

    # Concatenate images horizontally
    for prefix, images in image_groups.items():
        if len(images) != 2:
            continue

        left_image_name = [img for img in images if 'ViTPose' in img][0]
        right_image_name = [img for img in images if 'ProbPose' in img][0]

        left_image = cv2.imread(os.path.join(directory, left_image_name))
        right_image = cv2.imread(os.path.join(directory, right_image_name))

        # Resize the image to match the height of the base image
        left_image = cv2.resize(left_image, (right_image.shape[1], right_image.shape[0]))

        white_column = 255 * np.ones((right_image.shape[0], 10, 3), dtype=np.uint8)

        # Concatenate the images horizontally
        concat_image = cv2.hconcat([left_image, white_column, right_image])

        # Save the concatenated image
        output_path = os.path.join(directory, f'{prefix}_concatenated.jpg')
        cv2.imwrite(output_path, concat_image)

def main():
    # Specify the directory containing the images
    directory = '/mnt/disk/Users/mirap/CMP/papers_repos/ProbPose/static/images'

    # Call the function to concatenate the images
    concat_images(directory)

if __name__ == "__main__":
    main()