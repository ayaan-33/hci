import bpy
bpy.ops.wm.open_mainfile(filepath='/workspace/work/v3/team-stage.blend')
for o in bpy.data.objects:
 if o.type=='FONT' and o.data.body=='MEET TEAMGARI':o.data.body='TEAMGARI / THANK YOU'
 if o.type=='FONT' and o.data.body=='THE QUESTION':o.data.body='THANK YOU FOR WATCHING'
bpy.context.scene.render.filepath='/workspace/work/v3/closing-stage.png';bpy.ops.render.render(write_still=True)
