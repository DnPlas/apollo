def vehicle_offset(img):
    
    # THIS RATE CAN CHANGE GIVEN THE RESOLUTION OF THE CAMERA!!!!!
    # BE SURE TO CHANGE THIS IF USING DIFFERENT SIZE IMAGES!!!
    image_center = img.shape[1]/2
    
    ## find where lines hit the bottom of the image, closest to the car
#3    left_low = get_val(img.shape[0],left_fit)
#3    right_low = get_val(img.shape[0],right_fit)
#3    
#3    # pixel coordinate for center of lane
#3    lane_center = (left_low+right_low)/2.0
#3    
#3    ## vehicle offset
#3    distance = image_center - lane_center
    
    ## convert to metric
    return image_center 
