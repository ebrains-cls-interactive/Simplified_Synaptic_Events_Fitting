import os
import plotly


class PlotsSEF:
    
    def __init__(self, RB, w, out):
        filenamesexp={}
        valuesexp={}
        for name in os.listdir("."):
            if name.startswith('exp') and name.endswith('.txt'):
                filenamesexp[name]=name
                valuesexp[name]=False
        RB.options=sorted(w.value)
        tt = RB.value
        valRB = tt[tt.find('CA1'):len(tt)]
        expname = 'exp' + valRB[valRB.find('(')+1:valRB.find(')')] + '.txt'
        configname = expname.replace("exp", "config")
        newopt=[]
        for k in range(len(RB.options)):
            tt=RB.options[k]
            optRB=tt[tt.find('CA1'):len(tt)]
            newopt.append(optRB[optRB.find('(')+1:optRB.find(')')])
        from plotly import tools
        with out:
            nc = 2
            if len(w.value)%2==0:
                nr = len(w.value)/2
                fig = plotly.subplots.make_subplots(rows=int(nr), cols=nc, print_grid=False, subplot_titles=newopt)
            else:
                nr = len(w.value)/2+1
                specsr=[]
                for k in range(int(nr)-1):
                    specsc=[]
                    for l in range(nc):
                        specsc.append({})
                    specsr.append(specsc)
                specsc=[]
                for l in range(nc-1):
                    specsc.append({})
                specsc.append(None)
                specsr.append(specsc)   
                fig = plotly.subplots.make_subplots(rows=int(nr), cols=nc, print_grid=False, specs=specsr,subplot_titles=newopt)
            cl=1
            rw=1
            for k in range(len(RB.options)):
                tt=RB.options[k]
                optRB=tt[tt.find('CA1'):len(tt)]
                expname='exp'+optRB[optRB.find('(')+1:optRB.find(')')]+'.txt'
                configname=expname.replace("exp","config")
                layout = plotly.graph_objs.Layout(
                    title='10 traces',
                    updatemenus=list([
                            dict(
                            x=00.05,
                            y=1,
                            yanchor='top',
                            buttons=list([
                                        dict(
                                            args=['visible',[True,True,True,True,True,True,True,True,True,True]],
                                            label='All',
                                            method='restyle'
                                        ),
                                        dict(
                                            args=['visible',[True,False,False,False,False,False,False,False,False,False]],
                                            label='1',
                                            method='restyle'
                                        )
                                    ]),
                            )
                        ]),

                )
                nn=1
                dd=[]
                for jj in range(10):
                    [timevecprov,vecprov] = self.readexpfile(configname="data/config_files/" + configname, num=nn+jj)
                    timevecall = []
                    for i in range(len(timevecprov)):
                        timevecall.append(timevecprov[i]-timevecprov[0])
                    if (k==0):
                        fig.append_trace(
                            plotly.graph_objs.Scatter(x=timevecall, y=vecprov,mode = 'lines', name = nn+jj, legendgroup = jj),
                            row=rw, col=cl
                        )
                    else:
                        fig.append_trace(
                            plotly.graph_objs.Scatter(x=timevecall, y=vecprov,mode = 'lines', name = nn+jj, legendgroup = jj, showlegend=False),
                            row=rw, col=cl
                        )
                cl=cl+1
                if cl%2==1:
                    cl=1
                    rw=rw+1
            fig['layout']['showlegend'] = True
            fig['layout']['legend']['orientation']="h"
            fig['layout'].update(height=nr*300, width=1000)
            plotly.offline.iplot(fig)

        
    def readconffile(self, filename):
        fh=open(filename,"rU")
        fh.readline()#name of file containing raw traces
        inputfilename=fh.readline()
        fh.readline()#name of mod file
        modfilename=fh.readline()
        fh.readline()#name of parameters file
        parametersfilename=fh.readline()
        fh.readline()#flagdata==0 data with one time column for all currents; ==1 data with one time column for each current
        flagdata=int(fh.readline())
        fh.readline()#flagcut==0 data not cutted; ==1 data cutted below 20% of max
        flagcut=int(fh.readline())
        fh.readline()#number of traces
        nrtraces=int(fh.readline())
        fh.readline()#PROTOCOL
        fh.readline()#VCLAMP AMP
        Vrestf=int(fh.readline())
        fh.readline()#REVERSAL POTENTIAL
        esynf=int(fh.readline())
        fh.readline()#FITTING PARAMETERS AND INITIAL VALUES
        nrparamsfit=int(fh.readline())
        paramnr=[]
        paramname=[]
        paraminitval=[]
        for _ in range(nrparamsfit):
            line=fh.readline()
            par=line.split()
            x1=int(par[0])
            paramnr.append(x1)
            s=par[1]
            paramname.append(s)
            x2=float(par[2])
            paraminitval.append(x2)
        fh.readline()#CONSTRAINTS
        paramsconstraints=[]
        for _ in range(nrparamsfit):
            line=fh.readline()
            par=line.split()
            paramsconstraints.append([float(par[i]) for i in range(2)])
        fh.readline()#DEPENDENCY RULES FOR PARAMETERS NOT FITTED
        nrdepnotfit=int(fh.readline())
        depnotfit=[]
        for _ in range(nrdepnotfit):
            depnotfit.append(fh.readline())
        fh.readline()#EXCLUSION RULES 
        nrdepfit=int(fh.readline())
        depfit=[]
        for _ in range(nrdepfit):
            depfit.append(fh.readline())
        fh.readline()#seed
        seedinitvaluef=int(fh.readline())
        fh.close()
        return (inputfilename, modfilename, parametersfilename, flagdata, flagcut, nrtraces, Vrestf, esynf, nrparamsfit,
                paramnr, paramname, paraminitval, paramsconstraints, nrdepnotfit,depnotfit, nrdepfit, depfit, seedinitvaluef)

    def getColumns(self, inFile, delim="\t", header=True):
        cols = {}
        indexToName = {}
        for lineNum, line in enumerate(inFile):
            if lineNum == 0:
                headings = line.split(delim)
                i = 0
                for heading in headings:
                    heading = heading.strip()
                    if header:
                        cols[heading] = []
                        indexToName[i] = heading
                    else:
                        cols[i] = [heading]
                        indexToName[i] = i
                    i += 1
            else:
                cells = line.split(delim)
                i = 0
                for cell in cells:
                    cell = cell.strip()
                    cols[indexToName[i]] += [cell]
                    i += 1
        return cols, indexToName  

    
    def readexpfile(self, configname, num=0):
        [inputfilename, modfilename, parametersfilename, flagdata ,flagcut, nrtraces, Vrestf, esynf, nrparamsfit, paramnr, 
         paramname, paraminitval,paramsconstraints, nrdepnotfit, depnotfit, nrdepfit, depfit, seedinitvaluef] = self.readconffile(configname)
        times = []
        currents = []
        data = open("GUI/transfer/" + inputfilename.strip('\n'),'r')
        cols, indexToName =self.getColumns(data,header=False)
        if (flagdata==0):
            vecc=cols[0]
            timevecprov = [] 
            for elem in vecc:
                if elem:
                    timevecprov.append(float(elem))
            vecc2=cols[num]
            vecallprov = []
            for elem in vecc2:
                if elem:
                    vecallprov.append(float(elem))
        else:
            vecc = cols[2*num]
            timevecprov = []
            for elem in vecc:
                if elem:
                    timevecprov.append(float(elem))
            vecc2 = cols[2*num+1]
            vecallprov = []
            for elem in vecc2:
                if elem:
                    vecallprov.append(float(elem))
        return (timevecprov,vecallprov)  