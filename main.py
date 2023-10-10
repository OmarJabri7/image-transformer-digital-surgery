from utils import read_images, assert_inputs, generate_samples

if __name__ == "__main__":
    """Extract images from data folder"""
    img_dir = input("Input images folder\n")
    try:
        images = read_images(img_dir)
    except Exception as e:
        raise e
    if len(images) == 0:
        raise ValueError(f"No images found under directory {img_dir}")
    """Get fixed sample size for each image seperately"""
    samples_size = [int(input("Input fixed samples size\n")) for _ in range(len(images))]
    """Assert input data is correct and logical"""
    assert_inputs(images, samples_size)
    """Store random image samples into results folder for each image in images"""
    generate_samples(images, samples_size, n_samples=3, threaded = False)