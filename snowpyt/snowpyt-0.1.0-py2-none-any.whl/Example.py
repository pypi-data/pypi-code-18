
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

import pit_class as pc

filename = 'data_example/20161216_snowpit.csv'  #[insert path to file]

pit1 = pc.Snowpit_standard()
pit1.filename = filename
pit1.load_csv()
pit1.summary_plot(metadata=False)

pit1.summary_plot(metadata=True)

# change the panel order
pit1.summary_plot(plots_order=['density', 'temperature', 'hardness', 'stratigraphy'])

# plot less panel
pit1.summary_plot(plots_order=['stratigraphy', 'hardness'])






