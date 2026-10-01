function AddBlob(mesh, cx, cy, sx, sy)
	local v = LM.Vector2:new_local()
	local pts = {
		{-0.45, 0.10}, {-0.25, 0.42}, {0.18, 0.45}, {0.45, 0.20},
		{0.38, -0.22}, {0.04, -0.45}, {-0.36, -0.30}
	}
	mesh:SelectNone()
	local first = mesh:CountPoints()
	for i, p in ipairs(pts) do
		v.x = cx + p[1] * sx
		v.y = cy + p[2] * sy
		if i == 1 then
			mesh:AddLonePoint(v, 0)
		else
			mesh:AppendPoint(v, 0)
		end
	end
	mesh:WeldPoints(mesh:CountPoints() - 1, first, 0)
	for i = first, mesh:CountPoints() - 1 do
		mesh:Point(i):SetCurvature(MOHO.SMOOTH, 0)
	end
	mesh:SelectConnected()
end

function MohoScript(moho)
	moho:FileNew()
	local mesh = moho:Mesh()
	if mesh == nil then
		print("No mesh available")
		moho:Quit()
		return
	end
	AddBlob(mesh, 0, 0, 0.7, 0.9)
	moho:CreateShape(true, false, 0)
	moho:FileRender("D:\\Animate\\Projects\\HonestInterview\\ReferenceStudy\\interchange_test\\moho_shape_pass.png")
	moho:FileSaveAs("D:\\Animate\\Projects\\HonestInterview\\ReferenceStudy\\interchange_test\\moho_shape_pass.moho")
	print("Moho shape pass complete")
	moho:Quit()
end
