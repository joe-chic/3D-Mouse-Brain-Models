import sympy

# https://www.eurekalert.org/news-releases/560200
# non rigid transformation refers to a series of image techniques in which there are geometric differences that cannot be accounted by
# What is cross correlation?
# A rigid transformation is a geometric transformation in the Eucledean Space in which the Euclidean distance between every pair of points is preserved.
# What is handendness?

# current oblique height any factor addition is : 153 (images)

# >>> Why is the number of images variable between each view type?:
    # New images are made out of Frame Interpolation for Large Motion.
    # Are the number of images always the same as they are captured. If not, why not? Why yes, what is influencing the number? Is the size of the brain, is it the variability
    # of protein expression between brain sections affecting?

# Is the way of representing missing information proper? How is tissue discontinuity handled in other investigations? Is the use of black frames actually correct, is the scaling between images via pixels okay?
# I think so, but how to determine the amount of separation between histological cuts for our case?

# If it is feature based, then which regions would you use for comparing a full brain with expression brains?

factor = sympy.symbols('factor')
current_oblique_height = sympy.symbols('current_oblique_height')
# Even if we found an equilibrium between the dimensions of the images, that doesn't mean that the intersection between the brains will be perfect.
# In which ways the intersection will be flawed.
expr1 = (factor+1)*(current_oblique_height)-factor - 2668
expr2 = (current_oblique_height) / 2

solution = sympy.solve([expr1,expr2],factor)
print(solution)
