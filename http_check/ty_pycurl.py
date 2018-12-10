import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
    
    
class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0

    def store(self, buf):
        self.line = self.line + 1
        #self.contents = "%s%i: %s" % (self.contents, self.line, buf)
        self.contents = "%s%s" % (self.contents, buf)

    def __str__(self):
        return self.contents
    
    
class DataAnalysis:
    def __init__(self,lst_in):
        try:
            lst_in.sort(cmp=lambda x,y: cmp(float(x), float(y)), reverse = True)
            self.lst_in = lst_in
            
        except:
            pass
        
    def time(self):
        # get millisecond
        dic_out = {}
        dic_out['max'] = round(self.lst_in[0]*1000,1)
        all_a = 0
        for a in self.lst_in:
            a = round(a*1000,1)
            all_a = all_a + a
            dic_out['min'] = a
            
        dic_out['avg'] = all_a/len(self.lst_in)
        return dic_out
    
    def download_size(self):
        # swith B to kB
        lst_tmp = []
        for a in self.lst_in:
            lst_tmp.append(round(a/1024,2))
            
        dic_out = {}
        for b in lst_tmp:
            dic_out[b] = '%.0f%%' % (self.lst_in.count(a)/len(self.lst_in) * 100)
            
        return dic_out
    
    def http_code(self):
        dic_out = {}
        for a in self.lst_in:
            dic_out[a] = '%.0f%%' % (self.lst_in.count(a)/len(self.lst_in) * 100)
            
        return dic_out
    
    
class TyCurl:
    def __init__(self,ip,uri,lst_header):
        self.ip = ip
        self.uri = uri
        self.out = BytesIO()
        url = 'http://%s%s' % (ip,uri)
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.CONNECTTIMEOUT, 10)
        self.c.setopt(self.c.URL, url)
        self.c.setopt(self.c.HTTPHEADER, lst_header)
        
    def close(self):
        self.c.close()
    
    def check_time(self):
        """
            |
            |--NAMELOOKUP
            |--|--CONNECT
            |--|--|--APPCONNECT
            |--|--|--|--PRETRANSFER
            |--|--|--|--|--STARTTRANSFER
            |--|--|--|--|--|--TOTAL
            |--|--|--|--|--|--REDIRECT
        """
        dic_return = {}
        try:
            self.c.setopt(self.c.WRITEDATA, self.out)
            self.c.perform()
            dic_return['namelookup'] = self.c.getinfo(self.c.NAMELOOKUP_TIME)
            dic_return['connect'] = self.c.getinfo(self.c.CONNECT_TIME)
            dic_return['pertransfer'] = self.c.getinfo(self.c.PRETRANSFER_TIME)
            dic_return['starttransfer'] = self.c.getinfo(self.c.STARTTRANSFER_TIME)
            dic_return['totaltime'] = self.c.getinfo(self.c.TOTAL_TIME)
            
        except:
            pass
        
        return dic_return

    def check_httpcode(self):
        dic_return = {}
        try:
            self.c.setopt(self.c.WRITEDATA, self.out)
            self.c.perform()
            dic_return['httpcode'] = self.c.getinfo(self.c.RESPONSE_CODE)
            
        except:
            pass
        
        return dic_return


    def check_filesize(self):
        dic_return = {}
        try:
            self.c.setopt(self.c.WRITEDATA, self.out)
            self.c.perform()
            dic_return['downloadsize'] = self.c.getinfo(self.c.SIZE_DOWNLOAD)
            dic_return['downloadspeed'] = self.c.getinfo(self.c.SPEED_DOWNLOAD)
            
        except:
            pass
        
        return dic_return
    
    def check_all(self):
        dic_return = {}
        dic_tmp = {}
        recive_body = Storage()
        recive_header = Storage()
        self.c.setopt(self.c.WRITEFUNCTION, recive_body.store)
        self.c.setopt(self.c.HEADERFUNCTION, recive_header.store)
        try:
            self.c.perform()
            dic_return['httpcode'] = self.c.getinfo(self.c.RESPONSE_CODE)
            dic_return['downloadsize'] = self.c.getinfo(self.c.SIZE_DOWNLOAD)
            dic_return['totaltime'] = self.c.getinfo(self.c.TOTAL_TIME)
            dic_return['downloadspeed'] = self.c.getinfo(self.c.SPEED_DOWNLOAD)
            dic_return['responsebody'] = recive_body
            dic_return['responseheader'] = recive_header
            # detail time
            dic_tmp['namelookup'] = self.c.getinfo(self.c.NAMELOOKUP_TIME)
            dic_tmp['connect'] = self.c.getinfo(self.c.CONNECT_TIME)
            dic_tmp['pertransfer'] = self.c.getinfo(self.c.PRETRANSFER_TIME)
            dic_tmp['starttransfer'] = self.c.getinfo(self.c.STARTTRANSFER_TIME)
            dic_return['detailtime'] = dic_tmp
            
        except:
            pass
        
        return dic_return
