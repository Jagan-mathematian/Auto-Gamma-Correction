import cv2
import argparse
import numpy as np

def auto_gama_correction(image, output_path):
    # Converting the BGR Image to HSV Image and take the v channel to get the correct value of the Image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = hsv/255.0
    v = hsv[:, :, 2]
    # Calculate the mean and distribution of the Image using the v channel
    mu = v.mean()
    sigma = v.std()
    print("Mean : ", mu)
    print("Stdev : ", sigma)
    # Calculating the D value to Determine the low or High contrast Image
    # where D = 4 * sigma
    D = ((mu + (2*sigma)) - (mu - (2*sigma)))
    tres = 1/ 3
    Flag = ""
    if D < tres or D == tres:
      print("Low contrast Image")
      Flag = "Low"
    else:
      print("High contrast Image")
      Flag = "High"

    # Determining the Image is Brighter or Darker
    if mu >= 0.50:
      print("Bright")
    else:
      print("Dark")

    # Calculating the gamma value
    if Flag == "High":
      gamma = np.exp((1 - (mu + sigma)) / 2)
    else:
      gamma = -np.log(sigma)
    gamma = gamma.astype(np.float32)
    print("gamma value : ", gamma)

    # Calculating the Value of C
    heaviside_x = (0.50 - mu)

    if heaviside_x <= 0:
      heaviside = 0
    else:
      heaviside = 1
    
    print("heaviside : ", heaviside)
    power_val = np.power(image/255 , gamma)
    power_val = power_val.astype(np.float32)

    k = power_val + ((1- power_val) * np.power(mu, gamma))
    k = k.astype(np.float32)
    c = 1 / (1 + (heaviside * (k -1)))
    c = c.astype(np.float32)
    image_out = c * (np.power(image/255, gamma))
    image_out = image_out.astype(np.float32)
    image_out = np.round(image_out * 255.0)
    cv2.imwrite(output_path, image_out)
    return image_out
    
if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='pass input Image path and output path')
    my_parser.add_argument('--input', type=str, required=True, help='Image path to apply gamma correct')
    my_parser.add_argument('--output', type=str, required=True, help='Output Path to save the processed Image')
    
    args = my_parser.parse_args()
    image = cv2.imread(args.input)
    auto_gama_correction(image, args.output)
    
