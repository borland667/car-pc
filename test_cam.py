import cv

capture = cv.CaptureFromCAM(-1)

fourcc = cv.CV_FOURCC('M','J','P','G')
fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
w = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
h = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)
w, h = int(w), int(h)

stream = cv.CreateVideoWriter("test.avi", fourcc, fps, (w, h))
while True:
    frame = cv.QueryFrame(capture)
    cv.WriteFrame(stream, frame)