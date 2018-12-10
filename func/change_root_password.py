import func.overlord.client as func
import re
import sys
import string
from random import choice


def Get_Passwd():
    spec_chars = '!@#$%^&*()'
    allow_chars = string.letters + string.digits*3 + spec_chars*2
    new_passwd = ''.join([choice(allow_chars) for i in range(17)])
    return new_passwd


def Upd_Root_Passwd(hostname, passwd):
    import func.overlord.client as func
    """
    #--- test only ---
    dic_tmp = {}
    dic_tmp[hostname] = [0,'updated successfully']
    lst_res = []
    
    if dic_tmp[hostname][0] == 0 and re.search(r'updated successfully', dic_tmp[hostname][1]):
        str_res = 'True'
    else:
        str_res = 'False_CMD'
        
    return str_res
        
    #--- test only ---
    """
    cmd_upd_passwd = "echo '%s'|passwd --stdin root" % passwd

    client = func.Client(hostname)
    try:
        dic_tmp = client.command.run(cmd_upd_passwd)
        if dic_tmp[hostname][0] == 0 and re.search(r'updated successfully', dic_tmp[hostname][1]):
            str_res = 'True'

        else:
            str_res = 'False_CMD'

    except:
        str_res = 'False_FUNC'

    return str_res
    

if __name__ == "__main__":
    Cnt_All = 0
    Cnt_Oth = 0
    Cnt_Upd_Succ = 0
    Cnt_Upd_Fail = 0

    try:
        File = open('servlist.txt')
        # serverlist.txt format: hostname,ipaddress
        Print_Upd = open('update_serv.txt','wb')

    except:
        print 'servlist.txt not found'
        sys.exit()

    lst_line = File.readlines()
    for line in lst_line:
        Cnt_All = Cnt_All + 1

        lst_tmp = line.split(',')
        try:
            lanip = lst_tmp[1]
            hostname = lst_tmp[0]

            # Exec Change Root Password
            try:
                newpasswd = Get_Passwd()
                str_res = Upd_Root_Passwd(hostname, newpasswd)
                if str_res != 'True':
                    Cnt_Upd_Fail = Cnt_Upd_Fail + 1

                else:
                    Cnt_Upd_Succ = Cnt_Upd_Succ + 1

                Print_Upd.write(line.replace('##', '\t').strip('\n') + '\t%s\t%s\n' % (str_res, \
                                                                                       newpasswd))

            except Exception,msg:
                print msg
                Print_Upd.write(line.replace('##', '\t').strip('\n') + '\tFalse_EXE\n')
                Cnt_Upd_Fail = Cnt_Upd_Fail + 1

        except:
            Print_Upd.write(line.replace('##', '\t').strip('\n') + '\tFalse_Other\n')
            Cnt_Oth = Cnt_Oth + 1

    print "Total: %d\nOther: %d\nUpdate_Succ: %d\nUpdate_Fail: %d" % (Cnt_All,\
                                                                      Cnt_Oth,\
                                                                      Cnt_Upd_Succ,\
                                                                      Cnt_Upd_Fail)
