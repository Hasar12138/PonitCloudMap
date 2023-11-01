

from flask import Flask,render_template,request
from download import Convert_URL_format,download_pcd
from plane_detection import *
from utils import *
import open3d as o3d
import time 
import random
app = Flask(__name__ ,template_folder='templates')

path = './static/pcd_data/'

@app.route('/index',methods = ['GET','POST'])
def indeex():
    getdata = request.args.to_dict()
    print(getdata)
    # print(request.form['seg'])
    # try:
    #     return render_template('upload.html',content=getData)#上传到index.html页面中
    # except:
    #     getData=''
    #     return render_template('upload.html', content=getData)  # 上传到index.html页面中

    if not getdata :
        
        return render_template('index.html')

    if getdata:
        raw_url = getdata['URL']
        
        
        min_ratio = float(getdata['min_ratio'])
        threshold = float(getdata['threshold'])
        iterations=int(getdata['iterations'])
        
        print(getdata['seg'])
        if getdata['seg'] == 'seg':
            
            url_seg,filename_seg = Convert_URL_format(getdata['URL'])
            download_pcd(url_seg,path,filename_seg)
            
            
            points = pcl.load("./static/pcd_data/"+filename_seg)
            print(np.array(points).shape)
            t0 = time.time()
            points = RemoveNoiseStatistical(points, nb_neighbors=5, std_ratio=1.0)
            results = DetectMultiPlanes(points, min_ratio=min_ratio, threshold=threshold, iterations=iterations)
            print(len(results))
            print('Time:', time.time() - t0)
            planes = []
            colors = []
            for _, plane in results:

                r = random.random()
                g = random.random()
                b = random.random()

                color = np.zeros((plane.shape[0], plane.shape[1]))
                color[:, 0] = r
                color[:, 1] = g
                color[:, 2] = b

                planes.append(plane)
                colors.append(color)
            
            planes = np.concatenate(planes, axis=0)
            colors = np.concatenate(colors, axis=0)
            SaveResult(planes, colors,filename_seg)

            
            return render_template('show_map_seg.html',jay =  filename_seg)
        else:
            url,filename = Convert_URL_format(getdata['URL'])
            download_pcd(url,path,filename)
            return render_template('show_map.html',jay =  filename)


@app.route('/cath',methods = ['GET','POST'])
def cath():
    return render_template('show_cath.html')

@app.route('/ict_6th_1',methods = ['GET','POST'])
def ict_6th_1():
    return render_template('show_ict_6th_1.html')

@app.route('/ict_1st',methods = ['GET','POST'])
def ict_1st():
    return render_template('show_ict_1st.html')

@app.route('/cath_seg',methods = ['GET','POST'])
def cath_seg():
    return render_template('show_cath_seg.html')

@app.route('/ict_6th_2',methods = ['GET','POST'])
def ict_6th_2():
    return render_template('show_ict_6th_2.html')

@app.route('/ict_1st_seg',methods = ['GET','POST'])
def ict_1st_seg():
    return render_template('show_ict_1st_seg.html')

@app.route('/ict_2nd',methods = ['GET','POST'])
def ict_2nd():
    return render_template('show_ict_2nd.html')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port= 8888,
        debug=True
    )
    