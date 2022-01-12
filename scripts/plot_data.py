import matplotlib.pyplot as plt
import sys
import numpy as np
from numpy.polynomial.polynomial import polyfit

# read in the plotting data
data = open(sys.argv[1]).read()
fields = data.split()

x1=[]
y1=[]

x2=[]
y2=[]

x3=[]
y3=[]

# generate x,y lists for each income class
# x is change in people on SNAP
# y is expected number of jobs created
for f in fields:

     f=f.split("|")

     if f[3]=="LOW":
     
          x1+=[float(f[2])]
          y1+=[float(f[1])]

     elif f[3]=="MID":
     
          x2+=[float(f[2])]
          y2+=[float(f[1])]  

     elif f[3]=="HIGH":
     
          x3+=[float(f[2])]
          y3+=[float(f[1])]


fig, axes = plt.subplots(nrows=3,ncols=1)

# plot low income counties
axes[0].scatter(x1,y1,color='b', label="LOW INCOME")
axes[0].set_ylim((-100,2500))
axes[0].set_xlim((-25000,25000))

# plot middle income counties
axes[1].scatter(x2,y2,color='r',label="MIDDLE INCOME")
axes[1].set_ylim((-100,5000))
axes[1].set_xlim((-100000,100000))
axes[1].set_ylabel("Expected Number of Jobs Created", fontsize=8)

# plot high income counties
axes[2].scatter(x3,y3,color='g', label = "HIGH INCOME")
axes[2].set_ylim((-100,2000))
axes[2].set_xlim((-25000,25000))

# adjust margins of the plot
plt.subplots_adjust(left=0.1, bottom=0.1, top=.95, right=0.8)

# linear best fit line for low income counties
x1_np = np.array(x1)
a1, b1 = polyfit(x1_np,y1,1)
axes[0].plot(x1_np, a1+b1*x1_np, '-')

# linear best fit line for middle income counties
x2_np = np.array(x2)
a2, b2 = polyfit(x2_np,y2,1)
axes[1].plot(x2_np, a2+b2*x2_np, '-')

# linear best fit line for high income counties
x3_np = np.array(x3)
a3, b3 = polyfit(x3_np,y3,1)
axes[2].plot(x3_np, a3+b3*x3_np, '-')

# include key of colors and income types
fig.legend(loc="lower right", fontsize=7)

# label the x axis and title graph
plt.xlabel("Actual Change In People on SNAP", fontsize=8)
fig.suptitle("Expected Jobs Created against Change in People on SNAP", fontsize=9)

# save to pdf
fig.savefig("plot.pdf")

