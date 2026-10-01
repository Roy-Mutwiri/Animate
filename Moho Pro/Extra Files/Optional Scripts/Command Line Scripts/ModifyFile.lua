-- Use this script to modify an existing file. Call it like this:
-- moho.exe MyFile.moho ModifyFile.lua
-- Setting the curvature is just an example. What your script actually does is up to you.

function MohoScript(moho)
	local mesh = moho:Mesh()
	if (mesh == nil) then
		return
	end

	for i = 0, mesh:CountPoints() - 1 do
		local pt = mesh:Point(i)
		pt:SetCurvature(MOHO.SMOOTH, moho.drawingLayerFrame)
		pt:ResetControlHandles(moho.drawingLayerFrame)
	end

	moho:FileSave();
	print("Ran startup script");

	moho:Quit()
end
