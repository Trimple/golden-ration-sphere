#Author-
#Description-
# For more details see: https://capolight.wordpress.com/2018/07/02/how-to-sketch-equation-curves-in-fusion-360/
import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
	ui = None
	try:
		# Variables
		small_circle_diameter = 2
		big_circle_diameter = 20
		number_of_circles = 10

		# basic skeleton
		app = adsk.core.Application.get()
		ui = app.userInterface
		# doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) # Открывает новый файл
		design = app.activeProduct

		# Get the root component of the active design.
		rootComp = design.rootComponent
		features = rootComp.features

		#--------------------------------------#
		# Create a new sketch on the xy plane.
		sketches = rootComp.sketches
		xyPlane = rootComp.xYConstructionPlane
		circle_sketch = sketches.add(xyPlane)

		# Draw a circle.
		circles = circle_sketch.sketchCurves.sketchCircles
		circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), big_circle_diameter)
		circle2 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), small_circle_diameter)

        # Draw a line to use as the axis of revolution.
		lines = circle_sketch.sketchCurves.sketchLines
		axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(-big_circle_diameter, 0, 0), adsk.core.Point3D.create(big_circle_diameter, 0, 0))

        # Get the profile defined by the circle.
		big_circle_prof = circle_sketch.profiles.item(1)
		small_circle_prof = circle_sketch.profiles.item(0)

		# Create an revolution input to be able to define the input needed for a revolution
		# while specifying the profile and that a new component is to be created
		revolves = rootComp.features.revolveFeatures
		big_circle_revInput = revolves.createInput(big_circle_prof, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
		small_circle_revInput = revolves.createInput(small_circle_prof, axisLine, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Draw spheres
		angle = adsk.core.ValueInput.createByReal(2*math.pi)
		big_circle_revInput.setAngleExtent(False, angle)
		small_circle_revInput.setAngleExtent(False, angle)
		
        # Create the extrusion.
		big_circle_ext = revolves.add(big_circle_revInput)
		small_circle_ext = revolves.add(small_circle_revInput)
		#--------------------------------------#

		# Move small circle
		bodies = adsk.core.ObjectCollection.create()
		bodies.add(rootComp.bRepBodies.item(1))

		# Create a transform to do move
		vector = adsk.core.Vector3D.create(0.0, 20.0, 0.0)
		transform = adsk.core.Matrix3D.create()
		transform.translation = vector

        # Create a move feature
		moveFeats = features.moveFeatures
		moveFeatureInput = moveFeats.createInput(bodies, transform)
		moveFeats.add(moveFeatureInput)

		# copy sphere

		rootComp.features.copyPasteBodies.add(rootComp.bRepBodies.item(1))


		# rootComp.features.copyPasteBodies.add(sourceBodies) # дописать копирование

		#То что ниже, пока не важно 
		# points = adsk.core.ObjectCollection.create() # Create an object collection for the points.

		# sphere_radius = 5

		# # Enter variables here. E.g. E = 50
		# startRange = 0 # Start of range to be evaluated.
		# # endRange = 2*math.pi # End of range to be evaluated.
		# splinePoints = 1000 # Number of points that splines are generated.
		# # WARMING: Using more than a few hundred points may cause your system to hang.
		# i = 0
		# pi_value = 3.14159
		# golden_ratio = 0.618034
		# golden_ratio_angle = golden_ratio*2*pi_value

		# while i <= splinePoints:
		# 	lon=(i*golden_ratio-int(i*golden_ratio))*2*pi_value
		# 	if lon > pi_value:
		# 		lon -= 2*pi_value
			
		# 	lat = math.asin(-1 + 2*i/(float(splinePoints)))

		# 	xCoord = sphere_radius*math.cos(lat)*math.sin(lon)
		# 	yCoord = sphere_radius*math.cos(lat)*math.cos(lon)
		# 	zCoord = sphere_radius*math.sin(lat)
                 
		# 	points.add(adsk.core.Point3D.create(xCoord,yCoord,zCoord))
		# 	i = i + 1
			
		# #Generates the spline curve
		# sketch.sketchCurves.sketchFittedSplines.add(points)
	
	# Error handeling
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
