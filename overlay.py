import cv2
import numpy as np
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane
    
    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))
image = cv2.imread('Plantation.png')
overlay = cv2.imread('red_flower.png',-1)
x1=280
x2=100
y1=175
y2=230
cv2.rectangle(image,(200,175),(418,225),(0,255,0),3)
cv2.rectangle(image,(50,200),(200,275),(255,255,0),3)
res = cv2.resize(overlay,(20,20))
x=184
y=150
w,h,c=res.shape
#image[175:175+w,200:200+h,:] = blend_transparent(image[175:175+w,200:200+h,:],res)
i=1
for i in range(2):
    image[y1:y1+h,x1+(i-1)*w:x1+i*w,:]= blend_transparent(image[y1:y1+h,x1+(i-1)*w:x1+i*w,:],res)
image[y2:y2+w,x2:x2+h,:]= blend_transparent(image[y2:y2+w,x2:x2+h,:],res)
cv2.imshow("Image",image)
cv2.imshow("res",res)
cv2.waitKey(0)

