from image import Image
import numpy as np

def adjust_brightness(image, factor):
    x_pixels, y_pixels, num_channels = image.array.shape

    # make an  empty image
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    # intuitive way to do this is to use a for loop (not recommended non-vectorized)
    # for x in range(x_pixels):
    #     for y in range(y_pixels):
    #         for c in range(num_channels):
    #             new_image.array[x, y, c] = image.array[x, y, c] * factor


    # numpy way to do this (recommended vectorized version)
    new_image.array = image.array * factor
    
    return new_image


def adjust_contrast(image, factor, mid=0.5):
    x_pixels, y_pixels, num_channels = image.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid


    # vectorized version
    # new_image.array = (image.array - mid) * factor + mid
    return new_image

def blur(image, kernel_size):
    """ Kernel size is the no. of pixels to take into account when applying blur, i.e.
    kernel size  = 3 would be neighbors to left/righ, top/bottom, diagonals.
    The kernel size always should be an odd no.
    """
    x_pixels,y_pixels,num_channels = image.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range (max(x - neighbor_range), min(x_pixels-1,x+neighbor_range) + 1):
                    for y_i in range (max(y - neighbor_range), min(y_pixels-1,y+neighbor_range) + 1):
                        total += image.array[x_i, y_i, c]
                new_image.array[x,y,c] = total / (kernel_size ** 2)

    return new_image    

# note:
# The blur implemented above is a kernel of size n, where each value is 1/n**2
# for example, k=3 would be this kernel:
# [1/3, 1/3, 1/3]
# [1/3, 1/3, 1/3]
# [1/3, 1/3, 1/3]

def apply_kernel(image, kernel):
    # The kernel should be a numpy 2D array that represents the kernel 
    # for example the sobel x kernel (detecting horizontal edges) as following:
    # [1, 0,-1]
    # [2, 0,-2]
    # [1, 0,-1]
    
    x_pixels,y_pixels,num_channels = image.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    #how many neighbors to one side we need to look at  
    kernel_size = kernel.shape[0]
    neighbor_range = kernel_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range (max(0,x-neighbor_range), min(new_image.x_pixels-1,x+neighbor_range)+1):
                    for y_i in range (max(0,y-neighbor_range), min(new_image.y_pixels-1,y+neighbor_range)+1):
                        # find which kernel value this corresponds to 
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_image.array[x,y,c] = total

    return new_image

def combine_image(image1, image2):
    # check if the images have the same dimensions

    x_pixels,y_pixels,num_channels = image1.array.shape
    new_image = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)
    
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_image.array[x,y,c] = (image1.array[x,y,c]**2 + image2.array[x,y,c]**2) **0.5
    return new_image


if __name__ == '__main__':
    city = Image(filename='city.png')
    hills = Image(filename='hills.png')

    # brightened = adjust_brightness(city, 1.7)
    # brightened.write_image('brightened.png')

    # darkened = adjust_brightness(city, 0.3)
    # darkened.write_image('darkened.png')

    # increase contrast
    # contrast = adjust_contrast(city, 2, 0.5)
    # contrast.write_image('contrast.png')

    # decrease contrast
    # dec_contrast = adjust_contrast(city, 0.5,0.5)
    # dec_contrast.write_image('decreasedCont.png')

    # blur_3 = blur(city,3)
    # blur_3.write_image('blurred.png')

    # applying sobel edge detection kernel on the x and y axis 
    sobel_x_kernel = np.array([[1,2,1], [0,0,0], [-1,-2,-1]])
    sobel_y_kernel = np.array([[1,0,-1], [2,0,-2], [1,0,-1]])

    sobel_x = apply_kernel(city, sobel_x_kernel)
    # sobel_x.write_image('edge_x.png')
    sobel_y = apply_kernel(city, sobel_y_kernel)
    # sobel_y.write_image('edge_y.png')

    sobel_xy = combine_images(sobel_x,sobel_y)
    sobel_xy.write_image('edge_xy.png')
