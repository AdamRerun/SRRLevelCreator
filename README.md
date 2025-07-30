# Sonic Rush Rerun Level Creator

WARNING : UPDATE ALL THE SCRIPTS IN YOUR BLENDS WHEN YOU CAN

This is a level creator that uses blender to create the shape and geometry and then import it in unity.

This was made with inspiration from Strix's work. Thanks a lot to him for his work and expertise.

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


UPDATING LEVEL OBJECTS

If you made a level and put a bunch of objects that aren't up to date with current versions, don't worry.
In this project there is a python file called "UpdateExistingObjects.py".

Here are the steps to use it. 

1. Open the level you want to update the objects.
2. Do a quick check to make sure that the objects from the asset files are the updated versions. (Custom properties, transform, etc.)
3. Open the scripting tab.
4. Create a new Script and in it, paste the content of the UpdateExistingObjects.py script.
5. Take the updated version from the Asset explorer and place it wherever in your level.
(WARNING : The updated version needs to have the original name of the object. Example, if you wanted to update all of your springs. You'd need the newly placed spring to be called "Spring" not "Spring (1)".
So make sure that you rename it to be the original name.)
6. Select the newly placed object and run the script.
Normally, every instance of that object should have been replaced by an updated one but should have kept their custom properties.

The playground folder is ignored by the repo so you should be able to save your projects into it without affecting your local repo.

THO honestly you should save your work in the official Sonic Rush Rerun Asset Repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Rules :
If a mesh is Solid, Its name must contain "**Geometry**"
If a mesh is Solid AND box shaped, Its name must/can contain "**BoxGeometry**"
If a mesh is a OneWayPlatform, its name must contain "**OneWayPlatform**"
If a mesh is a RollZone, it must be boxshaped and its name must contain "**RollZone**"
If a mesh is a Breakable Wall, it must contain  "**Breakable**"
If you want a mesh to be invisible but still collide, add "(Hide)" to its name.
If you want a mesh to be a homing target, add "HomingTarget" to its name.
You can make grind rails by using a bevier curve and adding/putting "Rail" in its name. Make sure it has the right orientation.
**EXPERIMENTAL*** You can make geometry splines by adding a bevier curve to its children and adding/putting "Path" in its name.

LOOP ASSETS : 
Loop asset's geometry can be modified. But it's limited. You need to allow entry and exit for the character. So :
you may increase the scale and lower it. -> This mostly works perfectly fine.
You may modify the geometry to make the roof sit higher and make the walls thicker
BUT
It is your job to align the character's exit with the rest of the stage so the character doesnt fall off axis.
It is your job to make sure passing through the loop is still possible.
It is your job to make sure
While some weird loops may need specific modification in engine, we will discuss those, making sure the collision mesh is usable is YOUR JOB.

***To export grind rails and splines, use the Export curve data script. It will make a button appear in the object contextual menu on the bottom right. (The Orange Square)***
**DO NOT** put the name of any stage objects inside geometry objects as they will be overriden by the object replacement.


When in-game you have 3 options for reloading

Press " **H** " to go back to the browser to select a different level

Press " **R** " to quick reload the entire stage after making edits and go back to the start of the stage

Press " **T** " to soft quick reload, which is the same function as R, but keeps your current position 



Any Question, reach out to @Diamax in the discord



