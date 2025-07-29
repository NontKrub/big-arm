#   ----- Import ----- #
import cv2
import numpy as np
import time
import serial


#   ----- Set up the serial connections with uno ----- #
#arduino = serial.Serial('COM3', 9600) 
#time.sleep(2) # give time for UNO to reset


#   ----- Open the camera ----- #
cap = cv2.VideoCapture(0)

if not cap.isOpened(): #if cam isn't working 
    print("Error: Could not open camera.")
    exit()

print("Press Enter to start the program")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame.")
        break

    cv2.imshow("Live Camera Feed", frame)

    # Press 'enter' to start the program
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # Enter key
        print("Starting the program!")
        break

cap.release()
cv2.destroyAllWindows() #end


#   ----- Convert Bgr2hsv ----- #
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define color ranges in HSV
color_ranges = {
    'Red': [
        (np.array([0, 100, 100]), np.array([10, 255, 255])),
        (np.array([160, 100, 100]), np.array([179, 255, 255]))
    ],
    'Green': [
        (np.array([40, 70, 70]), np.array([80, 255, 255]))
    ],
    'Blue': [
        (np.array([100, 150, 0]), np.array([140, 255, 255]))
    ]
}

#   ----- Draw the rectangle ----- #
result = frame.copy() # copy the pervious frame

# Dictionary to hold detected centers by color
color_centers = {
#ex 'red': 120,
} 

for color_name, ranges in color_ranges.items():
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for lower, upper in ranges:
        mask |= cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    center_x = center_y = None

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500 and area > max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            center_x = x + w // 2
            center_y = y + h // 2
            max_area = area

    if center_x is not None and center_y is not None:
#   ----- store the variable in the color_ceter ----- #        
        color_centers[color_name] = center_x 

#   ----- Draw rectangle and center point ----- #    
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.circle(result, (center_x, center_y), 5, (0, 255, 0), -1)

#   ----- Label ----- #   
        label = f"{color_name} ({center_x}, {center_y})"
        cv2.putText(result, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 255), 2)

        print(f"{color_name} center at: x={center_x}, y={center_y}")

#   ----- Assign the angle ----- #   
angles = [30, 45, 135]

#   ----- Arrange the color by x axis (item[1]) ----- #   
sorted_colors = sorted(color_centers.items(), key=lambda item: item[1])

#   ----- Angle dataset ----- #   
color_angles = {color: angles[i] for i, (color, _) in enumerate(sorted_colors)}

#   ----- Find the angle by the x / not by arranging ----- #   
#def get_angle(value):
#    if 0 <= value <= 100:
#        return angles[0]
#    elif 100 <= value <= 200:
#        return angles[1]
#    elif 300 < value < 400:
#        return angles[2]
#    return None

#color_angles = {color: get_angle(value) for color, value in color_centers.items()}

#store the Angle datasets as variable
for color in ['Red', 'Green', 'Blue']:
    angle = color_angles.get(color)
    print(f"{color} angle: {angle}")
    #Serial with UNO
    #arduino.write(f"{red_angle}\n".encode())
    #arduino.write(f"{green_angle}\n".encode())
    #arduino.write(f"{blue_angle}\n".encode())

#-----  Quit program ----#
cv2.imshow("Result", result)
print("Press 'q' to quit the program.")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Quitting the program.")
        break

cv2.destroyAllWindows()
