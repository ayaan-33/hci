import bpy,math,os
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=12;s.frame_start=1;s.frame_end=240;s.display.render_aa='5'
s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.4;s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.show_specular_highlight=True;s.display.shading.background_type='WORLD';s.world.color=(.3,.42,.64);s.view_settings.view_transform='Standard';s.display.shading.studiolight_background_alpha=1
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);return m
navy=mat('Midnight',(.16,.23,.48));steel=mat('Brushed steel',(.12,.48,.88));mint=mat('Signal mint',(.12,1,.64));paper=mat('Ivory',(.91,.92,.84));boxmat=mat('Parcel kraft',(1,.52,.025));red=mat('Warning coral',(1,.08,.28));black=mat('Ink',(.10,.06,.25))
def cube(n,p,scale,m,bevel=.06):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=n;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:mod=o.modifiers.new('Soft machined edges','BEVEL');mod.width=bevel;mod.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def txt(text,p,size,m,rot=(math.pi/2,0,0)):
 bpy.ops.object.text_add(location=p,rotation=rot);o=bpy.context.object;o.data.body=text;o.data.size=size;o.data.extrude=.005;o.data.materials.append(m);return o
cube('Ground',(0,0,-.6),(35,30,.3),navy)
cube('Conveyor',(0,0,0),(13,2.8,.35),steel)
for x in range(-6,7):
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=.16,depth=2.65,location=(x,0,.25),rotation=(math.pi/2,0,0));bpy.context.object.data.materials.append(black)
for x in [-5,5]:
 for y in [-1,1]:cube('Leg',(x,y,-.5),(.18,.18,1),steel)
for y in [-1.7,1.7]:cube('Scanner post',(-1,y,1.6),(.25,.25,3.2),steel)
cube('Scanner lintel',(-1,0,3.2),(.5,3.65,.4),mint)
cube('Scanner beam',(-1,0,1.8),(.04,2.9,.035),mint,0)
# Bright modular factory details and lane markings.
purple=mat('Electric violet',(.53,.13,1));yellow=mat('Signal yellow',(1,.89,.03));pink=mat('Hot pink',(1,.12,.52))
for i in range(-6,7):
 cube('Lane light',(i,-1.52,.23),(.55,.13,.07),yellow,.02)
for x,y,h,m in [(-5,4,2,purple),(-4,5,3,pink),(7,6,4,purple),(-7,2,2.5,yellow)]:
 cube('Factory module',(x,y,h/2),(1.3,1.3,h),m,.15)
for i in range(3):
 p=cube('Following parcel',(-7-i*2,0,.95),(1.1,1,.95),purple if i%2 else pink,.09)
 for fr,xx in [(1,-7-i*2),(240,-3-i*2)]:p.location.x=xx;p.keyframe_insert(data_path='location',frame=fr)
# Raised destination platforms
cube('Wrong destination',(6,0,.4),(2.6,3.5,.35),red)
cube('Correct destination',(4,5,.4),(4,2.5,.35),mint)
txt('WRONG ADDRESS',(4.8,-1.78,1.2),.25,red)
txt('INTENDED ADDRESS',(2.5,3.7,.8),.26,mint)
# Parcel and label grouped so the original geometry travels together
root=bpy.data.objects.new('Parcel movement',None);s.collection.objects.link(root)
b=cube('Parcel',(0,0,1),(1.5,1.35,1.3),boxmat);b.parent=root
for obj in [cube('Packing tape',(0,0,1.66),(.25,1.36,.02),paper,.005),cube('Wrong address label',(0,-.686,1.1),(1.1,.02,.65),paper,.01),txt('TO: BAY 07',(-.47,-.71,1.23),.14,black),txt('LABEL ERROR',(-.47,-.71,.96),.12,red)]:obj.parent=root
for fr,x in [(1,-5),(145,-1),(210,-1),(360,5.3),(480,5.3)]:root.location.x=x;root.keyframe_insert(data_path='location',frame=max(1,round(fr/2)))
# Display behind sorter
cube('Status screen',(-1,4,3.2),(5,.16,1.4),black)
txt('ROUTE CONFIRMED',(-3.1,3.89,3.3),.3,mint)
txt('LABEL READ  /  CONTENT UNCHECKED',(-3.1,3.89,2.93),.13,paper)
bpy.ops.object.camera_add(location=(10,-15,10));cam=bpy.context.object;s.camera=cam;cam.data.type='PERSP';cam.data.lens=35
for fr,pos,target in [(1,(9,-15,10),(0,0,.8)),(200,(7,-12,7),(-1,0,1)),(360,(12,-12,9),(3,0,1)),(480,(11,-11,8),(3,0,1))]:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert(data_path='location',frame=max(1,round(fr/2)));cam.keyframe_insert(data_path='rotation_euler',frame=max(1,round(fr/2)))
s.frame_start=1;s.render.image_settings.file_format='PNG';s.render.filepath='/workspace/work/v2/intro_frames/';bpy.ops.wm.save_as_mainfile(filepath='/workspace/work/v2/parcel-sorter-vibrant.blend')
if os.getenv('SAMPLE'):s.frame_set(260);s.render.filepath='/workspace/work/intro_sample.png';bpy.ops.render.render(write_still=True)
else:bpy.ops.render.render(animation=True)
