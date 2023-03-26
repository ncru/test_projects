import os, time
import glob
import shutil
import matplotlib.pyplot as plt

def display_image(image_path):
    image = plt.imread(image_path)
    max_size = max(image.shape[:2])
    if max_size > 700:
        scale = 1000 / max_size
        figsize = (scale * image.shape[1] / 100, scale * image.shape[0] / 100)
        fig, ax = plt.subplots(figsize=figsize)
        ax.imshow(image)
    else:
        plt.imshow(image)
    plt.show()
    return image

def copy_image(source_path, dest_folder_path, filename):
    """Copy an image from the source path to the destination folder path."""
    dest_path = os.path.join(dest_folder_path, filename)
    if os.path.exists(dest_path):
        print(f"File '{filename}' already exists in '{os.path.basename(dest_folder_path)}'. Skipping.")
        time.sleep(1)
        plt.close()
        return False
    shutil.copy2(source_path, dest_path)
    return True

def process_image(image_path, dest_folder_path):
    # Open image and display to user
    image = display_image(image_path)

    # Get user input for destination folder
    dest_folder_name = input(f"Provide folder name to save this image: ").lower()
    os.system("cls")
    dest_folder_path = os.path.join(dest_folder_path, dest_folder_name)

    # Create destination folder if it does not exist
    if not os.path.exists(dest_folder_path):
        os.mkdir(dest_folder_path)

    # Get filename from image path
    filename = os.path.basename(image_path)

    # Copy image to destination folder
    copy_image(image_path, dest_folder_path, filename)

    # Close the figure
    plt.close()

def process_images_in_folder(progress, num_images, image_files, folder_path, progress_file):
    for i in range(progress, num_images):
        os.system("cls")
        print(f"Number of images in folder: {num_images}\n")
        # Get path to current image
        image_path = image_files[i]
        # Process the image
        process_image(image_path, folder_path)
        # Save progress to file
        with open(progress_file, "w") as f:
            f.write(str(i+1))
        # Close the figure
        plt.close()

def main():
    # clear current CMD output
    os.system("cls")

    # Enable interactive mode
    plt.ion()

    # Get path to folder containing images
    folder_path = input("Please enter the path to the folder containing images: ")

    progress_file = os.path.join(folder_path, "progress.txt")

    image_files = glob.glob(os.path.join(folder_path, "*.jpg")) + glob.glob(os.path.join(folder_path, "*.png")) + glob.glob(os.path.join(folder_path, "*.jpeg"))

    num_images = len(image_files) 
    print(f"Number of images in folder: {num_images}\n")


    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            progress = int(f.read().strip())
            # Remove progress file if all images have been processed
            if progress >= num_images:
                print("Folder already processed. Removing progress.")
                print("Program will now exit.")
                time.sleep(2)
                f.close()
                os.remove(progress_file)
            else:
                process_images_in_folder(progress, num_images, image_files, folder_path, progress_file)
    else:
        progress = 0
        process_images_in_folder(progress, num_images, image_files, folder_path, progress_file)

        # Remove progress file if all images have been processed
        if os.path.exists(progress_file):
            os.remove(progress_file)

    # Disable interactive mode
    plt.ioff()

if __name__ == "__main__":
    main()