# Sonic Rush Rerun Level Creator

This is a level creator that uses blender to create the shape and geometry and then import it in unity.

Steps :


SETUP



1. Export both files in the same folder.
2. Open SRRLevelCreatorBlend.blend
3. Go to Edit -> Preference -> File Paths
4. In Asset Libraries, add the folder in which you have both files.
   - Set the import method as "Append (Reuse Data)"
5. Then in the Asset Explorer, Refresh and you should have a library called the name of your folder!
   

Extra Help (WIP)

1. Go to Scripting
2. There should be a file called Toggle Trajectory Lines, Run it.
3. You'll have a new little menu called Trajectory where you can toggle trajectory previews when selecting objects. (Only works on springs and Dash Rings for now.)



EXPORTING


1. Select "**File"**, then scroll down to the "**Export**" option, then click "**glTF 2.0**"
2. over on the right side, select the "**Include**" drop-down menu, then toggle "**Custom** **Properties**"
3. toggle "**Remember Export Settings**" above said drop-menu

&nbsp;(Step 3 is optional, but it will save your setting so you dont have to re-select "custom properties" every time you export)

4\.    Name the file what ever you want!



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Rules :
If a mesh is Solid, Its name must contain "**Geometry**"
If a mesh is Solid AND box shaped, Its name must/can contain "**BoxGeometry**"
If a mesh is a OneWayPlatform, its name must contain "**OneWayPlatform**"
If a mesh is a RollZone, it must be boxshaped and its name must contain "**RollZone**"
If a mesh is a Breakable Wall, it must contain  "**Breakable**"
If you want a mesh to be invisible but still collide, add "(Hide)" to its name.
If you want a mesh to be a homing target, add "HomingTarget" to its name.
**DO NOT** put the name of any stage objects inside geometry objects as they will be overriden by the object replacement.


When in-game you have 3 options for reloading

Press " **H** " to go back to the browser to select a different level

Press " **R** " to quick reload the entire stage after making edits and go back to the start of the stage

Press " **T** " to soft quick reload, which is the same function as R, but keeps your current position 



Any Question, reach out to @Diamax in the discord