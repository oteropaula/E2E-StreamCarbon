import matplotlib.pyplot as plt
import numpy as np

# define the devices we want to compare
devices = ['Smartphone', 'Laptop', 'TV 50" LED']

# co2 emissions in g/h for each device by country/global
global_emissions = [12, 21, 67]   # estimated global average
china_emissions = [16, 29, 90]    # estimated for china
usa_emissions = [10, 19, 59]      # estimated for usa
spain_emissions = [6, 12, 37]     # estimated for spain

# x positions for the bars
x = np.arange(len(devices))
width = 0.2  # width of each bar, smaller because we have 4 groups

# create the figure and axis
fig, ax = plt.subplots(figsize=(12,5))

# draw the bars for each country/global, colors chosen to be distinct but soft
rects1 = ax.bar(x - 1.5*width, global_emissions, width, label='Global', color='#004ce5')  
rects2 = ax.bar(x - 0.5*width, china_emissions, width, label='China', color='#9a9eb2')   
rects3 = ax.bar(x + 0.5*width, usa_emissions, width, label='USA', color='#babdcc')       
rects4 = ax.bar(x + 1.5*width, spain_emissions, width, label='Spain', color='#d8dae5')   

# set axis labels and title
ax.set_ylabel('CO$_2$ emissions (g/h)')
ax.set_xlabel('Device')
ax.set_title('CO$_2$ emissions for HD streaming by device: Global vs China vs USA vs Spain')
ax.set_xticks(x)
ax.set_xticklabels(devices)
ax.legend()  # add legend to distinguish the groups

# function to add numbers above the bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}',  # show the height as text
                    xy=(rect.get_x() + rect.get_width() / 2, height),  # position above bar
                    xytext=(0,3),  # small offset
                    textcoords="offset points",
                    ha='center', va='bottom')  # center align horizontally and place above

# call the function for all sets of bars
autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)

# make layout tight so nothing overlaps
plt.tight_layout()

# save the figure as a png in current folder
plt.savefig('co2_comparison_four_countries_pastel.png', dpi=300)

# finally show the plot
plt.show()
