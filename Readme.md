# 3D printing unit cost optimization
#### Project developed for the course Bio-Inspired Artifical Intelligence taught at the University of Trento

## Requirements
python 3.6+

PIP modules:
```
inspyred
numpy
matplotlib
```

PrusaSlic3r or Slic3r

## How to run

Edit the file `slicing.py` and set the variable `slic3r_path` to the path on your system. Set `ini_file` to the path of your slic3r configuration.

### Material Optimization

To run the material optimization

```bash
python material_optimization.py
```


### Time Optimization

To run the time optimization

```bash
python time_optimization.py
```


### Overall Cost Optimization

To run the overall cost optimization

```bash
python main.py
```

you will find the results in the `gcodes` folder under the name `best_....gcode`, the summaries and fitness trends inside the folder `summaries`.

For the boxplots run the script `boxplot.py`, the results will be available in the `summaries` folder.