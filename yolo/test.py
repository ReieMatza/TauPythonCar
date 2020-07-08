import io
import matplotlib.pyplot as plt
import numpy as np
import cv2

def get_img_from_fig(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


# make a Figure and attach it to a canvas.
fig = plt.figure()

# Do some plotting here
ax = fig.add_subplot(111)
ax.plot([1, 2, 3])

plot_img_np = get_img_from_fig(fig)
cv2.imshow("ZED", fig)
#key = cv2.waitKey(5)