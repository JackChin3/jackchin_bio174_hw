import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.graph_objs import Histogram
from plotly.subplots import make_subplots
import streamlit as st


def newGen(fA, fit, pop):

    fa = (1 - fA)
    fAA = (fA ** 2)
    fAa = (2 * fA * fa)
    faa = (fa ** 2)
    wAA = fit[0]
    wAa = fit[1]
    waa = fit[2]
    M = (wAA*fAA) + (wAa*fAa) + (waa*faa)
    fAA1 = ((wAA*fAA) / M)
    fAa1 = ((wAa*fAa) / M)
    faa1 = ((faa*waa)/M)

    nAA1 = np.random.binomial(pop, fAA1)
    nAa1 = np.random.binomial(pop, fAa1)
    naa1 = np.random.binomial(pop, faa1)

    newpop =  nAA1 + nAa1 + naa1

    fA1 = (nAA1 + ((1/2) * nAa1)) / newpop
    return fA1


def simulate(initA, pop, fit, gen, sim):
    fig = make_subplots(rows=2, cols=1)
    hist = []
    for i in range(sim):
        gen_fA = []
        gen_fA.append(initA)
        newA = initA
        for i in range(gen):
            newA = newGen(newA, fit, pop)
            gen_fA.append(newA)
        fig.add_trace(go.Scatter(x = np.array(range(gen+1)), y = gen_fA, mode = 'lines')) 
        hist.append(gen_fA[-1])                     
        # print(gen_fA)
    histo = Histogram(x=hist, opacity=0.5, autobinx=False, xbins=dict(
        start=-0.01,
        end=1.01,
        size=0.01
    ))
    fig.append_trace(histo, 2, 1)
    fig['layout']['xaxis2'].update(range=[-0.01, 1.01])
    fig['layout']['yaxis1'].update(range=[0, 1])
    fig['layout'].update(height=600, width=800)
    fig['layout'].update(showlegend=False)
    return fig

with st.sidebar:
    nSim = st.slider('Number of Simulations:',min_value=1,max_value=100,step=1)
    AA = st.slider('Fitness of AA:',min_value=0.,max_value=1.,step=0.05,value=1.)
    Aa = st.slider('Fitness of Aa:',min_value=0.,max_value=1.,step=0.05,value=1.)
    aa = st.slider('Fitness of aa:',min_value=0.,max_value=1.,step=0.05,value=1.)
    pop = st.select_slider('Population Size:',[10,50,100,500,1000])
    gen = st.slider("Number of Generations:",min_value=100,max_value=1000,step=100)
    stA = st.slider("Starting frequency of A:", min_value=0.01,max_value=0.99,step=0.01, value=0.5)

with st.empty():
    plot = simulate(stA, pop, [AA, Aa, aa], gen, nSim)
    st.write(plot)
