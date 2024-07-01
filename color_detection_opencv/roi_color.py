import cv2

# Function to check if a point is inside the ROI
def is_point_in_roi(point, roi):
    x, y, w, h = roi
    return (x <= point[0] <= x + w) and (y <= point[1] <= y + h)

# Define the region of interest (ROI) as (x, y, width, height)
roi = (0, 300, 640, 420)  # Example ROI

# Define two points to check
point1 = (150, 150)
point2 = (50, 50)

# Define the desired frame dimensions
frame_width = 640
frame_height = 420

# Open the default camera
cap = cv2.VideoCapture(0)

# Set the frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

    # Resize the frame to the specified dimensions
    frame = cv2.resize(frame, (frame_width, frame_height))

    # Draw the ROI on the frame
    cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 255, 0), 2)

    # Check if the points are within the ROI
    if is_point_in_roi(point1, roi):
        cv2.circle(frame, point1, 5, (0, 0, 255), -1)  # Red circle if inside ROI
    else:
        cv2.circle(frame, point1, 5, (255, 0, 0), -1)  # Blue circle if outside ROI

    if is_point_in_roi(point2, roi):
        cv2.circle(frame, point2, 5, (0, 0, 255), -1)  # Red circle if inside ROI
    else:
        cv2.circle(frame, point2, 5, (255, 0, 0), -1)  # Blue circle if outside ROI

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
