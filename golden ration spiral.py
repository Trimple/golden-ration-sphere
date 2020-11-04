#Author-
#Description-
# For more details see: https://capolight.wordpress.com/2018/07/02/how-to-sketch-equation-curves-in-fusion-360/
import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
	ui = None
	try:
		# Variables
		small_circle_diameter = 3
		big_circle_diameter = 20
		number_of_circles = 50

		# basic skeleton
		app = adsk.core.Application.get()
		ui = app.userInterface
		# doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType) # Открывает новый файл
		design = app.activeProduct

		# Get the root component of the active design.
		rootComp = design.rootComponent
		features = rootComp.features
		# combineFeatures = features.combineFeatures

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

		i = 0
		pi_value = 3.14159
		golden_ratio = 0.618034
		golden_ratio_angle = golden_ratio*2*pi_value

		while i < number_of_circles:
			# Copy small circle
			rootComp.features.copyPasteBodies.add(rootComp.bRepBodies.item(1))

			# Make collection for the copied body
			bodies = adsk.core.ObjectCollection.create()
			# bodies.add(rootComp.bRepBodies.item(i+2))
			bodies.add(rootComp.bRepBodies.item(2))
			
			# Calculate spherical position of the sphere
			lon=(i*golden_ratio-int(i*golden_ratio))*2*pi_value
			if lon > pi_value:
				lon -= 2*pi_value
			
			lat = math.asin(-1 + 2*i/(float(number_of_circles)))

			# Calculate decart coordinates
			xCoord = big_circle_diameter*math.cos(lat)*math.sin(lon)
			yCoord = big_circle_diameter*math.cos(lat)*math.cos(lon)
			zCoord = big_circle_diameter*math.sin(lat)
			
			# Create a transform to do move
			vector = adsk.core.Vector3D.create(xCoord, yCoord, zCoord)
			transform = adsk.core.Matrix3D.create()
			transform.translation = vector

			# Create a move feature
			moveFeats = features.moveFeatures
			moveFeatureInput = moveFeats.createInput(bodies, transform)
			moveFeats.add(moveFeatureInput)
			
			i += 1
		
		# combine bodies
		bodies = adsk.core.ObjectCollection.create()
		i = 0
		for next_body in rootComp.bRepBodies:
			if i == 0:
				i = 1
				continue
			bodies.add(rootComp.bRepBodies.item(i))
			i += 1

		combineFeatures = features.combineFeatures
		main_body = rootComp.bRepBodies.item(0)
		combineFeatureInput = combineFeatures.createInput(main_body, bodies)
		combineFeatureInput.operation = 0
		combineFeatureInput.isKeepToolBodies = False
		combineFeatureInput.isNewComponent = False
		returnValue = combineFeatures.add(combineFeatureInput)



	# Error handeling
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
