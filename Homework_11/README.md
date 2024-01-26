# Yeast Genome Browser

Write a yeast Genome Browser program, similar to the one [here](http://dna.pomona.edu/bio174/index.html) or [here](http://dna.pomona.edu/bio174/doGenomeBrowser.html) (this second one made by a previous student). Your program should be able to do the following:

1. The user should be able to enter either a chromosome and a position, or the name of a gene. If the user enters all three, the gene name should take precedence. If the user doesn’t enter anything the browser should go by default to position 1 of chromosome 1. If the user only enters the chromosome number the browser should go to position 1 of that chromosome.

2. The genome browser should show the yeast chromosome in 5kb intervals. The interval starts at the position given by the user and shows 5kb starting at that position. If the user provides a gene name you should start the genome map at 1kb upstream of the start of the gene (or the end if the gene is in the negative strand).

3. Each gene should be presented in a line, protein coding genes in blue (dark blue for the forward strand and light blue for genes in the reverse strand) and tRNA genes in green (dark green in forward strand; light green in reverse).

4. When the user hovers over a line with the mouse, a gray square encompassing the whole line should show up to allow the easy identification of the gene name, which is in the left. This area should be linked with the page for the gene in SGD, you need to figure out how to link the gene to its SGD page.

5. Hovering over the rectangle representing the gene should show the start and end coordinates of the gene in a pop up.

6. Navigation: In addition to being able to navigate by entering the genome coordinates and gene name, the user should be able to move along the chromosome by clicking on the arrows by the top rectangle showing the genome sequence. The left arrow decreases the start position by 1000, and the right arrow increases the position by 1000. Make sure that the program will stop decreasing and increasing the coordinates when it reaches position 1 or the last position of a chromosome (in fact final position -5kb). (You might need to create a dictionary with the lengths of the yeast chromosomes to know where the end of the chromosome is).

7. The browser should keep track of the chromosome it is currently in. That means that the chromosome that is currently showing is the one that will be selected in the drop down by default.

8. These are the minimum requirements. Feel free to add bells and whistles to the browser. [Here](http://dna.pomona.edu/bio174/index.html) is an example of another way to do the genome browser that instead of opening a new window for the SGD page of the gene, opens the SDG page inside the current page, in addition it shows the SVG figure besides the form.

9. Use the database we made last class, or at least the gif table. After the user submits a query you should query the database for the genes in that part of the chromosome. The table also has the lengths of the yeast chromosomes.
