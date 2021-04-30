import os
import re
import json
import pytz
import plots
import shutil
import tarfile
import zipfile
import warnings
import requests
import dateutil
import subprocess
import unicodedata
import xml.etree.ElementTree

from ipywidgets import widgets
from IPython.display import clear_output

import cell_list
import unicore_api
import clb_nb_utils

class SEF:
    
    def __init__(self):
        
        subprocess.call("nrnivmodl")
        warnings.filterwarnings('ignore')
        
        self.RB = widgets.RadioButtons(options = [])
        self.RB1 = widgets.RadioButtons(description= 'Select mod file', options=['default','local'], style={'description_width': 'initial'})
        self.RB1.disabled = True
        self.RBHPC = widgets.RadioButtons(description= 'Run on:', options=['NSG', 'Service Account - NSG'])
        self.RBHPC.disabled = True
        self.RBM = widgets.RadioButtons(options=['all_traces','singletrace','demo'], description='run')
        self.RBM.disabled = True
        self.file_widget = widgets.FileUpload()
        self.KEY = 'Application_Fitting-DA5A3D2F8B9B4A5D964D4D2285A49C57'
        self.TOOL = 'NEURON77_TG'
        
        self.create_folder("GUI")
        os.chdir("GUI")
        self.prepare_transfer_folder()
        self.create_cell_selection()
        self.create_mod_radio()
        self.create_submission_panel()

        
    def create_folder(self, folder):
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        
        
    def prepare_transfer_folder(self):
        self.create_folder("transfer")
        os.chdir("transfer")
        for f in ["cellprop.py", "fitness.py", "fitting.py", "readconffile.py", "readexpfile.py"]:
            shutil.copy2(os.path.join('..','..', f), '.')
        for f in ["netstims.mod", "ProbGABAAB_EMS_GEPH_g.mod"]:
            shutil.copy2(os.path.join('..','..', 'data', f), '.')
        os.chdir("..")
        
        
    def create_cell_selection(self):
        
        def downloadNIP(_):
            with out:
                clear_output()
            os.chdir("transfer")
            for f in os.listdir("."):
                if f.startswith("exp"):
                    os.remove(f)

            w3 = []
            for k in range(len(w.value)):
                w4 = w.value[k]
                w4p = w4[w4.find('mice'):len(w4)]
                w3.append('exp' + w4p[w4p.find('(')+1:w4p.find(')')] + '.txt')
            for k in range(len(cell_list.listurldownload)):
                data_nrrd_url = cell_list.listurldownload[k]
                filename = data_nrrd_url[data_nrrd_url.find('exp'):len(data_nrrd_url)]
                if filename in w3:
                    my_data = requests.get(data_nrrd_url)
                    with open(filename, 'wb') as fd:
                        for chunk in my_data.iter_content():
                            fd.write(chunk)

            os.chdir("../..")
            plots.PlotsSEF(self.RB, w, out)
            os.chdir("GUI")
            TB.layout.display = ''
            self.RB.layout.display = ''
            self.RB1.disabled = False
            self.RBHPC.disabled = False
            self.RBM.disabled = False
        
        w = widgets.SelectMultiple(description='', options=cell_list.listnames, layout=widgets.Layout(width="100%", border='solid'))
        text = widgets.Text()
        text.value = 'Select experimental data to download from CSCS storage'
        text.disabled = True
        text.layout.width = '80%'
        display(text)
        
        TB = widgets.Text()
        TB.value='Select experimental data:'
        TB.disabled=True
        self.RB.layout={'width': 'max-content'}
        BB = widgets.VBox(children = [TB, self.RB])
        TB.layout.display='none'
        self.RB.layout.display='none'
        
        NIPD = widgets.Button()
        NIPD.background_color='gainsboro'
        NIPD.border_color='black'
        NIPD.layout.width='20%'
        NIPD.description = 'Download data'
        NIPD.on_click(downloadNIP)
        
        out = widgets.Output()
        
        display(w)
        display(NIPD)
        display(BB)
        display(out)
        
    
    def create_mod_radio(self):
        
        def params(_):
            if T9.value!='':
                myboxB.layout.display='none'
                names=[]
                listsB=[]
                myboxB.children=listsB
                for i in range(int(T9.value)):
                    names.append('T'+str(i+10))
                    T10=widgets.Text()
                    T10.disabled=True
                    T10.value=str(i)
                    T10.layout.width="10%"
                    T11=widgets.Text()
                    T11.value=''
                    T11.layout.width="15%"
                    T12=widgets.Text()
                    T12.value=''
                    T12.layout.width="15%"
                    T13=widgets.Text()
                    T13.value=''
                    T13.layout.width="15%"
                    T14=widgets.Text()
                    T14.value=''
                    T14.layout.width="15%"
                    lists1=[T10,T11,T12,T13,T14]
                    mybox1=widgets.HBox(children=lists1)
                    listsB.append(mybox1)
                myboxB.children=listsB
                myboxB.layout.display='' 
            else:
                myboxB.layout.display='none'
                
        def dep(_):
            if T15.value!='':
                myboxB2.layout.display='none'
                names2=[]
                listsB2=[]
                myboxB2.children=listsB2
                for i in range(int(T15.value)):
                    names2.append('T'+str(i+16))
                    T16=widgets.Text()
                    T16.layout.width="30%"
                    lists2=[T16]
                    mybox2=widgets.HBox(children=lists2)
                    listsB2.append(mybox2)
                myboxB2.children=listsB2
                myboxB2.layout.display=''
            else:
                myboxB2.layout.display='none'
                
                
        def excl(_):
            if T17.value!='':
                myboxB3.layout.display='none'
                names3=[]
                listsB3=[]
                myboxB3.children=listsB3
                for i in range(int(T17.value)):
                    names2.append('T'+str(i+18))
                    T18=widgets.Text()
                    T18.layout.width="30%"
                    T18.value=''
                    lists3=[T18]
                    mybox3=widgets.HBox(children=lists3)
                    listsB3.append(mybox3)
                myboxB3.children=listsB3
                myboxB3.layout.display=''
            else:
                myboxB3.layout.display='none'
                
            
        def fileloaded(_):
            os.chdir("..")
            import readconffile
            os.chdir("GUI")
            tt=self.RB.value
            if not(tt is None):
                BTC.disabled = False
                valRB=tt[tt.find('CA1'):len(tt)]
                expfilename='exp'+valRB[valRB.find('(')+1:valRB.find(')')]+'.txt'
                readconffile.filename = expfilename.replace("exp","config")
                os.chdir("../data/config_files/")
                [inputfilename,modfilename,parametersfilename,flagdata,flagcut,
                 nrtraces,Vrestf,esynf,nrparamsfit,paramnr,paramname,paraminitval,
                 paramsconstraints,nrdepnotfit,depnotfit,nrdepfit,depfit,seedinitvaluef] = readconffile.readconffile()
                os.chdir("../../GUI/")
                T1.value = expfilename
                l = list(self.file_widget.value.keys())
                if (len(l) > 0):
                    T2.value = l[0]
                T6.value = str(nrtraces)
                T7.value = str(Vrestf)
                T8.value = str(esynf)
                
        
        def writefile(_):
            for f in os.listdir("."):
                if f.startswith("config.txt"):
                    os.remove(f)
            with open('config.txt','w') as f:
                f.write('//name of file containing raw traces\n')
                f.write(T1.value.strip()+'\n')
                f.write('//name of mod file\n')
                f.write(T2.value.strip()+'\n')
                f.write('//name of parameters file\n')
                f.write(T3.value.strip()+'\n')
                f.write('//flagdata==0 data with one time column for all currents; ==1 data with one time column for each current\n')
                f.write(T4.value.strip()+'\n')
                f.write('//flagcut==0 data not cutted; ==1 data cutted below 20% of max\n')
                f.write(T5.value.strip()+'\n')
                f.write('//number of traces\n')
                f.write(T6.value.strip()+'\n')
                f.write('//PROTOCOL\n')
                f.write('//VCLAMP AMP\n')
                f.write(T7.value.strip()+'\n')
                f.write('//REVERSAL POTENTIAL\n')
                f.write(T8.value.strip()+'\n')
                f.write('//FITTING PARAMETERS AND INITIAL VALUES\n')
                f.write(T9.value.strip()+'\n')
                for i in range(int(T9.value.strip())):
                    f.write(myboxB.children[i].children[0].value+' '+myboxB.children[i].children[1].value+' '+myboxB.children[i].children[2].value)
                    f.write('\n')
                f.write('//CONSTRAINTS\n')
                for i in range(int(T9.value.strip())):
                    f.write(myboxB.children[i].children[3].value+' '+myboxB.children[i].children[4].value)
                    f.write('\n')
                f.write('//DEPENDENCY RULES FOR PARAMETERS NOT FITTED\n')
                f.write(T15.value.strip()+'\n')
                for i in range(int(T15.value.strip())):
                    f.write(myboxB2.children[i].children[0].value)
                    f.write('\n')
                f.write('//EXCLUSION RULES\n')
                f.write(T17.value.strip()+'\n')
                for i in range(int(T17.value.strip())):
                    f.write(myboxB3.children[i].children[0].value)
                    f.write('\n')
                f.write('//seed\n')
                f.write(T19.value.strip()+'\n')
                f.write('\n')
            f.close()
            with open(list(self.file_widget.value.keys())[0], "wb") as fp:
                fp.write(self.file_widget.value[list(self.file_widget.value.keys())[0]]['content'])

    
        def writefileifnotemptycell(_):
            BTC.disabled=True
            if T1.value.strip()!='' and T2.value.strip()!='' and T3.value.strip()!='' and T4.value.strip()!='' \
                and T5.value.strip()!='' and T6.value.strip()!='' and T7.value.strip()!='' and T8.value.strip()!='' and \
                T9.value.strip()!='' and T15.value.strip()!='' and T17.value.strip()!='' and T19.value.strip()!='':
                os.chdir("transfer")
                writefile(_)
                os.chdir("..")
            else:
                BTC.disabled=False
        
            
        def RB1click(_):
            if self.RB1.value == 'local':
                self.file_widget.layout.display = ''
                DM.visible = False
                HT.layout.display = ''
                tabs.layout.display = ''
            else:
                self.file_widget.layout.display = 'none'
                DM.visible = True
                HT.layout.display = 'none'
                tabs.layout.display = 'none'

        
        display(self.RB1)
        DM = widgets.Text()
        DM.value = 'ProbGABAAB_EMS_GEPH_g.mod'
        DM.visible = True
        DM.disabled = True
        display(DM)
        HM = widgets.HTML("""
            <input name="mioTesto" type="text" value="Select mod file" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        H1 = widgets.HTML("""
            <input name="mioTesto" type="text" value="name of file containing raw traces" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T1 = widgets.Text()
        T1.value = ''
        T1.disabled = True
        H2 = widgets.HTML("""
            <input name="mioTesto" type="text" value="name of mod file" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T2 = widgets.Text()
        self.file_widget.layout.display = ''
        T2.value = ''
        T2.disabled = True
        H3 = widgets.HTML("""
            <input name="mioTesto" type="text" value="name of parameters file" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T3 = widgets.Text()
        T3.value = 'parameters.txt'
        H4 = widgets.HTML("""
            <input name="mioTesto" type="text" rows="2" 
            value="flagdata==0 data with one time column for all currents; ==1 data with one time column for each current"
            style="color: black; background-color: white; border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        H4 = widgets.HTML("""
            <textarea name="textarea" rows="2" disabled="true" style="width:400px; height:40px;
            color: black; background-color: white; border: none; font-weight: bold; resize: none">
            flagdata==0 data with one time column for all currents; ==1 data with one time column for each current</textarea>
        """)
        T4 = widgets.Text()
        T4.value = '0'
        H5 = widgets.HTML("""
            <textarea name="textarea" rows="2" disabled="true" style="width:400px; height:40px; color: black; background-color: white;
            border: none; font-weight: bold; resize: none">flagcut==0 data not cutted;\n ==1 data cutted below 20% of max</textarea>
        """)
        T5 = widgets.Text()
        T5.value = '1'
        H6 = widgets.HTML("""
            <input name="mioTesto" type="text" value="number of traces" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
            """)
        T6 = widgets.Text()
        T6.value = ''
        T6.disabled = True
        H7 = widgets.HTML("""
            <input name="mioTesto" type="text" value="PROTOCOL" style="color: black; background-color: white; border: none; 
            font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        H8  =widgets.HTML("""
            <input name="mioTesto" type="text" value="VCLAMP AMP" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T7 = widgets.Text()
        T7.value = ''
        T7.disabled = True
        H9 = widgets.HTML("""
            <input name="mioTesto" type="text" value="REVERSAL POTENTIAL" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T8 = widgets.Text()
        T8.value = ''
        T8.disabled = True
        H10 = widgets.HTML("""
            <input name="mioTesto" type="text" value="FITTING PARAMETERS INITIAL VALUES AND CONSTRAINTS" style="color: black;
            background-color: white; border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />""")
        H11 = widgets.HTML("""
            <textarea name="textarea" disabled="true" style="width:460px; height:15px; color: black; background-color: white;
            border: none; font-weight: bold; resize: none">nr of params, names of params, initial values, min, max</textarea>
        """)
        T9 = widgets.Text()
        T9.value = '0'
        T9.layout.width = "10%"
        lists = [H1, T1, H2, T2, H3, T3, H4, T4, H5, T5, H6, T6, H7, H8, T7, H9, T8, H10, H11, T9]
        mybox = widgets.VBox(children=lists)

        names = []
        listsB = []
        for i in range(int(T9.value)):
            names.append('T'+str(i+10))
            T10 = widgets.Text()
            T10.value=str(i)
            T10.layout.width="10%"
            T10.disabled=True
            T11 = widgets.Text()
            T11.layout.value = ''
            T11.layout.width = "15%"
            T12 = widgets.Text()
            T12.value = ''
            T12.layout.width="15%"
            T13 = widgets.Text()
            T13.value = ''
            T13.layout.width="15%"
            T14 = widgets.Text()
            T14.value = ''
            T14.layout.width = "15%"
            lists1 = [T10, T11, T12, T13, T14]
            mybox1 = widgets.HBox(children = lists1)
            listsB.append(mybox1)

        myboxB = widgets.VBox(children = listsB)
        H12 = widgets.HTML("""
            <input name="mioTesto" type="text" value="DEPENDENCY RULES FOR PARAMETERS NOT FITTED" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T15 = widgets.Text()
        T15.value = '0'
        T15.layout.width = "10%"
        names2 = []
        listsB2 = []
        for i in range(int(T15.value)):
            names2.append('T'+str(i+16))
            T16 = widgets.Text()
            T16.layout.width="30%"
            lists2 = [T16]
            mybox2 = widgets.HBox(children=lists2)
            listsB2.append(mybox2)
        myboxB2 = widgets.VBox(children=listsB2)
        T15.observe(dep) 
        H13=widgets.HTML("""
            <input name="mioTesto" type="text" value="EXCLUSION RULES" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T17=widgets.Text()
        T17.value='0'
        T17.layout.width="10%"
        names3=[]
        listsB3=[]
        for i in range(int(T17.value)):
            names2.append('T'+str(i+18))
            T18=widgets.Text()
            T18.layout.width="30%"
            lists3=[T18]
            mybox3=widgets.HBox(children=lists3)
            listsB3.append(mybox3)

        myboxB3=widgets.VBox(children=listsB3)
        T17.observe(excl) 
        T9.observe(params)
        H14=widgets.HTML("""
            <input name="mioTesto" type="text" value="seed" style="color: black; background-color: white;
            border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        T19 = widgets.Text()
        T19.value = '1234567'
        T19.layout.width = "20%"

        H10.visible = False
        H11.visible = False
        T9.visible = False
        myboxB.layout.display = ''
        H12.visible = False
        T15.visible = False
        myboxB2.layout.display = ''
        H13.visible = False
        T17.visible = False
        myboxB3.layout.display = ''
        H14.visible = False
        T19.visible = False
        
        BTC = widgets.Button()
        BTC.description = 'Write config file'
        BTC.on_click(writefileifnotemptycell)
        BTC.disabled = True
        
        lists = [HM, self.file_widget]
        myboxpage1 =widgets.VBox(children=lists)
        page1 = widgets.Box(children=[myboxpage1])
        lists = [H1,T1,H2,T2,H6,T6,H7,H8,T7,H9,T8]
        myboxpage2 = widgets.VBox(children=lists)
        page2 = widgets.Box(children=[myboxpage2])
        lists = [H10,H11,T9,myboxB,H12,T15,myboxB2,H13,T17,myboxB3,H14,T19,BTC]
        myboxpage3 = widgets.VBox(children=lists)
        page3 = widgets.Box(children=[myboxpage3])
        tabs = widgets.Tab(children=[page1,page2,page3])
        tabs.observe(fileloaded)
        HT = widgets.HTML("""
            <input name="mioTesto" type="text" value="Select local mod file and write config file" style="color: black;
            background-color: white; border: none; font-weight: bold" size="60" maxlength="400" disabled="true" id="testo" />
        """)
        HT.layout.display = 'none'
        display(HT)
        tabs.layout.display = 'none'
        display(tabs)

        tabs.set_title(0, 'First page')
        tabs.set_title(1, 'Second page')
        tabs.set_title(2, 'Third page')
        self.RB1.on_trait_change(RB1click, 'value')
    
    
    def create_submission_panel(self):
        
        def assign_file_types(filename):
            """ assign file types based on file name and extension """
            fname, extension = os.path.splitext(filename)
            if extension == '.txt':
                filetype = 'text/plain'
            else:
                filetype = 'application/unknown'
            return filetype
        
        
        def checkloginNSG(_):
            username = username_widget.value
            password = password_widget.value
            headers = {'cipres-appkey' : self.KEY}
            URL = 'https://nsgr.sdsc.edu:8443/cipresrest/v1/job/' + username
            r = requests.get(URL, auth=(username, password),headers=headers,verify=False)
            root = xml.etree.ElementTree.fromstring(r.text)
            a=0
            for child in root:
                if child.tag == 'displayMessage':
                    a=1
                    msg=child.text
            if a==0:
                msg='Authenticated successfully'
                msg_widget.disabled=True
                buttonlogin.disabled=True
                username_widget.disabled=True
                password_widget.disabled=True
            msg_widget.value=msg
            msg_widget.layout.display=''
            RunSNSG.disabled = False
            
            
        
        def runNSG(RunSNSG):
            if msg_widget.value=='Authenticated successfully':
                self.RBHPC.disabled=True
                self.RBM.disabled=True
                TR.disabled=True
                TT.disabled=True
                TSK.disabled=True
                ND.disabled=True
                WT.disabled=True
                myboxUNSG.children[0].disabled=True
                runningUNSG=True
                IU.layout.display=''
                username=username_widget.value
                password=password_widget.value
                CRA_USER = username
                PASSWORD = password
                URL = 'https://nsgr.sdsc.edu:8443/cipresrest/v1'

                create_zip_nsg()

                headers = {'cipres-appkey' : self.KEY}
                if TT.value=='':
                    jobname='NSG_Job'
                else:
                    jobname=unicodedata.normalize('NFC', TT.value)
                nrcores=unicodedata.normalize('NFC', TSK.value)
                nrnodes=unicodedata.normalize('NFC', ND.value)
                runtime=unicodedata.normalize('NFC', WT.value)
                payload = {'tool' : self.TOOL,\
                           'metadata.statusEmail' : 'false',
                           'vparam.pythonoption_' : '1',
                           'metadata.clientJobId': jobname,
                           'vparam.number_cores_' : nrcores,
                           'vparam.number_nodes_' : nrnodes,
                           'vparam.runtime_' : float(runtime),
                           'vparam.filename_': 'start.py'}
                files = {'input.infile_' : open('transfer.zip', 'rb')}

                r = requests.post('{}/job/{}'.format(URL, CRA_USER), auth=(CRA_USER, PASSWORD), data=payload, headers=headers, files=files,verify=False)
                root = xml.etree.ElementTree.fromstring(r.text)
                global outputuri, selfuri
                for child in root:
                    if child.tag == 'resultsUri':
                        for urlchild in child:
                            if urlchild.tag == 'url':
                                outputuri = urlchild.text
                    if child.tag == 'selfUri':
                        for urlchild in child:
                            if urlchild.tag == 'url':
                                selfuri = urlchild.text
                myboxUNSG.children[1].layout.display=''
            else:
                runningUNSG=False
                CheckSNSG.layout.display='none'
                myboxConf.children[1].layout.display='none'
                myboxConf.layout.display=''
                myboxUNSG.children[0].disabled=True
            
       
        
        def checksimnsg(CheckSNSG):
            headers = {'cipres-appkey' : self.KEY}
            username = username_widget.value
            password = password_widget.value
            CRA_USER = username
            PASSWORD = password
            r = requests.get(selfuri, auth=(CRA_USER, PASSWORD), headers=headers,verify=False)
            root = xml.etree.ElementTree.fromstring(r.text)
            job_submissiontime=root.find('dateSubmitted').text
            job_name=root.find('metadata').find('entry').find('value').text
            for child in root:
                if child.tag == 'jobStage':
                    STN.layout.display=''
                    STN.value=job_name+' '+child.text+' '+\
                    dateutil.parser.parse(job_submissiontime).\
                    astimezone(pytz.timezone('CET')).strftime("%d/%m/%Y %H:%M:%S")
                    jobstage=child.text
                if child.tag == 'terminalStage':
                    jobstatus = child.text
            if (jobstatus=='true'):
                if (jobstage=='COMPLETED'):
                    IU.layout.display = 'none'
                    CheckSNSG.disabled = True
                    r = requests.get(outputuri, headers=headers, auth=(CRA_USER, PASSWORD),verify=False)
                    globaldownloadurilist = []
                    lengths = []
                    root = xml.etree.ElementTree.fromstring(r.text)
                    for child in root:
                        if child.tag == 'jobfiles':
                            for jobchild in child:
                                if jobchild.tag == 'jobfile':
                                    for downloadchild in jobchild:
                                        if downloadchild.tag == 'downloadUri':
                                            for attchild in downloadchild:
                                                if attchild.tag == 'url':
                                                    globaldownloadurilist.append(attchild.text)
                                        if downloadchild.tag == 'length':
                                            lengths.append(downloadchild.text)
                    r = requests.get(selfuri, auth=(CRA_USER, PASSWORD), headers=headers,verify=False)
                    root = xml.etree.ElementTree.fromstring(r.text)
                    for child in root:
                        if child.tag == 'messages':
                            for childs in child:
                                texts=[]
                                for childss in childs:
                                    texts.append(childss.text)
                                if texts[1]=='SUBMITTED':
                                    subname=texts[2]
                    os.chdir("..")
                    storeto_path = 'resultsNSG'
                    if not os.path.exists(storeto_path):
                        os.mkdir(storeto_path)
                    storeto = str(os.path.join(storeto_path,TT.value+'_fitting_'+\
                                               dateutil.parser.parse(job_submissiontime).\
                                               astimezone(pytz.timezone('CET')).\
                                               strftime("%d%m%Y%H%M%S")))
                    os.mkdir(storeto)
                    os.chdir(storeto)
                    for downloaduri in globaldownloadurilist:
                        if float(lengths[globaldownloadurilist.index(downloaduri)])<=5048000:
                            r = requests.get(downloaduri, auth=(CRA_USER, PASSWORD), headers=headers,verify=False)
                            d = r.headers['content-disposition']
                            filename_list = re.findall('filename=(.+)', d)
                            for filename in filename_list:
                                download_file_nsg(filename, r)  
                    runningUNSG=False
                    os.chdir("../../GUI")
                else:
                    IU.layout.display='none'
                    CheckSNSG.layout.display='none'
                    myboxConf.layout.display=''
                    runningUNSG=False
                    myboxUNSG.children[0].disabled=False
                    
                    
        def run_service_account_on_nsg(RunSNSG_SA):
            self.RBHPC.disabled=True
            self.RBM.disabled=True
            TR.disabled=True
            TT.disabled=True
            TSK.disabled=True
            ND.disabled=True
            WT.disabled=True
            myboxUNSG_SA.children[0].disabled=True
            runningUNSG=True
            IU.layout.display=''

            create_zip_nsg()

            POST_JOB_URL = 'https://bspsa.cineca.it/jobs/nsg/'

            nrcores=unicodedata.normalize('NFC', TSK.value)
            nrnodes=unicodedata.normalize('NFC', ND.value)
            runtime=unicodedata.normalize('NFC', WT.value)   
            if TT.value=='':
                title='ServiceAccount_Job'
            else:
                title=unicodedata.normalize('NFC', TT.value)

            payload = {
                'tool' : self.TOOL, 
                'python_option' : '1',
                'core_number' : nrcores, 
                'node_number' : nrnodes,
                'runtime' : float(runtime),
                'init_file': 'start.py',
                'title': title,
                'uc':' synaptic_events_fitting'
            }

            files = {'input.infile_' : open('transfer.zip','rb')}

            headers = unicore_api.get_oidc_auth()
            headers.update({'Content-Disposition':'attachment;filename=transfer.zip'})
            headers.update({'payload': json.dumps(payload)})


            r = requests.post(url=POST_JOB_URL, headers=headers, files=files)
            if r.status_code == 201:
                global jobid
                jobid = r.json()['job_id']
                myboxUNSG_SA.children[1].layout.display=''
            else:
                runningUNSG=False
                myboxConf.children[1].layout.display='none'
                myboxConf.layout.display=''
                myboxUNSG_SA.children[0].disabled=True


        def check_job_on_service_account(CheckSNSG):
            headers = unicore_api.get_oidc_auth()
            GET_JOB_URL = 'https://bspsa.cineca.it/jobs/nsg/bsp_nsg_01/' + jobid + '/'
            DOWNLOAD_OUTPUT_FILE = 'https://bspsa.cineca.it/files/nsg/bsp_nsg_01/' + jobid + '/'

            r = requests.get(url=GET_JOB_URL, headers=headers)
            if r.status_code == 200:
                job = r.json()

                job_submissiontime = job['init_date']
                job_stage = job['stage']
                job_terminal_stage = job['terminal_stage']

                STN.layout.display=''
                job_title = job['title']
                if job_title == "":
                    jobname = jobid
                else:
                    jobname = job_title
                STN.value = job_title + ' ' + job['stage'] + ' ' + \
                                dateutil.parser.parse(job_submissiontime).astimezone(pytz.timezone('CET')).strftime("%d/%m/%Y %H:%M:%S")

                if job_terminal_stage and job_stage == 'COMPLETED':
                    IU.layout.display='none'
                    CheckSNSG_SA.disabled=True 
                    r = requests.get(url=DOWNLOAD_OUTPUT_FILE, headers=headers)
                    if r.status_code == 200:
                        file_list = r.json()
                        os.chdir("..")
                        storeto_path = 'resultsNSG-SA'
                        if not os.path.exists(storeto_path):
                            os.mkdir(storeto_path)
                        os.chdir(storeto_path)
                        storeto = TT.value +'_fitting_' + dateutil.parser.parse(job_submissiontime).astimezone(pytz.timezone('CET')).strftime("%d%m%Y%H%M%S")
                        if not os.path.exists(storeto_path):
                            os.mkdir(storeto)
                        os.chdir(storeto)
                        for f in file_list:
                            filename = f['filename']
                            r = requests.get(url=DOWNLOAD_OUTPUT_FILE + f['fileid'] + '/', headers=unicore_api.get_oidc_auth())
                            if r.status_code == 200:
                                download_file_nsg(filename, r)  
                        os.chdir("../../GUI")
                    runningUNSG=False    
            else:
                IU.layout.display='none'
                CheckSNSG_SA.layout.display='none'
                myboxConf.layout.display=''
                runningUNSG=False
                myboxUNSG_SA.children[0].disabled=False
        
        
        def create_zip_nsg():
            with open(os.path.join('transfer', 'start.py'), 'w') as f:
                tt = self.RB.value
                valRB = tt[tt.find('CA1'):len(tt)]
                expf = 'exp'+valRB[valRB.find('(')+1:valRB.find(')')]+'.txt'
                if self.RB1.value=='local':
                    conff='config.txt'
                else:
                    conff=expf.replace("exp","config")
                f.write('import fitting')
                f.write('\n')
                if self.RB1.value=='local':
                    if self.RBM.value=='all_traces':
                        f.write('fitting.fitting('+'\''+conff+'\','+'\''+expf+'\','+'\''+\
                                list(self.file_widget.value.keys())[0]+\
                                '\','+'\''+'True'+'\','+'\''+'False'+'\','+'\''+'False'+'\','+'3)\n')
                    else:
                        if self.RBM.value=='singletrace':  
                            f.write('fitting.fitting('+'\''+conff+'\','+'\''+expf+'\','+'\''+\
                                    list(self.file_widget.value.keys())[0]+\
                                    '\','+'\''+'False'+'\','+'\''+'True'+'\','+'\''+'False'+'\','+\
                                    '\''+unicodedata.normalize('NFC', TR.value)+'\')\n')
                        else:
                            f.write('fitting.fitting('+'\''+conff+'\','+'\''+expf+'\','+'\''+\
                                    list(self.file_widget.value.keys())[0]+\
                                    '\','+'\''+'False'+'\','+'\''+'False'+'\','+'\''+'True'+'\','+\
                                    '\''+unicodedata.normalize('NFC', TR.value)+'\')\n')
                else:
                    if self.RBM.value=='all_traces':
                        f.write('fitting.fitting('+'\''+conff+'\','+'\''+expf+'\','+'\''+\
                                'ProbGABAAB_EMS_GEPH_g.mod'+\
                                '\','+'\''+'True'+'\','+'\''+'False'+'\','+'\''+'False'+'\','+'3)\n')           
                    else:
                        if self.RBM.value=='singletrace':  
                            f.write('fitting.fitting('+'\''+conff+'\','+'\''+expf+'\','+'\''+\
                                    'ProbGABAAB_EMS_GEPH_g.mod'+\
                                    '\','+'\''+'False'+'\','+'\''+'True'+'\','+'\''+'False'+'\','+\
                                    '\''+unicodedata.normalize('NFC', TR.value)+'\')\n')
                        else:
                            f.write('fitting.fitting('+'\''+conff+'\','+'\''+expf+'\','+'\''+\
                                    'ProbGABAAB_EMS_GEPH_g.mod'+\
                                    '\','+'\''+'False'+'\','+'\''+'False'+'\','+'\''+'True'+'\','+\
                                    '\''+unicodedata.normalize('NFC', TR.value)+'\')\n')
                f.write('\n')
            f.close()
            if self.RB1.value=='local':
                os.chdir('..')
                f = open('fitness.py', 'r')    
                lines = f.readlines()
                lines[241] = "\n" 
                lines[242] = "\n"
                lines[243] = "\n"
                lines[244] = "\n"
                lines[245] = "\n"
                f.close()   
                f = open('fitness.py', 'w')
                f.writelines(lines)
                f.close()
                os.chdir('GUI')
            else:
                shutil.copy2(os.path.join("..", "data", 'config_files', conff), 'transfer')

            zfName = 'transfer.zip'
            foo = zipfile.ZipFile(zfName, 'w')
            for root, dirs, files in os.walk('./transfer'):
                for f in files:
                    foo.write(os.path.join(root, f))
            foo.close()
            
        
        def download_file_nsg(filename, r):
            if filename=='output.tar.gz' or filename=='STDOUT' or filename=='STDERR':
                with open(filename, 'wb') as fd:
                    for chunk in r.iter_content():
                        fd.write(chunk) 
                if filename=='output.tar.gz':
                    ff = tarfile.open("output.tar.gz")
                    ff.extractall('OUTPUT')
                    ff.close()
                    os.remove('output.tar.gz')
                    for filename in os.listdir(os.path.join('OUTPUT','transfer')):
                        if filename.endswith("txt") or\
                        (filename.endswith("mod") and not(filename.startswith("netstims"))) or\
                        filename in ['test.csv', 'start.py']:
                            shutil.copy2(os.path.join('OUTPUT','transfer', filename), '.')
                    shutil.rmtree('OUTPUT')
                    
        
        def runmethod(change):
            if self.RBM.value=='all_traces':
                TR.value='3'
                TR.layout.display='none'
            else:
                TR.value='3'
                TR.layout.display=''
                
                
        def RBHPCclick(_):
            STU.layout.display='none'
            IU.layout.display='none'
            if self.RBHPC.value == 'NSG':
                formMNSG.layout.display=''
                myboxConf.children[0].layout.display= '' 
                myboxUNSG.children[0].layout.display=''
                RunSNSG_SA.layout.display='none'
                CheckSNSG_SA.layout.display='none'
                if runningUNSG:
                    myboxUNSG.children[1].layout.display=''
            elif self.RBHPC.value == 'Service Account - NSG':
                formMNSG.layout.display = 'none'
                myboxConf.children[0].layout.display= 'none'
                myboxUNSG_SA.children[0].layout.display=''
                RunSNSG.layout.display='none'
                CheckSNSG.layout.display='none'
                if runningUNSG:
                    myboxUNSG_SA.children[1].layout.display=''

            myboxConf.children[0].layout.display=''
            myboxConf.children[1].value='24'
            myboxConf.children[2].value='2'
            myboxConf.children[3].value='0.5'
            if runningUNSG:
                STN.layout.display=''
                IU.layout.display=''
        
        
        
        file = open("../data/img/Work-in-progress3.png", "rb")
        image = file.read()
        IU = widgets.Image(value=image, format='png', width=400)
        IU.layout.display='none'
        STU=widgets.Text()
        STU.description='status'
        STU.value=''
        STU.disabled=True
        STU.layout.width='70%'
        STU.layout.display='none'
        STN=widgets.Text()
        STN.description='status'
        STN.value=''
        STN.disabled=True
        STN.layout.width='70%'
        STN.layout.display='none'
        username_widget = widgets.Text(description='Username:')
        username_widget.layout.width='249px'
        password_widget = widgets.Password(description='Password:')
        buttonlogin = widgets.Button()
        buttonlogin.description = 'Login NSG'
        buttonlogin.background_color='gainsboro'
        buttonlogin.border_color='black'
        buttonlogin.layout.width='25%'
        buttonlogin.on_click(checkloginNSG)
        msg_widget = widgets.Text(layout=widgets.Layout(width='40%'))
        msg_widget.layout.display='none'
        
        display(self.RBHPC)
        display(self.RBM)
        self.RBM.observe(runmethod,names='value')
        formMNSG=widgets.VBox(children=[username_widget, password_widget, buttonlogin, msg_widget])
        formMNSG.layout.display=''
        display(formMNSG)
        TR = widgets.Text()
        TR.description = 'Trace:'
        TR.layout.display = 'none'
        display(TR)
        TT = widgets.Text()
        TT.description = 'Title:'
        WT = widgets.Text()
        WT.description = 'Walltime:'
        ND = widgets.Text()
        ND.description = 'N. of nodes'
        TSK = widgets.Text()
        TSK.description = 'N. of CPUs'
        myboxConf=widgets.VBox(children=[TT,TSK,ND,WT])
        myboxConf.children[1].value = '24'
        myboxConf.children[2].value = '2'
        myboxConf.children[3].value = '0.5'
        myboxConf.layout.display = ''
        display(myboxConf)
        
        RunSNSG = widgets.Button()
        RunSNSG.description = 'Run NSG simulation'
        RunSNSG.background_color = 'gainsboro'
        RunSNSG.border_color = 'black'
        RunSNSG.layout = widgets.Layout(width='25%')
        RunSNSG.on_click(runNSG)
        RunSNSG.disabled = True
        CheckSNSG = widgets.Button()
        CheckSNSG.description = 'Check NSG simulation'
        CheckSNSG.background_color='gainsboro'
        CheckSNSG.border_color='black'
        CheckSNSG.layout = widgets.Layout(width='25%')
        CheckSNSG.on_click(checksimnsg)
        buttonSNSG = [RunSNSG, CheckSNSG]
        myboxUNSG = widgets.HBox(children=buttonSNSG)
        myboxUNSG.children[0].layout.display=''
        myboxUNSG.children[1].layout.display='none'
        
        RunSNSG_SA = widgets.Button()
        RunSNSG_SA.description = 'Run NSG simulation'
        RunSNSG_SA.background_color = 'gainsboro'
        RunSNSG_SA.border_color = 'black'
        RunSNSG_SA.layout = widgets.Layout(width='25%')
        RunSNSG_SA.on_click(run_service_account_on_nsg)
        CheckSNSG_SA = widgets.Button()
        CheckSNSG_SA.description = 'Check NSG simulation'
        CheckSNSG_SA.background_color='gainsboro'
        CheckSNSG_SA.border_color='black'
        CheckSNSG_SA.layout = widgets.Layout(width='25%')
        CheckSNSG_SA.on_click(check_job_on_service_account)
        buttonSNSG_SA = [RunSNSG_SA, CheckSNSG_SA]
        myboxUNSG_SA = widgets.HBox(children=buttonSNSG_SA)
        myboxUNSG_SA.children[0].layout.display='none'
        myboxUNSG_SA.children[1].layout.display='none'
        
        display(STU)
        display(STN)
        display(myboxUNSG)
        display(myboxUNSG_SA)
        display(IU)
        
        runningU = False
        runningUNSG = False

        self.RBHPC.on_trait_change(RBHPCclick,'value')    
    
        