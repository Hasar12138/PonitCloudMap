from pcl import pcl_visualization
import pcl
import numpy as np
p = pcl.load("./forest.pcd")
np_data = np.array(p)
lt_data = np_data.tolist()

# print(lt_data)



def ground_segmentation(pcd_array, iter_cycle , threshold ):
        xyz = np.asarray(pcd_array)
        print(xyz.shape)
        height_col = int(np.argmin(np.var(xyz, axis = 0)))

        # Make a new column for index 
        temp = np.zeros((len(xyz[:,1]),4), dtype= float)
        temp[:,:3] = xyz[:,:3]
        temp[:,3] = np.arange(len(xyz[:,1]))
        xyz = temp

        # Filter the points based on the height value
        z_filter = xyz[(xyz[:,height_col]< np.mean(xyz[:,height_col]) + 1.5*np.std(xyz[:,height_col])) & (xyz[:,height_col]> np.mean(xyz[:,height_col]) - 1.5*np.std(xyz[:,height_col]))]
        # print(z_filter)
        # Normalize as per the height filter value
        max_z, min_z = np.max(z_filter[:,height_col]), np.min(z_filter[:,height_col])
        z_filter[:,height_col] = (z_filter[:,height_col] - min_z)/(max_z - min_z) 
        # print(z_filter)
        for i in range(iter_cycle):
            covariance = np.cov(z_filter[:,:3].T)
            w,v,h = np.linalg.svd(np.matrix(covariance))
            normal_vector = w[np.argmin(v)]
            
            #Resample points
            filter_mask = np.asarray(np.abs(np.matrix(normal_vector)*np.matrix(z_filter[:,:3]).T )<threshold)
            z_filter = np.asarray([z_filter[index[1]] for index,a in np.ndenumerate(filter_mask) if a == True])
        # print(z_filter)
        z_filter[:,height_col] = z_filter[:,height_col]*(max_z - min_z) + min_z
        world = np.array([row for row in xyz if row[3] not in z_filter[:,3]])
        # print(z_filter)

        pcl_ground= pcl.PointCloud()
        pcl_ground.from_list(z_filter[:,:3])
        print(z_filter[:,:3])
        return z_filter[:,:3]
ground = ground_segmentation(lt_data,10, 0.5)
# print(ground)

cloud = pcl.PointCloud(np.float32(ground))
visual = pcl.pcl_visualization.CloudViewing()
visual.ShowMonochromeCloud(cloud)


flag = True
while flag:
    flag != visual.WasStopped()