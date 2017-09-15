# TO-DO
## ScatterChart
* Multiple polygon selections
  [X] Add option to add several selections;
  [X] Add option to remove a selection;
  [ ] Add option to move a polygon selection.

* Polygon selection
  [ ] Add option to remove a point (POSTPONED DUE TOO MUCH WORK);
  [ ] Add option to move a point (POSTPONED DUE TOO MUCH WORK);
  [X] Remove the convex hull constraint.

* Dataset
  [ ] Add option to add point sets instead of rewritting the data;
  [ ] Apply the same color/properties to each point set;
  [ ] Add a legend to the plot.

## Projection classes
* Standarize the interface for the projection classes (if possible);
* Replace the tsneGen, mdsGen and genSPE methods for ``` __call__```;
  * This allows for a cleaner way of applying a projection and can currently be done by just replacing the methods' names.
