import json
import time
import requests
import clb_nb_utils
requests.packages.urllib3.disable_warnings()

"""
Helper methods for using UNICORE's REST API

For a full API reference and examples, have a look at
https://sourceforge.net/p/unicore/wiki/REST_API
https://sourceforge.net/p/unicore/wiki/REST_API_Examples
"""

def get_sites():
    """ get info about the known sites in the HPC Platform """
    sites = {}
    sites['JUQUEEN'] = {'name': 'JUQUEEN (JSC)', 'id': 'JUQUEEN', 
                        'url': "https://hbp-unic.fz-juelich.de:7112/HBP_JUQUEEN/rest/core" }
    sites['JURECA'] = {'name': 'JURECA (JSC)', 'id': 'JURECA',
                       'url': "https://hbp-unic.fz-juelich.de:7112/HBP_JURECA/rest/core" }
    sites['MARCONI'] = {'name': 'MARCONI (CINECA)', 'id': 'MARCONI',
                     'url': "https://grid.hpc.cineca.it:9111/CINECA-MARCONI/rest/core" }
    sites['GALILEO'] = {'name': 'GALILEO (CINECA)', 'id': 'MARCONI',
                     'url': "https://grid.hpc.cineca.it:9111/CINECA-GALILEO/rest/core" }
    sites['DAINT-CSCS'] = {'name': 'PIZDAINT (CSCS)', 'id': 'CSCS',
                     'url': "https://unicoregw.cscs.ch:8080/DAINT-CSCS/rest/core" }
    return sites


def get_site(name):
    return get_sites().get(name, None)


def get_properties(resource, headers={},verbose=True):
    """ get JSON properties of a resource """
    my_headers = headers.copy()
    my_headers['Accept']="application/json"
    resp=""
    try:
        r = requests.get(resource, headers=my_headers, verify=False)
        if r.status_code!=200:
            if r.status_code==500:
                js = "<script>alert('HPC server issues. Please try again later.');</script>"
                if verbose==True:
                    display(HTML(js))
                return "server issues"
            else:
                raise RuntimeError("Error getting properties: %s" % r.status_code)
        else:
            return r.json()
    except requests.exceptions.ConnectionError:
        return "Connection refused."       
    
def get_working_directory(job, headers={}, properties=None):
    """ returns the URL of the working directory resource of a job """
    if properties is None:
        properties = get_properties(job,headers)
    return properties['_links']['workingDirectory']['href']


def invoke_action(resource, action, headers, data={}):
    my_headers = headers.copy()
    my_headers['Content-Type']="application/json"
    action_url = get_properties(resource, headers)['_links']['action:'+action]['href']
    r = requests.post(action_url,data=json.dumps(data), headers=my_headers, verify=False)
    if r.status_code!=200:
        raise RuntimeError("Error invoking action: %s" % r.status_code)
    return r


def upload(destination, file_desc, headers):
    my_headers = headers.copy()
    my_headers['Content-Type']="application/octet-stream"
    name = file_desc['To']
    data = file_desc['Data']
    # TODO file_desc could refer to local file
    r = requests.put(destination+"/"+name, data=data, headers=my_headers, verify=False)
    if r.status_code!=204:
        raise RuntimeError("Error uploading data: %s" % r.status_code)
    else:
        jobURL=''


def submit(url, job, headers, inputs=[],verbose=True):
    """
    Submits a job to the given URL, which can be the ".../jobs" URL
    or a ".../sites/site_name/" URL
    If inputs is not empty, the listed input data files are
    uploaded to the job's working directory, and a "start" command is sent
    to the job.
    """
    my_headers = headers.copy()
    my_headers['Content-Type']="application/json"
    if len(inputs)>0:
        # make sure UNICORE does not start the job 
        # before we have uploaded data
        job['haveClientStageIn']='true'
        
    r = requests.post(url,data=json.dumps(job), headers=my_headers, verify=False)
    if r.status_code!=201:
        if r.status_code==500:
            jobURL=''
            js = "<script>alert('System is in maintenance. Please try again later.');</script>"
            if verbose==True:
                display(HTML(js))
        else:
            if r.status_code==403:
                jobURL=''
                js = "<script>alert('Authentication service is restarting. Please try again later.');</script>"
                if verbose==True:
                    display(HTML(js))
            else:
                raise RuntimeError("Error submitting job: %s" % r.status_code)
    else:
        jobURL = r.headers['Location']

        #  upload input data and explicitely start job
        if len(inputs)>0:
            working_directory = get_working_directory(jobURL, headers)
            for input in inputs:
                upload(working_directory+"/files", input, headers)
            try:
                invoke_action(jobURL, "start", headers)
            except:
                pass    
    return jobURL

    
def is_running(job, headers={}):
    """ check status for a job """
    properties = get_properties(job,headers)
    status = properties['status']
    return ("SUCCESSFUL"!=status) and ("FAILED"!=status)


def wait_for_completion(job, headers={}):
    """ wait until job is done """
    while is_running(job, headers):
        time.sleep(3)


def file_exists(wd, name, headers):
    """ check if a file with the given name exists
        if yes, return its URL
        of no, return None
    """
    files_url = get_properties(wd, headers)['_links']['files']['href']
    children = get_properties(files_url, headers)['children']
    return name in children or "/"+name in children


def get_file_content(file_url, headers, check_size_limit=True, MAX_SIZE=30240000):
    """ download binary file data """
    if check_size_limit:
        size = get_properties(file_url, headers)['size']
        if size>MAX_SIZE:
            raise RuntimeError("File size too large!")
    my_headers = headers.copy()
    my_headers['Accept']="application/octet-stream"
    r = requests.get(file_url, headers=my_headers, verify=False)
    if r.status_code!=200:
        raise RuntimeError("Error getting file data: %s" % r.status_code)
    else:
        return r.content

    
def list_files(dir_url, auth, path="/"):
    #return get_properties(dir_url+"/files"+path, auth)['children']
    return list(get_properties(dir_url+"/files"+path, auth)['content'].keys())


def get_oidc_auth():
    """ returns HTTP headers containing OIDC bearer token """
    token = clb_nb_utils.oauth.get_token()
    session = requests.Session()
    session.headers['Authorization'] = f'Bearer {token}'
    hdr = session.headers['Authorization']
    return {'Authorization': hdr}

def get_user_id(url, auth):
    """ returns the user id at the given url """
    return get_properties(url, auth)['client']['xlogin']['UID']