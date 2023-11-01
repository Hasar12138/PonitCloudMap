from urllib import request
from urllib.parse import urlparse
import string

# url = 'https://github.com/Hasar12138/PonitCloudMap/blob/main/test1.pcd'
# path Hasar12138/PonitCloudMap/blob/main/test1.pcd
# url = https://raw.github.com/lgsvl/autoware-data/blob/master/CubeTown/data/map/pointcloud_map/CubeTown.pcd
# path = './static/pcd_data/'

def Convert_URL_format(url_in):
    a = urlparse(url_in)
    raw_url = 'raw.'+a.netloc
    path =a.path
    f = path.split('/')
    # print(f[-1])
    # e = path.find('main')
    # filename = path[e+5:]
    filename= path.split('/')[-1]
    d = str(path)
    d = d.replace('/blob','')
    result = a.scheme + '://'+raw_url + d
    
    return result,filename


# print(Convert_URL_format(url))


def download_pcd(url,path,filename):
    location = path+filename
    request.urlretrieve(url, location)
    
# new_url,filename = Convert_URL_format(url)
# download_pcd(new_url,path,filename)
