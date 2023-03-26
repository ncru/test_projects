import os
import glob
import shutil
import matplotlib.pyplot as plt

os.system("cls")
# Enable interactive mode
plt.ion()

# Get path to folder containing images
folder_path = input("Please enter the path to the folder containing images: ")

# Check if progress and completed files exist
progress_file = os.path.join(folder_path, "progress.txt")
completed_file = os.path.join(folder_path, "completed.txt")

if os.path.exists(completed_file):
    print("Error: Folder has already been processed. Please select another folder.")
elif os.path.exists(progress_file):
    with open(progress_file, "r") as f:
        progress = int(f.read().strip())
else:
    progress = 0

    # Create list of image file paths
    image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + glob.glob(os.path.join(folder_path, "*.png")) + glob.glob(os.path.join(folder_path, "*.jpeg"))

    # Count number of images in folder
    num_images = len(image_files)
    print(f"Number of images in folder: {num_images}\n")

    # Loop through images in folder
    for i in range(progress, num_images):
        # Get path to current image
        image_path = image_files[i]

        # Open image and display to user
        image = plt.imread(image_path)

        # Determine maximum window size based on longer dimension of image
        max_size = max(image.shape[:2])
        if max_size > 700:
            scale = 1000 / max_size
            figsize = (scale * image.shape[1] / 100, scale * image.shape[0] / 100)
            fig, ax = plt.subplots(figsize=figsize)
            ax.imshow(image)
        else:
            plt.imshow(image)

        plt.show()

        # Get user input for destination folder
        dest_folder_name = input(f"Image {i+1} of {num_images} | Provide folder name to save this img: ").lower()
        os.system("cls")
        dest_folder_path = os.path.join(folder_path, dest_folder_name)

        # Create destination folder if it does not exist
        if not os.path.exists(dest_folder_path):
            os.mkdir(dest_folder_path)
        elif not os.path.isdir(dest_folder_path):
            print("Error: Destination folder already exists as a file.")
            continue

        # Get filename from image path
        filename = os.path.basename(image_path)

        # Copy image to destination folder
        dest_path = os.path.join(dest_folder_path, filename)
        if os.path.exists(dest_path):
            print(f"File '{filename}' already exists in '{dest_folder_name}'. Skipping.")
            continue
        shutil.copy2(image_path, dest_path)

        # Close the figure
        plt.close()

        # Save progress to file
        with open(progress_file, "w") as f:
            f.write(str(i+1))

    # Remove progress file if all images have been processed
    if progress == num_images:
        os.remove(progress_file)
        with open(os.path.join(folder_path, "completed.txt"), "w") as f:
            f.write("")

# Disable interactive mode
plt.ioff()
