from utils import read_images, assert_inputs, generate_samples, random

if __name__ == "__main__":
    """Extract images from data folder"""
    img_dir = input("Input images folder\n")
    is_test = input("Generate test cases (Random samples) ? (Y/N)\n")
    if is_test not in ["Y", "N"]:
        raise AttributeError("Answer should be Y or N!")
    try:
        images, names = read_images(img_dir)
    except Exception as e:
        raise e
    if len(images) == 0:
        raise ValueError(f"No images found under directory {img_dir}")
    """Input user preference (fixed/dynamic samples)"""
    sample_type = input("Please input sample preference: fixed (height = width) or dynamic (height != width)\n")
    if sample_type == "fixed":
        """Get fixed sample size for each image seperately"""
        if is_test == "Y":
            samples_size = [random.randint(0, images[i].shape[0]) for i in range(len(images))]
        else:
            try:
                samples_size = [int(input("Input fixed samples size\n")) for _ in range(len(images))]
            except:
                raise AttributeError("Samples size should be integers!")
    elif sample_type == "dynamic":
        """Get dynamic sample size for each image seperately"""
        samples_size = []
        for i in range(len(images)):
            if is_test == "Y":
                h, w = random.randint(0, images[i].shape[0]), random.randint(0, images[i].shape[1])
            else:
                inp = input("Input height and width as: height width \n").split(" ")
                h, w = [int(obj) for obj in inp]
            samples_size.append((h,w))
    else:
        raise AttributeError("Input sample type as either fixed or dynamic!")
    """Assert input data is correct and logical"""
    assert_inputs(images, samples_size)
    """Store random image samples into results folder for each image in images"""
    generate_samples(images, names, samples_size, n_samples=3)