"""Utility file that contains all functions needed for the assignment"""
import os
import cv2
import numpy as np
import random

def assert_inputs(images, samples_size):
    """Assert that all user inputs are logical and within constraints"""
    sample = 0
    for img in images:
        """Assert that images are non empty"""
        assert isinstance(img, np.ndarray), f"Image is not of the correct type numpy.ndarray"
        """Assert that samples size are within the respective image constraints"""
        if isinstance(samples_size[sample], tuple):
            assert samples_size[sample][0] >= 0 and samples_size[sample][1] >= 0, "Sample sizes need to be positive!"
            assert samples_size[sample][0] <= img.shape[0] and samples_size[sample][1] <= img.shape[1], f"Image sample sizes of ({samples_size[sample][0]}, {samples_size[sample][1]}) is greater than image dimensions of {img.shape}"   
        else:
            assert samples_size[sample] >= 0, "Sample size needs to be positive!"
            assert samples_size[sample] <= img.shape[0] and samples_size[sample] <= img.shape [1], f"Image sample sizes of ({samples_size}, {samples_size}) is greater than image dimensions of {img.shape}"
        sample+=1


def read_images(img_dir: str):
    """Reads all images into numpy arrays and load them in and returns a list"""
    images = []
    image_names = []
    for img_name in os.listdir(img_dir):
        img = cv2.imread(os.path.join(img_dir, img_name))
        if img is not None:
            images.append(img)
            image_names.append(img_name.split(".")[0])
    return images, image_names

def split_region_sequential(h, w, x_choices, y_choices, n_samples, sample, img, img_name):
    for i in range(n_samples):
        """Assert that the sub image patch does not exceed main image bounds"""
        if x_choices[i] + w > img.shape[1] or y_choices[i] + h > img.shape[0]:
            raise AssertionError("Sample region is outside of image constraints!")
        """Extract region and save it under samples folder"""
        region = img[y_choices[i]:y_choices[i] + h, x_choices[i]:x_choices[i] + w]
        cv2.imwrite(f"samples/{img_name}_{sample}_{i}.jpeg", region)

def generate_samples(images: list, image_names: list, samples_size: list, n_samples: int = 3) -> None:
    """Check if samples folder exists"""
    if not os.path.exists("samples"):
        os.makedirs("samples")
    sample = 0
    for img in images:
        """Check samples if h!=w or else h = w = sample_size"""
        h,w = None, None
        if isinstance(samples_size[sample], tuple):
            h, w = samples_size[sample]
        else:
            w = samples_size[sample]
            h = samples_size[sample]
        """Constrain image bounds by sample size to not exceed image bounds on x and y choices"""
        ranges_x = img.shape[1] - w
        ranges_y = img.shape[0] - h
        """Generate x and y choices based on ranges of rows and columns"""
        try:
            x_choices = random.choices([x for x in range(0, ranges_x)], k=n_samples)
            y_choices = random.choices([y for y in range(0, ranges_y)], k=n_samples)
        except:
            raise AssertionError(f"Sample size of {samples_size[sample]} is too large to generate sub regions")
        """Loop over samples to generate (default = 3)"""
        split_region_sequential(h, w, x_choices, y_choices, n_samples, sample, img, image_names[sample])
        """Go to next sample size and image"""
        sample+=1