# Fusion 360 golden ratio spiral for the sphere

This is a python script for the fusion 360. This script is used to generate a solid sphere that is wrapped around with lots of smaller spheres. Here are some examples:

<p> 
<image align="middle" src="/images/2000_spheres.png" alt="2000 spheres" width = 45%>
<image align="middle" src="/images/500_spheres.png" alt="500 spheres" width = 45%> <b>
<image align="middle" src="/images/50_spheres.png" alt="50 spheres" width = 45%>
<image align="middle" src="/images/30_spheres.png" alt="30 spheres" width = 45%>
</p>

You can play with 200 spheres model [here](https://a360.co/3mSpRJ5)

The script uses golden ratio points distribution. An interactive example can be seen [here](https://www.openprocessing.org/sketch/41142).

This script is completely free to use and modify and comes with a [MIT license](LICENCE.md)

## How to use

Right now script dosen't have a menue to input parameters from Fusion 360. You need to change this 3 values directly in the script file:

``` python
	small_circle_diameter = 1
	big_circle_diameter = 10
	number_of_circles = 1000
```
