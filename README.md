# Chicago Public Library Visitor Visualizations
## Created by: Christopher Carlsson, Rahul D'Mello, Nathan Parker

Hello! This readme provides the necessary details in order to take advantage of the Chicago Public Library visualizations.

Once this repo has been cloned, the file "chicagodash.py" can be run, which creates the dashboard of visualizations. These visualizations can be used to determine timing for renovations, which branches are most in need of renovations, and the impact that location of a closure would have on local branches.

The first visualization "Monthly Heatmap" shows the count of visitors for a branch in a given month. The visitors are standardized in order to compare the smaller branches with each other, after feedback that certain branches overwhelmed the rest of the visualization. December has a notably lower visitor count. Additionally, January and October seem to mark a decrease across a few different branches. This is helpful in determining the best time to close a branch.

![Screenshot 2023-12-05 004625](https://github.com/rahuldmello24/ds_4200_project/assets/122840422/96ede757-acb3-419d-baa2-3a7bc5cccaca)

The second visualization "Renovation Year" shows the last year that several branches had a renovation. This was developed after feedback was provided that a way to determine which branch is most in need of renovations would be helpful. This visualization has a way to filter which years were last renovated before a certain year, and reveals that North Austin is most overdue for a a renovation.

The third visualization "Geographic Rendering" visualizes the location of Chicago Public Libraries and the number of visitors they bring in each year. These libraries can then be compared by location, and can be used to determine what branches are most likely to receive an influx of visitors in the event of a closure for renovation.
