from skimage import data, exposure, filters, io, segmentation, external
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
%matplotlib inline

def Vector(x, y, image, int_thresh):
    
    ## Import picture as array
    
    im = io.imread(image)
    
    ## Set dendritic branching point(dbp) as the maximum value
    
    im[y, x] = 255
    
    ## Save image
    
    io.imsave('%s.png' % image, im)
    
    ## Define dbp with the input index (y, x)

    dbp = np.array([y, x])
    
    ## Retrieve the index of all pixel values above a threshold
    
    pixel_co = np.argwhere(im > int_thresh)        
    
    
    ## Substract the dbp index from every pixel to calculate the vectors
    
    norm_pixel_values = pixel_co - dbp

    norm_pixel_values[:,0]*= -1
   
    ## Find vector length to every pixel
    
    vec_length = np.linalg.norm(norm_pixel_values, axis=1)

    ## Delete dbp index
    
    dbp_index = np.argwhere(vec_length == 0)
    
    norm_pixel_values = np.delete(norm_pixel_values, (dbp_index), axis=0)
    
    vec_length = np.delete(vec_length, dbp_index)

    
    ## Normalize vector length 
    
    norm_vectors = norm_pixel_values / vec_length[:, np.newaxis]
    
    ## Add all vectors together 
    
    ori_vec = [norm_vectors.sum(axis=0)]
    
    ## Calculate length of the sum vector
    
    ori_vec_length = np.linalg.norm(ori_vec)
    
    ## Calculate normalized vector in the same orientation as sum vector
    
    norm_ori_vec = ori_vec / ori_vec_length  
    num_pixel = norm_pixel_values.shape[0]

    ## Calculate DSI (Direction Selectivity Index)
    
    DGI = np.divide(ori_vec_length, num_pixel)
 
    
    ## Plot the vector starting at the dbp in the image together with the used pixels as a scatterplot
    sns.set()
    ax = plt.subplot(111)
    
    ax.arrow( 0, 0, 100*norm_ori_vec[0, 1], 100*norm_ori_vec[0,0], width = 1.5, head_width= 10,
             head_length=15, fc='k', ec='k')
    ax.scatter( norm_pixel_values[:, 1], norm_pixel_values[:, 0], marker = '.', alpha = 0.1)
    plt.savefig('%s.png' % image, dpi = 1000)
    ax.axis('equal')
    
    plt.show()
    
     ## Save Data to csv file
    
    np.savetxt("%s.csv" % image, norm_vectors, fmt="%.10f", delimiter=',')
    
    
    return(norm_ori_vec, norm_pixel_values, DGI)

def dendritic_polarplot(sine, cos, nbins, norm_ori_vec, DSI, Name):
    
    ## Convert vector coordinates into degree
    angles = np.arctan2(cos, sine)
    vec_angles = np.degrees(angles)
    
    ## Separate the vectors into different bins according to directions
    
    histo = np.histogram(vec_angles, bins = nbins)
    histo = np.array(histo)
    
    ## Colour the bars differently
    
    cmap_hist = sns.husl_palette(nbins)
    
    ## Normalize the bar length
    
    bar_length = []
    for elem in histo[0]:
        bar_length.append(elem/np.sum(histo[0]))
    bar_length.append(0)
    bar_length = np.array(bar_length)
    
    ## Add the normalized orientation vector of the dendrite
    
    ori_angle = np.degrees(np.arctan2(-norm_ori_vec[0, 1], -norm_ori_vec[0, 0]))
    
    ## Round DSI to 3 decimals
    
    DSI = round(DSI, 4)
    
    ## Make polar plot and add vector
    sns.set()
    ax = plt.subplot(111, polar=True)
    
    bins = np.arange(0.0, 2*np.pi, 2*np.pi/nbins)
    arrow = ax.arrow((-ori_angle/180*np.pi)-np.pi/2, 0, 0, DSI, length_includes_head = True, head_width = 0.08, head_length = 0.05,label = DSI)
    bars = ax.bar(-bins-(np.pi/2), 3*bar_length[:-1], width = np.repeat(2*np.pi/nbins, nbins), bottom=0.0, alpha = 0.4)
    
    ax.set_rticks([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    ax.set_yticklabels(['', 0.2, '', 0.4, '', 0.6, '', 0.8])
    ax.set_rlabel_position(-ori_angle+90)
    legend = ax.legend(loc = 'upper right', bbox_to_anchor=(1.05,1.05), handles = [arrow])
    ax.set_xticklabels(['      Posterior', '', 'Dorsal', '', 'Anterior      ', '', 'Ventral', ''])
    for i in range(len(bars)):
        bars[i].set_facecolor(cmap_hist[i])
        bars[i].set_alpha(0.4)
        bars[i].set_edgecolor('k')
    plt.savefig('%s.png' % Name, dpi = 100)
    plt.show()
    
    return True


## How to use the script
# Download the Example_Neuron_tif
# Vector:
#   x:          x coordinate of dendritic branching point
#   y:          y coordinate of dendritic branching point
#   image:      path to image file used in the analysis
#   int_thresh: intensity threshold used to filter the image (usually between 0-255)
# dendritic_polarplot:
#   sine:           Sine coordinates used to bin the pixel values
#   cos:            Cosine coordinates used to bin the pixel values
#   nbins:          Number of bins used for the polar plot
#   norm_ori_vec:   Normalized orientation vector
#   DSI:            Calculated DSI of dendrite shape
#   Name:           Name of the output .png file
# 
# 
# norm_ori_vec, norm_pixel_values, DGI = Vector(96, 156, 'path/to/Example_Neuron.tif', 50)
# 
# dendritic_polarplot(norm_pixel_values[:,0], norm_pixel_values[:,1], 16, norm_ori_vec, DGI, 'Example_Neuron')