#!/usr/bin/env python
# coding: utf-8

# In[1]:


import segyio
import matplotlib.pyplot as plt
import numpy as np
from shutil import copyfile
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


filename = 'C:/Users/karth/Desktop/Research Literature/Dutch Government_F3_entire_8bit seismic.segy'


# In[3]:


seismic_data = segyio.tools.cube(filename)


# In[5]:


print(str(np.shape(seismic_data)[0])) ## Survey Inline.


# In[4]:


print(str(np.shape(seismic_data)[1])) ## Survey Crossline.


# In[6]:


## Plotting the seismic data. ( Amplitude Slice )

fig = plt.figure(figsize=(25,15))
ax = fig.add_subplot(121)

sim = ax.imshow(seismic_data[:,150,:].T,cmap = 'RdBu')
fig.colorbar(sim , ax = ax)

ax.invert_xaxis()


## Seismic Slice.

ax1 = fig.add_subplot(122)
amp = ax1.imshow(seismic_data[:,:,150], cmap='RdBu')
fig.colorbar(amp, ax=ax1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.invert_xaxis()


# # Inline For Amplitudes

# In[9]:


with segyio.open(filename, "r") as segyfile:
    # Print inline and crossline ranges
    print('Amplitude Inline range: ' + str(np.amin(segyfile.ilines)) + ' - ' +str(np.amax(segyfile.ilines))) 
    print('Amplitude Crossline range: ' + str(np.amin(segyfile.xlines)) + ' - ' +str(np.amax(segyfile.xlines)))


# In[20]:


## Printing Inline and twt values
i = 0
with segyio.open(filename) as f:

    data = segyio.tools.cube(f)
    inline_data = f.iline
    crossline_data = f.xline

    inlines = f.ilines
    crosslines = f.xlines  
    twt = f.samples
    sample_rate = segyio.tools.dt(f) / 1000
    print('Inline range from', inlines[0], 'to', inlines[-1])
    print('Crossline range from', crosslines[0], 'to', crosslines[-1])
    print('TWT from', twt[0], 'to', twt[-1])   
    print('Sample rate:', sample_rate, 'ms')
    
    fig = plt.figure(figsize=(25,15))
    ax1 = fig.add_subplot(122)
    plt.plot(f.trace[0])
    ax1.invert_yaxis()
    ax1.invert_xaxis()


# In[ ]:





# # Seismic And Similarity

# In[22]:


similarity = 1- seismic_data


fig = plt.figure(figsize=(14,6))

ax = fig.add_subplot(121)
sim = ax.imshow(similarity[:,15,:].T, cmap = 'seismic') ## Invert to view on reflection on floor.
fig.colorbar(sim, ax=ax)
ax.set_xticks([])
ax.set_yticks([])
ax.invert_xaxis()

ax1 = fig.add_subplot(122)
amp = ax1.imshow(seismic_data[:,15,:].T, cmap='seismic') ## Viewing 15 Inline.
fig.colorbar(amp, ax=ax1)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.invert_xaxis()


# # 2D Seismic Data

# In[23]:


filenm = 'C:/Users/karth/Downloads/L23741.SGY'


# In[24]:


with segyio.open(filenm, ignore_geometry=True) as f:
    # Get basic attributes
    n_traces = f.tracecount
    sample_rate = segyio.tools.dt(f) / 1000
    n_samples = f.samples.size
    twt = f.samples
    data = f.trace.raw[:]  # Get all data into memory (could cause on big files)

f'N Traces: {n_traces}, N Samples: {n_samples}, Sample rate: {sample_rate}ms, Trace length: {max(twt)}'


# In[26]:


def plot_segy(file):
    # Load data
    with segyio.open(file, ignore_geometry=True) as f:
        # Get basic attributes
        n_traces = f.tracecount
        sample_rate = segyio.tools.dt(f) / 1000
        n_samples = f.samples.size
        twt = f.samples
        data = f.trace.raw[:]
    # Plot
    plt.style.use('ggplot')  # Use ggplot styles for all plotting
    vm = np.percentile(data, 99)
    fig = plt.figure(figsize=(18, 8))
    ax = fig.add_subplot(1, 1, 1)
    extent = [1, n_traces, twt[-1], twt[0]]  # define extent
    ax.imshow(data.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto', extent=extent)
    ax.set_xlabel('CDP number')
    ax.set_ylabel('TWT [ms]')
    ax.set_title(f'{file}')


# In[32]:


# Setup the destination file
destination = 'Cut.SGY'
# Define the sample index to cut on
cut_time = 4000
cut_sample = int(cut_time / sample_rate)+1


# In[33]:


with segyio.open(filenm, ignore_geometry=True) as src:
    spec = segyio.tools.metadata(src)
    spec.samples = spec.samples[:cut_sample]
    with segyio.create(destination, spec) as dst:
        dst.text[0] = src.text[0]
        dst.bin = src.bin
        dst.bin.update(hns=len(spec.samples))
        dst.header = src.header
        dst.trace = src.trace


# In[31]:


plot_segy(filenm)


# In[34]:


plot_segy(destination)


# # Exploring Further
# 

# In[6]:


with segyio.open(filename) as f:
    ##for line in f.xline[2:10]:
        ##print(line)
        print(f.depth_slice[100])
        
        for line in f.iline[:200]:
            plt.imshow(line.T , cmap = 'seismic') ## Seismic Section of inline.


# In[40]:


with segyio.open(filename) as segyfile:
# Memory map file for faster reading (especially if file is big...)
    segyfile.mmap()

    # Print binary header info
    print(segyfile.bin)
    print(segyfile.bin[segyio.BinField.Traces])

    # Read headerword inline for trace 12
    print(segyfile.header[12][segyio.TraceField.INLINE_3D])

    # Print inline and crossline axis
    print(segyfile.xlines)
    print(segyfile.ilines)
    
    ## Post Stack data.
    # Read data along first xline
    data = segyfile.xline[segyfile.xlines[1]]

    # Read data along last iline
    data = segyfile.iline[segyfile.ilines[-1]]

    # Read data along 100th time slice
    data = segyfile.depth_slice[100]


# In[ ]:




