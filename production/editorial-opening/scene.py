"""Art-directed editorial courier opening: real 3D, PBR materials and lighting."""
import bpy,math,sys,argparse,os,json
from mathutils import Vector
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--scene',default='confirmation',choices=['dispatch','confirmation','reveal']);p.add_argument('--out',required=True);p.add_argument('--animate',action='store_true');p.add_argument('--engine',default='BLENDER_EEVEE_NEXT');p.add_argument('--samples',type=int,default=24);p.add_argument('--size',type=int,default=1920);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine=a.engine;s.render.resolution_x=a.size;s.render.resolution_y=a.size//2;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.fps=30;s.frame_start=1;s.frame_end=240;s.frame_step=2
s.view_settings.view_transform='AgX';s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.04,.055,.09,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.18
if a.engine=='CYCLES':s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.cycles.max_bounces=5
else:s.eevee.taa_render_samples=a.samples;s.eevee.use_raytracing=True
s.render.film_transparent=False

def material(n,c,metal=0,rough=.3,trans=0,emission=0):
 m=bpy.data.materials.new(n);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=rough;b.inputs['Transmission Weight'].default_value=trans;b.inputs['IOR'].default_value=1.45
 if emission:b.inputs['Emission Color'].default_value=(*c,1);b.inputs['Emission Strength'].default_value=emission
 m.diffuse_color=(*c,1);return m
obs=material('Obsidian anodised aluminium',(.025,.028,.04),.85,.28)
ink=material('Graphite',( .055,.065,.085),.65,.22)
ivory=material('Warm porcelain',(.78,.73,.62),.15,.23)
glass=material('Smoked frosted glass',(.12,.18,.24),.12,.23,.72)
champagne=material('Champagne metal',(.55,.35,.13),.82,.23)
mint=material('Mint light',(.19,.8,.65),.2,.24,0,4)
amber=material('Amber light',(1,.37,.08),.1,.25,0,4)
white=material('Ivory light',(.85,.88,.95),0,.25,0,2)
blue=material('Blue light',(.08,.2,.8),.2,.3,0,2)

def assign(o,m):o.data.materials.append(m);return o
def cube(n,loc,dim,m,bevel=.08,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);assign(o,m)
 if bevel:
  mod=o.modifiers.new('Precision chamfer','BEVEL');mod.width=bevel;mod.segments=5;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 if parent:o.parent=parent
 return o

def cyl(n,loc,r,depth,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=n;assign(o,m);b=o.modifiers.new('Soft rim','BEVEL');b.width=.045;b.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o

def empty(n):o=bpy.data.objects.new(n,None);s.collection.objects.link(o);return o
def key(o,f,loc=None,rot=None):
 if loc:o.location=loc;o.keyframe_insert('location',frame=f)
 if rot:o.rotation_euler=rot;o.keyframe_insert('rotation_euler',frame=f)

def light(n,loc,color,power,size,target=(0,0,0),shape='DISK'):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=n;o.data.energy=power;o.data.color=color;o.data.shape=shape;o.data.size=size;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o

def path(n,pts,m,r=.018):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.resolution_u=24;c.bevel_depth=r;c.bevel_resolution=4
 sp=c.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for b,pt in zip(sp.bezier_points,pts):b.co=pt;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 ob=bpy.data.objects.new(n,c);s.collection.objects.link(ob);assign(ob,m);return ob

def text(n,body,loc,size=.16,mat=white):
 bpy.ops.object.text_add(location=loc,rotation=(math.pi/2,0,0));o=bpy.context.object;o.name=n;o.data.body=body;o.data.size=size;o.data.extrude=.0005;o.data.font=bpy.data.fonts.load(str(Path(__file__).parent/'assets/Inter.ttf'));assign(o,mat);return o

def parcel(loc=(0,0,1.1)):
 r=empty('Floating birthday parcel');r.location=loc
 cube('Porcelain parcel shell',(0,0,0),(1.7,1.35,1.0),ivory,.13,r)
 cube('Lid',(0,0,.51),(1.76,1.41,.12),ivory,.05,r)
 cube('Graphite ribbon',(0,0,.58),(.16,1.43,.035),ink,.015,r)
 cube('Champagne seal',(.44,-.31,.60),(.56,.37,.04),champagne,.035,r)
 cube('Delivery label',(.0,-.687,.06),(1.34,.025,.52),obs,.035,r)
 # Discreet barcode geometry catches the rim light.
 for i in range(14):cube('Barcode',(-.55+i*.025,-.706,-.03),(.009 if i%3 else .016,.008,.17),ivory,.001,r)
 label=text('Original address','14 MAPLE STREET',(-.03,-.709,.06),.075,white);label.parent=r
 return r

cube('Infinite charcoal stage',(0,0,-.27),(160,160,.4),obs,.1)
cube('Floating stage',(0,0,-.025),(8,5.6,.16),ink,.15)
# Fine, inset line around the platform.
path('Stage edge',[(-3.6,-2.4,.06),(3.6,-2.4,.06),(3.6,2.4,.06)],blue,.006)
light('Large warm key',(2,-3,8),(1,.81,.59),1400,6)
light('Cool rim',(-4,3,5),(.22,.38,1),1800,5)
light('Mint strip',(4,1,2),(.23,1,.83),420,3,(0,0,1))
light('Front softbox',(0,-6,4),(.64,.73,1),550,5,(0,0,1))
if a.scene in ['dispatch','confirmation']:
 cube('Machined conveyor',(0,0,.25),(6.6,2.15,.36),obs,.12)
 for i in range(18):
  o=cyl('Anodised roller',(-2.9+i*.34,0,.48),.10,1.95,ink);o.rotation_euler[0]=math.pi/2
 for x in [-.8,.8]:
  cube('Scanner rail',(x,.91,1.7),(.08,.10,2.5),champagne,.035)
  cube('Scanner light',(x,.84,1.7),(.018,.025,2.2),mint,.008)
 cube('Scanner crossbar',(0,.91,3.0),(1.7,.12,.10),champagne,.04)
 r=parcel((-.35,-.15,1.3));key(r,1,(-1.1,-.15,1.3),(0,0,-.08));key(r,120,(-.15,-.15,1.4),(0,0,.015));key(r,240,(.55,-.15,1.3),(0,0,.07))
 # A real translucent interface slab; flat readable editorial overlays are added later.
 panel=cube('Floating smoked glass summary',(1.65,.4,2.1),(2.3,.075,1.55),glass,.08);panel.rotation_euler[2]=0
 cube('Panel top rail',(1.65,.34,2.82),(2.1,.024,.015),mint,.006)
 text('Panel label','RECORDED ADDRESS',(.64,.27,2.55),.095)
 text('Recipient','For Maya',(.64,.27,2.29),.14)
 text('Recorded destination','14 Beacon Point',(.64,.27,2.04),.13)
 cube('Confirm button',(1.64,.27,1.64),(1.92,.04,.30),mint,.04)
 text('Button label','Confirm',(1.30,.235,1.59),.13,obs)
 cyl('Confirmation light',(2.8,-1.6,.35),.19,.12,mint)
 path('Accepted route',[(.5,-1,.07),(1.1,-1.5,.07),(2.8,-1.6,.07)],mint,.015)
else:
 # A tiny sculptural lighthouse perched on the destination platform.
 cyl('Destination island',(1.4,.5,.08),1.6,.20,obs)
 cyl('Glass destination disc',(1.4,.5,.22),1.43,.07,glass)
 for i in range(5):cyl('Lighthouse tower',(1.4,.5,.5+i*.38),.32-i*.018,.38,ivory if i%2==0 else ink)
 cyl('Lantern balcony',(1.4,.5,2.25),.40,.10,champagne)
 cyl('Amber beacon',(1.4,.5,2.52),.23,.42,amber)
 cyl('Lantern cap',(1.4,.5,2.78),.38,.09,obs)
 for theta in [0,math.pi/2,math.pi,math.pi*1.5]:
  x=1.4+math.cos(theta)*.25;y=.5+math.sin(theta)*.25;cube('Lantern frame',(x,y,2.52),(.025,.025,.45),champagne,.009)
 r=parcel((.5,-1,1.0));key(r,1,(.1,-1.1,.9),(0,0,-.12));key(r,240,(.8,-.7,1.1),(0,0,.08))
 path('Wrong destination route',[(-3,-1.9,.07),(-1.8,-1.7,.07),(-.7,-.9,.07),(1.2,.5,.33)],amber,.02)
 path('Unvisited route',[(-2.4,-1.8,.06),(-2.4,.5,.06),(-2.8,1.5,.06)],ink,.02)
 cube('Unvisited house',(-2.8,1.5,.35),(.7,.65,.6),glass,.08)
 # Beacon glow, no cartoon person needed to carry the reveal.
 bpy.ops.object.light_add(type='POINT',location=(1.4,.5,2.5));bpy.context.object.data.energy=35;bpy.context.object.data.color=(1,.34,.07)

if a.scene=='dispatch':
 for ob in list(s.objects):
  if ob.name.startswith(('Floating smoked','Panel','Recipient','Recorded destination','Confirm button','Button label')):ob.hide_render=True
bpy.ops.object.camera_add(location=(8,-12,7));cam=bpy.context.object;s.camera=cam;cam.data.lens=52;cam.data.clip_end=250
for fr,loc,target in [(1,(9,-14,8),(-.4,0,1.1)),(120,(7.6,-12.8,6.8),(-.2,0,1.2)),(240,(6.9,-11.5,6.3),(0,0,1.25))]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert('location',frame=fr);cam.keyframe_insert('rotation_euler',frame=fr)
cam.data.dof.use_dof=True;cam.data.dof.focus_distance=(cam.location-Vector((0,0,1.2))).length;cam.data.dof.aperture_fstop=7.1
s.use_nodes=True;nodes=s.node_tree.nodes;nodes.clear();rl=nodes.new('CompositorNodeRLayers');glow=nodes.new('CompositorNodeGlare');glow.glare_type='FOG_GLOW';glow.quality='HIGH';glow.threshold=1.4;glow.mix=-.88;out=nodes.new('CompositorNodeComposite');s.node_tree.links.new(rl.outputs['Image'],glow.inputs['Image']);s.node_tree.links.new(glow.outputs['Image'],out.inputs['Image'])
# Export actual camera depth for the editorial 2.5D motion pass.
s.view_layers[0].use_pass_z=True
depth=s.node_tree.nodes.new('CompositorNodeMapRange');depth.inputs['From Min'].default_value=7;depth.inputs['From Max'].default_value=28;depth.inputs['To Min'].default_value=0;depth.inputs['To Max'].default_value=1;depth.use_clamp=True
s.node_tree.links.new(rl.outputs['Depth'],depth.inputs['Value'])
df=s.node_tree.nodes.new('CompositorNodeOutputFile');df.base_path=os.path.dirname(a.out);df.file_slots[0].path=a.scene+'-depth-';df.format.file_format='PNG';df.format.color_mode='BW';df.format.color_depth='16';s.node_tree.links.new(depth.outputs['Value'],df.inputs[0])
s.render.filepath=a.out
if a.animate:
 s.render.filepath=a.out.rstrip('/')+'/';bpy.ops.render.render(animation=True)
else:s.frame_set(120);bpy.ops.render.render(write_still=True)
