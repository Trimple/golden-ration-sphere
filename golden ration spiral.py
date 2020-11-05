#Author-
#Description-
# For more details see: https://capolight.wordpress.com/2018/07/02/how-to-sketch-equation-curves-in-fusion-360/
import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
	ui = None
	try:
		# Variables
		small_circle_diameter = 0.2
		big_circle_diameter = 10
		number_of_circles = 10000

		optimization_window_length = 20	# 20 is a good number, it is better to leave it as it is

		# basic skeleton
		app = adsk.core.Application.get()
		ui = app.userInterface
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
		# while specifying the profile and that a new body is to be created
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

		# Variables for golden ration algorithm
		i = 0	# iterator of circles
		optimization_counter = 0	# optimization counter
		optimization_counter_iteration = 0	# optimization counter
		pi_value = 3.14159
		golden_ratio = 0.618034
		golden_ratio_angle = golden_ratio*2*pi_value

		while i < number_of_circles:
			## Copy small circle
			rootComp.features.copyPasteBodies.add(rootComp.bRepBodies.item(1))

			# Make collection for the copied body
			bodies = adsk.core.ObjectCollection.create()
			bodies.add(rootComp.bRepBodies.item(i+2 - optimization_counter_iteration*optimization_window_length))
			
			# Calculate spherical position of that particular small sphere
			lon=(i*golden_ratio-int(i*golden_ratio))*2*pi_value
			if lon > pi_value:
				lon -= 2*pi_value
			
			lat = math.asin(-1 + 2*i/(float(number_of_circles)))

			# Calculate сartesian coordinates from spherical
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
			
			## Optimize script run-time.
			# for run-time optimization, we toggle "Do not capture design history" for every optimization_window_length small spheres 
			# and then immediately return design history. This script uses the move feature which is impossible without design history. 
			# Relaunching design history highly optimizes fusion 360 script runtime by clearing design history over and over again.
			# Also after every optimization_window_length small spheres, they all combine into a single body to optimize the number of bodies in use.
			optimization_counter += 1

			if optimization_counter == optimization_window_length:
				optimization_counter = 0
				optimization_counter_iteration +=1
				
				# Disable design history
				design.designType = adsk.fusion.DesignTypes.DirectDesignType
				design.designType = adsk.fusion.DesignTypes.ParametricDesignType

				# combine all bodies but the first small sphere into one body
				new_other_bodies = adsk.core.ObjectCollection.create()
				body_iterator = 0
				for next_body in rootComp.bRepBodies:
					if body_iterator < 2:
						body_iterator += 1
						continue
					new_other_bodies.add(rootComp.bRepBodies.item(body_iterator))
					body_iterator += 1
				
				combineFeatures = features.combineFeatures
				main_body = rootComp.bRepBodies.item(0)
				combineFeatureInput = combineFeatures.createInput(main_body, new_other_bodies)
				combineFeatureInput.operation = 0
				combineFeatureInput.isKeepToolBodies = False
				combineFeatureInput.isNewComponent = False
				returnValue = combineFeatures.add(combineFeatureInput)

			i += 1
		
		# combine all remaining bodies into one
		other_bodies = adsk.core.ObjectCollection.create()
		i = 0
		for next_body in rootComp.bRepBodies:
			if i == 0:
				i = 1
				continue
			other_bodies.add(rootComp.bRepBodies.item(i))
			i += 1

		combineFeatures = features.combineFeatures
		main_body = rootComp.bRepBodies.item(0)
		combineFeatureInput = combineFeatures.createInput(main_body, other_bodies)
		combineFeatureInput.operation = 0
		combineFeatureInput.isKeepToolBodies = False
		combineFeatureInput.isNewComponent = False
		returnValue = combineFeatures.add(combineFeatureInput)

	# Error handeling
	except:
		if ui:
			ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
