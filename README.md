SPiBlender
==========

SPiBlender is a package devoted to the generation of synthetic images for spaceborn instruments
based on SPICE geometry. It integrates Blender for rendering engine. 

SPICE is an essential tool for scientists and engineers alike in the 
planetary science field for Solar System Geometry. Please visit the NAIF 
website for more details about SPICE.

![alt text](https://github.com/esaSPICEservice/spiblender/blob/main/SIM/JUICE_JMC-12034-12-24T21:17:14.png?raw=true) 

Function and Purpose
--------------------

The generation of synthetic images is used in different steps of a space mission, from AOCS and GNC systems,
to Instrument Calibration and Data Analysis. SPiBlender requires the user to specify 
few parameters regarding the observing camera and time of interest, and SPiBlender
obtains the rest of the required geometric parameters from the kernel pool of the specified meta-kernel
to be loaded. 

SPiBlender is developed and maintained by the [ESA SPICE Service (ESS)](https://spice.esac.esa.int).


Approach for SPiBlender
----------------------

SPiBlender can either be provided as a Service by ESS or it can be provided as a 
piece of software to be integrated in the given project SGS system. Configuration 
management and distribution of the software is discussed in the appropriate 
section of this document. Depending on the taken approach the relationships 
with other systems might change. What is described here assumes service providing 


Configuration file
------------------

The parameters to be specified in the configuration file are described hereafter:

- **Metakernel**: Path to the meta-kernel to load.
- **utc0**: Start date
- **utcf**: End date
- **tsamples**: Number of samples (number of images)
- **instrument**: Name of instrument as defined in the SPICE Instrument Kernel for which field of view and detector parameters will be extracted
- **lt**: Light-time correction method. 
- **yfov** (optional): Field of view reference angle, if left blank, SPiBlender will try to obtain the reference angle from the kernel pool 
- **pxlines** (optional): Pixel lines, if left blank, SPiBlender will try to obtain the pixel lines from the kernel pool 
- **pxsamples** (optional): Pixel samples, if left blank, SPiBlender will try to obtain the pixel samples from the kernel pool 
- **lightfactor**: Float controlling the intensity of the illumination source
- **output**: Path to the output directory where to save the render images

Installation
------------

There is no need to install SPiBlender. If you wish to use SPiBlender, first download or clone the project. 
Then update the config file ``config.json`` with the parameters for your study case and run ``render.sh``.


Requirements:
-------------

- [Blender](https://www.blender.org/) >= 3.2
- [Python](https://www.python.org/) >= 3.6
- [numpy](https://numpy.org/) >= 1.8.0
- [matplotlib](https://matplotlib.org/) >= 3.5.0
- [spiceypy](https://github.com/AndrewAnnex/SpiceyPy/) >= 4.0.3
- [trimesh](https://trimsh.org/) >= 3.14.1
- [pyrender](https://github.com/mmatl/pyrender/) >= 0.1.45


How to Help
-----------

Feedback and new functionalities are always welcome, if you discover that a 
function is not 
working as expected or if you have a function that you believe can be of 
interest to other people please open an issue or contact [me](alfredo.escalantd.lopez@ext.esa.int).


Known Working Environments:
---------------------------

SPiBlender is compatible with modern 64 bits versions of Linux and Mac. 
If you run into issues with your system please submit an issue with details. 

- OS: OS X, Linux
- CPU: 64bit
- Python 3.5