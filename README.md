# Sonic Rush Rerun Level Creator

WARNING : UPDATE ALL THE SCRIPTS IN YOUR BLENDS WHEN YOU CAN

This is a level creator that uses blender to create the shape and geometry and then import it in unity.

This was made with inspiration from Strix's work. Thanks a lot to him for his work and expertise.

Steps :


SETUP



1. Export both files in the same folder.
2. Open Tutorial.blend
3. Go to Edit -> Preference -> File Paths
4. In Asset Libraries, add the folder in which you have both files.
   - Set the import method as "Append (Reuse Data)"
5. Then in the Asset Explorer, Refresh and you should have a library called the name of your folder!
6. Go to Scripting
7. In the Scripts Folder of this Repo, there should be a script called "Adam's Level Exporter". Import it to blender and Run it.
8. Now in your layout scene, you should have a Unity tab with a button that says "Export Unity Project". This will be your main way of exporting your level.
   8.1 - I advise right clicking the tab and pinning it so that it is always visible.
   
UPDATING LEVEL OBJECTS

If you made a level and put a bunch of objects that aren't up to date with current versions, don't worry.
In this project there is a python file called "UpdateExistingObjects.py".


The playground folder is ignored by the repo so you should be able to save your projects into it without affecting your local repo.

THO honestly you should save your work in the official [Sonic Rush Rerun Asset Repo](https://github.com/MelohRush/RushRerun-Repo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Rules :
If a mesh is Solid, Its name must contain "**Geometry**"
If a mesh is Solid AND box shaped, Its name must/can contain "**BoxGeometry**"
If a mesh is a OneWayPlatform, its name must contain "**OneWayPlatform**"
If a mesh is a RollZone, it must be boxshaped and its name must contain "**RollZone**"
If a mesh is a Breakable Wall, it must contain  "**Breakable**"
If you want a mesh to be invisible but still collide, add "(Hide)" to its name.
If you want a mesh to be a homing target, add "HomingTarget" to its name.
You can make grind rails by using a bevier curve and adding/putting "Rail" in its name. Make sure it has the right orientation.

***EXPERIMENTAL*** You can make geometry splines by adding a bevier curve to its children and adding/putting "Path" in its name.

Rails :
In Object Mode, Add A Bezier Curve to the scene.

Step 1. Tilt the Rail 90 degrees so that its normal are aligned with the level (Ctrl + T -> 90)
Step 2. Place your Bezier's Points to sculpt your Spline.
Step 3. In the Object Data Properties, In Geometry, Look for the Bevel section and set the Depth to something between .20 and .30 meters (.25m is perfect)
Step 4. Set the Offset to the same value as the Depth (This is to make it so the TOP of the rail is where Sonic bases himself. Depending on the tilt rotation, it should either be the value of the depth or its value negated.)
Step 5. Rename the curve so that the word "Rail" is contained in it.

LOOP ASSETS :
In The Asset Library, there should be an asset called Adam's Perfect Loop.
This Asset will be your base when adding loops to your project.
You can directly edit the Trigger Box (Box in which sonic gets attached to the loop)
and the spline (Z position of sonic when in the loop)
You can also scale it up and down (Press S -> Shift + Y To edit its size in the X and Z axis without modifying its depth).

[WARNING]

1. The spline must end OUTSIDE of the trigger box.
2. You may not rename any of the parts of Adam's Perfect Loop.
3. You can Edit the geometry of the loop but you must also edit the Path spline AND the Trigger Box to ensure they work.
4. These things are YOUR responsibility. Not mine.




(Deprecated -> The Old loops should still be working but please use the asset called Adam's Perfect Loop when putting loops in your level)
Loop asset's geometry can be modified. But it's limited. You need to allow entry and exit for the character. So :
you may increase the scale and lower it. -> This mostly works perfectly fine.
You may modify the geometry to make the roof sit higher and make the walls thicker
BUT
It is your job to align the character's exit with the rest of the stage so the character doesnt fall off axis.
It is your job to make sure passing through the loop is still possible.
It is your job to make sure The collision mesh doesnt mess with the character's angle limitation.
While some weird loops may need specific modification in engine, we will discuss those, making sure the collision mesh is usable is YOUR JOB.

***To export grind rails and splines, use the Export curve data script. It will make a button appear in the object contextual menu on the bottom right. (The Orange Square)***
**DO NOT** put the name of any stage objects inside geometry objects as they will be overriden by the object replacement.


When in-game you have 3 options for reloading

Press " **H** " to go back to the browser to select a different level

Press " **R** " to quick reload the entire stage after making edits and go back to the start of the stage

Press " **T** " to soft quick reload, which is the same function as R, but keeps your current position 



Any Question, reach out to @Diamax in the discord



