## How to use the script
* Download the Example_Neuron_tif
    * Vector:
        - x:          x coordinate of dendritic branching point
        - y:          y coordinate of dendritic branching point
        - image:      path to image file used in the analysis
        - int_thresh: intensity threshold used to filter the image (usually between 0-255)
    * dendritic_polarplot:
        - sine:           Sine coordinates used to bin the pixel values
        - cos:            Cosine coordinates used to bin the pixel values
        - nbins:          Number of bins used for the polar plot
        - norm_ori_vec:   Normalized orientation vector
        - DSI:            Calculated DSI of dendrite shape
        - Name:           Name of the output .png file

* How to call the functions

    norm_ori_vec, norm_pixel_values, DGI = Vector(96, 156, 'path/to/Example_Neuron.tif', 50)

    dendritic_polarplot(norm_pixel_values[:,0], norm_pixel_values[:,1], 16, norm_ori_vec, DGI, 'Example_Neuron')