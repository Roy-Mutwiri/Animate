-- Use this script to create a new file and put something in it. Call it like this:
-- moho.exe CreateNewFile.lua
-- The main function is MohoScript. The BuildGear function is used as an example, and not a general part of a command-line script.

taperedCogs = false

function BuildGear(mesh, numCogs, innerRadius)
	local numPoints = numCogs * 4
	local oldNumPoints = mesh:CountPoints()
	local v = LM.Vector2:new_local()
	local dAngle = (math.pi * 2) / numPoints
	local angle = dAngle * 1.5
	local startAngle = angle
	local bigR = 0.75
	local littleR = innerRadius
	local smallAngleStep = dAngle
	local bigAngleStep = dAngle

	if (not taperedCogs) then
		bigAngleStep = dAngle * 2
		--local d1 = littleR * math.sin(dAngle)
		local d2 = bigR * math.sin(dAngle)
		local l = littleR * math.cos(dAngle)
		smallAngleStep = math.atan(d2, l) - bigAngleStep / 2
		angle = bigAngleStep / 2 + smallAngleStep
	end
	startAngle = angle

	mesh:SelectNone()

	for i = 1, numCogs do
		if (not taperedCogs) then
			angle = startAngle - (i - 1) * bigAngleStep * 2
		end
		v.x = littleR * math.sin(angle)
		v.y = littleR * math.cos(angle)
		if (i == 1) then
			mesh:AddLonePoint(v, 0)
		else
			mesh:AppendPoint(v, 0)
		end
		angle = angle - smallAngleStep

		v.x = bigR * math.sin(angle)
		v.y = bigR * math.cos(angle)
		mesh:AppendPoint(v, 0)
		angle = angle - bigAngleStep

		v.x = bigR * math.sin(angle)
		v.y = bigR * math.cos(angle)
		mesh:AppendPoint(v, 0)
		angle = angle - smallAngleStep

		v.x = littleR * math.sin(angle)
		v.y = littleR * math.cos(angle)
		mesh:AppendPoint(v, 0)
		angle = angle - bigAngleStep
	end

	v.x = littleR * math.sin(angle)
	v.y = littleR * math.cos(angle)
	mesh:AppendPoint(v, 0)

	mesh:WeldPoints(oldNumPoints + numPoints, oldNumPoints, 0)

	for i = 0, numPoints - 1 do
		mesh:Point(oldNumPoints + i):SetCurvature(MOHO.PEAKED, 0)
	end

	mesh:SelectConnected()
end

function MohoScript(moho)
	moho:FileNew()

	local mesh = moho:Mesh()
	if (mesh == nil) then
		return
	end

	BuildGear(mesh, 7, 0.5)
	local shapeID = moho:CreateShape(true, false, 0)

	moho:FileSaveAs("C:\\Users\\somebody\\Desktop\\XXX.moho");
	print("Ran startup script");

	moho:Quit()
end
