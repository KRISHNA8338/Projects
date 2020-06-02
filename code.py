import numpy as np
import math

import cv2


cap = cv2.VideoCapture(0)

cap.set(3,320)
cap.set(4,240)

hmn=16
hmx=75
smn=93		
smx=220
vmn=96
vmx=255

x=320
x_l=320
ind=0
ind1=0
	
while True:
	# grab the current frame
	_,frame = cap.read()

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hue,sat,val = cv2.split(hsv)
	

	hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
	sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
	vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))

	tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))

	# construct a mask for the color needed, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.erode(tracking, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)


	# find contours in the mask and initialize the current
	cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	ind1=0
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		cnts_sort=sorted(cnts, key=cv2.contourArea,reverse=True)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		
		ind1=1
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		#x_centre=int(M["m10"] / M["m00"])
		
		
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 3, (0, 0, 255), -1)
			ind1=1
	ind=0	
	if len(cnts)>1:	
		c_l=cnts_sort[1]
		M_l = cv2.moments(c_l)
		center_l = (int(M_l["m10"] / M_l["m00"]), int(M_l["m01"] / M_l["m00"]))
		((x_l, y_l), radius_l) = cv2.minEnclosingCircle(c_l)
		#x_centre_l=int(M_l["m10"] / M_l["m00"])
		
		dist=math.sqrt((x-x_l)**2+(y-y_l)**2)
		
		if radius_l > 2 :
			if dist< radius:
				cv2.circle(frame, (int(x_l), int(y_l)), int(radius_l),
				(0, 0, 0), 2)
				ind=1
				
	cv2.imshow("Frame", frame)
	# if the 'q' key is pressed, stop the loop
	if  cv2.waitKey(1) & 0xFF == ord('q'):
		break
		
cap.release()
cv2.destroyAllWindows()

