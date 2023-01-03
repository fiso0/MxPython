def ecef2lla(x,y,z):
     
    '''
    x = 652954.1006
    y = 4774619.7919
    z = -4167647.7937
    '''
     
    #ecef转化为经纬高
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=False)#radians否用弧度返回值
 
    print ('纬度：',lat)
    print ('经度：',lon)
    print ('高度：',alt)
 
    return lat,lon,alt
	